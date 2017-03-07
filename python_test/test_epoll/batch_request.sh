#!/bin/bash

for i in $(seq $1)
do
  nohup sh client_test.sh &
done
