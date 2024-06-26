from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
import mysql.connector


app = FastAPI()

KEY = "mykey"
SIGNED_IN = "Sign-In"
app.add_middleware(SessionMiddleware, secret_key=KEY)

app.mount("/week7", StaticFiles(directory="task"))
templates = Jinja2Templates(directory="task")

#連結資料庫
def connect_to_db():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="website"
)
#驗證用戶
def validate_user(username,password):
    db_connection=connect_to_db()
    cursor=db_connection.cursor()
    query = "select * from member where username=%s and password=%s"
    cursor.execute(query,(username,password))
    result = cursor.fetchone()
    cursor.close()
    return result is not None


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    token = request.session.get(SIGNED_IN)
    if token:
        return RedirectResponse(url="/member") 
    return templates.TemplateResponse("homepage.html", {'request': request})

@app.post("/signin")
async def sign_in(request: Request, username: str = Form(None), password: str = Form(None)):
    if validate_user(username,password):
        request.session[SIGNED_IN] = True
        request.session["username"] = username
        db_connection=connect_to_db()
        try:
            cursor=db_connection.cursor()
            query = "select name,id from member where username = %s"
            cursor.execute(query,(username,))
            result = cursor.fetchone()
            if result:
                name, member_id = result
            request.session["id"] = member_id
            request.session["name"] = name
        finally:
            db_connection.close()
        return RedirectResponse(url="/member", status_code=303, headers={"username": username})
    else:
        return RedirectResponse(url="/error?message=Username or password is not correct", status_code=303)


@app.get("/member", response_class=HTMLResponse)
async def member(request: Request):
    username = request.session.get("username")
    name = request.session.get("name")
    token = request.session.get(SIGNED_IN)
    if not token:
        return RedirectResponse(url="/")
    db_connection=connect_to_db()
    try:
        cursor=db_connection.cursor()
        cursor.execute("select member.name,message.content,message.time from message join member on message.member_id = member.id order by time desc")
        data = cursor.fetchall()
        messages=[]
        for row in data:
            membername = row[0]
            messagecontent = row[1]
            messages.append((membername,messagecontent))
    finally:
        db_connection.close()
    return templates.TemplateResponse("memberpage.html", {'request': request,'username': username,'name' : name, 'messages':messages})

@app.get("/error")
async def error(request:Request, message: str):
    return templates.TemplateResponse(
        "error.html",
        {'request':request,'message': message}
    )

@app.get("/signout")
async def sign_out(request: Request):
    request.session[SIGNED_IN] = False
    request.session.pop("username", None) 
    return RedirectResponse(url="/")

@app.get("/register")
async def register(request:Request):
    return templates.TemplateResponse(
        "register.html",
        {'request':request}
    )
@app.post("/signup")
async def register(request:Request, name: str = Form(None), username: str = Form(None), password: str = Form(None)):
    if not name or not username or not password:
        return RedirectResponse(url="/error?message=請輸入用戶名及帳號和密碼", status_code=303)
    try:
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
        query = "select * from member where username = %s"
        cursor.execute(query, (username,))
        if cursor.fetchone():
            return RedirectResponse(url="/error?message=Repeated Username", status_code=303)
        insert_query = "Insert into member (name, username, password) values (%s,%s,%s)"
        cursor.execute(insert_query, (name, username, password))
        db_connection.commit()
        cursor.close()
        return RedirectResponse(url="/", status_code=303)
    finally:
        db_connection.close()
    
@app.post("/createMessage")
async def createMessage(request:Request, content: str = Form(None)):
    id = request.session.get("id")
    db_connection = connect_to_db()
    try:
        cursor = db_connection.cursor()
        insert_query= " insert into message (member_id, content) values (%s,%s)"
        cursor.execute(insert_query,(id,content))
        db_connection.commit()
        cursor.close()
        return RedirectResponse(url="/member", status_code=303)
    finally:
        db_connection.close()

@app.get("/api/member")
async def apimember(request:Request, username: str):
        token = request.session.get(SIGNED_IN)
        if not token:
            data = "null"
            return JSONResponse(content={"data": None})
        try:
            db_connection = connect_to_db()
            cursor = db_connection.cursor()
            query = "select id,name,username from member where username = %s"
            cursor.execute(query,(username,))
            data = cursor.fetchall()
            if not data:
                return JSONResponse(content={"data": None})
                
            else:
                field_names = [i[0] for i in cursor.description]
                data_dict = {}
                for i in range(len(field_names)):
                    data_dict[field_names[i]] = data[0][i]
                data = data_dict
        except:
            return JSONResponse(content={"data": None})
        finally:
            db_connection.close()
        return JSONResponse(content={"data": data}) #調回前端

@app.patch("/api/member")
async def updatename(request:Request):
    token = request.session.get(SIGNED_IN)
    username = request.session.get("username")
    if not token:
        return JSONResponse(content={"error": True})
    
    try:
        data = await request.json()
        new_name = data.get("name")
        if not new_name:
            return JSONResponse(content={"error": True})
        db_connection = connect_to_db()
        cursor = db_connection.cursor()
        query = "update member set name=%s where username = %s"
        cursor.execute(query,(new_name,username))
        db_connection.commit()   # 提交更新
        return JSONResponse(content={"ok": True})
    except:
        return JSONResponse(content={"error": True})
    finally:
        db_connection.close()
    
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
