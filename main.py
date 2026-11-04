from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates


app = FastAPI()
# directory => 앞으로 html 파일을 찾을 위치
templates = Jinja2Templates(directory='templates')


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

@app.get('/pong')
def pong(request: Request, count: int):
    cube = count ** 3
    return templates.TemplateResponse(
        request=request, 
        name='pong.html',
        context={'count': cube}
    )

