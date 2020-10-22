from PySide2 import QtCore

from Code.Openings import Opening
from Code import Manager
from Code.Base import Move, Position
from Code.QT import WindowJuicio
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code import Tutor
from Code.Engines import EngineResponse
from Code import Washing
from Code.Base.Constantes import *


def managerWashing(procesador):
    dbwashing = Washing.DBWashing(procesador.configuration)
    washing = dbwashing.washing
    engine = washing.last_engine(procesador.configuration)
    if engine.state == Washing.CREATING:
        procesador.manager = ManagerWashingCreate(procesador)
        procesador.manager.inicio(dbwashing, washing, engine)

    elif engine.state == Washing.TACTICS:
        procesador.manager = ManagerWashingTactics(procesador)
        procesador.manager.inicio(dbwashing, washing, engine)

    elif engine.state == Washing.REPLAY:
        procesador.manager = ManagerWashingReplay(procesador)
        procesador.manager.inicio(dbwashing, washing, engine)


class ManagerWashingReplay(Manager.Manager):
    def inicio(self, dbwashing, washing, engine):
        self.dbwashing = dbwashing
        self.washing = washing
        self.engine = engine

        self.dbwashing.add_game()

        self.game_type = GT_WASHING_REPLAY

        self.human_is_playing = False

        self.is_tutor_enabled = False
        self.main_window.set_activate_tutor(False)
        self.ayudas_iniciales = 0

        self.main_window.activaJuego(True, False, siAyudas=False)
        self.main_window.quitaAyudas(True, True)
        self.set_dispatcher(self.player_has_moved)
        self.show_side_indicator(True)

        self.partidaObj = self.dbwashing.restoreGame(self.engine)
        self.numJugadasObj = self.partidaObj.num_moves()
        self.posJugadaObj = 0

        li_options = [TB_CLOSE]
        self.main_window.pon_toolbar(li_options)

        self.errores = 0

        self.book = Opening.OpeningPol(999, elo=engine.elo)

        is_white = self.engine.color
        self.is_human_side_white = is_white
        self.is_engine_side_white = not is_white
        self.set_position(self.game.last_position)
        self.ponPiezasAbajo(is_white)

        self.set_label1("%s: %s\n%s: %s" % (_("Rival"), self.engine.name, _("Task"), self.engine.lbState()))

        self.pgnRefresh(True)

        self.game.pending_opening = True
        self.game.add_tag("Event", _("The Washing Machine"))

        player = self.configuration.nom_player()
        other = self.engine.name
        w, b = (player, other) if self.is_human_side_white else (other, player)
        self.game.add_tag("White", w)
        self.game.add_tag("Black", b)
        QTUtil.refresh_gui()

        self.check_boards_setposition()

        self.state = ST_PLAYING

        self.siguiente_jugada()

    def run_action(self, key):
        if key == TB_CLOSE:
            self.terminar()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True, siCambioTutor=False)

        elif key == TB_UTILITIES:
            self.utilidades()

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def siguiente_jugada(self):
        if self.state == ST_ENDGAME:
            return

        self.set_label2("<b>%s: %d</b>" % (_("Errors"), self.errores))

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()

        is_white = self.game.last_position.is_white

        self.set_side_indicator(is_white)
        self.refresh()

        siRival = is_white == self.is_engine_side_white

        if siRival:
            move = self.partidaObj.move(self.posJugadaObj)
            self.posJugadaObj += 1
            self.mueve_rival(move.from_sq, move.to_sq, move.promotion)
            self.siguiente_jugada()

        else:
            self.human_is_playing = True
            self.timekeeper.start()
            self.activate_side(is_white)

    def finPartida(self):
        ok = self.errores == 0
        self.dbwashing.done_reinit(self.engine)

        self.state = ST_ENDGAME
        self.disable_all()

        li_options = [TB_CLOSE, TB_CONFIG, TB_UTILITIES]
        self.main_window.pon_toolbar(li_options)

        if ok:
            mens = _("Congratulations, this washing is done")
        else:
            mens = "%s<br>%s: %d" % (_("Done with errors."), _("Errors"), self.errores)
        self.mensajeEnPGN(mens)

    def player_has_moved(self, from_sq, to_sq, promotion=None):
        move = self.checkmueve_humano(from_sq, to_sq, promotion)
        if not move:
            return False

        movUsu = move.movimiento().lower()
        self.dbwashing.add_time(self.timekeeper.stop())

        jgObj = self.partidaObj.move(self.posJugadaObj)
        movObj = jgObj.movimiento().lower()
        if movUsu != movObj:
            lic = []
            if jgObj.analysis:
                mrmObj, posObj = jgObj.analysis
                rmObj = mrmObj.li_rm[posObj]
                lic.append("%s: %s (%s)" % (_("Played previously"), jgObj.pgn_translated(), rmObj.abrTextoBase()))
                ptsObj = rmObj.centipawns_abs()
                rmUsu, posUsu = mrmObj.buscaRM(movUsu)
                if posUsu >= 0:
                    lic.append("%s: %s (%s)" % (_("Played now"), move.pgn_translated(), rmUsu.abrTextoBase()))
                    ptsUsu = rmUsu.centipawns_abs()
                    if ptsUsu < ptsObj - 10:
                        lic[-1] += ' <span style="color:red"><b>%s</b></span>' % _("Bad move")
                        self.errores += 1
                        self.dbwashing.add_hint()

                else:
                    lic.append("%s: %s (?) %s" % (_("Played now"), move.pgn_translated(), _("Bad move")))
                    self.errores += 1
                    self.dbwashing.add_hint()

            else:
                # Debe ser una move de libro para aceptarla
                fen = self.fenUltimo()
                siBookUsu = self.book.check_human(fen, from_sq, to_sq)
                bmove = _("book move")
                lic.append("%s: %s (%s)" % (_("Played previously"), jgObj.pgn_translated(), bmove))
                if siBookUsu:
                    lic.append("%s: %s (%s)" % (_("Played now"), move.pgn_translated(), bmove))
                else:
                    lic.append("%s: %s (?) %s" % (_("Played now"), move.pgn_translated(), _("Bad move")))
                    self.errores += 1
                    self.dbwashing.add_hint()

            comment = "<br>".join(lic)
            w = WindowJuicio.MensajeF(self.main_window, comment)
            w.mostrar()
            self.set_position(move.position_before)

        # Creamos un move sin analysis
        siBien, self.error, move = Move.get_game_move(
            self.game, self.game.last_position, jgObj.from_sq, jgObj.to_sq, jgObj.promotion
        )

        self.move_the_pieces(move.liMovs)
        self.add_move(move, True)
        self.posJugadaObj += 1
        if len(self.game) == self.partidaObj.num_moves():
            self.finPartida()

        else:
            self.error = ""
            self.siguiente_jugada()
        return True

    def add_move(self, move, siNuestra):
        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.check_boards_setposition()

    def mueve_rival(self, from_sq, to_sq, promotion):
        siBien, mens, move = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
        self.add_move(move, False)
        self.move_the_pieces(move.liMovs, True)
        self.error = ""

    def terminar(self):
        self.procesador.inicio()
        self.procesador.showWashing()

    def final_x(self):
        self.procesador.inicio()
        return False


class ManagerWashingTactics(Manager.Manager):
    def inicio(self, dbwashing, washing, engine):
        self.dbwashing = dbwashing
        self.washing = washing
        self.engine = engine

        self.game_type = GT_WASHING_TACTICS

        self.human_is_playing = False

        self.is_tutor_enabled = False
        self.main_window.set_activate_tutor(False)
        self.ayudas_iniciales = 0

        self.main_window.activaJuego(True, False, siAyudas=False)
        self.main_window.quitaAyudas(True, True)
        self.set_dispatcher(self.player_has_moved)
        self.show_side_indicator(True)

        self.next_line()

    def next_line(self):
        self.line = self.dbwashing.next_tactic(self.engine)
        self.num_lines = self.engine.numTactics()
        if not self.line:
            return

        li_options = [TB_CLOSE, TB_HELP]
        self.main_window.pon_toolbar(li_options)

        self.num_move = -1
        self.ayudas = 0
        self.errores = 0
        self.time_used = 0.0

        cp = Position.Position()
        cp.read_fen(self.line.fen)
        self.game.set_position(cp)

        is_white = cp.is_white
        self.is_human_side_white = is_white
        self.is_engine_side_white = not is_white
        self.set_position(self.game.last_position)
        self.ponPiezasAbajo(is_white)
        # r1 = self.line.label
        self.set_label1("")
        r2 = "<b>%s: %d</b>" % (_("Pending"), self.num_lines)
        self.set_label2(r2)
        self.pgnRefresh(True)

        self.game.pending_opening = False

        QTUtil.refresh_gui()

        self.check_boards_setposition()

        self.state = ST_PLAYING

        self.siguiente_jugada()

    def run_action(self, key):
        if key == TB_CLOSE:
            self.finPartida()

        elif key == TB_HELP:
            self.ayuda()

        elif key == TB_REINIT:
            self.reiniciar()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True, siCambioTutor=False)

        elif key == TB_UTILITIES:
            self.utilidades()

        elif key == TB_NEXT:
            self.next_line()

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def siguiente_jugada(self):
        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()

        is_white = self.game.last_position.is_white

        self.set_side_indicator(is_white)
        self.refresh()

        siRival = is_white == self.is_engine_side_white

        self.num_move += 1
        if self.num_move >= self.line.total_moves():
            self.end_line()
            return

        if siRival:
            pv = self.line.get_move(self.num_move)
            from_sq, to_sq, promotion = pv[:2], pv[2:4], pv[4:]
            self.mueve_rival(from_sq, to_sq, promotion)
            self.siguiente_jugada()

        else:
            self.ayudasEsteMov = 0
            self.erroresEsteMov = 0
            self.human_is_playing = True
            self.timekeeper.start()
            self.activate_side(is_white)

    def end_line(self):
        ok = (self.ayudas + self.errores) == 0
        self.dbwashing.done_tactic(self.engine, ok)
        self.num_lines = self.engine.numTactics()

        self.state = ST_ENDGAME
        self.disable_all()

        li_options = [TB_CLOSE, TB_CONFIG, TB_UTILITIES]

        if self.num_lines:
            li_options.append(TB_NEXT)

        self.main_window.pon_toolbar(li_options)

        self.set_label1(self.line.label)

        if ok:
            r2 = "<b>%s: %d</b>" % (_("Pending"), self.num_lines)
            self.set_label2(r2)
            mens = _("This line training is completed.")
            if self.num_lines == 0:
                mens = "%s\n%s" % (mens, _("You have solved all puzzles"))

            self.mensajeEnPGN(mens)
        else:
            QTUtil2.message_error(
                self.main_window, "%s: %d, %s: %d" % (_("Errors"), self.errores, _("Hints"), self.ayudas)
            )

    def player_has_moved(self, from_sq, to_sq, promotion=None):
        move = self.checkmueve_humano(from_sq, to_sq, promotion)
        if not move:
            self.errores += 1
            return False

        movimiento = move.movimiento().lower()
        if movimiento == self.line.get_move(self.num_move).lower():
            self.move_the_pieces(move.liMovs)
            self.add_move(move, True)
            self.error = ""
            self.time_used += self.timekeeper.stop()
            self.siguiente_jugada()
            return True

        self.errores += 1
        self.erroresEsteMov += 1
        self.sigueHumano()
        return False

    def add_move(self, move, siNuestra):
        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.check_boards_setposition()

    def mueve_rival(self, from_sq, to_sq, promotion):
        siBien, mens, move = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
        self.add_move(move, False)
        self.move_the_pieces(move.liMovs, True)
        self.error = ""

    def ayuda(self):
        self.set_label1(self.line.label)
        self.ayudas += 1
        mov = self.line.get_move(self.num_move).lower()
        self.board.markPosition(mov[:2])
        self.ayudasEsteMov += 1
        if self.ayudasEsteMov > 1 and self.erroresEsteMov > 0:
            self.board.ponFlechasTmp([(mov[:2], mov[2:], True)], 1200)

    def finPartida(self):
        self.procesador.inicio()
        self.procesador.showWashing()

    def final_x(self):
        self.procesador.inicio()
        return False


class ManagerWashingCreate(Manager.Manager):
    def inicio(self, dbwashing, washing, engine):
        self.dbwashing = dbwashing
        self.washing = washing

        self.engine = engine

        self.game_type = GT_WASHING_CREATE

        self.resultado = None
        self.human_is_playing = False
        self.state = ST_PLAYING

        is_white = self.engine.color
        self.is_human_side_white = is_white
        self.is_engine_side_white = not is_white
        self.is_competitive = True

        self.opening = Opening.OpeningPol(30, self.engine.elo)

        self.is_tutor_enabled = True
        self.siAnalizando = False
        # self.main_window.set_activate_tutor(self.is_tutor_enabled)

        rival = self.configuration.buscaRival(self.engine.key)

        self.xrival = self.procesador.creaManagerMotor(rival, None, None)
        self.xrival.is_white = self.is_engine_side_white
        self.rm_rival = None
        self.tmRival = 15.0 * 60.0 * engine.elo / 3000.0

        self.xtutor.maximizaMultiPV()
        self.is_analyzed_by_tutor = False

        self.main_window.activaJuego(True, False, False)
        self.quitaAyudas()
        li = [TB_CLOSE, TB_REINIT, TB_TAKEBACK]
        self.main_window.pon_toolbar(li)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.last_position)
        self.show_side_indicator(True)
        self.ponPiezasAbajo(is_white)

        self.set_label1(
            "%s: %s\n%s: %s\n %s: %s"
            % (_("Rival"), self.engine.name, _("Task"), self.engine.lbState(), _("Tutor"), self.xtutor.name)
        )
        self.ponRotuloDatos()

        self.ponCapInfoPorDefecto()

        self.pgnRefresh(True)

        game = dbwashing.restoreGame(engine)
        if not (game is None):
            if not game.is_finished():
                self.game = game
                self.goto_end()
                self.main_window.base.pgnRefresh()
        else:
            player = self.configuration.nom_player()
            other = self.xrival.name
            w, b = (player, other) if self.is_human_side_white else (other, player)
            self.game.add_tag("White", w)
            self.game.add_tag("Black", b)

        self.check_boards_setposition()

        self.siguiente_jugada()

    def ponRotuloDatos(self):
        datos = "%s: %d | %s: %d/%d | %s: %s" % (
            _("Games"),
            self.engine.games,
            _("Hints"),
            self.engine.hints_current,
            self.engine.hints,
            _("Time"),
            self.engine.lbTime(),
        )
        self.set_label2(datos)

    def siguiente_jugada(self):
        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()

        is_white = self.game.is_white()

        if self.game.is_finished():
            self.muestra_resultado()
            return

        self.set_side_indicator(is_white)
        self.refresh()

        siRival = is_white == self.is_engine_side_white

        if siRival:
            if self.juegaRival():
                self.siguiente_jugada()

        else:
            self.juegaHumano(is_white)

    def juegaRival(self):
        self.pensando(True)
        self.disable_all()

        from_sq = to_sq = promotion = ""
        siEncontrada = False

        if self.opening:
            siEncontrada, from_sq, to_sq, promotion = self.opening.run_engine(self.fenUltimo())
            if not siEncontrada:
                self.opening = None

        if siEncontrada:
            self.rm_rival = EngineResponse.EngineResponse("Opening", self.is_engine_side_white)
            self.rm_rival.from_sq = from_sq
            self.rm_rival.to_sq = to_sq
            self.rm_rival.promotion = promotion

        else:
            self.rm_rival = self.xrival.juegaTiempo(self.tmRival, self.tmRival, 0)

        self.pensando(False)

        siBien, self.error, move = Move.get_game_move(
            self.game, self.game.last_position, self.rm_rival.from_sq, self.rm_rival.to_sq, self.rm_rival.promotion
        )
        if siBien:
            self.add_move(move, False)
            self.move_the_pieces(move.liMovs, True)
            return True
        else:
            return False

    def juegaHumano(self, is_white):
        self.human_is_playing = True
        self.analizaInicio()
        self.timekeeper.start()
        self.activate_side(is_white)

    def run_action(self, key):
        if key == TB_REINIT:
            self.reiniciar()

        elif key == TB_TAKEBACK:
            self.atras()

        elif key == TB_CLOSE:
            self.final_x()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True)

        elif key == TB_UTILITIES:
            self.utilidades()

        else:
            self.rutinaAccionDef(key)

    def analizaInicio(self):
        self.siAnalizando = False
        self.is_analyzed_by_tutor = False
        if self.continueTt:
            if not self.is_finished():
                self.xtutor.ac_inicio(self.game)
                self.siAnalizando = True
                QtCore.QTimer.singleShot(200, self.analizaSiguiente)
        else:
            self.analizaTutor()
            self.is_analyzed_by_tutor = True

    def analizaSiguiente(self):
        if self.siAnalizando:
            if self.human_is_playing and self.state == ST_PLAYING:
                if self.xtutor.engine:
                    mrm = self.xtutor.ac_estado()
                    if mrm:
                        QtCore.QTimer.singleShot(1000, self.analizaSiguiente)

    def analizaFinal(self):
        estado = self.siAnalizando
        self.siAnalizando = False
        if self.is_analyzed_by_tutor:
            return
        if self.continueTt and estado:
            self.pensando(True)
            self.mrmTutor = self.xtutor.ac_final(max(self.xtutor.motorTiempoJugada, 5000))
            self.pensando(False)
        else:
            self.mrmTutor = self.analizaTutor()

    def analizaTerminar(self):
        if self.siAnalizando:
            self.siAnalizando = False
            self.xtutor.ac_final(-1)

    def sigueHumanoAnalisis(self):
        self.analizaInicio()
        Manager.Manager.sigueHumano(self)

    def player_has_moved(self, from_sq, to_sq, promotion=None):
        move = self.checkmueve_humano(from_sq, to_sq, promotion)
        if not move:
            return False

        movimiento = move.movimiento()
        self.add_time()

        siAnalisis = False

        is_selected = False

        if self.opening:
            fenBase = self.fenUltimo()
            if self.opening.check_human(fenBase, from_sq, to_sq):
                is_selected = True
            else:
                self.opening = None

        self.analizaFinal()  # tiene que acabar siempre
        if not is_selected:
            rmUser, n = self.mrmTutor.buscaRM(movimiento)
            if not rmUser:
                rmUser = self.xtutor.valora(self.game.last_position, from_sq, to_sq, move.promotion)
                if not rmUser:
                    self.sigueHumanoAnalisis()
                    return False
                self.mrmTutor.agregaRM(rmUser)
            siAnalisis = True
            pointsBest, pointsUser = self.mrmTutor.difPointsBest(movimiento)
            if (pointsBest - pointsUser) > 0:
                if not move.is_mate:
                    tutor = Tutor.Tutor(self, self, move, from_sq, to_sq, False)
                    if tutor.elegir(True):
                        self.set_piece_again(from_sq)
                        from_sq = tutor.from_sq
                        to_sq = tutor.to_sq
                        promotion = tutor.promotion
                        siBien, mens, jgTutor = Move.get_game_move(
                            self.game, self.game.last_position, from_sq, to_sq, promotion
                        )
                        if siBien:
                            move = jgTutor
                            self.add_hint()
                    del tutor

        self.move_the_pieces(move.liMovs)

        if siAnalisis:
            rm, nPos = self.mrmTutor.buscaRM(move.movimiento())
            if rm:
                move.analysis = self.mrmTutor, nPos

        self.add_move(move, True)
        self.error = ""
        self.siguiente_jugada()
        return True

    def add_move(self, move, siNuestra):
        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)

        self.check_boards_setposition()

        self.refresh()

    def finalizar(self):
        self.analizaTerminar()
        self.main_window.activaJuego(False, False)
        self.quitaCapturas()
        self.procesador.inicio()
        self.procesador.showWashing()

    def final_x(self):
        if len(self.game) > 0:
            self.add_time()
            self.saveGame(False)
        self.finalizar()

    def add_hint(self):
        self.dbwashing.add_hint()
        self.ponRotuloDatos()

    def add_time(self):
        secs = self.timekeeper.stop()
        if secs:
            self.dbwashing.add_time(secs)
            self.ponRotuloDatos()

    def add_game(self):
        self.dbwashing.add_game()
        self.ponRotuloDatos()

    def saveGame(self, siFinal):
        self.dbwashing.saveGame(self.game, siFinal)

    def cancelGame(self):
        self.dbwashing.saveGame(None, False)
        self.add_game()

    def atras(self):
        if len(self.game):
            self.analizaTerminar()
            self.game.anulaUltimoMovimiento(self.is_human_side_white)
            self.game.assign_opening()
            self.goto_end()
            self.opening = Opening.OpeningPol(30, self.engine.elo)
            self.is_analyzed_by_tutor = False
            self.add_hint()
            self.add_time()
            self.refresh()
            self.siguiente_jugada()

    def reiniciar(self):
        if not QTUtil2.pregunta(self.main_window, _("Restart the game?")):
            return

        self.add_time()
        self.add_game()
        self.game.set_position()
        self.dbwashing.saveGame(None, False)

        self.inicio(self.dbwashing, self.washing, self.engine)

    def muestra_resultado(self):
        self.state = ST_ENDGAME
        self.disable_all()
        self.human_is_playing = False

        mensaje, beep, player_win = self.game.label_resultado_player(self.is_human_side_white)

        self.beepResultado(beep)
        self.guardarGanados(player_win)
        QTUtil.refresh_gui()

        QTUtil2.message(self.main_window, mensaje)

        li_options = [TB_CLOSE, TB_CONFIG, TB_UTILITIES]
        if player_win:
            li_options.insert(1, TB_REINIT)
        self.main_window.pon_toolbar(li_options)
        self.quitaAyudas()

        if player_win:
            self.saveGame(True)
        else:
            self.cancelGame()

    def analizaPosicion(self, row, key):
        if self.state != ST_ENDGAME:
            return
        Manager.Manager.analizaPosicion(self, row, key)