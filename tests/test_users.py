from fastapi.testclient import TestClient
from app.main import app
from app.schemas	import UserOutgoing

from alembic	import command


client	=	TestClient( app )


def test_create_user ():
	
	email		=	"someone@SomeOne.com"
	jsonBody	=	{ "email":		email
					, "password":	"ApaSsWord123"
					}

	resp		=	client.post( "/users" , json=jsonBody )
	jsonResp	=	resp.json()
	newUser		=	UserOutgoing( **jsonResp )

	assert  newUser.email	 == email
	assert  resp.status_code == 201






def client ():

	command.upgrade( "head" )
	yield TestClient( app )
	command.downgrade( "base" )

