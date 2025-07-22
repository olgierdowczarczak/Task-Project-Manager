from pydantic import BaseModel


class CommentModel(BaseModel):
    content: str