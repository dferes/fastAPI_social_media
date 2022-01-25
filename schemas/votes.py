from pydantic import BaseModel, conint


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1, ge=0) # 1 = upvote 0 = downvote
