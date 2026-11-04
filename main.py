from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

app = FastAPI()
# directory => 앞으로 html 파일을 찾을 위치
templates = Jinja2Templates(directory='templates')

# 가상의 데이터
posts = {
    1: {'id': 1, 'title': '출석 인증', 'content': '출석 인증합니다.'},
    2: {'id': 2, 'title': '등업 요청', 'content': '등업 요청합니다.'},
}
next_id = max(posts) + 1 if posts else 1  # 다음 글에 줄 번호 (삭제와 상관없이 증가만 함)


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


# 전체 게시물 출력
@app.get('/posts')
def post_list(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='list.html',
        context={'posts': list(posts.values())}
    )


# ping
# 사용자가 데이터 입력할 수 있는 페이지 제공
@app.get('/posts/new')
def post_new(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='new.html'
    )


# pong
# 사용자가 넘겨준 데이터를 저장
# @app.get('/posts/create')
@app.post('/posts/create')
def post_create(title: str = Form(), content: str = Form()):
    global next_id          # 함수 밖의 next_id를 바꾸겠다는 선언
    new_id = next_id
    next_id += 1            # 번호표 한 장 뽑았으니 다음 번호로

    posts[new_id] = {'id': new_id, 'title': title, 'content': content}

    # 리디렉션
    # 게시물을 쓰면, 게시물을 보여주게 하고 싶을 때
    # return RedirectResponse('/posts', status_code=303)
    return RedirectResponse(f'/posts/{new_id}', status_code=303)


# 하나의 게시물 출력
@app.get('/posts/{post_id}')
def post_detial(request: Request, post_id: int):
    post = posts[post_id]
    return templates.TemplateResponse(
        request=request,
        name='detail.html',
        context={'post': post}
    )



@app.get('/posts/{post_id}/edit')
def post_edit(request: Request, post_id: int):
    post = posts[post_id]

    return templates.TemplateResponse(
        request=request,
        name='edit.html',
        context={'post': post}
    )


# 아마 post
@app.post('/posts/{post_id}/update')
def post_update(post_id: int,
                title: str = Form(), 
                content: str = Form()):
    # 기존 정보 찾기
    old_post = posts[post_id]
    # 수정하기
    old_post['title'] = title
    old_post['content'] = content
    new_post = old_post
    # 수정 적용
    posts[post_id] = new_post
    
    return RedirectResponse(f'/posts/{post_id}', status_code=303)


# @app.get('/posts/{post_id}/delete')
@app.post('/posts/{post_id}/delete')
def post_delete(post_id: int):
    posts.pop(post_id)

    return RedirectResponse('/posts', status_code=303)