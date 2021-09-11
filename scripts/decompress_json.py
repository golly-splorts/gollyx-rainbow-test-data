import gzip
import json

inputs = ['postseason.gz', 'season.gz']

for gz_file in inputs:
    with gzip.open(gz_file, 'r') as fin:
        json_bytes = fin.read()
    json_str = json_bytes.decode('utf-8')
    data = json.loads(json_str)
