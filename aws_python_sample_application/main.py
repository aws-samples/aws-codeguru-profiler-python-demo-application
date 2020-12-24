# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
import os
import threading
import time
import date

from image_processor import ImageProcessor
from task_publisher import TaskPublisher


def _get_environment_variable(key, example_value):
    value = os.getenv(key)
    if value is None:
        raise RuntimeError("Environment variable " + key + " must be set, e.g. " + example_value)
    return value


class SampleDemoApp:
    def __init__(self):
        self.sqs_queue_url = _get_environment_variable(
            key="DEMO_APP_SQS_URL", example_value="https://sqs.eu-west-2.amazonaws.com/123456789000/ImageQueue")
        self.s3_bucket_name = _get_environment_variable(
            key="DEMO_APP_BUCKET_NAME", example_value="test-images-for-my-demo-app")
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
    SampleDemoApp().run()
