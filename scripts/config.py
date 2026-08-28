import os
import re
from datetime import datetime, timezone, timedelta

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR    = os.path.dirname(SCRIPTS_DIR)

DATA_PATH      = os.path.join(BASE_DIR, 'input', 'theia') + os.sep
OUTPUT_PARSED  = os.path.join(BASE_DIR, 'output', 'theia', 'parsed') + os.sep
OUTPUT_GRAPHS  = os.path.join(BASE_DIR, 'output', 'theia', 'graphs') + os.sep
EDGES_FILE     = OUTPUT_PARSED + 'edges_all.txt'

pattern_uuid  = re.compile(r'uuid\":\s*\"(.*?)\"')
pattern_type  = re.compile(r'type\":\s*\"(.*?)\"')
pattern_time  = re.compile(r'timestampNanos\":(.*?),')
pattern_src   = re.compile(r'subject\":{\"com.bbn.tc.schema.avro.cdm18.UUID\":\"(.*?)\"}')
pattern_dst1  = re.compile(r'predicateObject\":{\"com.bbn.tc.schema.avro.cdm18.UUID\":\"(.*?)\"}')
pattern_dst2  = re.compile(r'predicateObject2\":{\"com.bbn.tc.schema.avro.cdm18.UUID\":\"(.*?)\"}')
pattern_mem_addr = re.compile(r'memoryAddress\":([\d]+)')


def show(msg):
    print(msg)


def update_ts(ts_map, uuid, timestamp):
    if uuid not in ts_map:
        ts_map[uuid] = {'first': timestamp, 'last': timestamp}
    else:
        if timestamp < ts_map[uuid]['first']:
            ts_map[uuid]['first'] = timestamp
        if timestamp > ts_map[uuid]['last']:
            ts_map[uuid]['last'] = timestamp


def ns_to_et(ns):
    if ns == '' or ns is None:
        return 'NO TIMESTAMP'
    utc = datetime.fromtimestamp(int(ns) / 1e9, tz=timezone.utc)
    et  = utc - timedelta(hours=4)
    return '{}-{:02d}-{:02d} {:02d}:{:02d}:{:02d} ET'.format(
        et.year, et.month, et.day, et.hour, et.minute, et.second)
