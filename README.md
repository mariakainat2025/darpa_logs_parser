# DARPA TC Provenance Parsing

## What these scripts are

`scripts/parse_provenance.py` — parses raw DARPA TC (CDM18) audit log JSON files into entity/edge maps and a sorted edge list.
`scripts/extract_graphs.py` — builds a provenance graph from those edges, and can split a large graph into smaller subgraphs.
`scripts/config.py` — shared paths and regex patterns both scripts import.


## Dependencies

- Python 3.9.19
- `networkx` 3.2.1
- `tqdm` 4.67.3


## Input / Output

`parse_provenance.py`
Input: Your raw log files, placed in `input/theia/`
Output: A list of all events (`edges_all.txt`), plus lookup files for names and types — saved in `output/theia/parsed/`

`extract_graphs.py`
Input: The event list from the step above
Output: The finished graph (`graph_output.json`) — saved in `output/theia/graphs/`

