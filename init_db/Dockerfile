FROM python:3
RUN pip install --upgrade pip && \
	pip install mysql-connector-python
RUN mkdir /init
COPY . /init
WORKDIR /init
