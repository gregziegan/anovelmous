#!/bin/sh

. ./resty -W $1 -H "Content-Type: application/json"

novel_name="test"
current_timestamp=`(date "+%Y.%m.%d-%H.%M.%S")`
novel_full_name="$novel_name$current_timestamp"

POST /novel "{\"name\": \"$novel_full_name\"}"


POST /story_token