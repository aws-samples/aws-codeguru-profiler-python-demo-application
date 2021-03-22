#!/bin/bash

START_DATETIME=$(date +%s)

COUNT=1000

for i in $(seq 1 $COUNT); do
  echo "> Running #$i from ${COUNT}... "
  sleep 1
  pytest integration_tests
  sleep 1.5
  curl -v -o /dev/null http://127.0.0.1:8000/hello
  sleep 2
  curl -v -o /dev/null http://127.0.0.1:8000/auth/login -L
done

END_DATETIME=$(date +%s)
RUNTIME=$((END_DATETIME - START_DATETIME))

echo "> Duration: ${RUNTIME} seconds ($((RUNTIME / 60)) minutes)"
