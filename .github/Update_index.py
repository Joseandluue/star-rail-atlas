import hashlib
import requests
import json
from pathlib import Path


root_path = Path(__file__).parent.parent
file = ['files.json','othername.json','path.json']

for file_name in file:
    print(file_name)
    res = requests.get(f'https://raw.githubusercontent.com/Nwflower/star-rail-atlas/master/{file_name}')
    # print(res.text)
    new_fileHash = hashlib.md5(res.content).hexdigest()
    print(new_fileHash)
    old_filePath = root_path / file_name
    if not old_filePath.exists():
        with open(old_filePath, 'w', encoding='utf-8') as f:
            new_fileData = json.loads(res.text)
            json.dump(new_fileData, f, ensure_ascii=False, indent=4)
    else:
        with open(old_filePath, 'rb') as f:
            old_fileData = f.read()
        old_fileHash = hashlib.md5(old_fileData).hexdigest()
        if new_fileHash != old_fileHash:
            with open(old_filePath, 'w', encoding='utf-8') as f:
                new_fileData = json.loads(res.text)
                json.dump(new_fileData, f, ensure_ascii=False, indent=4)
