#!/bin/bash

curl -X 'POST' \
  'http://localhost:8000/create_event' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": {
    "name": "Hoobastank Concert",
    "location": "Bonferroni Dacto"
  }
}'