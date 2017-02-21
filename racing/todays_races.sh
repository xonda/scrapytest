#!/bin/bash

DATE=`date +%d-%m-%Y`
FILENAME="races_$DATE.csv"

if [ -f $FILENAME ]; then
    rm $FILENAME
fi

scrapy crawl todays -o $FILENAME
