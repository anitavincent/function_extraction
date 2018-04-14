#!/bin/sh

echo "Backup name please"
read NAME

backup_date="$(date +'%d-%m')"
cp $PWD/pictures -r $PWD/../results_log/$backup_date-$NAME

echo "Readme description please"
read description

echo $description >> $PWD/../results_log/$backup_date-$NAME/README