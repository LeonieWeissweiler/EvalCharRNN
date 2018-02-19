#!/usr/bin/env bash

HOST=calc
FOLDER=Bachelorarbeit

echo " ======== Copying src/ to $HOST ======== "
rsync -r --delete --include='*.py' --exclude='*' ./ $HOST:$FOLDER

echo ""

echo " ======== Running on $HOST ======== "
ssh -t $HOST "cd $FOLDER; screen bash -c 'python3 main.py $1; bash'"


echo ""

echo " ======== Copying results.txt from $HOST ======== "
scp $HOST:$FOLDER/$1/plot.pdf $1/plot.pdf 2>/dev/null
