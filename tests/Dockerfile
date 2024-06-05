FROM		python:alpine

WORKDIR		/opt/app

COPY		tests/requirements.txt	tests/requirements.txt

COPY		requirements.txt	./

RUN			pip install --no-cache-dir							\
						--requirement tests/requirements.txt	\
						--upgrade

RUN			pip install --no-cache-dir							\
						--requirement requirements.txt			\
						--upgrade
