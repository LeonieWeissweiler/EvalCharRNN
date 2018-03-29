#!/usr/bin/env bash

HOST=$1
FOLDER=Bachelorarbeit

echo " ======== Copying src/ to $HOST ======== "
rsync -r --delete --include="*.sh" --include="src/" --include="src/*" --exclude="*" ./ $HOST:$FOLDER


# echo ""
# echo " ======== Running on $HOST ======== "
# ssh -t $HOST "cd $FOLDER/src; screen bash -c 'python3 generate.py $2; bash'"
