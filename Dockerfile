FROM		python:alpine

WORKDIR		/opt/app

COPY		requirements.txt	./

RUN			pip install --no-cache-dir  --requirement requirements.txt  --upgrade

COPY		.	.

CMD			[ "gunicorn"		, "app.main:app"					\
			, "--workers"		, "4" 								\
			, "--worker-class"	, "uvicorn.workers.UvicornWorker"	\
			, "--bind"			, "0.0.0.0:8000"					\
			]
