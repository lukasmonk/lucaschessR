from Code.Openings import Opening
from Code import Manager
from Code.Base import Move
from Code.QT import QTUtil2
from Code import Util
from Code.Engines import EngineResponse
from Code.Base.Constantes import *


class ManagerResistance(Manager.Manager):
    def start(self, resistance, numEngine, key):

        self.game_type = GT_RESISTANCE

        self.resistance = resistance
        self.numEngine = numEngine
        self.key = key
        is_white = "WHITE" in key
        self.segundos, self.puntos, self.maxerror = resistance.actual()
        self.movimientos = 0
        self.puntosRival = 0

        self.human_is_playing = False
        self.state = ST_PLAYING

        self.human_side = is_white
        self.is_engine_side_white = not is_white

        self.siBoxing = True

        self.rm_rival = None

        self.in_the_opening = False
        self.opening = Opening.OpeningPol(5)  # lee las aperturas

        # debe hacerse antes que rival
        self.procesador.stop_engines()
        self.xarbitro = self.procesador.creaManagerMotor(self.configuration.tutor, self.segundos * 1000, None)
        self.xarbitro.anulaMultiPV()

        engine = resistance.dameClaveEngine(numEngine)
        rival = self.configuration.buscaRival(engine)
        self.xrival = self.procesador.creaManagerMotor(rival, self.segundos * 1000, None)

        self.main_window.pon_toolbar((TB_RESIGN, TB_REINIT, TB_CONFIG, TB_UTILITIES))
        self.main_window.activaJuego(True, False, siAyudas=False)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.last_position)
        self.put_pieces_bottom(is_white)
        self.remove_hints()
        self.set_activate_tutor(False)
        self.show_side_indicator(True)
        self.ponRotuloObjetivo()
        self.ponRotuloActual()
        self.pgnRefresh(True)
        self.ponCapInfoPorDefecto()
        self.check_boards_setposition()

        tp = self.resistance.tipo
        if tp:
            b = n = False
            if tp == "p2":
                if is_white:
                    b = True
                else:
                    n = True
            elif tp == "p1":
                if is_white:
                    n = True
                else:
                    b = True
            self.board.mostrarPiezas(b, n)

        self.play_next_move()

    def ponRotuloObjetivo(self):
        label = self.resistance.rotuloActual()
        label += "<br><br><b>%s</b>: %s" % (_("Opponent"), self.xrival.name)
        label += "<br><b>%s</b>: %s" % (_("Record"), self.resistance.dameEtiRecord(self.key, self.numEngine))

        self.set_label1(label)

    def ponRotuloActual(self):
        label = "<b>%s</b>: %d" % (_("Moves"), self.movimientos)

        color = "black"
        if self.puntosRival != 0:
            color = "red" if self.puntosRival > 0 else "green"

        label += '<br><b>%s</b>: <font color="%s"><b>%d</b></font>' % (_("Score"), color, -self.puntosRival)

        self.set_label2(label)

    def run_action(self, key):
        if key == TB_RESIGN:
            self.finJuego(False)

        elif key == TB_CLOSE:
            self.procesador.stop_engines()
            self.procesador.start()
            self.procesador.entrenamientos.resistance(self.resistance.tipo)

        elif key == TB_REINIT:
            self.reiniciar()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True, siCambioTutor=False, siBlinfold=False)

        elif key == TB_UTILITIES:
            self.utilidades(siArbol=self.state == ST_ENDGAME)

        elif key in self.procesador.li_opciones_inicio:
            self.procesador.run_action(key)

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def reiniciar(self):
        if len(self.game) and QTUtil2.pregunta(self.main_window, _("Restart the game?")):
            self.game.set_position()
            self.start(self.resistance, self.numEngine, self.key)

    def final_x(self):
        return self.finJuego(False)

    def play_next_move(self):
        if self.state == ST_ENDGAME:
            return

        self.ponRotuloActual()

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()
        is_white = self.game.last_position.is_white

        if self.game.is_finished():
            self.autosave()
            if self.game.is_mate():
                si_ganado = self.human_side != is_white
                if si_ganado:
                    self.movimientos += 2000
                self.finJuego(True)
                return
            if self.game.is_draw():
                self.movimientos += 1000
                self.finJuego(True)
                return

        siRival = is_white == self.is_engine_side_white
        self.set_side_indicator(is_white)

        self.refresh()

        if siRival:
            self.thinking(True)
            self.disable_all()

            siPensar = True

            puntosRivalPrevio = self.puntosRival

            if self.in_the_opening:
                ok, from_sq, to_sq, promotion = self.opening.run_engine(self.last_fen())
                if ok:
                    self.rm_rival = EngineResponse.EngineResponse("Opening", self.is_engine_side_white)
                    self.rm_rival.from_sq = from_sq
                    self.rm_rival.to_sq = to_sq
                    self.rm_rival.promotion = promotion
                    siPensar = False

            if siPensar:
                self.rm_rival = self.xrival.juegaSegundos(self.segundos)
                self.puntosRival = self.rm_rival.centipawns_abs()
                self.ponRotuloActual()
            self.thinking(False)

            if self.play_rival(self.rm_rival):
                lostmovepoints = self.puntosRival - puntosRivalPrevio
                if self.siBoxing and self.puntosRival > self.puntos:
                    if self.check():
                        return
                if self.siBoxing and self.maxerror and lostmovepoints > self.maxerror:
                    if self.check():
                        return

                self.play_next_move()
        else:

            self.human_is_playing = True
            self.activate_side(is_white)

    def check(self):
        self.disable_all()
        if self.xrival.confMotor.key != self.xarbitro.confMotor.key:
            if self.segundos > 10:
                sc = 10
            elif self.segundos < 3:
                sc = 3
            else:
                sc = self.segundos

            um = QTUtil2.mensEspera.start(self.main_window, _("Checking..."))

            rm = self.xarbitro.juegaSegundos(sc)
            um.final()
            previoRival = self.puntosRival
            self.puntosRival = -rm.centipawns_abs()
            self.ponRotuloActual()
            if self.maxerror:
                lostmovepoints = self.puntosRival - previoRival
                if lostmovepoints > self.maxerror:
                    self.movimientos -= 1
                    return self.finJuego(False)

        if self.puntosRival > self.puntos:
            self.movimientos -= 1
            return self.finJuego(False)

        return False

    def finJuego(self, siFinPartida):
        if self.siBoxing and self.movimientos:
            siRecord = self.resistance.put_result(self.numEngine, self.key, self.movimientos)
            if siRecord:
                txt = "<h2>%s<h2>" % (_("New record!"))
                txt += "<h3>%s<h3>" % (self.resistance.dameEtiRecord(self.key, self.numEngine))
                self.ponRotuloObjetivo()
            else:
                if siFinPartida:
                    txt = "<h2>%s<h2>" % (_("Game ended"))
                    txt += "<h3>%s<h3>" % (self.resistance.dameEti(Util.today(), self.movimientos))
                else:
                    txt = "<h3>%s</h3>" % (_X(_("You have lost %1 centipawns."), str(-self.puntosRival)))

            if siFinPartida:
                self.mensajeEnPGN(txt)
            else:
                resp = QTUtil2.pregunta(
                    self.main_window,
                    txt + "<br>%s" % (_("Do you want to resign or continue playing?")),
                    label_yes=_("Resign"),
                    label_no=_("Continue"),
                )
                if not resp:
                    self.siBoxing = False
                    return False

        self.disable_all()
        self.state = ST_ENDGAME
        self.procesador.stop_engines()
        self.xarbitro.terminar()
        self.main_window.ajustaTam()
        self.main_window.resize(0, 0)
        if self.movimientos >= 1:
            li_options = [TB_CLOSE, TB_CONFIG, TB_UTILITIES]
            self.main_window.pon_toolbar(li_options)
        else:
            self.run_action(TB_CLOSE)

        return True

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        move = self.check_human_move(from_sq, to_sq, promotion)
        if not move:
            return False

        if self.in_the_opening:
            self.opening.check_human(self.last_fen(), from_sq, to_sq)

        self.move_the_pieces(move.liMovs)

        self.add_move(move, True)
        self.error = ""
        self.movimientos += 1
        self.play_next_move()
        return True

    def add_move(self, move, siNuestra):
        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.check_boards_setposition()

    def play_rival(self, engine_response):
        from_sq = engine_response.from_sq
        to_sq = engine_response.to_sq

        promotion = engine_response.promotion

        ok, mens, move = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
        if ok:
            self.error = ""
            self.add_move(move, False)
            self.move_the_pieces(move.liMovs, True)

            return True
        else:
            self.error = mens
            return False
