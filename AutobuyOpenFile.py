import json

if __name__ == '__main__':
    with open('./AutobuyJson/autobuy2022-11-09.json','r',encoding="utf-8") as f:
            json_object=json.load(f)
            f.close
    print(len(json_object))