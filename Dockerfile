FROM python:3
RUN mkdir -p /app/resources
RUN pip3 install boto3 scikit-image; pip3 install codeguru_profiler_agent
ARG IAM_ROLE
ARG SQS_URL
ARG S3_BUCKET
ENV IAM_ROLE_ENV=${IAM_ROLE}
ENV SQS_URL_ENV=${SQL_URL}
ENV S3_BUCKET_ENV=${S3_BUCKET}
WORKDIR /app
ADD aws_python_sample_application .
ADD resources resources/.
CMD python main.py -iam_role ${IAM_ROLE_ENV} -sqs_url ${SQS_URL_ENV} -s3_bucket ${S3_BUCKET_ENV}