FROM python:3.7
ADD json_posts_formatted.json /
ADD . /todo
WORKDIR /todo

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python","-u", "app.py"]
