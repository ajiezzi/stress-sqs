
FROM python:3-alpine

# Copy the python scripts into the working directory
ADD / /stress_sqs
WORKDIR /stress_sqs

RUN apk add --update --virtual .build-dependencies openssl-dev libffi-dev python-dev make gcc g++
RUN pip install -r requirements.txt

# Start the stress application
CMD python stress_sqs.py
