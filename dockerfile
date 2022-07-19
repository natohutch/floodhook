FROM postgis/postgis:14-3.2
COPY ./requirements.txt /requirements.txt
RUN apt update && apt install -y postgis python3-pip
RUN pip3 install -r requirements.txt
RUN pg_createcluster 14 main
COPY ./initdb.sh /initdb.sh
ENTRYPOINT ["bash", "./initdb.sh"]
COPY ./main.py /main.py
CMD ["python3", "main.py"]