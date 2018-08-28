import os
import sys
import logging
import random
import time

from boto3 import resource
from botocore.errorfactory import ClientError


class StressSQS:

    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def __init__(self):

        # Override the boto logging level to something less chatty
        logger = logging.getLogger('botocore.vendored.requests')
        logger.setLevel(logging.ERROR)

        # Start logging
        logging.basicConfig(
            level=logging.INFO,
            format=self.LOGGING_FORMAT
        )

        self.log = logging.getLogger("stress-sqs")

        # Verify environment vars for SQS config exist
        if 'SQS_NAME' not in os.environ.keys():
            self.log.error("SQS_NAME env var is not set.")
            sys.exit(1)

        if 'SQS_ENDPOINT' not in os.environ.keys():
            self.log.error("SQS_ENDPOINT env var is not set.")
            sys.exit(1)

        if 'INTERVAL' not in os.environ.keys():
            self.log.error("INTERVAL env var is not set.")
            sys.exit(1)

        self.interval = os.environ.get('INTERVAL')

    def send_message_batch(self):

        endpoint_url = os.environ.get('SQS_ENDPOINT')
        queue_name = os.environ.get('SQS_NAME')

        self.log.info("SQS queue name:  %s", queue_name)

        try:
            """Boto3 will use the AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, 
                and AWS_DEFAULT_REGION env vars as it's credentials
            """
            sqs = resource(
                'sqs',
                endpoint_url=endpoint_url
            )

            count = 0
            while count < random.randint(1, 11):
                sqs.send_message(MessageBody='stress testing SQS')
                count += 1

        except ClientError as e:
            self.log.error("Boto3 client error: %s", e.response)

    def run(self):

        while True:
            self.send_message_batch()
            self.log.info("Sleeping for %s seconds", self.interval)
            time.sleep(self.interval)

if __name__ == "__main__":
    stressSqs = StressSQS()
    stressSqs.run()
