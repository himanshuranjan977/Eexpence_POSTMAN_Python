from flask import Flask,request,jsonify
from uuid import uuid1 ,uuid4
import os,json,pytz
from datetime import date,datetime
import pandas as pd

db={}
db_filename="db.json"

if os.path.exists(db_filename):
    print("DB ExISTS")
    with open(db_filename,'r')as f:
        db=json.load(f)
else:
    print("DB DO NOT FOUND")
    accessKey =str(uuid1())       
    secretKey=str(uuid4()) 
    item_types=[
        "Food","Beverages","Clothings"
        "statonaries","Electronics Device","wierless"
    ]

    db={
        "accessKey":accessKey,
        "secretKey":secretKey,
        "item_types":item_types,
        "users":[]
    }

    with open (db_filename,"w+") as f:
        json.dump(db,f,indent=4)

app=Flask (__name__)   

@app.route('/signup',methods=['POST'])
def signup():
    if request.method=='POST':
        #print(request.form)
        name=request.form['name']
        email=request.form['email']
        password=request.form['password']
        usename=request.form['username']

    userDict={
        "name":name,
        "email":email,
        "password":password,
        "usename":usename,
        "purchases":{}

    }

    email_list=[]
    for user in db["users"]:
        email_list.append(user["email"])

    if len(db["users"])    ==0 or userDict["email"] not in email_list:
        db["users"].append(userDict)
        with open(db_filename,"r+") as f:
            f.seek(0)
            json.dump(db,f,indent=4)
            return "user signed up successfully "
    else:
        return "User already exists"    
    return "Methord not allowed"     
  
@app.route("/login",methods=["POST"])
def login():
    email = request.form["email"]
    password=request.form["password"]
    for user in db ["users"]:
        if user["email"]==email and user ["password"]==password:
            user_idx =db ["users"].index(user)
            response={
                "message":"Login successfully",
                "user_index": user_idx
            }
            return response
        else:
            continue
    return "Wrong email or password"

@app.route("/add_purchase",methods=["POST"]) 
def add_purchase():
    if request.method=='POST':
        user_index =int(request.form["user_index"])
        item_name=request.form["item_name"]
        item_type=request.form["item_type"]
        item_price=request.form["item_price"]

        curr_date=str(date.today())
        curr_time=str(datetime.now(pytz.timezone("Asia/Kolkata")))
        itemDict={
            "item_name":item_name,
            "item_type":item_type,
            "item_price":item_price,
            "purchase_time":curr_time
        }
        existing_dates=list(db["users"][user_index]["purchases"].keys())
        print(existing_dates)

        if len (db["users"][user_index]["purchases"])==0 or curr_date not in existing_dates:
            db["users"][user_index]["purchases"][curr_date]=[]
            db["users"][user_index]["purchases"][curr_date].append(itemDict)
            with open(db_filename,"r+") as f:
                f.seek(0)
                json.dump(db,f,indent=4)
            return "Item added seccussfully"
        else:
            db["users"][user_index]["purchases"][curr_date].append(itemDict)
            with open(db_filename,"r+") as f:
                f.seek(0)
                json.dump(db,f,indent=4)
            return "Item added seccussfully"
 
        return "asds"    
@app.route("/get_all_purchases_for_today", methods=["GET"])
def get_all_purchases_for_today():
    user_idx = int(request.args["user_index"])

    curr_date = str(date.today())

    purchases_today = db["users"][user_idx]["purchases"][curr_date]

    if len(purchases_today) == 0:
        return jsonify(msg="No items purchased today.")

    return jsonify(purchases_for_today=purchases_today)

@app.route("/get_purchases", methods=["GET"])
def get_purchases():
    data = request.json
    # print(data)
    user_idx =  data['user_index']
    start_date= data['start_date']
    end_date= data['end_date']


    dates_range=pd.date_range(start_date,end_date)
    db_dates=list(db["users"][user_idx]["purchases"].keys())
    #print(db_dates)

    purchase_list={}
    for dt in db_dates:
        if dt in dates_range:
            purchase_list[dt]=db["users"][user_idx]["purchases"][dt]
        else:
            continue    

    # return jsonify(messgae=purchase_list) 
    return purchase_list



    

if __name__=="__main__":
    app.run(host="0.0.0.0",port=6000,debug=True)

