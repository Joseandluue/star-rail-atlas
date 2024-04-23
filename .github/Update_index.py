import hashlib
import requests
import json
from pathlib import Path
import asyncio


class tool():
    root_path = Path(__file__).parent.parent

    @classmethod
    async def set_file_hash(cls, filePath:str, fileName:str, hashValue:int):
        if not filePath.exists():
            await cls.get_file_hash(filePath)
            print(f'{filePath}创建完成')
        with open(filePath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            data.update({'version':data['version'] + 1})
            data.update({fileName:hashValue})
            with open(filePath, 'w', encoding='utf-8') as f_new:
                json.dump(data, f_new, indent=4)

    @classmethod
    async def get_file_hash(cls, filePath):
        hashVer = {
            'version': 0,
            'files': '',
            'othername': '',
            'path':''
        }
        if not filePath.exists():
            with open(filePath, 'w', encoding='utf-8') as f:
                json.dump(hashVer, f, ensure_ascii=False, indent=4)
            return hashVer
        else:
            with open(filePath, 'r', encoding='utf-8') as f:
                date = json.load(f)
            return date

    @classmethod
    async def set_file_value(cls, paths, fileName, contents):
        fileData = json.loads(contents)
        if fileName == 'files' or 'path':
            k = 'guide_overview'
            data = fileData['guide for role']
        elif fileName == 'othername':
            k = 'characters'
            data = fileData['role']
        with open(paths, 'w', encoding='utf-8') as f:
            json.dump({k:data}, f, ensure_ascii=False, indent=4)

    @classmethod
    async def main(cls):
        file = ['files','othername','path']
        for file_name in file:
            res = requests.get(f'https://raw.githubusercontent.com/Nwflower/star-rail-atlas/master/{file_name}.json')
            new_fileHash = hashlib.md5(res.content).hexdigest()
            index_filePath = cls.root_path / f"{file_name}.json"
            hash_filePath = cls.root_path / 'filesHash.json'
            if not index_filePath.exists():
                await cls.set_file_hash(hash_filePath, file_name, new_fileHash)
                print(f"成功更新 '{file_name}.json' 的<hash>")
                await cls.set_file_value(index_filePath, file_name, res.text)
                print(f"创建 '{file_name}.json' 完成")
            else:
                old_hashdata = await cls.get_file_hash(hash_filePath)
                if new_fileHash != old_hashdata[file_name]:
                    print(f"正在更新 '{file_name}.json'")
                    await cls.set_file_hash(hash_filePath, file_name, new_fileHash)
                    print(f"成功更新 '{file_name}.json' 的<hash>")
                    await cls.set_file_value(index_filePath, file_name, res.text)
                    print(f"成功更新 '{file_name}.json' 的<content>")

async def run_main():
    await tool.main()

asyncio.run(run_main())
