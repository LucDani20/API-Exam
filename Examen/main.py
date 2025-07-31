from pydoc import pager
from typing import List
from fastapi import FastAPI, Response
from pydantic import BaseModel
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/ping")
def pong_affiche(): 
    return Response(encoding = "UTF-8",
             status_code = 200, content = "pong",
               media_type = "text/plain")

@app.get("/home")
def Say_welcome():
    with open ("welcome.html","r", encoding="utf-8") as file :
        html_content = file.read()
        return Response(content=html_content,status_code=200, media_type="text/html")
    
@app.get("/{full_path:path}")
def error (full_path: str): 
    with open("not_found.html","r", encoding="utf_8") as file : 
        html_content = file.read()
        return Response(content=html_content,status_code=404, media_type="text/html")


class Publication(BaseModel):
    author : str
    title : str
    content : str
    creation_datetime : str


    
@app.post("/posts")
def post(updated: List[Publication]):
    global posts
    existing_author = {Publication["author"]: Publication for Publication in posts}

    for  publication in updated:
        if Publication.author in existing_author:
            if existing_author[Publication.author] != pager.dict():
                for i, p in enumerate(posts):
                    if p["author"] == pager.author:
                        posts[i] = pager.dict()
        else:
            posts.append(pager.dict())
    
    return posts


@app.get("/posts")
def get_post():
    return posts

class Put_post(BaseModel) :
    title : str

@app.put("/posts")
def put_post(updated_posts : List[Put_post]):
    if len(updated_posts) == 0:
        return JSONResponse(content={"error message" : "0 taske to updated"},status_code=400)
    else:
        for updated_posts in updated_posts :