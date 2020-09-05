#!/bin/bash
### modify as appropriate for your system
### all builds have added features, 4 opening books can be used, adaptive ply,
### play by FIDE Elo ratings or CCRL Elo ratings
###

### time the compile process
set echo on
#DATE=$(shell date +"%m/%d/%y")
start=`date +%s`

# install packages if not already installed
unzip -v &> /dev/null || pacman -S --noconfirm unzip
make -v &> /dev/null || pacman -S --noconfirm make
g++ -v &> /dev/null || pacman -S --noconfirm mingw-w64-x86_64-gcc

# remove old version of honey
#rm honey.zip
#rm -r Stockfish-honey

# download the honey source code
wget https://github.com/MichaelB7/Stockfish/archive/honey.zip
unzip honey.zip
cd Stockfish-honey/src

# find the CPU architecture
# CPU without popcnt and bmi2 instructions (e.g. older than Intel Sandy Bridge)
ARCH="ARCH=x86-64"
# CPU with popcnt instruction (e.g. Intel Sandy Bridge)
if [ "$(g++ -Q -march=native --help=target | grep mpopcnt | grep enabled)" ] ; then
  ARCH="ARCH=x86-64-modern"
# CPU with bmi2 instruction (e.g. Intel Haswell or newer)
elif [ "$(g++ -Q -march=native --help=target | grep mbmi2 | grep enabled)" ] ; then
  ARCH="ARCH=x86-64-bmi2"
fi

#BUILD="build
BUILD="profile-build"

#COMP="COMP=clang"
COMP="COMP=mingw"
#COMP="COMP=gcc"
#COMP="COMP=icc"

#make function
function mke() {
make -j $BUILD $ARCH $COMP "$@"
}

mke NOIR=yes && wait
mke BLUEFISH=yes FORTRESS_DETECT=yes && wait
mke BLUEFISH=yes && wait
mke HONEY=yes BLUEFISH=yes && wait
mke HONEY=yes FORTRESS_DETECT=yes && wait
mke HONEY=yes && wait
mke WEAKFISH=yes && wait
mke FORTRESS_DETECT=yes && wait
mke

### The script code below computes the bench nodes for each version, and updates the Makefile
### with the bench nodes and the date this was run.
echo ""
mv benchnodes.txt benchnodes_old.txt
echo "$( date +'Based on commits through %m/%d/%Y:')">> benchnodes.txt
echo "======================================================">> benchnodes.txt
grep -E 'searched|Nodes/second' *.bench  /dev/null >> benchnodes.txt
echo "======================================================">> benchnodes.txt
sed -i -e  's/^/### /g' benchnodes.txt
#rm *.nodes benchnodes.txt-e
echo "$(<benchnodes.txt)"
sed -i.bak -e '30,52d' ../src/Makefile
sed '29r benchnodes.txt' <../src/Makefile >../src/Makefile.tmp
mv ../src/Makefile.tmp ../src/Makefile
end=`date +%s`
runtime=$((end-start))
echo ""
echo Processing time $runtime seconds...
