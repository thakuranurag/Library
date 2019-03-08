import sqlite3 as sql
from flask import session
from passlib.hash import sha256_crypt
from flask import jsonify
import os
import json
import random
from datetime import datetime

def insertUser(request):
    con = sql.connect("LibraryData.db")
    print("yaha tak chal raha hai")
    print("user name " + request.form['username'])
    sqlQuery = "select mobile from user_data where (mobile ='" + request.form['mobile'] + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        cur.execute("INSERT INTO user_data (username,mobile,email,password,user_type) VALUES (?,?,?,?,?)", (request.form['username'], 
                   request.form['mobile'],request.form['email'],sha256_crypt.encrypt(request.form['password'])
                   ,request.form['usertype']))
        con.commit()
        print "added user successfully"

       
    con.close()
    return not row


def authenticate(request):
    con = sql.connect("LibraryData.db")
    sqlQuery = "select password from user_data where mobile = '%s'"%request.form['mobile']  
    cursor = con.cursor()
    cursor.execute(sqlQuery)
    row = cursor.fetchone()
    con.close()
    if row:
       return sha256_crypt.verify(request.form['password'], row[0])
    else:
       return False
	

def get_librarian():
    print("here madafaka")
    response_array=[]
    mobile=session['mobile']
    con = sql.connect("LibraryData.db")
        # Uncomment line below if you want output in dictionary format
    #con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT username,email,user_type FROM user_data where user_type= 2;")
    rows = cur.fetchall()
    for r in rows:
        temp={}
        temp['name']=r[0]
        temp['email']=r[1]
        temp['user_type']=r[2]
        response_array.append(temp)
    con.close()
    print response_array
    return response_array


def insertotp(request):
    con = sql.connect("Flask_DB.db")
    mobile=session['mobile']
    otp = session['otp']
    sqlQuery = "select otp from otp_data where (mobile ='" + mobile + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    
    if not row:
        cur.execute("INSERT INTO otp_data (mobile,otp) VALUES (?,?)", (mobile,otp))
        print "otp added successfully"
    else:
        cur.execute("UPDATE otp_data SET otp= "+str(otp)+ " where mobile= "+ str(mobile) +" ")
    
    con.commit()   
    con.close()
    return not row


def getOtp(request):
    mobile=session['mobile']
    con = sql.connect("Flask_DB.db")
    sqlQuery = "select otp from otp_data where (mobile ='" + mobile + "')"
    cur = con.cursor()
    cur.execute(sqlQuery)
    row = cur.fetchone()
    con.close()
    return not row


def insertTweet(request):
    con = sql.connect("Flask_DB.db")
    mobile=session['mobile']
    tweet = request.form['tweet']
    added_on=datetime.date(datetime.now())

    sl = getSl(mobile)
    sl=sl+1

    print(">>>> "+ str(mobile) +"  >> " + str(tweet) +" >> "+str(added_on))
    cur = con.cursor()
    cur.execute("INSERT INTO tweet_data (mobile,sl,tweet,added_on) VALUES (?,?,?,?)", (mobile,sl,tweet,added_on))
    print "tweet added successfully"
    
    con.commit()   
    con.close()
    return "success"


def get_tweet():
    print("here madafaka")
    mobile=session['mobile']
    response_array=[]
    con = sql.connect("Flask_DB.db")
        # Uncomment line below if you want output in dictionary format
    #con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT tweet,likes,added_on FROM tweet_data where mobile = "+ mobile+" ")
    rows = cur.fetchall()
    for r in rows:
        tweets = {}
        tweets['tweet']=str(r[0])
        tweets['likes']=str(r[1])
        tweets['added_on']=str(r[2])

        response_array.append(tweets)

    con.close()
    return response_array


def getSl(mobile):
    mobile=mobile
    con=sql.connect("Flask_DB.db")
    cur=con.cursor()
    cur.execute("SELECT MAX(sl) FROM tweet_data WHERE mobile= "+ mobile)
    row= cur.fetchone()

    print(type(row))
    print(len(row))
    print(row)

    if not all(row):
        sl=0
    else:
        sl=row[0]

    con.close()
    print("serial is " + str(sl))
    return sl
























