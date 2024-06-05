from pydantic_settings	import BaseSettings


class Settings (BaseSettings):

	POSTGRES_PASSWORD:	str	=	"postgres"
	POSTGRES_DB:		str	=	"FastAPI"

	DB_HOSTNAME:	str	=	"localhost"
	DB_NAME:		str	=	POSTGRES_DB
	DB_USER:		str	=	"postgres"
	DB_PASSWORD:	str	=	POSTGRES_PASSWORD
	
	SECRET_KEY:						str	=	""
	ALGORITHM:						str	=	""
	ACCESS_TOKEN_EXPIRE_MINUTES:	int	=	30
	
	class Config:

		env_file	=	".env"




settings	=	Settings()
