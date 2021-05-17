FROM python:3
RUN mkdir -p /app/resources
RUN pip3 install boto3 scikit-image; pip3 install codeguru_profiler_agent
WORKDIR /app
ADD aws_python_sample_application .
ADD resources resources/.
ENTRYPOINT [ "python", "main.py"]
