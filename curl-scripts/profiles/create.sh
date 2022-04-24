#!/bin/bash

curl "http://localhost:8000/profiles/" \
  --include \
  --request POST \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "mango": {
      "name": "'"${NAME}"'",
      "age": "'"${AGE}"'",
      "about_me": "'"${ABOUT_ME}"'"
    }
  }'

echo
