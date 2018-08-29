import os
import sys
import logging
import random
import time

from boto3 import client
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
        if 'QUEUE_URL' not in os.environ.keys():
            self.log.error("QUEUE_URL env var is not set.")
            sys.exit(1)

        if 'INTERVAL' not in os.environ.keys():
            self.log.error("INTERVAL env var is not set.")
            sys.exit(1)

        """Boto3 will use the AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, 
        and AWS_DEFAULT_REGION env vars as it's credentials
        """
        self.sqs = client('sqs')

        self.url = os.environ.get('QUEUE_URL')
        self.interval = int(os.environ.get('INTERVAL'))

    def send_message_batch(self):

        try:

            count = 0
            batch_size = random.randint(1, 11)
            self.log.info("Sending batch of %s messages", batch_size)

            while count < batch_size:
                self.sqs.send_message(
                    QueueUrl=self.url,
                    MessageBody='stress testing SQS'
                )
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
