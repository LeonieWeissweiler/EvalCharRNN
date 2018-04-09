#!/bin/bash
LANG=$1
cd data/wikipedia/$LANG
# mkdir lstm
# mkdir rnn
# mv *.npy lstm
# mv logs lstm
# mv save lstm
mv generated* lstm
