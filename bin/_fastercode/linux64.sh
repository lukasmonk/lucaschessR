#!/usr/bin/env bash

cd ./source/irina
gcc -Wall -fPIC -O3 -c lc.c board.c data.c eval.c hash.c loop.c makemove.c movegen.c movegen_piece_to.c search.c util.c pgn.c parser.c polyglot.c -DNDEBUG
gcc -shared -o ../irina.so lc.o board.o data.o eval.o hash.o loop.o makemove.o movegen.o movegen_piece_to.o search.o util.o pgn.o parser.o polyglot.o
rm *.o

cd ..

cat Faster_Irina.pyx Faster_Polyglot.pyx > FasterCode.pyx

x=$(pwd)
export LIBRARY_PATH=$x
export LD_LIBRARY_PATH=$x
export PATH=$x:$PATH
python3 ./setup_linux.py build_ext --inplace --verbose

cp ./FasterCode.cpython-37m-x86_64-linux-gnu.so ../../OS/linux
cp ./irina.so ../../OS/linux
