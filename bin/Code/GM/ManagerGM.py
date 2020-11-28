import copy
import random

import Code
from Code.Openings import Opening
from Code.GM import GM
from Code import Manager
from Code import Adjourns
from Code.Base import Move
from Code.GM import WindowGM
from Code.QT import WindowJuicio
from Code.QT import QTUtil2
from Code import Util
from Code.SQL import UtilSQL
from Code.Base.Constantes import *


class ManagerGM(Manager.Manager):
    def __init__(self, procesador):
        super().__init__(procesador)

    def start(self, record):
        self.base_inicio(record)
        self.siguiente_jugada()

    def base_inicio(self, record):
        self.game_type = GT_AGAINST_GM

        self.hints = 9999  # Para que analice sin problemas

        self.puntos = 0

        self.record = record

        self.gm = record.gm
        self.is_white = record.is_white
        self.modo = record.modo
        self.siJuez = record.siJuez
        self.showevals = record.showevals
        self.engine = record.engine
        self.vtime = record.vtime
        self.depth = record.depth
        self.multiPV = record.multiPV
        self.mostrar = record.mostrar
        self.rival_name = record.rival_name
        self.jugInicial = record.jugInicial
        self.gameElegida = record.gameElegida
        self.bypassBook = record.bypassBook
        self.opening = record.opening
        self.onBypassBook = True if self.bypassBook else False
        if self.onBypassBook:
            self.bypassBook.polyglot()
        self.onOpening = True if self.opening else False

        self.siAnalizando = False

        if self.siJuez:
            self.puntos = 0
            tutor = self.configuration.buscaRival(self.engine)
            t_t = self.vtime * 100
            self.xtutor = self.procesador.creaManagerMotor(tutor, t_t, self.depth)
            self.xtutor.setMultiPV(self.multiPV)
            self.analysis = None

        self.book = Opening.OpeningPol(999)

        self.pensando(True)

        default = Code.path_resource("GM")
        carpeta = default if self.modo == "estandar" else self.configuration.personal_training_folder
        self.motorGM = GM.GM(carpeta, self.gm)
        self.motorGM.filter_side(self.is_white)
        if self.gameElegida is not None:
            self.motorGM.set_game_selected(self.gameElegida)

        self.is_human_side_white = self.is_white
        self.is_engine_side_white = not self.is_white
        self.pensando(False)

        # self.main_window.pon_toolbar((TB_CLOSE, TB_REINIT, TB_CONFIG, TB_UTILITIES))
        self.main_window.pon_toolbar((TB_CLOSE, TB_REINIT, TB_ADJOURN, TB_CONFIG, TB_UTILITIES))
        self.main_window.activaJuego(True, False)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.last_position)
        self.show_side_indicator(True)
        self.quitaAyudas()
        self.ponPiezasAbajo(self.is_white)
        dic = GM.dic_gm()
        self.nombreGM = dic[self.gm.lower()] if self.modo == "estandar" else self.gm
        rot = _("Grandmaster")
        rotulo1 = rot + ": <b>%s</b>" if self.modo == "estandar" else "<b>%s</b>"
        self.set_label1(rotulo1 % self.nombreGM)

        self.nombreRival = ""
        self.textoPuntuacion = ""
        self.ponRotuloSecundario()
        self.pgnRefresh(True)
        self.ponCapInfoPorDefecto()

        self.state = ST_PLAYING

        self.check_boards_setposition()

        self.siguiente_jugada()

    def ponRotuloSecundario(self):
        self.set_label2(self.nombreRival + "<br><br>" + self.textoPuntuacion)

    def run_action(self, key):
        if key == TB_CLOSE:
            self.end_game()

        elif key == TB_REINIT:
            self.reiniciar()

        elif key == TB_ADJOURN:
            self.adjourn()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True)

        elif key == TB_UTILITIES:
            self.utilidades()

        elif key in self.procesador.li_opciones_inicio:
            self.procesador.run_action(key)

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def final_x(self):
        if self.state == ST_ENDGAME:
            return True
        return self.end_game()

    def end_game(self):
        self.analizaTerminar()
        siJugadas = len(self.game) > 0
        if siJugadas and self.state != ST_ENDGAME:
            self.game.set_unknown()
            self.ponFinJuego()
        self.procesador.start()

        return False

    def reiniciar(self):
        if QTUtil2.pregunta(self.main_window, _("Restart the game?")):
            self.analizaTerminar()
            self.game.set_position()
            self.start(self.record)

    def analizaInicio(self):
        if not self.is_finished():
            self.xtutor.ac_inicio(self.game)
            self.siAnalizando = True

    def analizaEstado(self):
        self.xtutor.engine.ac_lee()
        self.mrm = copy.deepcopy(self.xtutor.ac_estado())
        return self.mrm

    def analizaMinimo(self, minTime):
        self.mrm = copy.deepcopy(self.xtutor.ac_minimo(minTime, False))
        return self.mrm

    def analizaFinal(self):
        if self.siAnalizando:
            self.siAnalizando = False
            self.xtutor.ac_final(-1)

    def siguiente_jugada(self):
        self.analizaFinal()
        self.disable_all()

        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()

        is_white = self.game.last_position.is_white

        if (len(self.game) > 0) and self.motorGM.is_finished():
            self.put_result()
            return

        self.set_side_indicator(is_white)
        self.refresh()

        siRival = is_white == self.is_engine_side_white

        if self.jugInicial > 1:
            siJugInicial = (len(self.game) / 2 + 1) <= self.jugInicial
        else:
            siJugInicial = False

        liAlternativas = self.motorGM.alternativas()
        nliAlternativas = len(liAlternativas)

        # Movimiento automatico
        if siJugInicial or self.onOpening or self.onBypassBook:
            siBuscar = True
            if self.onOpening:
                li_pv = self.opening.a1h8.split(" ")
                nj = len(self.game)
                if len(li_pv) > nj:
                    move = li_pv[nj]
                    if move in liAlternativas:
                        siBuscar = False
                    else:
                        self.onOpening = False
                else:
                    self.onOpening = False

            if siBuscar:
                if self.onBypassBook:
                    li_moves = self.bypassBook.get_list_moves(self.last_fen())
                    liN = []
                    for from_sq, to_sq, promotion, pgn, peso in li_moves:
                        move = from_sq + to_sq + promotion
                        if move in liAlternativas:
                            liN.append(move)
                    if liN:
                        siBuscar = False
                        nliAlternativas = len(liN)
                        if nliAlternativas > 1:
                            pos = random.randint(0, nliAlternativas - 1)
                            move = liN[pos]
                        else:
                            move = liN[0]
                    else:
                        self.onBypassBook = None

            if siBuscar:
                if siJugInicial:
                    siBuscar = False
                    if nliAlternativas > 1:
                        pos = random.randint(0, nliAlternativas - 1)
                        move = liAlternativas[pos]
                    elif nliAlternativas == 1:
                        move = liAlternativas[0]

            if not siBuscar:
                self.play_rival(move)
                self.siguiente_jugada()
                return

        if siRival:
            if nliAlternativas > 1:
                if self.rival_name:
                    li_moves = self.motorGM.get_moves_txt(self.game.last_position, False)
                    from_sq, to_sq, promotion = WindowGM.eligeJugada(self, li_moves, False)
                    move = from_sq + to_sq + promotion
                else:
                    pos = random.randint(0, nliAlternativas - 1)
                    move = liAlternativas[pos]
            else:
                move = liAlternativas[0]

            self.play_rival(move)
            self.siguiente_jugada()

        else:
            self.human_is_playing = True
            self.pensando(True)
            self.analizaInicio()
            self.activate_side(is_white)
            self.pensando(False)

    def analizaTerminar(self):
        if self.siAnalizando:
            self.siAnalizando = False
            self.xtutor.terminar()

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        jgUsu = self.check_human_move(from_sq, to_sq, promotion)
        if not jgUsu:
            return False

        movimiento = jgUsu.movimiento()
        position = self.game.last_position
        isValid = self.motorGM.is_valid_move(movimiento)
        analysis = None

        if not isValid:
            self.board.set_position(position)
            self.board.activate_side(self.is_human_side_white)
            li_moves = self.motorGM.get_moves_txt(position, True)
            desdeGM, hastaGM, promotionGM = WindowGM.eligeJugada(self, li_moves, True)
            siAnalizaJuez = self.siJuez
            if siAnalizaJuez:
                if self.book:
                    fen = self.last_fen()
                    siH = self.book.check_human(fen, from_sq, to_sq)
                    is_gm = self.book.check_human(fen, desdeGM, hastaGM)
                    if is_gm and siH:
                        siAnalizaJuez = False
                    else:
                        self.book = False
        else:
            siAnalizaJuez = (
                self.siJuez and self.mostrar is None
            )  # None es ver siempre False no ver nunca True ver si diferentes
            if len(movimiento) == 5:
                promotion = movimiento[4].lower()
            desdeGM, hastaGM, promotionGM = from_sq, to_sq, promotion

        ok, mens, jgGM = Move.get_game_move(self.game, position, desdeGM, hastaGM, promotionGM)
        movGM = jgGM.pgn_translated()
        movUsu = jgUsu.pgn_translated()

        if siAnalizaJuez:
            um = QTUtil2.analizando(self.main_window)
            mrm = self.analizaMinimo(self.vtime * 100)

            import time
            t = time.time()

            rmUsu, nada = mrm.buscaRM(jgUsu.movimiento())
            if rmUsu is None:
                um = QTUtil2.analizando(self.main_window)
                self.analizaFinal()
                rmUsu = self.xtutor.valora(position, from_sq, to_sq, promotion)
                mrm.agregaRM(rmUsu)
                self.analizaInicio()
                um.final()


            rmGM, pos_gm = mrm.buscaRM(jgGM.movimiento())
            if rmGM is None:
                self.analizaFinal()
                rmGM = self.xtutor.valora(position, desdeGM, hastaGM, promotionGM)
                pos_gm = mrm.agregaRM(rmGM)
                self.analizaInicio()

            um.final()

            analysis = mrm, pos_gm
            dpts = rmUsu.centipawns_abs() - rmGM.centipawns_abs()

            if self.mostrar is None or ((self.mostrar is True) and not isValid):
                w = WindowJuicio.WJuicio(
                    self,
                    self.xtutor,
                    self.nombreGM,
                    position,
                    mrm,
                    rmGM,
                    rmUsu,
                    analysis,
                    is_competitive=not self.showevals,
                )
                w.exec_()

                rm, pos_gm = w.analysis[0].buscaRM(jgGM.movimiento())
                analysis = w.analysis[0], pos_gm

                dpts = w.difPuntos()

            self.puntos += dpts

            comentario0 = "<b>%s</b> : %s = %s<br>" % (self.configuration.x_player, movUsu, rmUsu.texto())
            comentario0 += "<b>%s</b> : %s = %s<br>" % (self.nombreGM, movGM, rmGM.texto())
            comentario1 = "<br><b>%s</b> = %+d<br>" % (_("Difference"), dpts)
            comentario2 = "<b>%s</b> = %+d<br>" % (_("Points accumulated"), self.puntos)
            self.textoPuntuacion = comentario2
            self.ponRotuloSecundario()

            if not isValid:
                jgGM.comment = (
                    (comentario0 + comentario1 + comentario2)
                    .replace("<b>", "")
                    .replace("</b>", "")
                    .replace("<br>", "\n")
                )

        self.analizaFinal()

        self.move_the_pieces(jgGM.liMovs)

        jgGM.analysis = analysis
        self.add_move(jgGM, True)
        self.error = ""
        self.siguiente_jugada()
        return True

    def analizaPosicion(self, row, key):
        if self.state != ST_ENDGAME:
            return
        Manager.Manager.analizaPosicion(self, row, key)

    def play_rival(self, move):
        from_sq = move[:2]
        to_sq = move[2:4]
        promotion = move[4:]

        ok, mens, move = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
        if ok:
            self.error = ""

            self.add_move(move, False)
            self.move_the_pieces(move.liMovs, True)

            return True
        else:
            self.error = mens
            return False

    def add_move(self, move, siNuestra):
        self.game.add_move(move)
        self.game.check()

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        txt = self.motorGM.label_game_if_unique(is_gm=self.modo == "estandar")
        if txt:
            self.nombreRival = txt
        self.ponRotuloSecundario()

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.motorGM.play(move.movimiento())

        self.check_boards_setposition()

    def put_result(self):
        self.state = ST_ENDGAME
        self.board.disable_all()

        mensaje = _("Game ended")

        txt, porc, txtResumen = self.motorGM.resultado(self.game)
        mensaje += "<br><br>" + txt
        if self.siJuez:
            mensaje += "<br><br><b>%s</b> = %+d<br>" % (_("Points accumulated"), self.puntos)

        self.mensajeEnPGN(mensaje)

        dbHisto = UtilSQL.DictSQL(self.configuration.ficheroGMhisto)

        gmK = "P_%s" % self.gm if self.modo == "personal" else self.gm

        dic = {}
        dic["FECHA"] = Util.today()
        dic["PUNTOS"] = self.puntos
        dic["PACIERTOS"] = porc
        dic["JUEZ"] = self.engine
        dic["TIME"] = self.vtime
        dic["RESUMEN"] = txtResumen

        liHisto = dbHisto[gmK]
        if liHisto is None:
            liHisto = []
        liHisto.insert(0, dic)
        dbHisto[gmK] = liHisto
        dbHisto.pack()
        dbHisto.close()

    def save_state(self):
        dic = {}
        li_vars = dir(self)
        ti = type(1)
        tb = type(True)
        ts = type("x")
        for var in li_vars:
            xvar = getattr(self, var)
            if not var.startswith("__"):
                if type(xvar) in (ti, tb, ts):
                    dic[var] = xvar
        dic["record"] = self.record
        dic["game"] = self.game.save()
        return dic

    def run_adjourn(self, dic):
        for k, v in dic.items():
            if k == "record":
                self.base_inicio(v)
            elif k == "game":
                self.game.restore(v)
            else:
                setattr(self, k, v)
        self.siguiente_jugada()

    def adjourn(self):
        if QTUtil2.pregunta(self.main_window, _("Do you want to adjourn the game?")):
            dic = self.save_state()

            label_menu = "%s %s" % (_("Play like a Grandmaster"), self.nombreGM)
            self.state = ST_ENDGAME

            with Adjourns.Adjourns() as adj:
                adj.add(self.game_type, dic, label_menu)
                adj.si_seguimos(self)

    def current_pgn(self):
        gm = self.gm
        motor_gm = self.motorGM

        game_gm = motor_gm.get_last_game()

        if game_gm:
            event = game_gm.event
            oponent = game_gm.oponent
            fecha = game_gm.date
            result = game_gm.result
        else:
            event = "?"
            oponent = "?"
            fecha = "????.??.??"
            result = "*"

        if self.is_white:
            blancas = gm
            negras = oponent
        else:
            blancas = oponent
            negras = gm

        resp = '[Event "%s"]\n' % event
        resp += '[Date "%s"]\n' % fecha
        resp += '[White "%s"]\n' % blancas
        resp += '[Black "%s"]\n' % negras
        resp += '[Result "%s"]\n' % result.strip()

        ap = self.game.opening
        if ap:
            resp += '[ECO "%s"]\n' % ap.eco
            resp += '[Opening "%s"]\n' % ap.trNombre

        resp += "\n" + self.game.pgnBase() + " " + result.strip()

        return resp
