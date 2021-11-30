from fastapi  import Response,status,Depends,HTTPException,APIRouter
from .. import models,schemas,oauth2
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get('/',response_model=List[schemas.PostOut])
def posts(db:Session = Depends(get_db),limit:int = 10,skip:int = 0,search:Optional[str] = ''):

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()

    
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post:schemas.PostCreate,db:Session = Depends(get_db),
    current_user:int = Depends(oauth2.get_current_user)):

    #cursor.execute('''INSERT INTO posts(title,content,publish) VALUES(%s,%s,%s) RETURNING *''',(post.title,post.content,post.publish))
    #new_post = cursor.fetchone()
    #conn.commit()
    #print(**post.dict())

    new_post = models.Post(title = post.title,content=post.content,publish=post.publish,user_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{post_id}",response_model=schemas.PostOut)
def get_post(post_id:int,db:Session = Depends(get_db)):
    #cursor.execute('''SELECT * FROM posts where id=%s''',(str(post_id),))
    #post = cursor.fetchone()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(
            models.Post.id == post_id).first()

    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with Id {post_id} does not exist")
    return post

@router.put("/{post_id}",response_model=schemas.Post)
def update_post(post_id:int,post:schemas.PostCreate,db:Session = Depends(get_db),
    current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute('''UPDATE posts SET title=%s,content=%s,publish=%s WHERE id=%s RETURNING *''',(post.title,post.content,post.publish,str(post_id)))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_first = post_query.first()
    
    if post_first == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with Id {post_id} does not exist")

    if post_first.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail=f"Not allowed to Modify")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{post_id}",status_code = status.HTTP_204_NO_CONTENT)
def delete_post(post_id:int,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    #cursor.execute('''DELETE FROM posts WHERE id=%s RETURNING *''',(str(post_id),))

    #deleted_post = cursor.fetchone()

    #conn.commit()

    post = db.query(models.Post).filter(models.Post.id ==post_id)
    if not post.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail=f"Post with Id {post_id} does not exist")

    if post.first().user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail=f"Not allowed to Modify")
    
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
