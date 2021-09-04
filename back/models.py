from pydantic import BaseModel, constr, Field


class Profile(BaseModel):
    name: constr(min_length=2, max_length=40)  # Constrained Str
    age: int = Field(
        ...,
        gt=0,
        lt=150,
        description='user age(Human)'
    )


class Config:
    schema_extra = {
        'example': {
            'name': 'very_important_user',
            'age': 42,
        }
    }


class Message(BaseModel):
    text: str
