import time
import random

from Code import Manager
from Code.Polyglots import Books
from Code import TrListas
from Code.QT import QTUtil2
from Code.QT import Iconos
from Code.QT import QTVarios
from Code import Util
from Code.Openings import OpeningLines
from Code.Engines import EngineResponse
from Code.Base import Game, Move, Position
from Code.Base.Constantes import *


class ManagerOpeningEngines(Manager.Manager):
    def start(self, pathFichero):
        self.board.saveVisual()
        self.pathFichero = pathFichero
        dbop = OpeningLines.Opening(pathFichero)
        self.board.dbvisual_set_file(dbop.nom_fichero)
        self.reinicio(dbop)

    def reinicio(self, dbop):
        self.dbop = dbop
        self.dbop.open_cache_engines()
        self.game_type = GT_OPENING_LINES

        self.level = self.dbop.getconfig("ENG_LEVEL", 0)
        self.numengine = self.dbop.getconfig("ENG_ENGINE", 0)

        self.trainingEngines = self.dbop.trainingEngines()

        self.auto_analysis = self.trainingEngines.get("AUTO_ANALYSIS", True)
        self.ask_movesdifferent = self.trainingEngines.get("ASK_MOVESDIFFERENT", False)

        liTimes = self.trainingEngines.get("TIMES")
        if not liTimes:
            liTimes = [500, 1000, 2000, 4000, 8000]
        liBooks = self.trainingEngines.get("BOOKS")
        if not liBooks:
            liBooks = ["", "", "", "", ""]
        liBooks_sel = self.trainingEngines.get("BOOKS_SEL")
        if not liBooks_sel:
            liBooks_sel = ["", "", "", "", ""]
        liEngines = self.trainingEngines["ENGINES"]
        num_engines_base = len(liEngines)
        liEnginesExt = [key for key in self.trainingEngines.get("EXT_ENGINES", []) if not (key in liEngines)]
        num_engines = num_engines_base + len(liEnginesExt)

        if self.numengine >= num_engines:
            self.level += 1
            self.numengine = 0
            self.dbop.setconfig("ENG_LEVEL", self.level)
            self.dbop.setconfig("ENG_ENGINE", 0)
        num_levels = len(liTimes)
        if self.level >= num_levels:
            if QTUtil2.pregunta(self.main_window, "%s.\n%s" % (_("Training finished"), _("Do you want to reinit?"))):
                self.dbop.setconfig("ENG_LEVEL", 0)
                self.dbop.setconfig("ENG_ENGINE", 0)
                self.reinicio(dbop)
            return

        self.time = liTimes[self.level]
        nombook = liBooks[self.level]
        if nombook:
            list_books = Books.ListBooks()
            list_books.restore_pickle(self.configuration.file_books)
            self.book = list_books.buscaLibro(nombook)
            if self.book:
                self.book.polyglot()
                self.book.mode = liBooks_sel[self.level]
                if not self.book.mode:
                    self.book.mode = "mp"
        else:
            self.book = None

        if self.numengine < num_engines_base:
            self.keyengine = liEngines[self.numengine]
        else:
            self.keyengine = liEnginesExt[self.numengine - num_engines_base - 1]

        self.plies_mandatory = self.trainingEngines["MANDATORY"]
        self.plies_control = self.trainingEngines["CONTROL"]
        self.plies_pendientes = self.plies_control
        self.lost_points = self.trainingEngines["LOST_POINTS"]

        self.is_human_side_white = self.trainingEngines["COLOR"] == "WHITE"
        self.is_engine_side_white = not self.is_human_side_white

        self.siAprobado = False

        rival = self.configuration.buscaRival(self.keyengine)
        self.xrival = self.procesador.creaManagerMotor(rival, self.time, None)
        self.xrival.is_white = self.is_engine_side_white


        self.xanalyzer.cambiaOpciones(max(self.xtutor.motorTiempoJugada, self.time + 5.0), 0)

        juez = self.configuration.buscaRival(self.trainingEngines["ENGINE_CONTROL"])
        self.xjuez = self.procesador.creaManagerMotor(juez, int(self.trainingEngines["ENGINE_TIME"] * 1000), None)
        self.xjuez.anulaMultiPV()

        self.li_info = [
            "<b>%s</b>: %d/%d - %s" % (_("Engine"), self.numengine + 1, num_engines, self.xrival.name),
            '<b>%s</b>: %d/%d - %0.1f"' % (_("Level"), self.level + 1, num_levels, self.time / 1000.0),
        ]

        self.dicFENm2 = self.trainingEngines["DICFENM2"]

        self.siAyuda = False
        self.board.dbvisual_set_show_allways(False)
        self.hints = 9999  # Para que analice sin problemas

        self.game = Game.Game()

        self.main_window.pon_toolbar((TB_CLOSE, TB_RESIGN, TB_REINIT))
        self.main_window.activaJuego(True, False, siAyudas=False)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.last_position)
        self.show_side_indicator(True)
        self.remove_hints()
        self.put_pieces_bottom(self.is_human_side_white)
        self.pgnRefresh(True)

        self.ponCapInfoPorDefecto()

        self.state = ST_PLAYING

        self.check_boards_setposition()

        self.errores = 0
        self.ini_time = time.time()
        self.muestraInformacion()
        self.play_next_move()

    def play_next_move(self):
        self.muestraInformacion()
        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()

        is_white = self.game.last_position.is_white

        self.set_side_indicator(is_white)
        self.refresh()

        siRival = is_white == self.is_engine_side_white

        if not self.runcontrol():
            if siRival:
                self.disable_all()
                if self.play_rival():
                    self.play_next_move()

            else:
                self.activate_side(is_white)
                self.human_is_playing = True

    def play_rival(self):
        si_obligatorio = len(self.game) <= self.plies_mandatory
        si_pensar = True
        fenm2 = self.game.last_position.fenm2()
        moves = self.dicFENm2.get(fenm2, set())
        if si_obligatorio:
            nmoves = len(moves)
            if nmoves == 0:
                si_obligatorio = False
            else:
                move = self.dbop.get_cache_engines(self.keyengine, self.time, fenm2)
                if move is None:
                    if self.book:
                        move_book = self.book.eligeJugadaTipo(self.game.last_position.fen(), "au")
                        if move_book in list(moves):
                            move = move_book
                    if move is None:
                        move = random.choice(list(moves))
                    self.dbop.set_cache_engines(self.keyengine, self.time, fenm2, move)
                from_sq, to_sq, promotion = move[:2], move[2:4], move[4:]
                si_pensar = False

        if si_pensar:
            move = self.dbop.get_cache_engines(self.keyengine, self.time, fenm2)
            if self.book:
                move = self.book.eligeJugadaTipo(self.game.last_position.fen(), self.book.mode)
            if not move:
                rm_rival = self.xrival.juegaPartida(self.game)
                move = rm_rival.movimiento()
                self.dbop.set_cache_engines(self.keyengine, self.time, fenm2, move)
            from_sq, to_sq, promotion = move[:2], move[2:4], move[4:]
            if si_obligatorio:
                if not (move in moves):
                    move = list(moves)[0]
                    from_sq, to_sq, promotion = move[:2], move[2:4], move[4:]

        ok, mens, move = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
        if ok:
            self.add_move(move, False)
            self.move_the_pieces(move.liMovs, True)

            self.error = ""

            return True
        else:
            self.error = mens
            return False

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        move = self.check_human_move(from_sq, to_sq, promotion)
        if not move:
            return False

        fenm2 = self.game.last_position.fenm2()
        li_mv = self.dicFENm2.get(fenm2, [])
        nmv = len(li_mv)
        if nmv > 0:
            if not (move.movimiento() in li_mv):
                for mv in li_mv:
                    self.board.creaFlechaMulti(mv, False)
                self.board.creaFlechaMulti(move.movimiento(), True)
                if self.ask_movesdifferent:
                    mensaje = "%s\n%s" % (
                        _("This is not the move in the opening lines"),
                        _("Do you want to go on with this move?"),
                    )
                    if not QTUtil2.pregunta(self.main_window, mensaje):
                        self.ponFinJuego()
                        return True
                else:
                    self.mensajeEnPGN(_("This is not the move in the opening lines, you must repeat the game"))
                    self.ponFinJuego()
                    return True

        self.move_the_pieces(move.liMovs)

        self.add_move(move, True)
        self.play_next_move()
        return True

    def add_move(self, move, siNuestra):
        fenm2 = move.position_before.fenm2()
        move.es_linea = False
        if fenm2 in self.dicFENm2:
            if move.movimiento() in self.dicFENm2[fenm2]:
                move.add_nag(GOOD_MOVE)
                move.es_linea = True
        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.check_boards_setposition()

    def muestraInformacion(self):
        li = []
        li.extend(self.li_info)

        si_obligatorio = len(self.game) < self.plies_mandatory
        if si_obligatorio and self.state != ST_ENDGAME:
            fenm2 = self.game.last_position.fenm2()
            moves = self.dicFENm2.get(fenm2, [])
            if len(moves) > 0:
                li.append("<b>%s</b>: %d/%d" % (_("Mandatory move"), len(self.game) + 1, self.plies_mandatory))
            else:
                si_obligatorio = False

        if not si_obligatorio and self.state != ST_ENDGAME:
            tm = self.plies_pendientes
            if tm > 1 and len(self.game) and not self.game.move(-1).es_linea:
                li.append("%s: %d" % (_("Moves until the control"), tm - 1))

        self.set_label1("<br>".join(li))

    def run_auto_analysis(self):
        lista = []
        for njg in range(self.game.num_moves()):
            move = self.game.move(njg)
            if move.is_white() == self.is_human_side_white:
                fenm2 = move.position_before.fenm2()
                if not (fenm2 in self.dicFENm2):
                    move.njg = njg
                    lista.append(move)
                    move.fenm2 = fenm2
        total = len(lista)
        move_max = 0
        for pos, move in enumerate(lista, 1):
            if self.is_canceled():
                break
            self.ponteEnJugada(move.njg)
            self.mensEspera(siCancelar=True, masTitulo="%d/%d" % (pos, total))
            name = self.xanalyzer.name
            vtime = self.xanalyzer.motorTiempoJugada
            depth = self.xanalyzer.motorProfundidad
            mrm = self.dbop.get_cache_engines(name, vtime, move.fenm2, depth)
            ok = False
            if mrm:
                rm, pos = mrm.buscaRM(move.movimiento())
                if rm:
                    ok = True
            if not ok:
                mrm, pos = self.xanalyzer.analyse_move(
                    move, self.xanalyzer.motorTiempoJugada, self.xanalyzer.motorProfundidad
                )
                self.dbop.set_cache_engines(name, vtime, move.fenm2, mrm, depth)

            move.analysis = mrm, pos
            self.main_window.base.pgnRefresh()
            if pos == 0:
                move_max += 1

        return move_max < total  # si todos son lo máximo aunque pierda algo hay que darlo por probado


    def mensEspera(self, siFinal=False, siCancelar=False, masTitulo=None):
        if siFinal:
            if self.um:
                self.um.final()
        else:
            if self.um is None:
                self.um = QTUtil2.mensajeTemporal(
                    self.main_window, _("Analyzing"), 0, physical_pos="ad", siCancelar=True, titCancelar=_("Cancel")
                )
            if masTitulo:
                self.um.label(_("Analyzing") + " " + masTitulo)
            self.um.me.activarCancelar(siCancelar)

    def is_canceled(self):
        si = self.um.cancelado()
        if si:
            self.um.final()
        return si

    def runcontrol(self):
        puntosInicio, mateInicio = 0, 0
        puntosFinal, mateFinal = 0, 0
        num_moves = len(self.game)
        if num_moves == 0:
            return False

        self.um = None  # controla unMomento

        def aprobado():
            mens = '<b><span style="color:green">%s</span></b>' % _("Congratulations, goal achieved")
            self.li_info.append("")
            self.li_info.append(mens)
            self.muestraInformacion()
            self.dbop.setconfig("ENG_ENGINE", self.numengine + 1)
            self.mensajeEnPGN(mens)
            self.siAprobado = True

        def suspendido():
            mens = '<b><span style="color:red">%s</span></b>' % _("You must repeat the game")
            self.li_info.append("")
            self.li_info.append(mens)
            self.muestraInformacion()
            self.mensajeEnPGN(mens)

        def calculaJG(move, siinicio):
            fen = move.position_before.fen() if siinicio else move.position.fen()
            name = self.xjuez.name
            vtime = self.xjuez.motorTiempoJugada
            mrm = self.dbop.get_cache_engines(name, vtime, fen)
            if mrm is None:
                self.mensEspera()
                mrm = self.xjuez.analiza(fen)
                self.dbop.set_cache_engines(name, vtime, fen, mrm)

            rm = mrm.mejorMov()
            if (" w " in fen) == self.is_human_side_white:
                return rm.puntos, rm.mate
            else:
                return -rm.puntos, -rm.mate

        siCalcularInicio = True
        if self.game.is_finished():
            self.ponFinJuego()
            move = self.game.move(-1)
            if move.is_mate:
                if move.is_white() == self.is_human_side_white:
                    aprobado()
                else:
                    suspendido()
                self.ponFinJuego()
                return True
            puntosFinal, mateFinal = 0, 0

        else:
            move = self.game.move(-1)
            if move.es_linea:
                self.plies_pendientes = self.plies_control
            else:
                self.plies_pendientes -= 1
            if self.plies_pendientes > 0:
                return False
            # Si la ultima move es de la linea no se calcula nada
            self.mensEspera()
            puntosFinal, mateFinal = calculaJG(move, False)

        # Se marcan todas las num_moves que no siguen las lineas
        # Y se busca la ultima del color del player
        if siCalcularInicio:
            jg_inicial = None
            for njg in range(num_moves):
                move = self.game.move(njg)
                fenm2 = move.position_before.fenm2()
                if fenm2 in self.dicFENm2:
                    moves = self.dicFENm2[fenm2]
                    if not (move.movimiento() in moves):
                        move.add_nag(QUESTIONABLE_MOVE)
                        if jg_inicial is None:
                            jg_inicial = move
                elif jg_inicial is None:
                    jg_inicial = move
            if jg_inicial:
                puntosInicio, mateInicio = calculaJG(jg_inicial, True)
            else:
                puntosInicio, mateInicio = 0, 0

        self.li_info.append("<b>%s:</b>" % _("Score"))
        template = "&nbsp;&nbsp;&nbsp;&nbsp;<b>%s</b>: %d"

        def appendInfo(label, puntos, mate):
            mens = template % (label, puntos)
            if mate:
                mens += " %s %d" % (_("Mate"), mate)
            self.li_info.append(mens)

        appendInfo(_("Start"), puntosInicio, mateInicio)
        appendInfo(_("End"), puntosFinal, mateFinal)
        perdidos = puntosInicio - puntosFinal
        ok = perdidos < self.lost_points
        if mateInicio or mateFinal:
            ok = mateFinal > mateInicio
        mens = template % ("(%d)-(%d)" % (puntosInicio, puntosFinal), perdidos)
        mens = "%s %s %d" % (mens, "&lt;" if ok else "&gt;", self.lost_points)
        self.li_info.append(mens)

        if not ok:
            if self.auto_analysis:
                si_suspendido = self.run_auto_analysis()
            else:
                si_suspendido = True
            self.mensEspera(siFinal=True)
            if si_suspendido:
                suspendido()
            else:
                aprobado()
        else:
            self.mensEspera(siFinal=True)
            aprobado()

        self.ponFinJuego()
        return True

    def run_action(self, key):
        if key == TB_CLOSE:
            self.end_game()

        elif key in (TB_REINIT, TB_NEXT):
            self.reiniciar()

        elif key == TB_REPEAT:
            self.dbop.setconfig("ENG_ENGINE", self.numengine)
            self.reiniciar()

        elif key == TB_RESIGN:
            self.ponFinJuego()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True)

        elif key == TB_UTILITIES:
            liMasOpciones = []
            liMasOpciones.append(("books", _("Consult a book"), Iconos.Libros()))
            liMasOpciones.append((None, None, None))
            liMasOpciones.append((None, _("Options"), Iconos.Opciones()))
            mens = _("cancel") if self.auto_analysis else _("activate")
            liMasOpciones.append(("auto_analysis", "%s: %s" % (_("Automatic analysis"), mens), Iconos.Analizar()))
            liMasOpciones.append((None, None, None))
            mens = _("cancel") if self.ask_movesdifferent else _("activate")
            liMasOpciones.append(
                (
                    "ask_movesdifferent",
                    "%s: %s" % (_("Ask when the moves are different from the line"), mens),
                    Iconos.Pelicula_Seguir(),
                )
            )
            liMasOpciones.append((None, None, True))  # Para salir del submenu
            liMasOpciones.append((None, None, None))
            liMasOpciones.append(("run_analysis", _("Specific analysis"), Iconos.Analizar()))
            liMasOpciones.append((None, None, None))
            liMasOpciones.append(("add_line", _("Add this line"), Iconos.OpeningLines()))

            resp = self.utilidades(liMasOpciones)
            if resp == "books":
                self.librosConsulta(False)

            elif resp == "add_line":
                num_moves, nj, row, is_white = self.jugadaActual()
                game = self.game
                if num_moves != nj + 1:
                    menu = QTVarios.LCMenu(self.main_window)
                    menu.opcion("all", _("Add all moves"), Iconos.PuntoAzul())
                    menu.separador()
                    menu.opcion("parcial", _("Add until current move"), Iconos.PuntoVerde())
                    resp = menu.lanza()
                    if resp is None:
                        return
                    if resp == "parcial":
                        game = self.game.copia(nj)

                self.dbop.append(game)
                self.dbop.updateTrainingEngines()
                QTUtil2.message_bold(self.main_window, _("Done"))

            elif resp == "auto_analysis":
                self.auto_analysis = not self.auto_analysis
                self.trainingEngines["AUTO_ANALYSIS"] = self.auto_analysis
                self.dbop.setTrainingEngines(self.trainingEngines)

            elif resp == "ask_movesdifferent":
                self.ask_movesdifferent = not self.ask_movesdifferent
                self.trainingEngines["ASK_MOVESDIFFERENT"] = self.ask_movesdifferent
                self.dbop.setTrainingEngines(self.trainingEngines)

            elif resp == "run_analysis":
                self.um = None
                self.mensEspera()
                self.run_auto_analysis()
                self.mensEspera(siFinal=True)

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def final_x(self):
        return self.end_game()

    def end_game(self):
        self.dbop.close()
        self.board.restoreVisual()
        self.procesador.start()
        self.procesador.openings()
        return False

    def reiniciar(self):
        self.reinicio(self.dbop)

    def ponFinJuego(self):
        self.state = ST_ENDGAME
        self.disable_all()
        li_options = [TB_CLOSE]
        if self.siAprobado:
            li_options.append(TB_NEXT)
            li_options.append(TB_REPEAT)
        else:
            li_options.append(TB_REINIT)
        li_options.append(TB_CONFIG)
        li_options.append(TB_UTILITIES)
        self.main_window.pon_toolbar(li_options)


class ManagerOpeningLines(Manager.Manager):
    def start(self, pathFichero, modo, num_linea):
        self.board.saveVisual()

        self.pathFichero = pathFichero
        dbop = OpeningLines.Opening(pathFichero)
        self.board.dbvisual_set_file(dbop.nom_fichero)
        self.reinicio(dbop, modo, num_linea)

    def reinicio(self, dbop, modo, num_linea):
        self.dbop = dbop
        self.game_type = GT_OPENING_LINES

        self.modo = modo
        self.num_linea = num_linea

        self.training = self.dbop.training()
        self.liGames = self.training["LIGAMES_%s" % modo.upper()]
        self.game_info = self.liGames[num_linea]
        self.li_pv = self.game_info["LIPV"]
        self.numPV = len(self.li_pv)

        self.calc_totalTiempo()

        self.dicFENm2 = self.training["DICFENM2"]
        li = self.dbop.getNumLinesPV(self.li_pv)
        if len(li) > 10:
            mensLines = ",".join(["%d" % line for line in li[:10]]) + ", ..."
        else:
            mensLines = ",".join(["%d" % line for line in li])
        self.liMensBasic = []
        if self.modo != "sequential":
            self.liMensBasic.append("%d/%d" % (self.num_linea + 1, len(self.liGames)))
        self.liMensBasic.append("%s: %s" % (_("Lines"), mensLines))

        self.siAyuda = False
        self.board.dbvisual_set_show_allways(False)

        self.game = Game.Game()

        self.hints = 9999  # Para que analice sin problemas

        self.is_human_side_white = self.training["COLOR"] == "WHITE"
        self.is_engine_side_white = not self.is_human_side_white

        self.main_window.pon_toolbar((TB_CLOSE, TB_HELP, TB_REINIT))
        self.main_window.activaJuego(True, False, siAyudas=False)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.last_position)
        self.show_side_indicator(True)
        self.remove_hints()
        self.put_pieces_bottom(self.is_human_side_white)
        self.pgnRefresh(True)

        self.ponCapInfoPorDefecto()

        self.state = ST_PLAYING

        self.check_boards_setposition()

        self.errores = 0
        self.ini_time = time.time()
        self.muestraInformacion()
        self.play_next_move()

    def calc_totalTiempo(self):
        self.tm = 0
        for game_info in self.liGames:
            for tr in game_info["TRIES"]:
                self.tm += tr["TIME"]

    def ayuda(self):
        self.siAyuda = True
        self.main_window.pon_toolbar((TB_CLOSE, TB_REINIT, TB_CONFIG, TB_UTILITIES))
        self.board.dbvisual_set_show_allways(True)

        self.muestraAyuda()
        self.muestraInformacion()

    def muestraInformacion(self):
        li = []
        li.append("%s: %d" % (_("Errors"), self.errores))
        if self.siAyuda:
            li.append(_("Help activated"))
        self.set_label1("\n".join(li))

        tgm = 0
        for tr in self.game_info["TRIES"]:
            tgm += tr["TIME"]

        mens = "\n" + "\n".join(self.liMensBasic)
        mens += "\n%s:\n    %s %s\n    %s %s" % (
            _("Working time"),
            time.strftime("%H:%M:%S", time.gmtime(tgm)),
            _("Current"),
            time.strftime("%H:%M:%S", time.gmtime(self.tm)),
            _("Total"),
        )

        self.set_label2(mens)

        if self.siAyuda:
            dic_nags = TrListas.dic_nags()
            mens3 = ""
            fenm2 = self.game.last_position.fenm2()
            reg = self.dbop.getfenvalue(fenm2)
            if reg:
                mens3 = reg.get("COMENTARIO", "")
                ventaja = reg.get("VENTAJA", 0)
                valoracion = reg.get("VALORACION", 0)
                if ventaja:
                    mens3 += "\n %s" % dic_nags[ventaja]
                if valoracion:
                    mens3 += "\n %s" % dic_nags[valoracion]
            self.set_label3(mens3 if mens3 else None)

    def gameTerminada(self, is_complete):
        self.state = ST_ENDGAME
        tm = time.time() - self.ini_time
        li = [_("Line finished.")]
        if self.siAyuda:
            li.append(_("Help activated"))
        if self.errores > 0:
            li.append("%s: %d" % (_("Errors"), self.errores))

        if is_complete:
            mensaje = "\n".join(li)
            self.mensajeEnPGN(mensaje)
        dictry = {"DATE": Util.today(), "TIME": tm, "AYUDA": self.siAyuda, "ERRORS": self.errores}
        self.game_info["TRIES"].append(dictry)

        sinError = self.errores == 0 and not self.siAyuda
        if is_complete:
            if sinError:
                self.game_info["NOERROR"] += 1
                noError = self.game_info["NOERROR"]
                if self.modo == "sequential":
                    salto = 2 ** (noError + 1)
                    numGames = len(self.liGames)
                    for x in range(salto, numGames):
                        game_info = self.liGames[x]
                        if game_info["NOERROR"] != noError:
                            salto = x
                            break

                    liNuevo = self.liGames[1:salto]
                    liNuevo.append(self.game_info)
                    if numGames > salto:
                        liNuevo.extend(self.liGames[salto:])
                    self.training["LIGAMES_SEQUENTIAL"] = liNuevo
                    self.main_window.pon_toolbar((TB_CLOSE, TB_NEXT))
                else:
                    self.main_window.pon_toolbar((TB_CLOSE, TB_REINIT, TB_CONFIG, TB_UTILITIES))
            else:
                self.game_info["NOERROR"] -= 1

                self.main_window.pon_toolbar((TB_CLOSE, TB_REINIT, TB_CONFIG, TB_UTILITIES))
        else:
            if not sinError:
                self.game_info["NOERROR"] -= 1
        self.game_info["NOERROR"] = max(0, self.game_info["NOERROR"])

        self.dbop.setTraining(self.training)
        self.state = ST_ENDGAME
        self.calc_totalTiempo()
        self.muestraInformacion()

    def muestraAyuda(self):
        pv = self.li_pv[len(self.game)]
        self.board.creaFlechaMov(pv[:2], pv[2:4], "mt80")
        fenm2 = self.game.last_position.fenm2()
        for pv1 in self.dicFENm2[fenm2]:
            if pv1 != pv:
                self.board.creaFlechaMov(pv1[:2], pv1[2:4], "ms40")

    def run_action(self, key):
        if key == TB_CLOSE:
            self.end_game()

        elif key == TB_REINIT:
            self.reiniciar()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True)

        elif key == TB_UTILITIES:
            self.utilidades()

        elif key == TB_NEXT:
            self.reinicio(self.dbop, self.modo, self.num_linea)

        elif key == TB_HELP:
            self.ayuda()

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def final_x(self):
        return self.end_game()

    def end_game(self):
        self.dbop.close()
        self.board.restoreVisual()
        self.procesador.start()
        if self.modo == "static":
            self.procesador.openingsTrainingStatic(self.pathFichero)
        else:
            self.procesador.openings()
        return False

    def reiniciar(self):
        if len(self.game) > 0 and self.state != ST_ENDGAME:
            self.gameTerminada(False)
        self.reinicio(self.dbop, self.modo, self.num_linea)

    def play_next_move(self):
        self.muestraInformacion()
        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()

        is_white = self.game.last_position.is_white

        self.set_side_indicator(is_white)
        self.refresh()

        siRival = is_white == self.is_engine_side_white

        num_moves = len(self.game)
        if num_moves >= self.numPV:
            self.gameTerminada(True)
            return
        pv = self.li_pv[num_moves]

        if siRival:
            self.disable_all()

            self.rm_rival = EngineResponse.EngineResponse("Opening", self.is_engine_side_white)
            self.rm_rival.from_sq = pv[:2]
            self.rm_rival.to_sq = pv[2:4]
            self.rm_rival.promotion = pv[4:]

            self.play_rival(self.rm_rival)
            self.play_next_move()

        else:
            self.activate_side(is_white)
            self.human_is_playing = True
            if self.siAyuda:
                self.muestraAyuda()

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        move = self.check_human_move(from_sq, to_sq, promotion)
        if not move:
            return False
        pvSel = from_sq + to_sq + (promotion if promotion else "")
        pvObj = self.li_pv[len(self.game)]

        if pvSel != pvObj:
            fenm2 = move.position_before.fenm2()
            li = self.dicFENm2.get(fenm2, [])
            if pvSel in li:
                mens = _("You have selected a correct move, but this line uses another one.")
                QTUtil2.mensajeTemporal(self.main_window, mens, 2, physical_pos="tb", background="#C3D6E8")
                self.sigueHumano()
                return False

            self.errores += 1
            mens = "%s: %d" % (_("Error"), self.errores)
            QTUtil2.mensajeTemporal(
                self.main_window, mens, 1.2, physical_pos="ad", background="#FF9B00", pmImagen=Iconos.pmError()
            )
            self.muestraInformacion()
            self.sigueHumano()
            return False

        self.move_the_pieces(move.liMovs)

        self.add_move(move, True)
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
            self.add_move(move, False)
            self.move_the_pieces(move.liMovs, True)

            self.error = ""

            return True
        else:
            self.error = mens
            return False


class ManagerOpeningLinesPositions(Manager.Manager):
    def start(self, pathFichero):
        self.pathFichero = pathFichero
        dbop = OpeningLines.Opening(pathFichero)
        self.reinicio(dbop)

    def reinicio(self, dbop):
        self.dbop = dbop
        self.game_type = GT_OPENING_LINES

        self.training = self.dbop.training()
        self.li_trainPositions = self.training["LITRAINPOSITIONS"]
        self.trposition = self.li_trainPositions[0]

        self.tm = 0
        for game_info in self.li_trainPositions:
            for tr in game_info["TRIES"]:
                self.tm += tr["TIME"]

        self.liMensBasic = ["%s: %d" % (_("Moves"), len(self.li_trainPositions))]

        self.siAyuda = False
        self.with_automatic_jump = True

        cp = Position.Position()
        cp.read_fen(self.trposition["FENM2"] + " 0 1")

        self.game = Game.Game(ini_posicion=cp)

        self.hints = 9999  # Para que analice sin problemas

        self.is_human_side_white = self.training["COLOR"] == "WHITE"
        self.is_engine_side_white = not self.is_human_side_white

        self.main_window.pon_toolbar((TB_CLOSE, TB_HELP, TB_CONFIG))
        self.main_window.activaJuego(True, False, siAyudas=False)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(cp)
        self.show_side_indicator(True)
        self.remove_hints()
        self.put_pieces_bottom(self.is_human_side_white)
        self.pgnRefresh(True)

        self.ponCapInfoPorDefecto()

        self.state = ST_PLAYING

        self.check_boards_setposition()

        self.remove_info()

        self.errores = 0
        self.ini_time = time.time()
        self.muestraInformacion()
        self.play_next_move()

    def ayuda(self):
        self.siAyuda = True
        self.main_window.pon_toolbar((TB_CLOSE, TB_CONFIG))

        self.muestraAyuda()
        self.muestraInformacion()

    def muestraInformacion(self):
        li = []
        li.append("%s: %d" % (_("Errors"), self.errores))
        if self.siAyuda:
            li.append(_("Help activated"))
        self.set_label1("\n".join(li))

        tgm = 0
        for tr in self.trposition["TRIES"]:
            tgm += tr["TIME"]

        mas = time.time() - self.ini_time

        mens = "\n" + "\n".join(self.liMensBasic)
        mens += "\n%s:\n    %s %s\n    %s %s" % (
            _("Working time"),
            time.strftime("%H:%M:%S", time.gmtime(tgm + mas)),
            _("Current"),
            time.strftime("%H:%M:%S", time.gmtime(self.tm + mas)),
            _("Total"),
        )

        self.set_label2(mens)

    def posicionTerminada(self):
        tm = time.time() - self.ini_time

        siSalta = self.with_automatic_jump and self.errores == 0 and self.siAyuda is False

        if not siSalta:
            li = [_("Finished.")]
            if self.siAyuda:
                li.append(_("Help activated"))
            if self.errores > 0:
                li.append("%s: %d" % (_("Errors"), self.errores))

            QTUtil2.mensajeTemporal(self.main_window, "\n".join(li), 1.2)

        dictry = {"DATE": Util.today(), "TIME": tm, "AYUDA": self.siAyuda, "ERRORS": self.errores}
        self.trposition["TRIES"].append(dictry)

        sinError = self.errores == 0 and not self.siAyuda
        if sinError:
            self.trposition["NOERROR"] += 1
        else:
            self.trposition["NOERROR"] = max(0, self.trposition["NOERROR"] - 1)
        noError = self.trposition["NOERROR"]
        salto = 2 ** (noError + 1) + 1
        numPosics = len(self.li_trainPositions)
        for x in range(salto, numPosics):
            posic = self.li_trainPositions[x]
            if posic["NOERROR"] != noError:
                salto = x
                break

        liNuevo = self.li_trainPositions[1:salto]
        liNuevo.append(self.trposition)
        if numPosics > salto:
            liNuevo.extend(self.li_trainPositions[salto:])
        self.training["LITRAINPOSITIONS"] = liNuevo
        self.main_window.pon_toolbar((TB_CLOSE, TB_NEXT, TB_CONFIG))

        self.dbop.setTraining(self.training)
        self.state = ST_ENDGAME
        self.muestraInformacion()
        if siSalta:
            self.reinicio(self.dbop)

    def muestraAyuda(self):
        liMoves = self.trposition["MOVES"]
        for pv in liMoves:
            self.board.creaFlechaMov(pv[:2], pv[2:4], "mt80")

    def run_action(self, key):
        if key == TB_CLOSE:
            self.end_game()

        elif key == TB_CONFIG:
            base = _("What to do after solving")
            if self.with_automatic_jump:
                liMasOpciones = [("lmo_stop", "%s: %s" % (base, _("Stop")), Iconos.PuntoRojo())]
            else:
                liMasOpciones = [("lmo_jump", "%s: %s" % (base, _("Jump to the next")), Iconos.PuntoVerde())]

            resp = self.configurar(siSonidos=True, siCambioTutor=False, liMasOpciones=liMasOpciones)
            if resp in ("lmo_stop", "lmo_jump"):
                self.with_automatic_jump = resp == "lmo_jump"

        elif key == TB_UTILITIES:
            self.utilidades()

        elif key == TB_NEXT:
            self.reinicio(self.dbop)

        elif key == TB_HELP:
            self.ayuda()

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def final_x(self):
        return self.end_game()

    def end_game(self):
        self.dbop.close()
        self.procesador.start()
        self.procesador.openings()
        return False

    def play_next_move(self):
        self.muestraInformacion()
        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()

        is_white = self.game.last_position.is_white

        self.set_side_indicator(is_white)
        self.refresh()

        self.activate_side(is_white)
        self.human_is_playing = True
        if self.siAyuda:
            self.muestraAyuda()

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        move = self.check_human_move(from_sq, to_sq, promotion)
        if not move:
            return False
        pvSel = from_sq + to_sq + promotion
        lipvObj = self.trposition["MOVES"]

        if not (pvSel in lipvObj):
            self.errores += 1
            mens = "%s: %d" % (_("Error"), self.errores)
            QTUtil2.mensajeTemporal(self.main_window, mens, 2, physical_pos="ad", background="#FF9B00")
            self.muestraInformacion()
            self.sigueHumano()
            return False

        self.move_the_pieces(move.liMovs)

        self.add_move(move, True)
        self.posicionTerminada()
        return True

    def add_move(self, move, siNuestra):
        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.check_boards_setposition()
