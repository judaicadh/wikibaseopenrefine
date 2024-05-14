FROM python:3.9-slim

WORKDIR /openrefine-wikibase


COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . /openrefine-wikibase

EXPOSE 8000
CMD [ "python", "app.py" ]
