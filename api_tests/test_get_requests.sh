#!/bin/bash

. ./resty -W $1 -H "Content-Type: application/json"

GET /novel

GET /novel/1  # query by id

GET /chapter

GET /chapter/1

GET /vote

GET /vote/1

GET /story_token

GET /story_token/1
