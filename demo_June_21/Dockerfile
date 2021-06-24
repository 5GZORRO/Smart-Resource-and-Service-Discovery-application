FROM python:3.7
ADD product_offers_with_SLAs.json /
ADD product_offers_with_SLAs_template.json /
ADD . /todo
WORKDIR /todo

RUN pip3 install --no-cache-dir -r requirements.txt
ENV PORT 5000
EXPOSE 5000

CMD ["python","-u", "SRD.py"]
