FROM python:2.7.12
RUN pip2.7 install boto requests area53
COPY . /app

CMD python2.7 /app/dyndns53.py
