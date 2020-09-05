#!/bin/bash

#name if "getnet.sh" or something you prefer
# by MichaelB7  08/12/20
# A little script to update to current SF net and to rename net file to "eval.bin"
# designed to be run from the src folder , modify as you wish.
# This script is covered by the usual disclaimers, meaning that I am not possibly
# responsible, financially or otherwise, for anything that may possibly go
# wrong. There is absolutely no implied warranty, merchantability
# or fitness for any particular purpose whatsoever.


cd ../  ## move up a directory, modify to your own preference
wget https://github.com/official-stockfish/Stockfish/raw/master/src/ucioption.cpp
sha256nn="$(grep EvalFile ucioption.cpp | sed 's/.*\(nn-[a-z0-9]\{12\}.nnue\).*/\1/')"
echo "sha256 = $sha256"
binurl=" https://tests.stockfishchess.org/api/nn/$sha256nn"

##renames nnue file to eval.bin , modify "eval.bin" to your own preference
wgetnet="wget -O eval.bin"

## pulls the most recent and latest official NN from the SF GitHub repository
$wgetnet $binurl
rm ucioption.cpp   ## no longer needed.
sleep 1  ##  need to wait 1 second, before moving file or might error as being busy

# I like to keep it in my SF build folder, modify to your own preference
mv eval.bin src/
cd - ## return to previous directory
