FROM python:2.7.12
RUN pip2.7 install boto area53
COPY dyndns53.py /

CMD python2.7 /dyndns53.py
