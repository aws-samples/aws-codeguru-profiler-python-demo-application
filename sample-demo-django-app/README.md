# Amazon CodeGuru Profiler Python Demo Django Web Application

![CodeGuru Profiler Console Screenshot](resources/CodeGuruProfilerPythonScreenshotDemoDjango.png)

### Code

The code for the Django web application is based on the [Django official tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/), with modifications to make some network operations.

## Setup

Here is the summary of the steps that follow.

1. Make sure you have installed the latest version of [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html).
Use an IAM entity for the AWS CLI that has permissions to access CodeGuru Profiler, S3 and SQS to create all the required components for the demo application to run.
2. Create a profiling group in CodeGuru Profiler, named `PythonDemoDjangoApplication`.
3. Create a S3 bucket, e.g. `s3://python-demo-application-test-bucket`. Note, the bucket name must be unique across all of Amazon S3.
See [here](https://docs.aws.amazon.com/cli/latest/reference/s3/mb.html) for more details.
5. Create virtual environment with venv, e.g. `python3 -m venv ./venv`.
6. Activate the virtual environment, e.g. `source venv/bin/activate`.
7. Install the needed dependencies that are used for the demo application through `pip` using the `requirements.txt` file.

Here are the commands to run on your machine.

```bash
aws configure # Set up your AWS credentials and region as usual.
```

```bash
aws codeguruprofiler create-profiling-group --profiling-group-name PythonDemoDjangoApplication

# It is required to set the DEMO_APP_BUCKET_NAME environment applications for later running the demo application.

# Make sure you update `YOUR-BUCKET-NAME-REPLACE-ME`with a bucket name that is unique across all of Amazon S3.
export DEMO_APP_BUCKET_NAME=YOUR-BUCKET-NAME-REPLACE-ME
aws s3 mb s3://${DEMO_APP_BUCKET_NAME}
```

```bash
python3 -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to run

The main entry point is in ``sample-demo-django-app/mysite/wsgi.py`` where the configuration is set to be read from ``mysite.settings`` that is in ``sample-demo-django-app/mysite/settings.py``.

* The ``INSTALLED_APPS`` in that file contains what applications to install, including the ``polls.apps.PollsConfig`` that is configured in the ``sample-demo-django-app/polls`` folder; for example, you can find the mapping for each url in ``sample-demo-django-app/polls/urls.py``.

* There you can find the configuration for CodeGuru Profiler to start and to log.

### Run the service.

1. Create the tables in the databases and load the initial data.
    ```bash
    python manage.py migrate
    python3 manage.py loaddata initial_local_db_data.json
    ```

2. Start the service using **one** of the following commands, depending on what web server you want.

    2.1 Start the service using a development server.
    ```bash
    python manage.py runserver
    ```

    2.2. Start the service using [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/) with multiple workers; use the `--enable-threads` and `--lazy-apps` parameters  for your startup configuration, so Profiler can be started. This was tested for uswgi version 2.0.19.1.
    ```bash
    uwsgi --http :8000 --chdir . --wsgi-file mysite/wsgi.py --enable-threads --lazy-apps --disable-logging --workers=4
    ```

    2.3. Start the service using [Apache HTTP server (httpd)](https://httpd.apache.org/) with the [mod_wsgi](https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/modwsgi/) module. Make sure the `wsgi.py` file is configured to be visible in the `httpd.conf` file. This was tested for httpd version 2.4.46.
    ```bash
    <Directory [to_be_replaced]/aws-codeguru-profiler-python-demo-application/sample-demo-django-app/mysite>
    <Files wsgi.py>
    Require all granted
    </Files>
    </Directory>
    ```

    ```bash
    apachectl start
    ````

### Generate traffic

1. Generate traffic by running the following script that will make thousands of requests to the local server started at `http://127.0.0.1:8000`.
    ```bash
    ./generate_traffic.sh
    ```

## How to see the results

Go to the [AWS CodeGuru Profiler console](https://console.aws.amazon.com/codeguru/profiler) to check the results. Choose the region you picked and your profiling group.

The attached screenshot was captured by hiding the `subprocess:Popen:_try_wait` frame because it covered more than half of the time.
