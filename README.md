# stress-sqs
Dockerized application that can be run under Marathon management to stress an AWS Simple Queue Service by adding messages.

## Prerequisites
1. A running DC/OS cluster
2. DC/OS CLI installed on your local machine

If running on a DC/OS cluster in Permissive or Strict mode, an user or service account with the appropriate permissions to modify Marathon jobs.  An example script for setting up a service account can be found in create-service-account.sh

## Installation/Configuration

### Building the Docker container

How to build the container:
    
    docker build .
    docker tag <tag-id> <docker-hub-name>/stress-sqs:latest
    docker push <docker-hub-name>/stress-sqs:latest

### Marathon example
Update the environment variables in the [Marathon definition](stress-sqs-marathon.json) to match your specific configuration.

Core environment variables available to the application:

    SQS_NAME # name of the aws simple queue service
    SQS_ENDPOINT # endpoint url of the sqs service
    AWS_ACCESS_KEY_ID # aws access key
    AWS_SECRET_ACCESS_KEY # aws secret key
    AWS_DEFAULT_REGION # aws region

## Program Execution / Usage

Add your application to Marathon using the DC/OS Marathon CLI.

    $ dcos marathon app add stress-sqs-marathon.json

Verify the app is added with the command `$ dcos marathon app list`

