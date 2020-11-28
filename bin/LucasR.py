# ==============================================================================
# Author : Lucas Monge, lukasmonk@gmail.com
# Web : http://lucaschess.pythonanywhere.com/
# Blog : http://lucaschess.blogspot.com
# Licence : GPL 3.0
# ==============================================================================
import sys

# TODO Grabar automáticamente todas las games con mas de 10 movimientos
# TODO En análisis usar el mismo sistema que en Databases, para mostrar todo sin que se escondan los botones
# TODO Añadir en databases, ir a la siguiente/anterior
# TODO Facilitar el acceso a la carpeta UsrData
# TODO no guarda cambios en tags PGN save

import Code.Translate as Translate

Translate.install()

# sys.argv = ['./LucasR.py', '-tournament', 'C:\\lucaschess\\pyLCR\\UserData\\Tournaments\\Todos.mvm', 'C:\\lucaschess\\pyLCR\\UserData\\Tournaments\\worker.00001']
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
