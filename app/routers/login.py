from fastapi					import Depends, APIRouter , status , HTTPException
from fastapi.security.oauth2	import OAuth2PasswordRequestForm
from ..schemas					import Token
from ..utils					import hash , verify
from ..database					import conn , cursor
from ..OAuth2					import createAccessToken


router	=	APIRouter( prefix="/login" , tags=[ "Users" , "Login" ] )


@router.post( "/" , response_model=Token )
def login (userLogin: OAuth2PasswordRequestForm = Depends()):

	user	=	cursor.execute( """SELECT * FROM users WHERE email = %s""" , (userLogin.username , ) ).fetchone()

	if not user  or  not verify( userLogin.password , user[ "password" ] ) :

		raise	HTTPException( status_code=status.HTTP_403_FORBIDDEN , detail="Invalid Credentials" )


	data		=	{ "user_id" : user[ "id" ] }
	accessToken	=	createAccessToken( data=data )

	response	=	{ "access_token" : accessToken
			, "token_type"   : "bearer"
			}

	return  response

