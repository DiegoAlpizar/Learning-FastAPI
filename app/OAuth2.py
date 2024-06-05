from jose				import JWTError , jwt
from datetime			import datetime , timedelta
from .schemas			import TokenData
from fastapi			import Depends , status , HTTPException
from fastapi.security	import OAuth2PasswordBearer
from .config			import settings


def createAccessToken (data: dict):

	expire			=	datetime.utcnow() + timedelta( minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES )
	dataWithExpire	=	data.copy()

	dataWithExpire.update( { "exp" : expire } )

	encoded_JWT	=	jwt.encode( dataWithExpire , settings.SECRET_KEY , algorithm=settings.ALGORITHM )

	return  encoded_JWT



def verifyAccessToken (token: str , credentialsException):

	try:

		payload	=	jwt.decode( token , settings.SECRET_KEY , algorithms=settings.ALGORITHM )
		id		=	payload.get( "user_id" )

		if not id:

			raise credentialsException


		tokenData	=	TokenData( id=id )

	except JWTError:

		raise credentialsException


	return  tokenData



oauth2Scheme	=	OAuth2PasswordBearer( tokenUrl='login' )


def getCurrentUser (token: str = Depends( oauth2Scheme )):

	credentialsException	=	HTTPException( status_code=status.HTTP_401_UNAUTHORIZED
											 , detail="Could not validate credentials"
											 , headers={ "WWW-Authenticate" : "Bearer" }
											 )
	tokenData				=	verifyAccessToken( token , credentialsException )

	return  tokenData.id


