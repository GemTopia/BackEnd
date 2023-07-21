FROM python:3

ENV PYTHONPATH "${PYTHONPATH}:/BackEnd"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /gemtopia

COPY . /gemtopia

RUN pip install --upgrade pip

RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install gunicorn

RUN python3 -m pip install mysqlclient

RUN chmod -R +x run.sh

ENV PATH="/py/bin:/:$PATH"

RUN mkdir /logs

CMD ["./run.sh"]