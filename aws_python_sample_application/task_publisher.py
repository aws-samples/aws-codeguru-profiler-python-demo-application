# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import os
import boto3
import random

SAMPLE_IMAGES_FOLDER = "input-images/"
EXAMPLE_IMAGE_LOCAL_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "resources", "example-image.png"
)


class TaskPublisher:
    def __init__(self, sqs_queue_url, s3_bucket_name):
        self.s3_client = boto3.client('s3')
        self.sqs_client = boto3.client('sqs')
        self.sqs_queue_url = sqs_queue_url
        self.s3_bucket_name = s3_bucket_name

    def _list_image_on_s3(self):
        try:
            print("Listing image in " + self.s3_bucket_name + " under " + SAMPLE_IMAGES_FOLDER)
            response = self.s3_client.list_objects_v2(Bucket=self.s3_bucket_name, Prefix=SAMPLE_IMAGES_FOLDER)

            objects_in_s3 = list(map(lambda x: x["Key"], response["Contents"]))
            print("Listed image in " + self.s3_bucket_name + " under " + SAMPLE_IMAGES_FOLDER + " successfully.")
            return list(filter(lambda x: x != SAMPLE_IMAGES_FOLDER, objects_in_s3))
        except Exception:
            print("Failed to list images in " + self.s3_bucket_name + " under " + SAMPLE_IMAGES_FOLDER)
            return []

    def _upload_images_onto_s3(self):
        try:
            print("Uploading example image onto S3")
            self.s3_client.upload_file(Filename=EXAMPLE_IMAGE_LOCAL_PATH, Bucket=self.s3_bucket_name,
                                       Key=SAMPLE_IMAGES_FOLDER + "example-image.png")
            print("Successfully uploaded example image onto S3")
        except Exception:
            print("Failed to upload example image onto S3")
            raise

    def _send_sqs_message(self, message):
        try:
            self.sqs_client.send_message(
                QueueUrl=self.sqs_queue_url,
                MessageBody=message
            )
            print("Sent task to SQS.")
        except Exception:
            print("Failed to send message onto sqs queue")

    def publish_image_transform_task(self, num_of_tasks=10):
        images = self._list_image_on_s3()
        if len(images) == 0:
            print("No images in bucket. Uploading example image...")
            self._upload_images_onto_s3()
            return

        print("Start publishing task onto sqs...")
        for i in range(num_of_tasks):
            lucky_number = random.randint(0, len(images)-1)
            self._send_sqs_message(str(images[lucky_number]))
