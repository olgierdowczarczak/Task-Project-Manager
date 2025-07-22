from pydantic import BaseModel, Field


class CommentModel(BaseModel):
    content: str = Field(alias="content")