FROM python:slim
MAINTAINER Matthew Hartley <Matthew.Hartley@jic.ac.uk>

RUN apt-get update && apt-get install pigz libmagic1 && apt-get clean
COPY jobarchitect-0.1.0-py3-none-any.whl /root/
RUN pip install /root/jobarchitect-0.1.0-py3-none-any.whl

