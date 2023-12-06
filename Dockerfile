FROM python:bullseye

COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
