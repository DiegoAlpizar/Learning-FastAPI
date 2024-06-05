from fastapi		import Depends, APIRouter , Response , status , HTTPException
from psycopg.errors import NoDataFound, RaiseException
from starlette.status import HTTP_403_FORBIDDEN

from app import OAuth2
from ..schemas		import *
from ..database		import conn , cursor


from alembic_utils.pg_function import PGFunction


router	=	APIRouter( prefix="/posts" , tags=[ "Posts" ] )


@router.get( "/" , response_model=list[ PostOutgoing ] )
#@router.get( "/" )
def getPosts (search: str  = "" , limit: int = 5 , skip: int = 0) :
	
	query	=	"""
				SELECT		posts.*
							, COUNT( votes.post_id ) AS votes
				FROM		posts
				LEFT JOIN	votes
				ON			posts.id = votes.post_id
				WHERE		title LIKE %s
				GROUP BY	posts.id
				LIMIT		%s
				OFFSET		%s
				"""
	print( query )
	posts	=	cursor.execute( query , ('%'+search+'%' , limit , skip) ).fetchall()

	return  posts



@router.get( "/{id}" , response_model=PostOutgoing )
def getPost (id: int) :

	query	=	"""
				SELECT		posts.*
							, COUNT( votes.post_id ) AS votes
				FROM		posts
				LEFT JOIN	votes
				ON			posts.id = votes.post_id
				WHERE		id = %s
				GROUP BY	posts.id
				"""
	post	=	cursor.execute( query , (str( id ) , ) ).fetchone()

	if not post :

		raise	HTTPException( status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with ID: { id } was not found" )


	return  post



@router.post( "/" , status_code=status.HTTP_201_CREATED , response_model=NewPostCreated )
def createPost (newPost: Post , user_ID: int = Depends( OAuth2.getCurrentUser )) :
	
	createdPost	=	cursor.execute( """INSERT INTO posts (title , content , published , user_id) VALUES (%s , %s , %s , %s) RETURNING *""" , (newPost.title , newPost.content , newPost.published , user_ID) ).fetchone()

	conn.commit()

	print( createdPost )

	return  createdPost



@router.put( "/{id}" , response_model=NewPostCreated)
def updatePost (id: int , newPost: Post , user_ID: int = Depends( OAuth2.getCurrentUser )) :

	updatedPost	=	cursor.execute( """UPDATE posts SET title = %s , content = %s , published = %s  WHERE id = %s RETURNING *""" , (newPost.title , newPost.content , newPost.published , str( id )) ).fetchone()


	if not updatedPost :

		raise  HTTPException( status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with ID: { id } was not found" )

	
	if updatedPost[ "user_id" ] != user_ID :

		conn.rollback()
		raise  HTTPException( status_code=HTTP_403_FORBIDDEN , detail=f"User ID: { user_ID } is not the owner of post ID: { id }" )


	conn.commit()

	return  updatedPost



@router.delete( "/{id}" , status_code=status.HTTP_204_NO_CONTENT )
def deletePost (id: int , user_ID: int = Depends( OAuth2.getCurrentUser )) :

	try:

		cursor.execute( """SELECT * FROM delete_post( %s, %s )""" , (str( id ) , user_ID ) ).fetchone()
		conn.commit()

	except NoDataFound :

		conn.rollback()
		raise	HTTPException( status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with ID: { id } was not found" )

	except RaiseException :

		conn.rollback()
		raise	HTTPException( status_code=status.HTTP_403_FORBIDDEN , detail=f"User ID: { user_ID } is not the owner of post ID: { id }" )



delete_post	=	PGFunction( schema		= 'public'
						  , signature	= "delete_post(_id INT , _user_id INT)"
						  , definition	= """
						  				RETURNS posts AS
										$BODY$
										DECLARE
											deleted_post	posts%ROWTYPE ;
										BEGIN
											DELETE
											FROM		posts
											WHERE		id = _id
											RETURNING	*
											INTO STRICT	deleted_post
											;
											
											IF deleted_post.user_id != _user_id
											THEN
												RAISE 'User ID --> % is not the owner of post ID --> %' , _user_id , _id ;
											END IF ;
											
											RETURN	deleted_post ;
										EXCEPTION
											WHEN NO_DATA_FOUND THEN RAISE NO_DATA_FOUND USING MESSAGE = 'Nonexistent post ID --> %' || _id ;
										END ;
										$BODY$
										LANGUAGE plpgsql ;
										"""
						  )
