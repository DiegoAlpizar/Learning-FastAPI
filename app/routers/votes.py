from fastapi import APIRouter, Depends, HTTPException, status
from psycopg.errors import ForeignKeyViolation, UniqueViolation

from app import OAuth2, schemas
from ..database		import conn , cursor



router	=	APIRouter( prefix="/votes" , tags=[ "Votes" ] )


@router.post( "/{post_ID}" , status_code=status.HTTP_201_CREATED )
def vote (post_ID: int , user_ID: int = Depends( OAuth2.getCurrentUser )):

	try:

		createdVote	=	cursor.execute( """INSERT INTO votes (post_id , user_id) VALUES (%s , %s) RETURNING *""" , (post_ID , user_ID) ).fetchone()
		conn.commit()

	except ForeignKeyViolation:

		conn.rollback()
		raise	HTTPException( status_code=status.HTTP_404_NOT_FOUND , detail=f"Post with ID: { post_ID } does not exist" )

	except UniqueViolation:

		conn.rollback()
		raise  HTTPException( status_code=status.HTTP_409_CONFLICT , detail=f"Already voted on post { post_ID }" )


	return  createdVote
	


@router.delete( "/{post_ID}" , status_code=status.HTTP_204_NO_CONTENT )
def withdrawVote (post_ID: int , user_ID: int = Depends( OAuth2.getCurrentUser )):

	deletedVote	=	cursor.execute( """DELETE FROM votes WHERE post_id = %s AND user_id = %s RETURNING *""" , (post_ID , user_ID ) ).fetchone()

	if not deletedVote :

		raise  HTTPException( status_code=status.HTTP_404_NOT_FOUND , detail=f"Vote for Post with ID: { post_ID } does not exist" )


	conn.commit()


