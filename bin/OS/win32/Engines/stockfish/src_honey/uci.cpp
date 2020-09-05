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

#include <cassert>

#include <iostream>
#include <sstream>
#include <string>
#include <cmath>  // convert to winning %
#include <iomanip> //set precision in winning %

#include "evaluate.h"
#include "movegen.h"
#include "position.h"
#include "search.h"
#include "thread.h"
#include "timeman.h"
#include "tt.h"
#include "uci.h"
#include "syzygy/tbprobe.h"

using namespace std;

extern vector<string> setup_bench(const Position&, istream&);

namespace {

  // FEN string of the initial position, normal chess
  const char* StartFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";


  // position() is called when engine receives the "position" UCI command.
  // The function sets up the position described in the given FEN string ("fen")
  // or the starting position ("startpos") and then makes the moves given in the
  // following move list ("moves").

  void position(Position& pos, istringstream& is, StateListPtr& states) {

    Move m;
    string token, fen;

    is >> token;

    if (token == "startpos")
    {
        fen = StartFEN;
        is >> token; // Consume "moves" token if any
    }
    else if (token == "fen")
        while (is >> token && token != "moves")
            fen += token + " ";
#ifdef Add_Features
    else if (token == "f")
        while (is >> token && token != "moves")
            fen += token + " ";
#endif
    else
        return;

    states = StateListPtr(new std::deque<StateInfo>(1)); // Drop old and create a new one
    pos.set(fen, Options["UCI_Chess960"], &states->back(), Threads.main());

    // Parse move list (if any)
    while (is >> token && (m = UCI::to_move(pos, token)) != MOVE_NONE)
    {
        states->emplace_back();
        pos.do_move(m, states->back());
    }
  }

  // trace_eval() prints the evaluation for the current position, consistent with the UCI
  // options set so far.

  void trace_eval(Position& pos) {

    StateListPtr states(new std::deque<StateInfo>(1));
    Position p;
    p.set(pos.fen(), Options["UCI_Chess960"], &states->back(), Threads.main());

    Eval::verify_NNUE();

    sync_cout << "\n" << Eval::trace(p) << sync_endl;
  }


  // setoption() is called when engine receives the "setoption" UCI command. The
  // function updates the UCI option ("name") to the given value ("value").

  void setoption(istringstream& is) {

    string token, name, value;

    is >> token; // Consume "name" token

    // Read option name (can contain spaces)
    while (is >> token && token != "value")
        name += (name.empty() ? "" : " ") + token;

    // Read option value (can contain spaces)
    while (is >> token)
        value += (value.empty() ? "" : " ") + token;

    if (Options.count(name))
        Options[name] = value;
    else
        sync_cout << FontColor::error << "No such option: " << name << sync_endl;
}

// set() is called by typing "s" from the terminal when the user wants to use abbreviated
// non-UCI comamnds and avoid the uci option protocol "setoption name (option name) value (xxx) ",
// e.g., instead of typing "setoption name threads value 8" to set cores to 8 at the terminal,
// the user simply types "s threads 8" - restricted to option names that do not contain
// any white spaces - see ucioption.cpp.  The argument can take white spaces e.g.,
// "s syzygypath /endgame tablebases/syzygy" will work
void set(istringstream& is) {
    string token, name, value;

    // Read option name (no white spaces in option name)
    is >> token;
    name = token;

    // Read option value (can contain white spaces)
    while (is >> token)
        value += string(" ", value.empty() ? 0 : 1) + token;

    // provide user confirmation
    if (Options.count(name)) {
        Options[name] = value;
        sync_cout << FontColor::engine << "Confirmation: "<< name << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "960")
    {
      Options["UCI_Chess960"] = {value};
      sync_cout << FontColor::engine << "Confirmation: "<< "UCI_Chess960" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "dpa")
    {
      Options["Deep Pro Analysis"] = {value};
      sync_cout << FontColor::engine << "Confirmation: "<< "Deep Pro Analysis" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "h")  {
      TT.resize(stoi(value));
      sync_cout << FontColor::engine << "Confirmation: "<< "Hash" << " set to " << value << " Mb" << FontColor::reset << sync_endl;
    }
    else if (name == "mo")
    {
    Options["Min Output"] = {value};
    sync_cout << FontColor::engine << "Confirmation: "<< "Min Output" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "mv")
    {
      Options["MultiPV"] = {value};
      sync_cout << FontColor::engine << "Confirmation: "<< "MultiPV" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "nn")
    {
      Options["UseNN"] = {value};
      sync_cout << FontColor::engine << "Confirmation: "<< "UseNN" << " set to " << value << FontColor::reset << sync_endl;
      if (Options["UseNN"])
          sync_cout << "info string: NN evaluation using " << std::string(Options["EvalFile"]) << " enabled." << sync_endl;
      else
          sync_cout << "info string: Classical evaluation enabled." << FontColor::reset << sync_endl;
    }
    else if (name == "proa")
    {
      Options["Pro Analysis"] = {value};
      sync_cout << FontColor::engine << "Confirmation: "<< "Pro Analysis" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "prov")
    {
      Options["Pro Value"] = {value};
      sync_cout << FontColor::engine << "Confirmation: "<< "Pro Value" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "so")
    {
    Options["Score Output"] = {value};
    sync_cout << FontColor::engine << "Confirmation: "<< "Score Output" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "t")  {
      Threads.set(stoi(value));
      sync_cout << FontColor::engine << "Confirmation: "<< "Threads" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "ta")
    {
    Options["Tactical"] = {value};
    sync_cout << FontColor::engine << "Confirmation: "<< "Tactical" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "z")
    {
      Tablebases::init(value);
      sync_cout << FontColor::engine << "Confirmation: "<< "SyzygyPath" << " set to " << value << FontColor::reset << sync_endl;
    }
    else if (name == "" || name == "option" )
    {
      sync_cout << ""  << sync_endl;
      sync_cout <<  " Shortcut Commands:"  << sync_endl;
      sync_cout << "  Note: setoption name 'option name'  value 'value'"  << sync_endl;
      sync_cout << "  is replaced  by:"  <<  sync_endl;
      sync_cout << FontColor::engine << "    set (or 's'), 'option name' or 'option shortcut' 'value'"  << sync_endl;
      sync_cout << FontColor::reset << "  Note: 'set' or 's', without an 'option' entered, displays the shortcuts"  << sync_endl;
      sync_cout << "\n Shortcuts:"  << sync_endl;
      sync_cout << FontColor::engine << "    '960' -> shortcut for 'UCI_Chess960'"  <<  sync_endl;
      sync_cout << "    'd'   -> shortcut for 'depth'"  <<  sync_endl;
      sync_cout << "    'dpa' -> shortcut for 'Deep_Pro_Analysis'"  << sync_endl;
      sync_cout << "    'g'   -> shortcut for 'go'"  << sync_endl;
      sync_cout << "    'i'   -> shortcut for 'infinite'"  << sync_endl;
      sync_cout << "    'm'   -> shortcut for 'Mate'"  << sync_endl;
      sync_cout << "    'mo'  -> shortcut for 'Min Output'" << sync_endl;
      sync_cout << "    'mv'  -> shortcut for 'MultiPV'"  << sync_endl;
      sync_cout << "    'mt'  -> shortcut for 'Movetime'-> " << FontColor::reset << sync_endl;
      sync_cout << FontColor::reset << "  Note: 'mt' is in seconds, while" << sync_endl;
      sync_cout << "  movetime is in milliseconds"  << sync_endl;
      sync_cout << FontColor::engine << "    'p f' -> shortcut for 'position fen'" << sync_endl;
      sync_cout << "    'nn'  ->  shortcut for 'UseNN'"  << sync_endl;
      sync_cout << "    'proa'-> shortcut for 'Pro Analysis'"  << sync_endl;
      sync_cout << "    'prov'-> shortcut for 'Pro Value'"  << sync_endl;
      sync_cout << "    'sm'  -> shortcut for 'SearchMoves'" << FontColor::reset << sync_endl;
      sync_cout << "  Note: 'sm' or 'SearchMoves' MUST be the" << sync_endl;
      sync_cout << "  last option on the command line!"  << sync_endl;
      sync_cout << FontColor::engine << "    'so'  -> shortcut for 'Score Output'" << FontColor::engine << sync_endl;
      sync_cout << "    't'   -> shortcut for 'Threads'"  << sync_endl;
      sync_cout << "    'ta'  -> shortcut for 'Tactical'"  << sync_endl;
      sync_cout << "    'q'   -> shortcut for 'quit'"  << sync_endl;
      sync_cout << "    'z'   -> shortcut for 'SyzygyPath'"  << sync_endl;
      sync_cout << "    '?'   -> shortcut for 'stop'"  << FontColor::reset << sync_endl;


    }
    else
      sync_cout << FontColor::error << "No such option: " << name << FontColor::reset<< sync_endl;

}

  // go() is called when engine receives the "go" UCI command. The function sets
  // the thinking time and other parameters from the input string, then starts
  // the search.

  void go(Position& pos, istringstream& is, StateListPtr& states) {

    Search::LimitsType limits;
    string token;
    bool ponderMode = false;

    limits.startTime = now(); // As early as possible!

    while (is >> token)
#ifdef Add_Features
        if (token == "searchmoves" || token == "sm")  // Needs to be the last command on the line
#else
        if (token == "searchmoves")  // Needs to be the last command on the line
#endif
            while (is >> token)
                limits.searchmoves.push_back(UCI::to_move(pos, token));

        else if (token == "wtime")     is >> limits.time[WHITE];
        else if (token == "btime")     is >> limits.time[BLACK];
        else if (token == "winc")      is >> limits.inc[WHITE];
        else if (token == "binc")      is >> limits.inc[BLACK];
        else if (token == "movestogo") is >> limits.movestogo;
        else if (token == "depth")     is >> limits.depth;
        else if (token == "nodes")     is >> limits.nodes;
        else if (token == "movetime")  is >> limits.movetime;
        else if (token == "mate")      is >> limits.mate;
        else if (token == "perft")     is >> limits.perft;
        else if (token == "infinite")  limits.infinite = 1;
        else if (token == "ponder")    ponderMode = true;
#ifdef Add_Features
        else if (token == "d")         is >> limits.depth;
        else if (token == "i")         limits.infinite = 1;
        else if (token == "m")         is >> limits.mate;
        else if (token == "mt")   {
          is >> limits.movetime;
          limits.movetime *= 1000;
        }
#endif

    Threads.start_thinking(pos, states, limits, ponderMode);
  }


  // bench() is called when engine receives the "bench" command. Firstly
  // a list of UCI commands is setup according to bench parameters, then
  // it is run one by one printing a summary at the end.

  void bench(Position& pos, istream& args, StateListPtr& states) {

    string token;
    uint64_t num, lap_nodes = 0, nodes = 0, cnt = 1;

    vector<string> list = setup_bench(pos, args);
    num = count_if(list.begin(), list.end(), [](string s) { return s.find("go ") == 0 || s.find("eval") == 0; });

    TimePoint elapsed = now();
    TimePoint lap_time_elapsed = elapsed;

    for (const auto& cmd : list)
    {
        istringstream is(cmd);
        is >> skipws >> token;

        if (token == "go" || token == "eval")
        {

            cerr << "\nPosition: " << cnt++ << '/' << num << endl;
            if (token == "go")
            {
               lap_time_elapsed = now();
               go(pos, is, states);
               Threads.main()->wait_for_search_finished();
               nodes += Threads.nodes_searched();
               lap_nodes = Threads.nodes_searched();
               lap_time_elapsed = now() - lap_time_elapsed + 1;
               if (lap_nodes * 1000 / lap_time_elapsed < 10000000)
                   cerr << "Nodes/Second: " << (lap_nodes * 1000) / lap_time_elapsed << endl;
               else
                   cerr << "Nodes/Second: " << lap_nodes / lap_time_elapsed << "k" << endl;
               if (Options["UseNN"])
                   cerr << "NN evaluation using " << std::string(Options["EvalFile"]) << " enabled." << sync_endl;
                else
                   cerr << "Classical evaluation enabled." <<  sync_endl;
            }
            else
               trace_eval(pos);
        }
        else if (token == "setoption")  setoption(is);
#ifdef Add_Features
        else if (token == "s")          set(is);
#endif
#ifndef Noir
        else if (token == "position")   position(pos, is, states);
#else
        else if (token == "position")
        {
          position(pos, is, states);

          if (Options["Clean Search"] == 1)
              Search::clear();
        }
#endif
        else if (token == "ucinewgame") { Search::clear(); elapsed = now(); } // Search::clear() may take some while
    }

    elapsed = now() - elapsed + 1; // Ensure positivity to avoid a 'divide by zero'

    dbg_print(); // Just before exiting
    cerr << FontColor::reset  << endl;
    cerr << "\n================================="
         << "\nTotal time (ms) : " << elapsed
         << "\nNodes searched  : " << nodes << endl;
    if (nodes * 1000 / elapsed < 10000000)
         cerr << "\nNodes/second    : " << (nodes * 1000) / elapsed << endl;
         else
         cerr << "\nNodes/second    : " << nodes / elapsed << "k" << endl;
  }

  // The win rate model returns the probability (per mille) of winning given an eval
  // and a game-ply. The model fits rather accurately the LTC fishtest statistics.
  int win_rate_model(Value v, int ply) {

     // The model captures only up to 240 plies, so limit input (and rescale)
     double m = std::min(192, ply) / 32;

     // Coefficients of a 3rd order polynomial fit based on fishtest data
     // for two parameters needed to transform eval to the argument of a
     // logistic function.
     double as[] = {-8.24404295, 64.23892342, -95.73056462, 153.86478679};
     double bs[] = {-3.37154371, 28.44489198, -56.67657741,  72.05858751};
     double a = (((as[0] * m + as[1]) * m + as[2]) * m) + as[3];
     double b = (((bs[0] * m + bs[1]) * m + bs[2]) * m) + bs[3];

     // Transform eval to centipawns with limited range
     double x = std::clamp(double(100 * v) / PawnValueEg, -2000.0, 2000.0);

     // Return win rate in per mille (rounded to nearest)
     return int(0.5 + 1000 / (1 + std::exp((a - x) / b)));
  }

} // namespace


/// UCI::loop() waits for a command from stdin, parses it and calls the appropriate
/// function. Also intercepts EOF from stdin to ensure gracefully exiting if the
/// GUI dies unexpectedly. When called with some command line arguments, e.g. to
/// run 'bench', once the command is executed the function returns immediately.
/// In addition to the UCI ones, also some additional debug commands are supported.

void UCI::loop(int argc, char* argv[]) {

  Position pos;
  string token, cmd;
  StateListPtr states(new std::deque<StateInfo>(1));

  pos.set(StartFEN, false, &states->back(), Threads.main());

  for (int i = 1; i < argc; ++i)
      cmd += std::string(argv[i]) + " ";

    do {
        if (argc == 1 && !getline(cin, cmd)) // Block here waiting for input or EOF
            cmd = "quit";
#ifdef Add_Features
        else if (token == "q")
            cmd = "quit";
#endif

      istringstream is(cmd);

      token.clear(); // Avoid a stale if getline() returns empty or blank line
      is >> skipws >> token;

        // The GUI sends 'ponderhit' to tell us the user has played the expected move.
        // So 'ponderhit' will be sent if we were told to ponder on the same move the
        // user has played. We should continue searching but switch from pondering to
        // normal search. In case Threads.stopOnPonderhit is set we are waiting for
        // 'ponderhit' to stop the search, for instance if max search depth is reached.
        if (    token == "quit"
                ||  token == "stop"
                ||  token == "q"
                ||  token == "?"
            )
            Threads.stop = true;

      // The GUI sends 'ponderhit' to tell us the user has played the expected move.
      // So 'ponderhit' will be sent if we were told to ponder on the same move the
      // user has played. We should continue searching but switch from pondering to
      // normal search.
      else if (token == "ponderhit")
          Threads.main()->ponder = false; // Switch to normal search

      else if (token == "uci")
          sync_cout << "id name " << engine_info(true)
                    << "\n"       << Options
                    << "\nuciok"  << sync_endl;

      else if (token == "setoption")  setoption(is);
      else if (token == "go")         go(pos, is, states);
      else if (token == "b")          bench(pos, is, states);
      else if (token == "so")         setoption(is);
      else if (token == "set")        set(is);
      else if (token == "s")          set(is);

      else if (token == "g")          go(pos, is, states);
      else if (token == "q")          cmd = "quit";
      else if (token == "position")
      {
          position(pos, is, states);
          if (Options["Clean_Search"])
              Search::clear();
      }

      else if (token == "p")
      {
          position(pos, is, states);
          if (Options["Clean_Search"])
              Search::clear();
      }
      else if (token == "ucinewgame") Search::clear();
      else if (token == "isready")    sync_cout << "readyok" << sync_endl;

      // Additional custom non-UCI commands, mainly for debugging.
      // Do not use these commands during a search!
      else if (token == "flip")     pos.flip();
      else if (token == "bench")    bench(pos, is, states);
      else if (token == "d")        sync_cout << pos << sync_endl;
      else if (token == "eval")     trace_eval(pos);
      else if (token == "compiler") sync_cout << compiler_info() << sync_endl;
      else if (token == "c++") sync_cout << compiler_info() << sync_endl;
      else if (token == "")  {
        Eval::init_NNUE();
        Eval::verify_NNUE();
        sync_cout << sync_endl;
      }
      else
          sync_cout << FontColor::error << "Unknown command: " << cmd << FontColor::reset << sync_endl;

  } while (token != "quit" && token != "q" && argc == 1);
    // Command line args are one-shot
}

#ifndef Noir
/// UCI::value() converts a Value to a string suitable for use with the UCI
/// protocol specification:
///
/// cp <x>    The score from the engine's point of view in centipawns.
/// mate <y>  Mate in y moves, not plies. If the engine is getting mated
///           use negative values for y.

string UCI::value(Value v) {

  assert(-VALUE_INFINITE < v && v < VALUE_INFINITE);

  stringstream ss;
  float vs = (float)v;
  constexpr float sf = 2.15; // scoring percentage factor
  constexpr float vf = 0.31492; // centipawn value factor

  if (abs(v) < VALUE_MATE_IN_MAX_PLY)   {
    if  (  Options["Score Output"] == "ScorPct-GUI")
        ss << "cp " << fixed << setprecision(0) << 10000 * (pow (sf,(sf * vs /1000)))
          / (pow(sf,(sf * vs /1000)) + 1);
    else
        ss << "cp " << fixed << setprecision(0) << vs * vf;
        }
  else
      ss  << "mate " << (v > 0 ? VALUE_MATE - v + 1 : -VALUE_MATE - v) / 2;

  return ss.str();
}


/// UCI::wdl() report WDL statistics given an evaluation and a game ply, based on
/// data gathered for fishtest LTC games.

string UCI::wdl(Value v, int ply) {

  stringstream ss;

  int wdl_w = win_rate_model( v, ply);
  int wdl_l = win_rate_model(-v, ply);
  int wdl_d = 1000 - wdl_w - wdl_l;
  ss << " wdl " << wdl_w << " " << wdl_d << " " << wdl_l;

  return ss.str();
}


/// UCI::square() converts a Square to a string in algebraic notation (g1, a7, etc.)

std::string UCI::square(Square s) {
  return std::string{ char('a' + file_of(s)), char('1' + rank_of(s)) };
}


/// UCI::move() converts a Move to a string in coordinate notation (g1f3, a7a8q).
/// The only special case is castling, where we print in the e1g1 notation in
/// normal chess mode, and in e1h1 notation in chess960 mode. Internally all
/// castling moves are always encoded as 'king captures rook'.

string UCI::move(Move m, bool chess960) {

  Square from = from_sq(m);
  Square to = to_sq(m);

  if (m == MOVE_NONE)
      return "(none)";

  if (m == MOVE_NULL)
      return "0000";

  if (type_of(m) == CASTLING && !chess960)
      to = make_square(to > from ? FILE_G : FILE_C, rank_of(from));

  string move = UCI::square(from) + UCI::square(to);

  if (type_of(m) == PROMOTION)
      move += " pnbrqk"[promotion_type(m)];

  return move;
}


/// UCI::to_move() converts a string representing a move in coordinate notation
/// (g1f3, a7a8q) to the corresponding legal Move, if any.

Move UCI::to_move(const Position& pos, string& str) {

  if (str.length() == 5) // Junior could send promotion piece in uppercase
      str[4] = char(tolower(str[4]));

  for (const auto& m : MoveList<LEGAL>(pos))
      if (str == UCI::move(m, pos.is_chess960()))
          return m;

  return MOVE_NONE;
}
#else

/// UCI::value() converts a Value to a string suitable for use with the UCI
/// protocol specification:
///
/// cp <x>    The score from the engine's point of view in centipawns.
/// mate <y>  Mate in y moves, not plies. If the engine is getting mated
///           use negative values for y.

string UCI::value(Value v, Value v2) {

  assert(-VALUE_INFINITE < v && v < VALUE_INFINITE);

  stringstream ss;
  float vs = (float)v;
  float vs2 = (float)v2;
  constexpr float sf = 2.15; // scoring percentage factor
  constexpr float vf = 0.31492; // centipawn value factor



  if (abs(v) < VALUE_MATE_IN_MAX_PLY)
  {
      if (   abs(vs) < 95 * PawnValueEg
           && abs(vs - vs2) < PawnValueEg)
           vs = (vs + vs2) / 2;
      if ( Options["Score Output"] == "ScorPct-GUI")
           ss << "cp " << fixed << setprecision(0) << 10000 * (pow (sf,(sf * vs /1000)))
           / (pow(sf,(sf * vs /1000)) + 1);

      else
           ss << "cp " << fixed << setprecision(0) << vs * vf;
  }
  else
       ss  << "mate " << (v > 0 ? VALUE_MATE - v + 1 : -VALUE_MATE - v) / 2;

  return ss.str();
}


/// UCI::wdl() report WDL statistics given an evaluation and a game ply, based on
/// data gathered for fishtest LTC games.

string UCI::wdl(Value v, int ply) {

  stringstream ss;

  int wdl_w = win_rate_model( v, ply);
  int wdl_l = win_rate_model(-v, ply);
  int wdl_d = 1000 - wdl_w - wdl_l;
  ss << " wdl " << wdl_w << " " << wdl_d << " " << wdl_l;

  return ss.str();
}


/// UCI::square() converts a Square to a string in algebraic notation (g1, a7, etc.)

std::string UCI::square(Square s) {
  return std::string{ char('a' + file_of(s)), char('1' + rank_of(s)) };
}


/// UCI::move() converts a Move to a string in coordinate notation (g1f3, a7a8q).
/// The only special case is castling, where we print in the e1g1 notation in
/// normal chess mode, and in e1h1 notation in chess960 mode. Internally all
/// castling moves are always encoded as 'king captures rook'.

string UCI::move(Move m, bool chess960) {

  Square from = from_sq(m);
  Square to = to_sq(m);

  if (m == MOVE_NONE)
      return "(none)";

  if (m == MOVE_NULL)
      return "0000";

  if (type_of(m) == CASTLING && !chess960)
      to = make_square(to > from ? FILE_G : FILE_C, rank_of(from));

  string move = UCI::square(from) + UCI::square(to);

  if (type_of(m) == PROMOTION)
      move += " pnbrqk"[promotion_type(m)];

  return move;
}


/// UCI::to_move() converts a string representing a move in coordinate notation
/// (g1f3, a7a8q) to the corresponding legal Move, if any.

Move UCI::to_move(const Position& pos, string& str) {

  if (str.length() == 5) // Junior could send promotion piece in uppercase
      str[4] = char(tolower(str[4]));

  for (const auto& m : MoveList<LEGAL>(pos))
      if (str == UCI::move(m, pos.is_chess960()))
          return m;

  return MOVE_NONE;
}
#endif //Noir
