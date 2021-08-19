# Amazon CodeGuru Profiler Python Demo Lambda Application

To enable Amazon CodeGuru Profiler for a Lambda application, follow these instructions:
* For Python 3.8: Enable `Code Profiling` for your Lambda's configuration in the `Monitoring and operation tools` tab: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-short.html#setting-up-step-2

* For Python 3.6+: Follow these instructions for enabling Profiler https://docs.aws.amazon.com/codeguru/latest/profiler-ug/python-lambda.html

Here's a sample code you can run in a Python Lambda in your account. You can follow the instructions to have a Python Lambda deployed in your account with CodeGuru Profiler enabled.

### Create resources

First step is to create the resources needed to run the application.

* Go to the S3 console, create an S3 bucket and take a note of the name.
    * Example of the name: profiler-python-recommendations-demo

* Create a IAM role with these permissions to be used by the Lambda application
    * Choose Lambda to allow our lambda functions to call AWS services on your behalf.
    * Choose AWSLambdaBasicExecutionRole.
    * Create an inline policy and name it profiler-python-recommendations-demo-policy.
    * Name the role profiler-python-recommendations-demo-role.
```
{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject",
                    "cloudwatch:PutMetricData"
                ],
                "Resource": "*"
            }
        ]
    }
```
* Create a Lambda with the following configuration:
    * Name: profiler-python-recommendations-demo.
    * Runtime: Python 3.8.
    * Change the default execution role to the newly created one.
    * Add environment variable S3_BUCKET with the value of the bucket name that was just created.
    * Update timeout to 10 seconds.
* Copy-paste the code from this repository from `lambda_function.py`in the `lambda_function.py` file directly in the Lambda console in the Code tab.

### Run the application

Now, let’s run the application.

* Run Deploy and Test.
    * The Lambda should be successful and print some logs.
    * You can also check the published metrics in the CloudWatch console.
* Configure it to run every 1 minute.
    * Click “Add trigger”.
    * Choose EventBridge (Cloudwatch Events).
    * Create a new rule named “profiler-python-recommendations-demo-rule”.
    * Set schedule expression to “rate(1 minute)”.
    * Click “Add”.
* You can check now the Monitor tab to see the CloudWatch metrics about invocations, duration, success and others.
* You can also go to the Cloudwatch console and see the metrics the application is publishing in the customer namespace as part of the code.

### Enable code profiling

* Enable code profiling by using the [automated onboarding process for Lambda](https://aws.amazon.com/about-aws/whats-new/2021/07/amazon-codeguru-profiler-announces-automated-onboarding-process-aws-lambda-functions/).
    * Go to the Configuration tab.
    * Click Monitoring and operations tools.
    * Click Edit and enable “Code profiling”.

### Analyzing the application

Go to the Monitor tab for your Lambda and then click “View profiles in CodeGuru”. Your profiling group’s name will be the same as your Lambda’s name.

Wait for 15 minutes for CodeGuru Profiler to aggregate and show the data and approximately 1 hour for the recommendations.
