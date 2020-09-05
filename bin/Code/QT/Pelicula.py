from Code.QT import FormLayout
from Code.QT import Iconos
from Code.Base.Constantes import *


def paramPelicula(configuration, parent):

    nomVar = "PARAMPELICULA"
    dicVar = configuration.leeVariables(nomVar)

    # Datos
    liGen = [(None, None)]

    # # Segundos
    liGen.append((_("Number of seconds between moves") + ":", dicVar.get("SECONDS", 2)))
    liGen.append(FormLayout.separador)

    # # Si from_sq el principio
    liGen.append((_("Start from first move") + ":", dicVar.get("START", True)))
    liGen.append(FormLayout.separador)

    liGen.append((_("Show PGN") + ":", dicVar.get("PGN", True)))

    # Editamos
    resultado = FormLayout.fedit(liGen, title=_("Replay game"), parent=parent, anchoMinimo=460, icon=Iconos.Pelicula())

    if resultado:
        accion, liResp = resultado

        segundos, siPrincipio, siPGN = liResp
        dicVar["SECONDS"] = segundos
        dicVar["START"] = siPrincipio
        dicVar["PGN"] = siPGN
        configuration.escVariables(nomVar, dicVar)
        return segundos, siPrincipio, siPGN
    else:
        return None


class Pelicula:
    def __init__(self, manager, segundos, siInicio, siPGN):
        self.manager = manager
        self.procesador = manager.procesador
        self.main_window = manager.main_window
        self.if_starts_with_black = manager.game.if_starts_with_black
        self.board = manager.board
        self.segundos = segundos
        self.siInicio = siInicio
        self.rapidez = 1.0

        self.w_pgn = self.main_window.base.pgn
        self.siPGN = siPGN
        if not siPGN:
            self.w_pgn.hide()

        li_acciones = (TB_END, TB_SLOW, TB_PAUSE, TB_CONTINUE, TB_FAST, TB_REPEAT, TB_PGN)

        self.antAcciones = self.main_window.get_toolbar()
        self.main_window.pon_toolbar(li_acciones)

        self.manager.ponRutinaAccionDef(self.process_toolbar)

        self.muestraPausa(True)

        self.num_moves, self.jugInicial, self.filaInicial, self.is_white = self.manager.jugadaActual()

        self.li_moves = self.manager.game.li_moves
        self.current_position = 0 if siInicio else self.jugInicial

        self.siStop = False

        self.muestraActual()

    def muestraActual(self):
        if self.siStop:
            return

        move = self.li_moves[self.current_position]
        self.board.set_position(move.position_before)
        liMovs = [("b", move.to_sq), ("m", move.from_sq, move.to_sq)]
        if move.position.li_extras:
            liMovs.extend(move.position.li_extras)
        self.move_the_pieces(liMovs)

        self.skip()

    def move_the_pieces(self, liMovs):
        cpu = self.procesador.cpu
        cpu.reset()
        segundos = None

        move = self.li_moves[self.current_position]
        num = self.current_position
        if self.if_starts_with_black:
            num += 1
        row = int(num / 2)
        self.main_window.pgnColocate(row, move.position_before.is_white)
        self.main_window.base.pgnRefresh()

        # primero los movimientos
        for movim in liMovs:
            if movim[0] == "m":
                if segundos is None:
                    from_sq, to_sq = movim[1], movim[2]
                    dc = ord(from_sq[0]) - ord(to_sq[0])
                    df = int(from_sq[1]) - int(to_sq[1])
                    # Maxima distancia = 9.9 ( 9,89... sqrt(7**2+7**2)) = 4 segundos
                    dist = (dc ** 2 + df ** 2) ** 0.5
                    rp = self.rapidez if self.rapidez > 1.0 else 1.0
                    segundos = 4.0 * dist / (9.9 * rp)

                cpu.muevePieza(movim[1], movim[2], siExclusiva=False, segundos=segundos)

        if segundos is None:
            segundos = 1.0

        # segundo los borrados
        for movim in liMovs:
            if movim[0] == "b":
                n = cpu.duerme(segundos * 0.80)
                cpu.borraPieza(movim[1], padre=n)

        # tercero los cambios
        for movim in liMovs:
            if movim[0] == "c":
                cpu.cambiaPieza(movim[1], movim[2], siExclusiva=True)
        cpu.runLineal()
        self.manager.put_arrow_sc(move.from_sq, move.to_sq)

        self.board.set_position(move.position)

        self.manager.put_view()

        cpu.reset()
        cpu.duerme(self.segundos / self.rapidez)
        cpu.runLineal()

    def muestraPausa(self, siPausa):
        self.main_window.show_option_toolbar(TB_PAUSE, siPausa)
        self.main_window.show_option_toolbar(TB_CONTINUE, not siPausa)

    def process_toolbar(self, key):
        if key == TB_END:
            self.terminar()
        elif key == TB_SLOW:
            self.lento()
        elif key == TB_PAUSE:
            self.pausa()
        elif key == TB_CONTINUE:
            self.seguir()
        elif key == TB_FAST:
            self.rapido()
        elif key == TB_REPEAT:
            self.repetir()
        elif key == TB_PGN:
            self.siPGN = not self.siPGN
            if self.siPGN:
                self.w_pgn.show()
            else:
                self.w_pgn.hide()

    def terminar(self):
        self.siStop = True
        self.main_window.pon_toolbar(self.antAcciones)
        self.manager.ponRutinaAccionDef(None)
        self.manager.xpelicula = None
        if not self.siPGN:
            self.w_pgn.show()

    def lento(self):
        self.rapidez /= 1.2

    def rapido(self):
        self.rapidez *= 1.2

    def pausa(self):
        self.siStop = True
        self.muestraPausa(False)

    def seguir(self):
        num_moves, self.current_position, filaInicial, is_white = self.manager.jugadaActual()
        self.siStop = False
        self.muestraPausa(True)
        self.muestraActual()

    def repetir(self):
        self.current_position = 0 if self.siInicio else self.jugInicial
        self.siStop = False
        self.muestraPausa(True)
        self.muestraActual()

    def skip(self):
        if self.siStop:
            return
        self.current_position += 1
        if self.current_position == self.num_moves:
            self.pausa()
        else:
            self.muestraActual()
