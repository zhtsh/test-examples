#!/bin/bash

count=0
while true
do
  curl http://localhost:8080 >/dev/null 2>&1
  sleep 3
done
