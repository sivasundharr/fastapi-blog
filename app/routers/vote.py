from fastapi  import status,Depends,HTTPException,APIRouter
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags = ["Vote"]
)

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND,detail=f'Post does not exist')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
        models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=HTTP_409_CONFLICT,detail=f'user {current_user.id} has already voted')

        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"successfully deleted voted"}
