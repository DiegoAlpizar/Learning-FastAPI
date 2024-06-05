from datetime	import datetime
from pydantic	import BaseModel, EmailStr
from typing		import Optional


class Post (BaseModel):

	title:		str
	content:	str
	published:	bool	=	True



class User (BaseModel):

	email:		EmailStr



class UserLogin (User):

	password:	str



class UserOutgoing (User):

	id:	int



class NewPostCreated (Post):
	
	id:			int
	user_id:	int
	created_at: datetime



class PostOutgoing (NewPostCreated):

	votes:	int
	#user:		UserOutgoing



class Token (BaseModel):

	access_token:	str
	token_type:		str



class TokenData (BaseModel):

	id:	int | None	=	None



class Vote (BaseModel):

	post_id:	int
	did_vote:	bool



