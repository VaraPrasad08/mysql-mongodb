from fastapi import  FastAPI
from pydantic import BaseModel 
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import mysql

class info(BaseModel):
    Roll_number: int
    Name: str
    Email_addess: str
    Mobile_number: int
    Address: str
    State: str
    Country: str
    Zip: int

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
   
    cursor.execute("""SELECT * FROM info""")
    data=cursor.fetchall()
    return{"data":data}


@app.post("/registration")
def create_info(info:info):
    sql=" INSERT INTO info (Roll_number,Name, Email_address, Mobile_number, Address, Country, State, Zip) VALUES  (%s,%s,%s,%s,%s,%s,%s,%s)"
    val=(info.Roll_number,info.Name,info.Email_addess,info.Mobile_number,info.Address,info.Country,info.State,info.Zip)
    #return sql,val

    cursor.execute(sql,val)
    new_data=cursor.fetchone()
    conn.commit()
    return{"data":new_data}


@app.get("/registration/{Roll_number}")
def get_info(Roll_number:int):
   
    cursor.execute("""SELECT  * FROM info WHERE Roll_number = %s """,(str(Roll_number), ))
    data=cursor.fetchone()
    return{"data":data}


@app.delete("/registration/{Roll_number}")
def delete_info(Roll_number:int):
   
    cursor.execute("""DELETE FROM info WHERE roll_number =%s returning *""",(str(Roll_number),))
    deleted_data=cursor.fetchone()
    conn.commit()
    return{"data":deleted_data}

@app.put("/registration/{Roll_number}")
def update_info(Roll_number:int,info:info):
    sql="UPDATE info SET Roll_number=%s,Name=%s, Email_address=%s, Mobile_number=%s, Address=%s, Country=%s, State=%s, Zip=%s WHERE Roll_number =%s"
    val=(info.Roll_number,info.Name,info.Email_addess,info.Mobile_number,info.Address,info.Country,info.State,info.Zip,str(Roll_number))

    cursor.execute(sql,val)
    updated_data=cursor.fetchone()
    conn.commit()
    return{"data":updated_data}