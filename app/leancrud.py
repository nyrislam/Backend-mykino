from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

test = FastAPI()

test.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # "*" означает, что мы разрешаем запросы с ЛЮБОГО фронтенда (удобно для локальной разработки)
    allow_credentials=True,
    allow_methods=["*"], # Разрешаем все методы (GET, POST, DELETE и т.д.)
    allow_headers=["*"], # Разрешаем любые заголовки
)

class Kino(BaseModel):
    id: int | None = None
    title: str 
    description: str 
    genres: list[str] | None = None
    rating: int

my_post = [{
        "id": 1,"title": "Во все тяжкие","description": "Учитель химии становится наркобароном","genres": ["Драма", "Криминал"],"rating": 10
    },{
        "id": 2,"title": "Игра в кальмара","description": "Люди играют в смертельные игры ради денег","genres": ["Триллер", "Драма"],"rating": 8
    },]

def find_post(id):
    for post in my_post:
        if post['id'] == id:
            return post
        
def find_post_delete(id, el):
    for idx, post in enumerate(el):
        post_id = post['id'] if isinstance(post, dict) else post.id
        if post_id == id:
            return idx

@test.get("/")
def read_root():
    return {"messege": "Hello World"}

@test.get("/posts", status_code=status.HTTP_200_OK)
def post():
    return {"data":my_post}

@test.post("/posts", status_code=status.HTTP_201_CREATED)
def creat_post(kino: Kino):
    kino_dict = kino.dict()
    kino_dict['id'] = len(my_post)+1
    my_post.testend(kino_dict)
    
    return {"data": my_post}

@test.get("/posts/{id}")
def get_post(id: int, resp: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Не нашел id={id} и да статус {resp.status_code}")
        # resp.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Не нашел id={id} и да статус {resp.status_code}"}
    return post

@test.delete("/posts/{id}")
def delete_post(id: int):
    idx = find_post_delete(id, my_post)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Не нашел id={id} и да статус {status.HTTP_404_NOT_FOUND}")
    
    my_post.pop(idx)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@test.put("/posts/{id}")
def update_post(id: int, kino: list[Kino], title: str | None = None, description: str | None = None):
    print(kino[0])
    idx = find_post_delete(id, kino)
    print(idx)
    if idx == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Не нашел id={id} и да статус {status.HTTP_404_NOT_FOUND}")

    if title is not None:
        my_post[idx]['title'] = title
    if description is not None:
        my_post[idx]['description'] = description
    return {"data": kino}