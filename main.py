"""
    코딩에서 살아남기 제 1장 : "확실하지 않으면 커밋하지 마라."
"""

# 코딩에서 살아남기 제 2장 : "예측 불가능하게 임포트 해라."
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, HTMLResponse
import sqlite3, html

# 코딩에서 살아남기 제 3장 : "항상 변수를 조심할 것."
app = FastAPI()

reload = lambda msg:f'''
    <script>
        alert("{msg}");
        window.location.reload();
    </script>
'''

goHome = lambda msg:f'''
    <script>
        alert("{msg}");
        window.location.href = "/";
    </script>
'''

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
        user_escaped = html.escape(i['user'])
        todo_escaped = html.escape(i['todo'])
        response += f"<h3>{user_escaped} 님의 할일 : {todo_escaped}</h3>"
    cur.close()
    con.close()
    return response

@app.post("/api/uploadTodo", response_class=HTMLResponse)
def uploadTodo(user : str = Form(...), todo : str = Form(...)):
    if user == "" :
        return reload(msg= "이름을 입력 해주세요.")
    elif todo == "" :
        return reload(msg= "내용을 입력 해주세요.")
    else :
        con = getConnectDB()
        cur = con.cursor()
        cur.execute("INSERT INTO todo (user, todo) VALUES (?, ?)", (user.replace("<", "&lt;").replace(">", "&gt;"), todo.replace("<", "&lt;").replace(">", "&gt;")))
        con.commit()
        cur.close()
        con.close()
        return goHome(msg= "할일이 작성 되었습니다.")