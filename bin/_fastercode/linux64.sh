#!/bin/bash

echo ""
echo ":: Building FasterCode"
echo ""

cd ./source/irina
gcc -Wall -fPIC -O3 -c lc.c board.c data.c eval.c hash.c loop.c makemove.c movegen.c movegen_piece_to.c search.c util.c pgn.c parser.c polyglot.c -DNDEBUG
ar cr ../libirina.a lc.o board.o data.o eval.o hash.o loop.o makemove.o movegen.o movegen_piece_to.o search.o util.o pgn.o parser.o polyglot.o
rm *.o

cd ..

cat Faster_Irina.pyx Faster_Polyglot.pyx > FasterCode.pyx

python3 setup_linux.py build_ext --inplace --verbose

cp FasterCode.cpython-3?-x86_64-linux-gnu.so ../../OS/linux

echo ""
echo ":: Building Complete"
echo ""

echo ":: Making all engines executable"
echo ""
echo ">> Alouette" && chmod 755 ../../OS/linux/Engines/Alouette/Alouette-0.1.4
echo ">> Amoeba" && chmod 755 ../../OS/linux/Engines/Amoeba/Amoeba-2.6
echo ">> Andscacs" && chmod 755 ../../OS/linux/Engines/Andscacs/Andscacs-0.95
echo ">> Arasan" && chmod 755 ../../OS/linux/Engines/Arasan/Arasan-22.2
echo ">> Asymptote" && chmod 755 ../../OS/linux/Engines/Asymptote/Asymptote-0.8
echo ">> Beef" && chmod 755 ../../OS/linux/Engines/Beef/Beef-0.36
echo ">> Cassandre" && chmod 755 ../../OS/linux/Engines/Cassandre/Cassandre-0.24
echo ">> CeeChess" && chmod 755 ../../OS/linux/Engines/CeeChess/CeeChess-1.3.2
echo ">> Cheng" && chmod 755 ../../OS/linux/Engines/Cheng/Cheng-4.40
echo ">> Chessika" && chmod 755 ../../OS/linux/Engines/Chessika/Chessika-2.21
echo ">> Cinnamon" && chmod 755 ../../OS/linux/Engines/Cinnamon/Cinnamon-1.2b
echo ">> Clarabit" && chmod 755 ../../OS/linux/Engines/Clarabit/Clarabit-1.00
echo ">> Counter" && chmod 755 ../../OS/linux/Engines/Counter/Counter-3.7
echo ">> Critter" && chmod 755 ../../OS/linux/Engines/Critter/Critter-1.6a
echo ">> CT800" && chmod 755 ../../OS/linux/Engines/CT800/CT800-1.42
echo ">> Daydreamer" && chmod 755 ../../OS/linux/Engines/Daydreamer/Daydreamer-1.75
echo ">> Delocto" && chmod 755 ../../OS/linux/Engines/Delocto/Delocto-0.61n
echo ">> Discocheck" && chmod 755 ../../OS/linux/Engines/Discocheck/Discocheck-5.2.1
echo ">> Dragontooth" && chmod 755 ../../OS/linux/Engines/Dragontooth/Dragontooth-0.2
echo ">> Drofa" && chmod 755 ../../OS/linux/Engines/Drofa/Drofa-2.2.0
echo ">> Ethereal" && chmod 755 ../../OS/linux/Engines/Ethereal/Ethereal-12.75
echo ">> FracTal" && chmod 755 ../../OS/linux/Engines/FracTal/FracTal-1.0
echo ">> Fruit" && chmod 755 ../../OS/linux/Engines/Fruit/Fruit-2.1
echo ">> Gaviota" && chmod 755 ../../OS/linux/Engines/Gaviota/Gaviota-0.84
echo ">> Glaurung" && chmod 755 ../../OS/linux/Engines/Glaurung/Glaurung-2.2
echo ">> Godel" && chmod 755 ../../OS/linux/Engines/Godel/Godel-7.0
echo ">> Goldfish" && chmod 755 ../../OS/linux/Engines/Goldfish/Goldfish-1.13.0
echo ">> Greko" && chmod 755 ../../OS/linux/Engines/Greko/GreKo-2020.03
echo ">> Gunborg" && chmod 755 ../../OS/linux/Engines/Gunborg/Gunborg-1.35
echo ">> Hactar" && chmod 755 ../../OS/linux/Engines/Hactar/Hactar-0.9.0
echo ">> Igel" && chmod 755 ../../OS/linux/Engines/Igel/Igel-3.0.0
echo ">> Irina" && chmod 755 ../../OS/linux/Engines/Irina/Irina-0.15
echo ">> Jabba" && chmod 755 ../../OS/linux/Engines/Jabba/Jabba-1.0
echo ">> K2" && chmod 755 ../../OS/linux/Engines/K2/K2-0.99
echo ">> Komodo" && chmod 755 ../../OS/linux/Engines/Komodo/Komodo-12.1.1-bmi2
echo ">> Laser" && chmod 755 ../../OS/linux/Engines/Laser/Laser-1.17
echo ">> Lc0" && chmod 755 ../../OS/linux/Engines/Lc0/Lc0-0.27.0
echo ">> Maia" && chmod 755 ../../OS/linux/Engines/Maia/Lc0-0.27.0
echo ">> Marvin" && chmod 755 ../../OS/linux/Engines/Marvin/Marvin-5.0.0
echo ">> Monochrome" && chmod 755 ../../OS/linux/Engines/Monochrome/Monochrome
echo ">> Monolith" && chmod 755 ../../OS/linux/Engines/Monolith/Monolith-2.01
echo ">> Octochess" && chmod 755 ../../OS/linux/Engines/Octochess/Octochess-r5190
echo ">> Pawny" && chmod 755 ../../OS/linux/Engines/Pawny/Pawny-1.2
echo ">> Pigeon" && chmod 755 ../../OS/linux/Engines/Pigeon/Pigeon-1.5.1
echo ">> Pulse" && chmod 755 ../../OS/linux/Engines/Pulse/Pulse-1.6.1
echo ">> Quokka" && chmod 755 ../../OS/linux/Engines/Quokka/Quokka-2.1
echo ">> Rocinante" && chmod 755 ../../OS/linux/Engines/Rocinante/Rocinante-2.0
echo ">> RodentII" && chmod 755 ../../OS/linux/Engines/RodentII/RodentII-0.9.64
echo ">> Shallow-blue" && chmod 755 ../../OS/linux/Engines/Shallow-blue/Shallow-blue-2.0.0
echo ">> Simplex" && chmod 755 ../../OS/linux/Engines/Simplex/Simplex-0.9.8
echo ">> Sissa" && chmod 755 ../../OS/linux/Engines/Sissa/Sissa-2.0
echo ">> SpaceDog" && chmod 755 ../../OS/linux/Engines/SpaceDog/SpaceDog-0.97.7
echo ">> Stash" && chmod 755 ../../OS/linux/Engines/Stash/Stash-29.0
echo ">> Stockfish" && chmod 755 ../../OS/linux/Engines/Stockfish/Stockfish-13
echo ">> Supernova" && chmod 755 ../../OS/linux/Engines/Supernova/Supernova-2.3
echo ">> Teki" && chmod 755 ../../OS/linux/Engines/Teki/Teki-2
echo ">> Texel" && chmod 755 ../../OS/linux/Engines/Texel/Texel-1.06
echo ">> Tucano" && chmod 755 ../../OS/linux/Engines/Tucano/Tucano-9.00
echo ">> Tunguska" && chmod 755 ../../OS/linux/Engines/Tunguska/Tunguska-1.1
echo ">> Velvet" && chmod 755 ../../OS/linux/Engines/Velvet/Velvet-1.2.0
echo ">> Weiss" && chmod 755 ../../OS/linux/Engines/Weiss/Weiss-1.2
echo ">> Wowl" && chmod 755 ../../OS/linux/Engines/Wowl/Wowl-1.3.7
echo ">> WyldChess" && chmod 755 ../../OS/linux/Engines/WyldChess/WyldChess-1.51
echo ">> Zappa" && chmod 755 ../../OS/linux/Engines/Zappa/Zappa-1.1
echo ">> Zurichess" && chmod 755 ../../OS/linux/Engines/Zurichess/Zurichess-1.7.4
echo ""
echo ":: All done!"

