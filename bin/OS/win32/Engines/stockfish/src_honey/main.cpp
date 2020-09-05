/*
  Honey, a UCI chess playing engine derived from Glaurung 2.1
  Copyright (C) 2004-2020 The Stockfish developers (see AUTHORS file)

  Honey is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Honey is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

#include <iostream>

#include "bitboard.h"
#include "endgame.h"
#include "position.h"
#include "search.h"
/*#ifdef Sullivan  //  Replace Mobility table with log equations (with rook mg exception). #1784
#include "evaluate.h"
#endif*/
#include "thread.h"
#include "tt.h"
#include "uci.h"
#include "syzygy/tbprobe.h"
#include "polybook.h"

namespace PSQT {
  void init();
}

int main(int argc, char* argv[]) {

  std::cout << splash() << std::endl;
  std::cout << engine_info() << std::endl;

  CommandLine::init(argc, argv);
  UCI::init(Options);
  Tune::init();
  PSQT::init();
  Bitboards::init();
  Position::init();
  Bitbases::init();
  Endgames::init();

   polybook1.init(Options["Book_File_1"]);  // book idea from Marco Zerbanti
   polybook2.init(Options["Book_File_2"]);
   polybook3.init(Options["Book_File_3"]);
   polybook4.init(Options["Book_File_4"]);
#ifdef Weakfish
  Threads.set(size_t(1));
#else
  Threads.set(size_t(Options["Threads"]));
#endif
  Search::clear(); // After threads are up
  Eval::init_NNUE();

  UCI::loop(argc, argv);

  Threads.set(0);
  return 0;
}
