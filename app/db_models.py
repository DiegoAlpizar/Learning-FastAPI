
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String , Identity
from sqlalchemy.sql.expression import text
from .database	import Base


def createdAt () :

	return  Column( TIMESTAMP( timezone=True ) , nullable=False , server_default=text( "now()" ) )



class Post (Base) :

	__tablename__	=	"posts"

	id			=	Column( Integer , Identity( always=True )	, nullable=False , primary_key=True )
	title		=	Column( String								, nullable=False )
	content		=	Column( String								, nullable=False )
	published	=	Column( Boolean								, nullable=False , server_default="True" )
	created_at	=	Column( TIMESTAMP( timezone=True )			, nullable=False , server_default=text( "now()" ) )

	user_id		=	Column( Integer , ForeignKey( "users.id" , ondelete="CASCADE" ) , nullable=False )



class User (Base) :

	__tablename__	=	"users"

	id			=	Column( Integer , Identity( always=True )	, nullable=False , primary_key=True )
	email		=	Column( String								, nullable=False , unique=True )
	password	=	Column( String								, nullable=False )
	created_at	=	createdAt()



class Vote (Base):

	__tablename__	=	"votes"

	post_id	=	Column( Integer , ForeignKey( "posts.id" , ondelete="CASCADE" ) , primary_key=True )
	user_id	=	Column( Integer , ForeignKey( "users.id" , ondelete="CASCADE" ) , primary_key=True )



