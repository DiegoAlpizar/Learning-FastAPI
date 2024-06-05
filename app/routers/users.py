from fastapi		import Depends, APIRouter , Response , status , HTTPException
from psycopg.errors import Error
from ..schemas		import *
from ..utils		import hash , verify
from ..database		import conn , cursor


router	=	APIRouter( prefix="/users" , tags=[ "Users" ] )


@router.post( "/" , status_code=status.HTTP_201_CREATED , response_model=UserOutgoing )
def createUser (newUser: UserLogin) :
	
	hashed_password	=	hash( newUser.password )
	
	try:	# Email may already be registered

		createdUser		=	cursor.execute( """INSERT INTO users (email , password) VALUES (%s , %s) RETURNING *""" , (newUser.email , hashed_password) ).fetchone()

	except Error :	# Don't tell posible attacker about it (account enumeration). Just pretend it was succesfully created.

		conn.rollback()

		createdUser		=	cursor.execute( """SELECT * FROM users WHERE email = %s""" , (newUser.email , ) ).fetchone()


	conn.commit()

	return  createdUser



@router.get( "/{id}" , response_model=UserOutgoing )
def getUser (id: int) :

	user	=	cursor.execute( """SELECT * FROM users WHERE id = %s""" , (str( id ) , ) ).fetchone()

	if not user :

		raise	HTTPException( status_code=status.HTTP_404_NOT_FOUND , detail=f"User with ID: { id } was not found" )


	return  user
