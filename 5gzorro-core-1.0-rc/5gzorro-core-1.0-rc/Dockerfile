FROM python:3.7
ADD . /todo
WORKDIR /todo

RUN pip3 install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
ENV PORT 5556
EXPOSE 5556

CMD ["python","-u", "SRD_temp.py"]
