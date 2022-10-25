# -*- coding:utf-8 _*-
import mysql.connector
import json
import time
import os

def uploadprod():
    print("hello")

def uploadtag(datas,mycursor,timetag):
    for data in datas:
        key=str(data.keys())[12:-3]
        value = str(data.values())[14:-3]
        if(isTagExist(key,mycursor)==False):
            addtag(key,value,mycursor,timetag)
    print("upload ok")

        
    
def isTagExist(key,mycursor):
    mycursor.execute("SELECT tag_id FROM tag_compare WHERE tag_id = %s;",(key,))
    record = mycursor.fetchone()
    if record == None:
        return False
    else:
        return True

def addtag(key,value,mycursor,timetag):
    mycursor.execute("INSERT INTO tag_compare (	tag_id, tag_zhtw, create_date) VALUES (%s, %s, %s)",(key,value,timetag))

def uploadtagprod(json_object,mycursor,timetag):
    for datas in json_object:
        id = datas['id']
        price = datas['price']
        last_number =int(id[-1:])
        if(isProdExist(id,mycursor)==False):
            addprod(datas,mycursor,timetag)
            addprodtag(datas,mycursor)
        if last_number==1:
            mycursor.execute("INSERT INTO last_1 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==2:
            mycursor.execute("INSERT INTO last_2 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==3:
            mycursor.execute("INSERT INTO last_3 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==4:
            mycursor.execute("INSERT INTO last_4 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==5:
            mycursor.execute("INSERT INTO last_5 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==6:
            mycursor.execute("INSERT INTO last_6 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==7:
            mycursor.execute("INSERT INTO last_7 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==8:
            mycursor.execute("INSERT INTO last_8 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==9:
            mycursor.execute("INSERT INTO last_9 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))
        elif last_number==0:
            mycursor.execute("INSERT INTO last_0 (fk_prod_id,price,upload_date) VALUES (%s, %s, %s)",(id,price,timetag))
            mycursor.execute("UPDATE maintable SET last_update_date = %s WHERE prod_id = %s",(timetag,id))

        





def isProdExist(key,mycursor):
    mycursor.execute("SELECT prod_id FROM maintable WHERE prod_id = %s;",(key,))
    record = mycursor.fetchone()
    if record == None:
        return False
    else:
        return True

def addprod(datas,mycursor,timetag):
    name = datas['name']
    id = datas['id']
    mycursor.execute("INSERT INTO maintable ( prod_id, inital_date, last_update_date, prodavailable, prodname) VALUES (%s, %s, %s, %s, %s)",(id,timetag,timetag,'1',name))

def addprodtag(datas,mycursor):
    id = datas['id']
    tags = datas['tags']
    for tag in tags:
        try:
            mycursor.execute("INSERT INTO tag_prod ( fk_prod_id,fk_tag) VALUES (%s, %s)",(id,tag))
        except Exception as e:
            print(e)
            print(id)
            print(tag)
            with open('logs.txt','a',encoding="utf-8") as f:
                f.write(str(time.strftime("%Y-%m-%d", time.localtime()))+" SQL "+str(e)+"\n")
                f.close()

if __name__ == "__main__":
    timetag = time.strftime("%Y-%m-%d", time.localtime())
    # timetag = "2022-10-24"
    if os.path.exists('mysql.json'):
        print("have mysql.json")
        with open('mysql.json','r',encoding="utf-8") as f:
                mysql_json=json.load(f)
                f.close()
        mydb = mysql.connector.connect(
        host=mysql_json["host"],
        user=mysql_json["user"],
        password=mysql_json["password"],
        database=mysql_json["database"],
        port=mysql_json["port"]
        )  
    else:
        print("use default config")
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="autobuy",
        port=3306
        )

    mycursor = mydb.cursor()    
    first = os.path.exists('./AutobuyJson/autobuy'+timetag+'.json')
    second = os.path.exists('./AutobuyJson/autobuy_tag'+timetag+'.json')
    print(timetag)
    if (second):
        with open('./AutobuyJson/autobuy_tag'+timetag+'.json','r',encoding="utf-8") as f:
                json_object2=json.load(f)
                f.close()
        uploadtag(json_object2,mycursor,timetag)
        print("first ok")

    if(first):
        with open('./AutobuyJson/autobuy'+timetag+'.json','r',encoding="utf-8") as f:
                json_object=json.load(f)
                f.close()
        uploadtagprod(json_object,mycursor,timetag)
        print("second ok")

    mydb.commit()
    print("commit success")
    mydb.close()
    if second:
        os.remove('./AutobuyJson/autobuy_tag'+timetag+'.json')
