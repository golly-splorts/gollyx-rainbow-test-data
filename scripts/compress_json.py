import gzip
import json

inputs = ['postseason.json', 'season.json']
outputs = ['postseason.gz', 'season.gz']

for json_file, gz_file in zip(inputs, outputs):
    with open(json_file, 'r') as f:
        dat = json.load(f)
    json_str = json.dumps(dat)
    json_bytes = json_str.encode('utf-8')
    with gzip.open(gz_file, 'w') as fout:
        fout.write(json_bytes)
