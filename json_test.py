import json
import pymysql

def insert_user(json_pack):
 str= json.loads(json_pack)
 user_name = str.get('NEW_ACC').get('USERNAME')
 password = str.get('NEW_ACC').get('PASSWORD')
 try:
   conn=pymysql.connect(host='localhost',user='pi',passwd='piaccess12!',db='party_time',port= 3306)
   cur=conn.cursor()

   cur.execute('insert into User(User_Account,Password) values("%s","%s")'%(user_name,password))

   conn.commit()
   cur.close()
   conn.close()

 except pymysql.Error as e:
    print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))


json_pack1 = '{"NEW_ACC": {"USERNAME": "Stone123", "PASSWORD": "123","EMAIL": "user_email"}}'
insert_user(json_pack1)