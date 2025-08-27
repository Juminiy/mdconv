from mdconv.parse import explain_json
from json import loads

if __name__=='__main__':
    for filename in ['full_test', 'gin-README', 'tensorflow-README']:
        with open(f'data/json/{filename}.json') as jsonf:
            with open(f'data/md/{filename}-gen.md', 'w+') as mdf:
                mdf.write(explain_json(loads(jsonf.read())))
                mdf.close()
                jsonf.close()