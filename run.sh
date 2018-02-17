#!/usr/bin/env bash

HOST=calc
FOLDER=Bachelorarbeit

if [ -z "$1" ]
then
	echo " ======== Copying src/ to $HOST ======== "
	rsync -r --delete --include='*/' --exclude='data/' --include='*.py' --exclude='*'  ./ $HOST:$FOLDER

	echo ""

	echo " ======== Running on $HOST ======== "
	ssh -t $HOST "cd $FOLDER; screen bash -c 'python3 main.py $2; bash'"

elif [ $1 == "recover" ]
then
	echo " ======== Reconnecting to screen on $HOST ======== "
	ssh -t $HOST "screen -r"
else
	echo "Invalid option $1, valid are either nothing or 'recover'"
	exit 1
fi

echo ""

echo " ======== Copying results.txt from $HOST ======== "
scp $HOST:$FOLDER/plot.pdf . 2>/dev/null
