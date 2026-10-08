
import os
import re
import json
import glob

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

pattern_uuid = re.compile(r'uuid\":\s*\"(.*?)\"')
pattern_type = re.compile(r'type\":\s*\"(.*?)\"')
pattern_time = re.compile(r'timestampNanos\":(.*?),')
pattern_src  = re.compile(r'subject\":{\"com.bbn.tc.schema.avro.cdm18.UUID\":\"(.*?)\"}')
pattern_dst1 = re.compile(r'predicateObject\":{\"com.bbn.tc.schema.avro.cdm18.UUID\":\"(.*?)\"}')
pattern_dst2 = re.compile(r'predicateObject2\":{\"com.bbn.tc.schema.avro.cdm18.UUID\":\"(.*?)\"}')
pattern_label = re.compile(r'"label":"(.*?)"')


def find_input_files():
    skip = {'names.json', 'types.json'}
    return sorted(
        fp for fp in glob.glob(os.path.join(THIS_DIR, '*.json'))
        if os.path.basename(fp) not in skip
    )


def parse_one(input_file, id_nodetype_map, id_nodename_map):
    tag = re.sub(r'\.json$', '', os.path.basename(input_file))
    readable_out = os.path.join(THIS_DIR, 'edges_{}_readable.txt'.format(tag))

    n_lines = n_events = n_edges = n_unknown_type = n_unknown_name = 0

    with open(input_file, 'r', encoding='utf-8', errors='replace') as fin, \
         open(readable_out, 'w', encoding='utf-8') as freadable:

        for line in fin:
            n_lines += 1
            if 'com.bbn.tc.schema.avro.cdm18.Event' not in line:
                continue

            uuid_match  = pattern_uuid.findall(line)
            etype_match = pattern_type.findall(line)
            ts_match    = pattern_time.findall(line)
            if not uuid_match or not etype_match or not ts_match:
                continue
            eventUuid = uuid_match[0]
            edgeType = etype_match[0]
            try:
                timestamp = int(ts_match[0].strip())
            except ValueError:
                continue

            if edgeType in {'EVENT_MPROTECT', 'EVENT_MMAP', 'EVENT_SHM'}:
                continue

            n_events += 1

            srcId_match = pattern_src.findall(line)
            if not srcId_match:
                continue
            srcId = srcId_match[0]
            srcType = id_nodetype_map.get(srcId)
            if srcType is None:
                n_unknown_type += 1
                srcType = 'UNKNOWN'
            srcName = id_nodename_map.get(srcId)
            if srcName is None:
                n_unknown_name += 1
                srcName = 'N/A'

            for dst_pattern in (pattern_dst1, pattern_dst2):
                dstId_match = dst_pattern.findall(line)
                if dstId_match and dstId_match[0] != 'null':
                    d = dstId_match[0]
                    if d == '00000000-0000-0000-0000-000000000000':
                        continue
                    dType = id_nodetype_map.get(d, 'UNKNOWN')
                    dName = id_nodename_map.get(d, 'N/A')
                    freadable.write('{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n'.format(
                        eventUuid, srcId, srcName, srcType, edgeType, d, dType, dName))
                    n_edges += 1

    print('  {}'.format(os.path.basename(input_file)))
    print('    Lines read               : {:,}'.format(n_lines))
    print('    Events matched           : {:,}'.format(n_events))
    print('    Readable edges written   : {:,}  -> {}'.format(n_edges, os.path.basename(readable_out)))


def main():
    types_path = os.path.join(THIS_DIR, 'types.json')
    names_path = os.path.join(THIS_DIR, 'names.json')

    print('Loading node-type map: {}'.format(types_path))
    with open(types_path, 'r', encoding='utf-8') as f:
        id_nodetype_map = json.load(f)
    print('  {:,} known node types'.format(len(id_nodetype_map)))

    print('Loading name map: {}'.format(names_path))
    with open(names_path, 'r', encoding='utf-8') as f:
        id_nodename_map = json.load(f)
    print('  {:,} known node names'.format(len(id_nodename_map)))

    input_files = find_input_files()
    print('\nFound {} input json file(s) in {}'.format(len(input_files), THIS_DIR))
    for fp in input_files:
        parse_one(fp, id_nodetype_map, id_nodename_map)


if __name__ == '__main__':
    main()
