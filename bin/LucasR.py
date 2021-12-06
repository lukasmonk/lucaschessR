#!/usr/bin/env python
# ==============================================================================
# Author : Lucas Monge, lukasmonk@gmail.com
# Web : http://lucaschess.pythonanywhere.com/
# Blog : http://lucaschess.blogspot.com
# Licence : GPL 3.0
# ==============================================================================
import sys
import warnings

warnings.simplefilter("ignore", UserWarning)


n_args = len(sys.argv)
if n_args == 1:
    import Code.Base.Init

    Code.Base.Init.init()

elif n_args >= 2:
    arg = sys.argv[1].lower()
    if arg.endswith(".pgn") or arg.endswith(".jks") or arg.endswith(".lcdb") or arg == "-play" or arg.endswith(".bmt"):
        import Code.Base.Init

        Code.Base.Init.init()

    elif arg == "-kibitzer":
        import Code.Kibitzers.RunKibitzer

        Code.Kibitzers.RunKibitzer.run(sys.argv[2])

    elif arg == "-tournament":
        import Code.Tournaments.RunTournament

        user = sys.argv[4] if len(sys.argv) >= 5 else ""
        Code.Tournaments.RunTournament.run(user, sys.argv[2], sys.argv[3])
