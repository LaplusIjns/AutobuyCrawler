import os.path
import requests
import json

if __name__ == '__main__':

    session = requests.Session()
    response = session.get('https://www.autobuy.tw')
    print(session.cookies.get_dict()['ABSESSID'])
    if os.path.exists('config.json'):
        with open('config.json','r',encoding="utf-8") as f:
                json_object2=json.load(f)
                f.close()
        json_object2['ABSESSID']=str(session.cookies.get_dict()['ABSESSID'])
        json_object = json.dumps(json_object2)
        with open('config.json','w',encoding="utf-8") as f:
                f.write(json_object)
                f.close()
        print("update ABSESSID sueecee")
    else:
        print("didnt find config.json")
