# ==============================================================================
# Author : Lucas Monge, lukasmonk@gmail.com
# Web : http://lucaschess.pythonanywhere.com/
# Blog : http://lucaschess.blogspot.com
# Licence : GPL 3.0
# ==============================================================================
import sys

# TODO Variations, que sea editable directamente el movimiento
# TODO Analisis/kibitzers con todos los movimientos
# TODO Grabar automáticamente todas las partidas con mas de 10 movimientos
# TODO En análisis usar el mismo sistema que en Databases, para mostrar todo sin que se escondan los botones
# sys.argv = ['./LucasR.py', '-tournament', 'C:\\lucaschess\\pyLCR\\UserData\\Tournaments\\Irina vs 1400 Honey.mvm',
# 'C:\\lucaschess\\pyLCR\\UserData\\Tournaments\\Workers\\worker.00001']
import Code.Translate as Translate

Translate.install()

n_args = len(sys.argv)
if n_args == 1:
    import Code.Base.Init
    Code.Base.Init.init()

elif n_args >= 2:
    arg = sys.argv[1].lower()
    if (
        arg.endswith(".pgn")
        or arg.endswith(".jks")
        or arg.endswith(".lcdb")
        or arg == "-play"
        or arg.endswith(".bmt")
    ):
        import Code.Base.Init

        Code.Base.Init.init()

    elif arg == "-kibitzer":
        import Code.Kibitzers.RunKibitzer

        Code.Kibitzers.RunKibitzer.run(sys.argv[2])

    elif arg == "-tournament":
        import Code.Tournaments.RunTournament
        user = sys.argv[4] if len(sys.argv) >= 5 else ""
        Code.Tournaments.RunTournament.run(user, sys.argv[2], sys.argv[3])
