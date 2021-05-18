# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import os
import threading
import time
import sys  
import argparse

from image_processor import ImageProcessor
from task_publisher import TaskPublisher

import boto3
from codeguru_profiler_agent import Profiler

def assume_role(iam_role):

    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(RoleArn =  iam_role,
                                      RoleSessionName = "CodeGuru_Python_App",
                                      DurationSeconds = 900)

    codeguru_session = boto3.Session(
        aws_access_key_id     = assumed_role['Credentials']['AccessKeyId'],
        aws_secret_access_key = assumed_role['Credentials']['SecretAccessKey'],
        aws_session_token     = assumed_role['Credentials']['SessionToken']
    )

    return codeguru_session


class SampleDemoApp:
    def __init__(self, sqs_queue_url, s3_bucket_name):
        self.sqs_queue_url = sqs_queue_url
        self.s3_bucket_name = s3_bucket_name
        self.task_publisher = TaskPublisher(self.sqs_queue_url, self.s3_bucket_name)
        self.image_processor = ImageProcessor(self.sqs_queue_url, self.s3_bucket_name)

    def _publish_task(self):
        """
        Setup a thread to publish 10 image transform task every 10 seconds
        """
        while True:
            task_thread = threading.Thread(target=self.task_publisher.publish_image_transform_task,
                                           name="task-publisher")
            task_thread.start()
            task_thread.join()
            time.sleep(10)

    def _process_message(self):
        """
        Setup a thread to process message
        """
        while True:
            task_thread = threading.Thread(target=self.image_processor.run, name="task-publisher")
            task_thread.start()
            task_thread.join()

    def run(self):
        # Publisher
        task_publisher_thread = threading.Thread(target=self._publish_task, name="task_publisher_scheduler")
        task_publisher_thread.start()

        # Listener
        task_processor_thread = threading.Thread(target=self._process_message(), name="task_processor_thread")
        task_processor_thread.start()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-iam_role")
    parser.add_argument("-sqs_url")
    parser.add_argument("-s3_bucket")
    args = parser.parse_args()
    iam_role=args.iam_role
    sqs_queue_url=args.sqs_url
    s3_bucket_name=args.s3_bucket

    print(args)

    iam_role="arn:aws:iam::758007484833:role/CrossAccountCodeGuruProfilerRole"
    sqs_queue_url="https://sqs.eu-west-1.amazonaws.com/338918620411/CodeGuruPythonApp"
    s3_bucket_name="338918620411-account-bucket"

    codeguru_session = assume_role(iam_role)
    
    Profiler(profiling_group_name="codeguru-python-app", 
             region_name="eu-west-1", 
             aws_session=codeguru_session).start()

    SampleDemoApp(sqs_queue_url, s3_bucket_name).run()
