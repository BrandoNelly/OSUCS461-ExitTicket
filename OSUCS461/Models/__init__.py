from pydantic import BaseModel

class BasePydanticModel(BaseModel):
	class Config:
		from_attributes = False
		validate_assignment = True


class User(BasePydanticModel):
	uuid: str
	name: str
	time_created: int

class ReadUser(User):
	uuid: str
	name: str
	time_created: int


class UserPost(BaseModel):
	uuid: str
	user_uuid: str
	post_9char: str
	text: str
	time_created: int


class CreateUserRequest(BaseModel):
	email: str


class CreatePostRequest(BaseModel):
	text:str
	user_uuid: str


class ReadUserPost(UserPost):
	uuid: str
	user_uuid: str
	post_9char: str
	text: str
	time_created: int

class PreviewUserPost(BaseModel):
	uuid: str
	post_9char: str
	time_created: int

