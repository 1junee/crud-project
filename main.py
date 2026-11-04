from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates


app = FastAPI()
# directory => 앞으로 html 파일을 찾을 위치
templates = Jinja2Templates(directory='templates')

# 가상의 데이터
posts = {
    1: {'id': 1, 'title': '출석 인증', 'content': '출석 인증합니다.'},
    2: {'id': 2, 'title': '등업 요청', 'content': '등업 요청합니다.'},
}


@app.get('/')
def home():
    return {'hello': 'world'}


@app.get('/ping')
def ping(request: Request):
    return templates.TemplateResponse(
        # 필수 2개
        request=request,
        name='ping.html',
        # 선택
        # context=,
    )

# 받는 정보를 사용하는 페이지 (get 방식)
@app.get('/pong')
def pong(request: Request, count: int):
    cube = count ** 3
    return templates.TemplateResponse(
        request=request, 
        name='pong.html',
        context={'result': cube}
    )
# http://127.0.0.1:8000/pong?count=3


# 받는 정보를 사용하는 페이지 (post 방식)
@app.post('/pong')
def pong_post(request: Request, count: int = Form()):
    return templates.TemplateResponse(
        request=request,
        name='pong.html',
        context={'result': count ** 2}
    )


