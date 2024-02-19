"""
    코딩에서 살아남기 제 1장 : "확실하지 않으면 커밋하지 마라."
"""

# 코딩에서 살아남기 제 2장 : "예측 불가능하게 임포트 해라."
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import sqlite3

# 코딩에서 살아남기 제 3장 : "항상 변수를 조심할 것."
app = FastAPI()

# 코딩에서 살아남기 제 4장 : "함수는 코드 아니면 멀리할것."
def getConnectDB():
    """connect the sqlite3 DB(todo.db)"""
    con = sqlite3.connect('todo.db')
    con.row_factory = sqlite3.Row
    return con

# 코딩에서 살아남기 제 5장 : "http코드가 404면 빠르게 라우팅 할것."
@app.get("/",response_class=FileResponse)
def index():
    return "html/index.html"

# 코딩에서 살아남기 제 6장 : "프론트의 API 요청을 유도할것."
@app.get("/api/getTodo", response_class=HTMLResponse)
def getTodo():
    con = getConnectDB()
    cur = con.cursor()
    todo = cur.execute("SELECT * FROM todo")
    response = ""
    for i in todo:
        response += f"<h3>{i['user']}님의 할일 : {i['todo']}</h3>"
    
    return response