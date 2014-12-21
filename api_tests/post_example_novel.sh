#!/bin/sh

. ./resty -W $1 -H "Content-Type: application/json"

novel_name="test"
current_timestamp=`(date "+%Y.%m.%d-%H.%M.%S")`
novel_full_name="$novel_name$current_timestamp"

novel_id=$(POST /novel "{\"name\": \"$novel_full_name\"}" | jsawk "return out(this.id)")
current_chapter_id=$(POST /chapter "{\"name\": \"Chapter 1\", \"novel_id\": $novel_id}" | jsawk "return out(this.id)")

index=0
is_chapter_num=0
for WORD in $(cat ./huck_finn.txt); do
    if [ "$WORD" == "CHAPTER" ]; then
        let current_chapter_id=current_chapter_id+1
        POST /chapter "{\"name\": \"Chapter $current_chapter_id\", \"novel_id\": $novel_id}"
        is_chapter_num=1
        continue
    fi
    if [ is_chapter_num == 1 ]; then
        is_chapter_num=0
        continue
    fi

    POST /novel_token "{\"token\": \"$WORD\", \"ordinal\": $index, \"chapter_id\": $current_chapter_id}"
    let index=index+1
done