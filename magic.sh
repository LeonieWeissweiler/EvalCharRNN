#!/bin/bash
LANG=$1
MODEL=$2
GPU=$3

# # Position: Bachelorarbeit
# python src/google_drive_download.py $CODE data/wikipedia/$LANG.tar.lzma
#
# # Position: Bacheloararbeit/data/wikipedia
# cd data/wikipedia
#
# tar --lzma -xf $LANG.tar.lzma
#
# # Position: Bachelorarbeit/data/wikipedia/$LANG
# cd $LANG
#
# mv full.txt huge.txt
#
# export PYTHONIOENCODING=utf8
# python3 ../../../src/gen_data.py 5000000
# python3 ../../../src/wordlist.py full
# python3 ../../../src/wordlist.py input
#
# # Position: Bachelorarbeit
# cd ../../..

export CUDA_VISIBLE_DEVICES=$GPU
python3 src/generate.py $LANG $MODEL
python3 src/wordlist.py data/wikipedia/$LANG/$MODEL/generated
