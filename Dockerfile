FROM python:3.8.5

ADD api.py /

ADD example_database.db /

RUN pip install flask

RUN pip install flask_restful

RUN pip install sqlalchemy

RUN pip install flask_jsonpify

EXPOSE 5003

CMD [ "python", "./api.py" ]

