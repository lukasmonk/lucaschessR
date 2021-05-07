import os

import FasterCode

import Code
from Code import Adjournments
from Code import DGT
from Code import Manager
from Code import Personalities
from Code import Tutor
from Code import Util
from Code.Analysis import Analysis
from Code.Base import Game, Move, Position
from Code.Base.Constantes import *
from Code.Engines import EngineResponse, SelectEngines
from Code.Openings import Opening
from Code.PlayAgainstEngine import WPlayAgainstEngine
from Code.Polyglots import Books, WindowBooks
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios


class ManagerPlayAgainstEngine(Manager.Manager):
    reinicio = None
    cache = None
    is_analyzing = False
    timekeeper = None
    summary = None
    with_summary = False
    human_side = False
    is_engine_side_white = False
    conf_engine = None
    lirm_engine = None
    next_test_resign = 0
    aperturaStd = None
    aperturaObl = None
    primeroBook = False
    bookP = None
    bookPdepth = 0
    bookR = None
    bookRR = None
    bookRdepth = 0
    is_tutor_enabled = False
    nArrows = 0
    thoughtOp = -1
    thoughtTt = -1
    continueTt = False
    nArrowsTt = 0
    chance = True
    tutor_con_flechas = False
    tutor_book = None
    nAjustarFuerza = 0
    resign_limit = -99999
    siBookAjustarFuerza = True
    siTiempo = False
    maxSegundos = 0
    segundosJugada = 0
    segExtra = 0
    zeitnot = 0
    vtime = None
    is_analyzed_by_tutor = False
    bookMandatory = None
    maxMoveBook = 9999
    toolbar_state = None
    premove = None

    def start(self, dic_var):
        self.base_inicio(dic_var)
        if self.siTiempo:
            if self.hints:
                self.xtutor.check_engine()
            self.xrival.check_engine()
            self.start_message()

        self.play_next_move()

    def base_inicio(self, dic_var):
        self.reinicio = dic_var

        self.cache = dic_var.get("cache", {})

        self.game_type = GT_AGAINST_ENGINE

        self.human_is_playing = False
        self.plays_instead_of_me_option = True
        self.state = ST_PLAYING
        self.is_analyzing = False

        self.summary = {}  # numJugada : "a"ccepted, "s"ame, "r"ejected, dif points, time used
        self.with_summary = dic_var.get("SUMMARY", False)

        is_white = dic_var["ISWHITE"]
        self.human_side = is_white
        self.is_engine_side_white = not is_white

        self.conf_engine = dic_var["RIVAL"].get("CM", None)

        self.lirm_engine = []
        self.next_test_resign = 0
        self.resign_limit = -99999  # never

        self.aperturaObl = self.aperturaStd = None

        self.fen = dic_var["FEN"]
        if self.fen:
            cp = Position.Position()
            cp.read_fen(self.fen)
            self.game.set_position(cp)
            self.game.pending_opening = False
        else:
            if dic_var["OPENING"]:
                self.aperturaObl = Opening.JuegaOpening(dic_var["OPENING"].a1h8)
                self.primeroBook = False  # la opening es obligatoria

        self.bookR = dic_var.get("BOOKR", None)
        if self.bookR:
            self.bookRdepth = dic_var.get("BOOKRDEPTH", 0)
            self.bookR.polyglot()
            self.bookRR = dic_var.get("BOOKRR", "mp")
        elif dic_var["RIVAL"].get("TYPE", None) in (SelectEngines.MICGM, SelectEngines.MICPER):
            if self.conf_engine.book:
                self.bookR = Books.Book("P", self.conf_engine.book, self.conf_engine.book, True)
                self.bookR.polyglot()
                self.bookRR = "mp"
                self.bookRdepth = 0

        self.bookP = dic_var.get("BOOKP", None)
        if self.bookP:
            self.bookPdepth = dic_var.get("BOOKPDEPTH", 0)
            self.bookP.polyglot()

        self.is_tutor_enabled = (Code.dgtDispatch is None) and self.configuration.x_default_tutor_active
        self.main_window.set_activate_tutor(self.is_tutor_enabled)

        self.hints = dic_var["HINTS"]
        self.ayudas_iniciales = self.hints  # Se guarda para guardar el PGN
        self.nArrows = dic_var.get("ARROWS", 0)
        n_box_height = dic_var.get("BOXHEIGHT", 24)
        self.thoughtOp = dic_var.get("THOUGHTOP", -1)
        self.thoughtTt = dic_var.get("THOUGHTTT", -1)
        self.continueTt = not Code.configuration.x_engine_notbackground
        self.nArrowsTt = dic_var.get("ARROWSTT", 0)
        self.chance = dic_var.get("2CHANCE", True)

        if self.nArrowsTt != 0 and self.hints == 0:
            self.nArrowsTt = 0

        self.with_takeback = dic_var.get("TAKEBACK", True)

        self.tutor_con_flechas = self.nArrowsTt > 0 and self.hints > 0
        self.tutor_book = Books.BookGame(Code.tbook)

        mx = max(self.thoughtOp, self.thoughtTt)
        if mx > -1:
            self.set_hight_label3(n_box_height)

        dr = dic_var["RIVAL"]
        rival = dr["CM"]

        if dr["TYPE"] == SelectEngines.ELO:
            r_t = 0
            r_p = rival.fixed_depth
            self.nAjustarFuerza = ADJUST_BETTER

        else:
            r_t = dr["ENGINE_TIME"] * 100  # Se guarda en decimas -> milesimas
            r_p = dr["ENGINE_DEPTH"]
            self.nAjustarFuerza = dic_var.get("ADJUST", ADJUST_BETTER)

        if not self.xrival:  # reiniciando is not None
            if r_t <= 0:
                r_t = None
            if r_p <= 0:
                r_p = None
            if r_t is None and r_p is None and not dic_var["WITHTIME"]:
                r_t = 1000
            self.xrival = self.procesador.creaManagerMotor(rival, r_t, r_p, self.nAjustarFuerza != ADJUST_BETTER)
            if self.nAjustarFuerza != ADJUST_BETTER:
                self.xrival.maximizaMultiPV()
        self.resign_limit = dic_var["RESIGN"]

        self.game.set_tag("Event", _("Play against an engine"))

        player = self.configuration.nom_player()
        other = self.xrival.name
        w, b = (player, other) if self.human_side else (other, player)
        self.game.set_tag("White", w)
        self.game.set_tag("Black", b)

        self.siBookAjustarFuerza = self.nAjustarFuerza != ADJUST_BETTER

        self.xrival.is_white = self.is_engine_side_white

        self.siTiempo = dic_var["WITHTIME"]
        if self.siTiempo:
            self.maxSegundos = dic_var["MINUTES"] * 60.0
            self.segundosJugada = dic_var["SECONDS"]
            self.segExtra = dic_var.get("MINEXTRA", 0) * 60.0
            self.zeitnot = dic_var.get("ZEITNOT", 0)

            self.vtime = {WHITE: Util.Timer(self.maxSegundos), BLACK: Util.Timer(self.maxSegundos)}
            if self.segExtra:
                self.vtime[self.human_side].ponSegExtra(self.segExtra)

            time_control = "%d" % int(self.maxSegundos)
            if self.segundosJugada:
                time_control += "+%d" % self.segundosJugada
            self.game.set_tag("TimeControl", time_control)
            if self.segExtra:
                self.game.set_tag("TimeExtra" + "White" if self.human_side else "Black", "%d" % self.segExtra)

        self.pon_toolbar()

        self.main_window.activaJuego(True, self.siTiempo)

        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.last_position)
        self.show_side_indicator(True)
        if self.ayudas_iniciales:
            self.ponAyudasEM()
        else:
            self.remove_hints(siQuitarAtras=False)
        self.put_pieces_bottom(is_white)

        self.ponRotuloBasico()
        self.set_label2("")

        if self.nAjustarFuerza != ADJUST_BETTER:
            pers = Personalities.Personalities(None, self.configuration)
            label = pers.label(self.nAjustarFuerza)
            if label:
                self.game.set_tag("Strength", label)

        self.ponCapInfoPorDefecto()

        self.pgnRefresh(True)

        rival = self.xrival.name
        player = self.configuration.x_player
        bl, ng = player, rival
        if self.is_engine_side_white:
            bl, ng = ng, bl

        active_clock = max(self.thoughtOp, self.thoughtTt) > -1

        if self.siTiempo:
            tp_bl = self.vtime[True].etiqueta()
            tp_ng = self.vtime[False].etiqueta()
            self.main_window.ponDatosReloj(bl, tp_bl, ng, tp_ng)
            active_clock = True
            self.refresh()
        else:
            self.main_window.base.change_player_labels(bl, ng)

        if active_clock:
            self.main_window.start_clock(self.set_clock, 400)

        self.main_window.set_notify(self.mueve_rival_base)

        self.is_analyzed_by_tutor = False

        self.game.tag_timestart()

        self.check_boards_setposition()

    def pon_toolbar(self):
        if self.state == ST_PLAYING:
            if self.toolbar_state != self.state:
                li = [TB_CANCEL, TB_RESIGN, TB_DRAW, TB_HELP_TO_MOVE, TB_REINIT, TB_PAUSE, TB_ADJOURN, TB_CONFIG, TB_UTILITIES, TB_STOP]
                if self.with_takeback:
                    li.insert(3, TB_TAKEBACK)

                self.main_window.pon_toolbar(li)
            hip = self.human_is_playing
            self.main_window.enable_option_toolbar(TB_RESIGN, hip)
            self.main_window.enable_option_toolbar(TB_DRAW, hip)
            self.main_window.enable_option_toolbar(TB_TAKEBACK, hip)
            self.main_window.enable_option_toolbar(TB_HELP_TO_MOVE, hip)
            self.main_window.enable_option_toolbar(TB_CONFIG, hip)
            self.main_window.enable_option_toolbar(TB_UTILITIES, hip)
            self.main_window.enable_option_toolbar(TB_STOP, not hip)

        elif self.state == ST_PAUSE:
            li = [TB_CONTINUE]
            self.main_window.pon_toolbar(li)
        else:
            li = [TB_CLOSE]
            self.main_window.pon_toolbar(li)

        self.toolbar_state = self.state

    def ponRotuloBasico(self):
        rotulo1 = ""
        if self.bookR:
            rotulo1 += "<br>%s: <b>%s</b>" % (_("Book"), os.path.basename(self.bookR.name))
        self.set_label1(rotulo1)

    def show_time(self, siUsuario):
        is_white = siUsuario == self.human_side
        ot = self.vtime[is_white]
        eti, eti2 = ot.etiquetaDif2()
        if eti:
            if is_white:
                self.main_window.ponRelojBlancas(eti, eti2)
            else:
                self.main_window.ponRelojNegras(eti, eti2)

    def set_clock(self):
        if self.state == ST_ENDGAME:
            self.main_window.stop_clock()
            return
        if self.state != ST_PLAYING:
            return

        if self.human_is_playing:
            if self.is_analyzing:
                mrm = self.xtutor.ac_estado()
                if mrm:
                    rm = mrm.mejorMov()
                    if self.nArrowsTt > 0:
                        self.showPV(rm.pv, self.nArrowsTt)
                    if self.thoughtTt > -1:
                        self.show_dispatch(self.thoughtTt, rm)
        elif self.thoughtOp > -1 or self.nArrows > 0:
            rm = self.xrival.current_rm()
            if rm:
                if self.nArrows:
                    self.showPV(rm.pv, self.nArrows)
                if self.thoughtOp > -1:
                    self.show_dispatch(self.thoughtOp, rm)

        if not self.siTiempo:
            return

        def mira(xis_white):
            ot = self.vtime[xis_white]

            eti, eti2 = ot.etiquetaDif2()
            if eti:
                if xis_white:
                    self.main_window.ponRelojBlancas(eti, eti2)
                else:
                    self.main_window.ponRelojNegras(eti, eti2)

            siJugador = self.human_side == xis_white
            if ot.siAgotado():
                if siJugador and QTUtil2.pregunta(self.main_window, _X(_("%1 has won on time."), self.xrival.name) + "\n\n" + _("Add time and keep playing?")):
                    minX = WPlayAgainstEngine.dameMinutosExtra(self.main_window)
                    if minX:
                        ot.ponSegExtra(minX * 60)
                        return
                self.game.set_termination(TERMINATION_WIN_ON_TIME, RESULT_WIN_BLACK if xis_white else RESULT_WIN_WHITE)
                self.state = ST_ENDGAME  # necesario que esté antes de reloj_stop para no entrar en bucle
                self.reloj_stop(siJugador)
                self.muestra_resultado()
                return

            elif siJugador and ot.isZeitnot():
                self.beepZeitnot()

            return

        if Code.dgt:
            DGT.writeClocks(self.vtime[True].etiquetaDGT(), self.vtime[False].etiquetaDGT())

        if self.human_is_playing:
            is_white = self.human_side
        else:
            is_white = not self.human_side
        mira(is_white)

    def reloj_start(self, siUsuario):
        if self.siTiempo:
            self.vtime[siUsuario == self.human_side].iniciaMarcador()
            self.vtime[siUsuario == self.human_side].setZeitnot(self.zeitnot)

    def reloj_stop(self, siUsuario):
        if self.siTiempo:
            self.vtime[siUsuario == self.human_side].paraMarcador(self.segundosJugada)
            self.show_time(siUsuario)

    def run_action(self, key):
        if key == TB_CANCEL:
            self.finalizar()

        elif key == TB_RESIGN:
            self.rendirse()

        elif key == TB_DRAW:
            self.tablasPlayer()

        elif key == TB_TAKEBACK:
            self.takeback()

        elif key == TB_PAUSE:
            self.xpause()

        elif key == TB_CONTINUE:
            self.xcontinue()

        elif key == TB_HELP_TO_MOVE:
            self.ayudaMover()

        elif key == TB_REINIT:
            self.reiniciar(True)

        elif key == TB_CONFIG:
            liMasOpciones = []
            if self.state == ST_PLAYING:
                liMasOpciones.append((None, None, None))
                liMasOpciones.append(("rival", _("Change opponent"), Iconos.Motor()))
            resp = self.configurar(liMasOpciones, siSonidos=True, siCambioTutor=self.ayudas_iniciales > 0)
            if resp == "rival":
                self.cambioRival()

        elif key == TB_UTILITIES:
            liMasOpciones = []
            if self.human_is_playing or self.is_finished():
                liMasOpciones.append(("books", _("Consult a book"), Iconos.Libros()))

            resp = self.utilidades(liMasOpciones)
            if resp == "books":
                siEnVivo = self.human_is_playing and not self.is_finished()
                liMovs = self.librosConsulta(siEnVivo)
                if liMovs and siEnVivo:
                    from_sq, to_sq, promotion = liMovs[-1]
                    self.player_has_moved(from_sq, to_sq, promotion)
            elif resp == "play":
                self.play_current_position()

        elif key == TB_ADJOURN:
            self.adjourn()

        elif key == TB_STOP:
            self.stop_engine()

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def save_state(self):
        self.analizaTerminar()
        dic = self.reinicio

        # cache
        dic["cache"] = self.cache

        # game
        dic["game_save"] = self.game.save()

        # tiempos
        if self.siTiempo:
            self.main_window.stop_clock()
            dic["time_white"] = self.vtime[WHITE].save()
            dic["time_black"] = self.vtime[BLACK].save()

        dic["is_tutor_enabled"] = self.is_tutor_enabled

        dic["hints"] = self.hints
        dic["summary"] = self.summary

        return dic

    def restore_state(self, dic):
        self.base_inicio(dic)
        self.game.restore(dic["game_save"])

        if self.siTiempo:
            self.vtime[WHITE].restore(dic["time_white"])
            self.vtime[BLACK].restore(dic["time_black"])

        self.is_tutor_enabled = dic["is_tutor_enabled"]
        self.hints = dic["hints"]
        self.summary = dic["summary"]
        self.goto_end()

    def close_position(self, key):
        if key == TB_CLOSE:
            self.procesador.run_action(TB_QUIT)
        else:
            self.run_action(key)

    def play_position(self, dic, restore_game):
        self.ponRutinaAccionDef(self.close_position)
        self.base_inicio(dic)
        self.game.restore(restore_game)
        player = self.configuration.nom_player()
        other = self.xrival.name
        w, b = (player, other) if self.human_side else (other, player)
        self.game.set_tag("White", w)
        self.game.set_tag("Black", b)
        self.goto_end()
        self.play_next_move()

    def reiniciar(self, siPregunta):
        if siPregunta:
            if not QTUtil2.pregunta(self.main_window, _("Restart the game?")):
                return
        if self.siTiempo:
            self.main_window.stop_clock()
        self.analizaTerminar()
        # self.game.set_position()
        self.reinicio["cache"] = self.cache
        self.game.reset()
        self.toolbar_state = ST_ENDGAME
        self.autosave()
        self.start(self.reinicio)

    def adjourn(self):
        if QTUtil2.pregunta(self.main_window, _("Do you want to adjourn the game?")):
            dic = self.save_state()

            # se guarda en una bd Adjournments dic key = fecha y hora y tipo
            label_menu = _("Play against an engine") + ". " + self.xrival.name

            self.state = ST_ENDGAME

            self.finalizar()
            if self.is_analyzing:
                self.is_analyzing = False
                self.xtutor.ac_final(-1)

            with Adjournments.Adjournments() as adj:
                adj.add(self.game_type, dic, label_menu)
                adj.si_seguimos(self)

    def run_adjourn(self, dic):
        self.restore_state(dic)
        self.check_boards_setposition()
        if self.siTiempo:
            self.show_clocks()
        if self.siTiempo:
            if self.hints:
                self.xtutor.check_engine()
            self.xrival.check_engine()
            self.start_message()

        self.play_next_move()

    def xpause(self):
        self.state = ST_PAUSE
        self.thinking(False)
        if self.is_analyzing:
            self.is_analyzing = False
            self.xtutor.ac_final(-1)
        self.board.set_position(self.game.first_position)
        self.board.disable_all()
        self.main_window.hide_pgn()
        self.pon_toolbar()

    def xcontinue(self):
        self.state = ST_PLAYING
        self.board.set_position(self.game.last_position)
        self.pon_toolbar()
        self.main_window.show_pgn()
        self.play_next_move()

    def final_x(self):
        return self.finalizar()

    def stop_engine(self):
        if not self.human_is_playing:
            self.xrival.stop()

    def finalizar(self):
        if self.state == ST_ENDGAME:
            return True
        siJugadas = len(self.game) > 0
        if siJugadas:
            if not QTUtil2.pregunta(self.main_window, _("End game?")):
                return False  # no abandona
            if self.siTiempo:
                self.main_window.stop_clock()
            if self.is_analyzing:
                self.is_analyzing = False
                self.xtutor.ac_final(-1)
            self.state = ST_ENDGAME
            self.stop_engine()
            self.game.set_unknown()
            self.ponFinJuego(self.with_takeback)
            self.autosave()
        else:
            if self.siTiempo:
                self.main_window.stop_clock()
            if self.is_analyzing:
                self.is_analyzing = False
                self.xtutor.ac_final(-1)
            self.state = ST_ENDGAME
            self.stop_engine()
            self.main_window.activaJuego(False, False)
            self.quitaCapturas()
            if self.xRutinaAccionDef:
                self.xRutinaAccionDef(TB_CLOSE)
            else:
                self.procesador.start()

        return False

    def rendirse(self):
        if self.state == ST_ENDGAME:
            return True
        if self.siTiempo:
            self.main_window.stop_clock()
        if len(self.game) > 0:
            if not QTUtil2.pregunta(self.main_window, _("Do you want to resign?")):
                return False  # no abandona
            self.game.set_termination(TERMINATION_RESIGN, self.human_side)
            self.saveSummary()
            self.ponFinJuego(self.with_takeback)
            self.autosave()
        else:
            self.analizaTerminar()
            self.main_window.activaJuego(False, False)
            self.quitaCapturas()
            self.procesador.start()

        return False

    def analizaTerminar(self):
        if self.is_analyzing:
            self.is_analyzing = False
            self.xtutor.ac_final(-1)

    def takeback(self):
        if len(self.game):
            self.analizaTerminar()
            if self.hints:
                self.hints -= 1
                self.tutor_con_flechas = self.nArrowsTt > 0 and self.hints > 0
            self.ponAyudasEM()
            self.game.anulaUltimoMovimiento(self.human_side)
            if not self.fen:
                self.game.assign_opening()
            self.goto_end()
            self.reOpenBook()
            self.refresh()
            if self.state == ST_ENDGAME:
                self.state = ST_PLAYING
                self.toolbar_state = None
                self.pon_toolbar()
            self.check_boards_setposition()
            self.play_next_move()

    def testBook(self):
        if self.bookR:
            resp = self.bookR.get_list_moves(self.last_fen())
            if not resp:
                self.bookR = None
                self.ponRotuloBasico()

    def reOpenBook(self):
        self.bookR = self.reinicio.get("BOOK", None)
        if self.bookR:
            self.bookR.polyglot()
            self.ponRotuloBasico()

    def play_next_move(self):
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

        if self.bookR:
            self.testBook()

        if siRival:
            self.juegaRival(is_white)

        else:
            self.juegaHumano(is_white)

    def setSummary(self, key, value):
        njug = len(self.game)
        if not (njug in self.summary):
            self.summary[njug] = {}
        self.summary[njug][key] = value

    def analizaInicio(self):
        if not self.is_tutor_enabled:
            return
        self.is_analyzing = False
        self.is_analyzed_by_tutor = False
        if not self.tutor_con_flechas:
            if self.aperturaObl or not self.is_tutor_enabled or self.ayudas_iniciales <= 0:
                return
        if not self.is_finished():
            if self.continueTt:
                self.xtutor.ac_inicio(self.game)
            else:
                self.xtutor.ac_inicio_limit(self.game)
            self.is_analyzing = True

    def analizaFinal(self, is_mate=False):
        if not self.is_tutor_enabled:
            if self.is_analyzing:
                self.xtutor.stop()
                self.is_analyzing = False
            return
        if is_mate:
            if self.is_analyzing:
                self.xtutor.stop()
            return
        if self.is_analyzed_by_tutor:
            return
        estado = self.is_analyzing
        self.is_analyzing = False
        if not self.tutor_con_flechas:
            if self.is_analyzed_by_tutor or not self.is_tutor_enabled or self.ayudas_iniciales <= 0:
                return
        if self.is_analyzed_by_tutor:
            return
        self.main_window.pensando_tutor(True)
        if self.continueTt:
            self.mrmTutor = self.xtutor.ac_final(self.xtutor.motorTiempoJugada)
        else:
            self.mrmTutor = self.xtutor.ac_final_limit()
        self.main_window.pensando_tutor(False)
        self.is_analyzed_by_tutor = True

    def ajustaPlayer(self, mrm):
        position = self.game.last_position

        FasterCode.set_fen(position.fen())
        li = FasterCode.get_exmoves()

        li_options = []
        for rm in mrm.li_rm:
            li_options.append((rm, "%s (%s)" % (position.pgn_translated(rm.from_sq, rm.to_sq, rm.promotion), rm.abrTexto())))
            mv = rm.movimiento()
            for x in range(len(li)):
                if li[x].move() == mv:
                    del li[x]
                    break

        for mj in li:
            rm = EngineResponse.EngineResponse("", position.is_white)
            rm.from_sq = mj.from_sq()
            rm.to_sq = mj.to_sq()
            rm.promotion = mj.promotion()
            rm.puntos = None
            li_options.append((rm, position.pgn_translated(rm.from_sq, rm.to_sq, rm.promotion)))

        if len(li_options) == 1:
            return li_options[0][0]

        menu = QTVarios.LCMenu(self.main_window)
        titulo = _("White") if position.is_white else _("Black")
        icono = Iconos.Carpeta()

        self.main_window.cursorFueraBoard()
        menu.opcion(None, titulo, icono)
        menu.separador()
        icono = Iconos.PuntoNaranja() if position.is_white else Iconos.PuntoNegro()
        for rm, txt in li_options:
            menu.opcion(rm, txt, icono)
        while True:
            resp = menu.lanza()
            if resp:
                return resp

    def eligeJugadaBookBase(self, book, bookRR):
        num_moves = self.game.last_position.num_moves
        if self.maxMoveBook:
            if self.maxMoveBook <= num_moves:
                return False, None, None, None
        fen = self.last_fen()

        if bookRR == "su":
            listaJugadas = book.get_list_moves(fen)
            if listaJugadas:
                resp = WindowBooks.eligeJugadaBooks(self.main_window, listaJugadas, self.game.last_position.is_white)
                return True, resp[0], resp[1], resp[2]
        else:
            pv = book.eligeJugadaTipo(fen, bookRR)
            if pv:
                return True, pv[:2], pv[2:4], pv[4:]

        return False, None, None, None

    def eligeJugadaBook(self):
        return self.eligeJugadaBookBase(self.bookR, self.bookRR)

    def eligeJugadaBookAjustada(self):
        if self.nAjustarFuerza < 1000:
            return False, None, None, None
        dicPersonalidad = self.configuration.liPersonalidades[self.nAjustarFuerza - 1000]
        nombook = dicPersonalidad.get("BOOK", None)
        if (nombook is None) or (not Util.exist_file(nombook)):
            return False, None, None, None

        book = Books.Book("P", nombook, nombook, True)
        book.polyglot()
        return self.eligeJugadaBookBase(book, "pr")

    def juegaHumano(self, is_white):
        self.reloj_start(True)
        self.timekeeper.start()
        self.human_is_playing = True
        if self.premove:
            from_sq, to_sq = self.premove
            promotion = "q" if self.game.last_position.siPeonCoronando(from_sq, to_sq) else None
            ok, error, move = Move.get_game_move(self.game, self.game.last_position, self.premove[0], self.premove[1], promotion)
            if ok:
                self.player_has_moved(from_sq, to_sq, promotion)
                return
            self.premove = None

        self.pon_toolbar()
        self.analizaInicio()

        self.activate_side(is_white)

    def juegaRival(self, is_white):
        self.board.remove_arrows()
        self.reloj_start(False)
        self.timekeeper.start()
        self.human_is_playing = False
        self.rm_rival = None
        self.pon_toolbar()
        if not self.is_tutor_enabled:
            self.activate_side(self.human_side)

        fen_ultimo = self.last_fen()

        if fen_ultimo in self.cache:
            move = self.cache[fen_ultimo]
            self.add_move(move, False)
            self.move_the_pieces(move.liMovs, True)
            if self.siTiempo:
                self.vtime[self.is_engine_side_white].restore(move.cacheTime)
            return self.play_next_move()

        from_sq = to_sq = promotion = ""
        si_encontrada = False

        if self.aperturaObl:
            si_encontrada, from_sq, to_sq, promotion = self.aperturaObl.run_engine(fen_ultimo)
            if not si_encontrada:
                self.aperturaObl = None

        if not si_encontrada and self.bookR:
            if self.game.last_position.num_moves < self.maxMoveBook:
                si_encontrada, from_sq, to_sq, promotion = self.eligeJugadaBook()
            if not si_encontrada:
                self.bookR = None

        if not si_encontrada and self.aperturaStd:
            si_encontrada, from_sq, to_sq, promotion = self.aperturaStd.run_engine(fen_ultimo)
            if not si_encontrada:
                self.aperturaStd = None

        if not si_encontrada and self.siBookAjustarFuerza:
            si_encontrada, from_sq, to_sq, promotion = self.eligeJugadaBookAjustada()  # book de la personalidad
            if not si_encontrada:
                self.siBookAjustarFuerza = False

        if si_encontrada:
            rm_rival = EngineResponse.EngineResponse("Opening", self.is_engine_side_white)
            rm_rival.from_sq = from_sq
            rm_rival.to_sq = to_sq
            rm_rival.promotion = promotion
            self.play_rival(rm_rival)
        else:
            self.thinking(True)
            if self.siTiempo:
                tiempoBlancas = self.vtime[True].tiempoPendiente
                tiempoNegras = self.vtime[False].tiempoPendiente
                segundosJugada = self.segundosJugada
            else:
                tiempoBlancas = tiempoNegras = 10 * 60 * 1000
                segundosJugada = 0

            self.xrival.play_time(self.main_window.notify, tiempoBlancas, tiempoNegras, segundosJugada, nAjustado=self.nAjustarFuerza)

    def sigueHumanoAnalisis(self):
        self.analizaInicio()
        Manager.Manager.sigueHumano(self)

    def mueve_rival_base(self):
        self.play_rival(self.main_window.dato_notify)

    def play_rival(self, rm_rival):
        self.reloj_stop(False)
        self.thinking(False)
        time_s = self.timekeeper.stop()
        self.setSummary("TIMERIVAL", time_s)

        if self.state in (ST_ENDGAME, ST_PAUSE):
            return self.state == ST_ENDGAME
        if self.nAjustarFuerza == ADJUST_SELECTED_BY_PLAYER:
            rm_rival = self.ajustaPlayer(rm_rival)

        self.lirm_engine.append(rm_rival)
        if not self.valoraRMrival():
            self.muestra_resultado()
            return True

        ok, self.error, move = Move.get_game_move(self.game, self.game.last_position, rm_rival.from_sq, rm_rival.to_sq, rm_rival.promotion)
        self.rm_rival = rm_rival
        if ok:
            fen_ultimo = self.last_fen()
            move.set_time_ms(int(time_s * 1000))
            self.add_move(move, False)
            self.move_the_pieces(move.liMovs, True)

            if self.siTiempo:
                move.cacheTime = self.vtime[self.is_engine_side_white].save()
            self.cache[fen_ultimo] = move
            self.play_next_move()
            return True

        else:
            return False

    def check_premove(self, from_sq, to_sq):
        self.board.remove_arrows()
        if self.premove:
            if from_sq == self.premove[0] and to_sq == self.premove[1]:
                self.premove = None
                return
        self.board.creaFlechaPremove(from_sq, to_sq)
        self.premove = from_sq, to_sq

        return True

    def ayudaMover(self):
        if not self.is_finished():
            move = Move.Move(self.game, position_before=self.game.last_position.copia())
            if self.is_tutor_enabled:
                self.analizaFinal()
                move.analysis = self.mrmTutor, 0
            Analysis.show_analysis(self.procesador, self.xtutor, move, self.board.is_white_bottom, 999, 0, must_save=False)

    def juegaPorMi(self):
        if self.state != ST_PLAYING or self.is_finished():
            return

        if self.hints:
            self.hints -= 1

        fen_base = self.last_fen()

        if self.bookR and self.bookMandatory:
            listaJugadas = self.bookR.get_list_moves(fen_base)
            if listaJugadas:
                apdesde, aphasta, appromotion, nada, nada1 = listaJugadas[0]
                return self.player_has_moved_base(apdesde, aphasta, appromotion)

        if self.aperturaObl:
            apdesde, aphasta = self.aperturaObl.from_to_active(fen_base)
            if apdesde:
                return self.player_has_moved_base(apdesde, aphasta)

        if self.is_tutor_enabled:
            self.analizaFinal()
            rm = self.mrmTutor.mejorMov()
            return self.player_has_moved_base(rm.from_sq, rm.to_sq, rm.promotion)

        return Manager.Manager.juegaPorMi(self)

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        if not self.human_is_playing:
            return self.check_premove(from_sq, to_sq)
        move = self.check_human_move(from_sq, to_sq, promotion, not self.is_tutor_enabled)
        if not move:
            return False

        movimiento = move.movimiento()

        siAnalisis = False

        is_selected = False

        fen_base = self.last_fen()

        if self.bookR and self.bookMandatory:
            listaJugadas = self.bookR.get_list_moves(fen_base)
            if listaJugadas:
                li = []
                for apdesde, aphasta, appromotion, nada, nada1 in listaJugadas:
                    mx = apdesde + aphasta + appromotion
                    if mx.strip().lower() == movimiento:
                        is_selected = True
                        break
                    li.append((apdesde, aphasta, False))
                if not is_selected:
                    self.board.ponFlechasTmp(li)
                    self.sigueHumano()
                    return False

        if not is_selected and self.aperturaObl:
            if self.aperturaObl.check_human(fen_base, from_sq, to_sq):
                is_selected = True
            else:
                apdesde, aphasta = self.aperturaObl.from_to_active(fen_base)
                if apdesde is None:
                    self.aperturaObl = None
                else:
                    self.board.ponFlechasTmp(((apdesde, aphasta, False),))
                    self.sigueHumano()
                    return False

        if not is_selected and self.aperturaStd:
            if self.aperturaStd.check_human(fen_base, from_sq, to_sq):
                is_selected = True
            else:
                if not self.aperturaStd.is_active(fen_base):
                    self.aperturaStd = None

        self.setSummary("TIMEUSER", self.timekeeper.stop())
        self.reloj_stop(True)

        is_mate = move.is_mate
        self.analizaFinal(is_mate)  # tiene que acabar siempre
        if not is_mate and not is_selected and self.is_tutor_enabled:
            if not self.tutor_book.si_esta(fen_base, movimiento):
                rmUser, n = self.mrmTutor.buscaRM(movimiento)
                if not rmUser:
                    self.main_window.pensando_tutor(True)
                    rmUser = self.xtutor.valora(self.game.last_position, from_sq, to_sq, move.promotion)
                    self.main_window.pensando_tutor(False)
                    if not rmUser:
                        self.sigueHumanoAnalisis()
                        return False
                    self.mrmTutor.agregaRM(rmUser)
                siAnalisis = True
                pointsBest, pointsUser = self.mrmTutor.difPointsBest(movimiento)
                self.setSummary("POINTSBEST", pointsBest)
                self.setSummary("POINTSUSER", pointsUser)
                difpts = self.configuration.x_tutor_difpoints
                difporc = self.configuration.x_tutor_difporc
                if self.mrmTutor.mejorRMQue(rmUser, difpts, difporc):
                    if not move.is_mate:
                        si_tutor = True
                        if self.chance:
                            num = self.mrmTutor.numMejorMovQue(movimiento)
                            if num:
                                rmTutor = self.mrmTutor.rmBest()
                                menu = QTVarios.LCMenu(self.main_window)
                                menu.opcion("None", _("There are %d best moves") % num, Iconos.Motor())
                                menu.separador()
                                resp = rmTutor.abrTextoBase()
                                if not resp:
                                    resp = _("Mate")
                                menu.opcion("tutor", "&1. %s (%s)" % (_("Show tutor"), resp), Iconos.Tutor())
                                menu.separador()
                                menu.opcion("try", "&2. %s" % _("Try again"), Iconos.Atras())
                                menu.separador()
                                menu.opcion("user", "&3. %s (%s)" % (_("Select my move"), rmUser.abrTextoBase()), Iconos.Player())
                                self.main_window.cursorFueraBoard()
                                resp = menu.lanza()
                                if resp == "try":
                                    self.sigueHumanoAnalisis()
                                    return False
                                elif resp == "user":
                                    si_tutor = False
                                elif resp != "tutor":
                                    self.sigueHumanoAnalisis()
                                    return False
                        if si_tutor:
                            tutor = Tutor.Tutor(self, move, from_sq, to_sq, False)

                            if self.aperturaStd:
                                liApPosibles = self.listaOpeningsStd.list_possible_openings(self.game)
                            else:
                                liApPosibles = None

                            if tutor.elegir(self.hints > 0, liApPosibles=liApPosibles):
                                if self.hints > 0:  # doble entrada a tutor.
                                    self.set_piece_again(from_sq)
                                    self.hints -= 1
                                    self.tutor_con_flechas = self.nArrowsTt > 0 and self.hints > 0
                                    from_sq = tutor.from_sq
                                    to_sq = tutor.to_sq
                                    promotion = tutor.promotion
                                    ok, mens, jgTutor = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
                                    if ok:
                                        move = jgTutor
                                        self.setSummary("SELECTTUTOR", True)
                            if self.configuration.x_save_tutor_variations:
                                tutor.ponVariations(move, 1 + len(self.game) / 2)

                            del tutor

        self.move_the_pieces(move.liMovs)

        if siAnalisis:
            rm, nPos = self.mrmTutor.buscaRM(move.movimiento())
            if rm:
                move.analysis = self.mrmTutor, nPos

        self.add_move(move, True)
        self.error = ""
        self.play_next_move()
        return True

    def add_move(self, move, siNuestra):
        self.game.add_move(move)
        self.beepExtendido(siNuestra)

        self.put_arrow_sc(move.from_sq, move.to_sq)

        self.ponAyudasEM()

        self.pgnRefresh(self.game.last_position.is_white)

        self.check_boards_setposition()

        self.refresh()

    def saveSummary(self):
        if not self.with_summary or not self.summary:
            return

        j_num = 0
        j_same = 0
        st_accept = 0
        st_reject = 0
        nt_accept = 0
        nt_reject = 0
        j_sum = 0

        time_user = 0.0
        ntime_user = 0
        time_rival = 0.0
        ntime_rival = 0

        for njg, d in self.summary.items():
            if "POINTSBEST" in d:
                j_num += 1
                p = d["POINTSBEST"] - d["POINTSUSER"]
                if p:
                    if d.get("SELECTTUTOR", False):
                        st_accept += p
                        nt_accept += 1
                    else:
                        st_reject += p
                        nt_reject += 1
                    j_sum += p
                else:
                    j_same += 1
            if "TIMERIVAL" in d:
                ntime_rival += 1
                time_rival += d["TIMERIVAL"]
            if "TIMEUSER" in d:
                ntime_user += 1
                time_user += d["TIMEUSER"]

        comment = self.game.first_comment
        if comment:
            comment += "\n"

        if j_num:
            comment += _("Tutor") + ": %s\n" % self.xtutor.name
            comment += _("Number of moves") + ":%d\n" % j_num
            comment += _("Same move") + ":%d (%0.2f%%)\n" % (j_same, j_same * 1.0 / j_num)
            comment += _("Accepted") + ":%d (%0.2f%%) %s: %0.2f\n" % (
                nt_accept,
                nt_accept * 1.0 / j_num,
                _("Average centipawns lost"),
                st_accept * 1.0 / nt_accept if nt_accept else 0.0,
            )
            comment += _("Rejected") + ":%d (%0.2f%%) %s: %0.2f\n" % (
                nt_reject,
                nt_reject * 1.0 / j_num,
                _("Average centipawns lost"),
                st_reject * 1.0 / nt_reject if nt_reject else 0.0,
            )
            comment += _("Total") + ":%d (100%%) %s: %0.2f\n" % (j_num, _("Average centipawns lost"), j_sum * 1.0 / j_num)

        if ntime_user or ntime_rival:
            comment += _("Average time (seconds)") + ":\n"
            if ntime_user:
                comment += "%s: %0.2f\n" % (self.configuration.x_player, time_user / ntime_user)
            if ntime_rival:
                comment += "%s: %0.2f\n" % (self.xrival.name, time_rival / ntime_rival)

        self.game.first_comment = comment

    def muestra_resultado(self):
        self.state = ST_ENDGAME
        self.disable_all()
        self.human_is_playing = False
        if self.siTiempo:
            self.main_window.stop_clock()

        mensaje, beep, player_win = self.game.label_resultado_player(self.human_side)

        self.beepResultado(beep)
        self.saveSummary()
        self.autosave()
        QTUtil.refresh_gui()
        if QTUtil2.pregunta(self.main_window, mensaje + "\n\n" + _("Do you want to play again?")):
            self.reiniciar(False)
        else:
            self.ponFinJuego(self.with_takeback)

    def ponAyudasEM(self):
        self.ponAyudas(self.hints, siQuitarAtras=False)

    def cambioRival(self):
        dic = WPlayAgainstEngine.cambioRival(self.main_window, self.configuration, self.reinicio)

        if dic:
            dr = dic["RIVAL"]
            rival = dr["CM"]
            if hasattr(rival, "icono"):
                delattr(rival, "icono")

            Util.save_pickle(self.configuration.ficheroEntMaquina, dic)
            for k, v in dic.items():
                self.reinicio[k] = v

            is_white = dic["ISWHITE"]

            self.pon_toolbar()

            self.nAjustarFuerza = dic["ADJUST"]

            r_t = dr["TIME"] * 100  # Se guarda en decimas -> milesimas
            r_p = dr["DEPTH"]
            if r_t <= 0:
                r_t = None
            if r_p <= 0:
                r_p = None
            if r_t is None and r_p is None and not dic["SITIEMPO"]:
                r_t = 1000

            dr["RESIGN"] = self.resign_limit
            self.xrival.terminar()
            self.xrival = self.procesador.creaManagerMotor(rival, r_t, r_p, self.nAjustarFuerza != ADJUST_BETTER)

            self.xrival.is_white = not is_white

            rival = self.xrival.name
            player = self.configuration.x_player
            bl, ng = player, rival
            if not is_white:
                bl, ng = ng, bl
            self.main_window.change_player_labels(bl, ng)

            # self.put_pieces_bottom( is_white )
            self.ponRotuloBasico()

            self.put_pieces_bottom(is_white)
            if is_white != self.human_side:
                self.human_side = is_white
                self.is_engine_side_white = not is_white

                self.play_next_move()

    def show_dispatch(self, tp, rm):
        if rm.time or rm.depth:
            color_engine = "DarkBlue" if self.human_is_playing else "brown"
            if rm.nodes:
                nps = "/%d" % rm.nps if rm.nps else ""
                nodes = " | %d%s" % (rm.nodes, nps)
            else:
                nodes = ""
            seldepth = "/%d" % rm.seldepth if rm.seldepth else ""
            li = ['<span style="color:%s">%s' % (color_engine, rm.name), '<b>%s</b> | <b>%d</b>%s | <b>%d"</b>%s' % (rm.abrTextoBase(), rm.depth, seldepth, rm.time // 1000, nodes)]
            pv = rm.pv
            if tp < 999:
                li1 = pv.split(" ")
                if len(li1) > tp:
                    pv = " ".join(li1[:tp])
            p = Game.Game(self.game.last_position)
            p.read_pv(pv)
            li.append(p.pgnBaseRAW())
            self.set_label3("<br>".join(li) + "</span>")
            QTUtil.refresh_gui()

    def analizaPosicion(self, row, key):
        if row < 0:
            return

        move, is_white, siUltimo, tam_lj, pos = self.dameJugadaEn(row, key)
        if not move:
            return

        max_recursion = 9999

        if not (hasattr(move, "analysis") and move.analysis):
            me = QTUtil2.mensEspera.start(self.main_window, _("Analyzing the move...."), physical_pos="ad")
            mrm, pos = self.xanalyzer.analysis_move(move, self.xanalyzer.motorTiempoJugada, self.xanalyzer.motorProfundidad)
            move.analysis = mrm, pos
            me.final()

        Analysis.show_analysis(self.procesador, self.xanalyzer, move, self.board.is_white_bottom, max_recursion, pos)
        self.put_view()

    def show_clocks(self):
        if Code.dgt:
            DGT.writeClocks(self.vtime[True].etiquetaDGT(), self.vtime[False].etiquetaDGT())

        for is_white in (WHITE, BLACK):
            ot = self.vtime[is_white]

            eti, eti2 = ot.etiquetaDif2()
            if eti:
                if is_white:
                    self.main_window.ponRelojBlancas(eti, eti2)
                else:
                    self.main_window.ponRelojNegras(eti, eti2)

