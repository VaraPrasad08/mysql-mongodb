from unittest import result
from fastapi import  FastAPI,status
from pydantic import BaseModel 
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import mysql

class data(BaseModel):
    Roll_number: int
    Name: str
    Address: str
    Mobile_number: int
    Branch:str
    State: str
    Country: str

while True:
    try:
        conn =mysql.connector.connect(host='localhost',user='root',password="",database='student')
        cursor=conn.cursor()
        print("database connection is successfull")
        break
    except Exception as error:
        print("connection to database failed")
        print("error:",error)    

app=FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/registration")
def get_info():
   
    cursor.execute("SELECT * FROM data")
    rows=cursor.fetchall()
    posts = []
    for row in rows:
        post = {
            "Roll_number": row[0],
            "Name": row[1],
            "Address": row[2],
            "Mobile_number": row[3],
            "Branch":row[4],
            "State": row[5],
            "Country": row[6]
            
        }
        posts.append(post)
    conn.commit()

    return  posts



@app.post("/post")
def create_info(data:data):
    sql=" INSERT INTO data (Roll_number,Name, Mobile_number, Address,Branch, Country, State) VALUES  (%s,%s,%s,%s,%s,%s,%s)"
    val=(data.Roll_number,data.Name,data.Mobile_number,data.Address,data.Branch,data.State,data.Country)
    #return sql,val

    cursor.execute(sql,val)
    # new_data=cursor.fetchone()


    conn.commit()

    return JSONResponse(status_code=status.HTTP_201_CREATED)