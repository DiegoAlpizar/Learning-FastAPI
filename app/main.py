from fastapi					import FastAPI
from fastapi.middleware.cors	import CORSMiddleware
#from fastapi.params	import Body
#from psycopg.extras import RealDictCursor
#from sqlalchemy.orm import Session
#from .				import db_models
#from .database		import engine #, get_db
from .routers	import posts , users , login , votes


#db_models.Base.metadata.create_all( bind=engine )


origins	=	[ "*" ]

app	=	FastAPI()

app.add_middleware( CORSMiddleware
				  , allow_origins=origins
				  , allow_credentials=True
				  , allow_methods=["*"]
				  , allow_headers=["*"]
				  ,
				  )

app.include_router( posts.router )
app.include_router( users.router )
app.include_router( login.router )
app.include_router( votes.router )


@app.get( "/" )
def root () :
	
	return { "message" : "Hello World!" }


from .config	import settings

print( settings )
