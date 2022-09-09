FROM python:latest

RUN mkdir /app/
WORKDIR /app/

COPY ./requirements.txt  /app/requirements.txt
COPY ./acceleration-calc.py  /app/acceleration-calc.py

RUN pip3 install -r /app/requirements.txt

ENV FLASK_APP=acceleration-calc

#ENTRYPOINT ["python3"]
#CMD ["acceleration-a.py"]
CMD flask run -h 0.0.0.0 -p 80
