#!/bin/bash

curl "http://localhost:8000/profiles/${ID}/" \
  --include \
  --request PATCH \
  --header "Content-Type: application/json" \
  --header "Authorization: Token ${TOKEN}" \
  --data '{
    "profile": {
      "name": "'"${NAME}"'",
      "age": "'"${AGE}"'",
      "about_me": "'"${ABOUT_ME}"'"
    }
  }'

echo
