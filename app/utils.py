from passlib.context	import	CryptContext


pwd_context	=	CryptContext( schemes=[ "bcrypt" ] , deprecated="auto" )


def hash (password: str):

	return  pwd_context.hash( password )



def verify (plainPassword , hashedPassword):

	return  pwd_context.verify( plainPassword , hashedPassword )	# It throws! ... if it doesn't recognize the hash


