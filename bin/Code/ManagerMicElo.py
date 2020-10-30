import datetime
import random

from Code.Polyglots import Books
from Code import DGT
from Code.Engines import EnginesMicElo, EngineResponse
from Code import Manager
from Code.Base import Move
from Code.QT import QTUtil2
from Code import Util
from Code.SQL import UtilSQL
import Code
from Code.Base.Constantes import *


class DicMicElos:
    def __init__(self):
        self.variable = "DicMicElos"
        self.configuration = Code.configuration
        self._dic = self.configuration.leeVariables(self.variable)

    def dic(self):
        return self._dic

    def cambia_elo(self, clave_motor, nuevo_elo):
        self._dic = self.configuration.leeVariables(self.variable)
        self._dic[clave_motor] = nuevo_elo
        self.configuration.escVariables(self.variable, self._dic)


def lista():
    li = EnginesMicElo.all_engines()
    dic_elos = DicMicElos().dic()
    for mt in li:
        k = mt.key
        if k in dic_elos:
            mt.elo = dic_elos[k]

    return li


class ManagerMicElo(Manager.Manager):
    li_t = None

    @staticmethod
    def calc_dif_elo(elo_jugador, elo_rival, resultado):
        if resultado == RS_WIN_PLAYER:
            result = 1
        elif resultado == RS_DRAW:
            result = 0
        else:
            result = -1
        return Util.fideELO(elo_jugador, elo_rival, result)

    def list_engines(self, elo):
        self.li_t = (
            (0, 50, 3),
            (20, 53, 5),
            (40, 58, 4),
            (60, 62, 4),
            (80, 66, 5),
            (100, 69, 4),
            (120, 73, 3),
            (140, 76, 3),
            (160, 79, 3),
            (180, 82, 2),
            (200, 84, 9),
            (300, 93, 4),
            (400, 97, 3),
        )
        # self.liK = ((0, 60), (800, 50), (1200, 40), (1600, 30), (2000, 30), (2400, 10))

        li = []
        self.liMotores = lista()
        numX = len(self.liMotores)
        for num, mt in enumerate(self.liMotores):
            mtElo = mt.elo
            mt.siJugable = abs(mtElo - elo) < 400
            mt.siOut = not mt.siJugable
            mt.baseElo = elo  # servira para rehacer la lista y elegir en aplazamiento
            if mt.siJugable or (mtElo > elo):

                def rot(res):
                    return self.calc_dif_elo(elo, mtElo, res)

                def rrot(res):
                    return self.calc_dif_elo(mtElo, elo, res)

                mt.pgana = rot(RS_WIN_PLAYER)
                mt.ptablas = rot(RS_DRAW)
                mt.ppierde = rot(RS_WIN_OPPONENT)

                mt.rgana = rrot(RS_WIN_PLAYER)
                mt.rtablas = rrot(RS_DRAW)
                mt.rpierde = rrot(RS_WIN_OPPONENT)

                mt.number = numX - num

                li.append(mt)

        return li

    def engineAplazado(self, alias, basElo):
        li = self.list_engines(basElo)
        for mt in li:
            if mt.alias == alias:
                return mt
        return None

    def inicio(self, datosMotor, minutos, segundos, aplazamiento=None):

        self.game_type = GT_MICELO

        self.is_competitive = True

        self.resultado = None
        self.human_is_playing = False
        self.state = ST_PLAYING
        self.puestoResultado = False  # Problema doble asignacion de ptos Thomas

        if aplazamiento:
            is_white = aplazamiento["ISWHITE"]
        else:
            is_white = self.determinaColor(datosMotor)

        self.is_human_side_white = is_white
        self.is_engine_side_white = not is_white

        self.lirm_engine = []
        self.next_test_resign = 0
        self.resign_limit = -1000

        self.is_tutor_enabled = False
        self.main_window.set_activate_tutor(False)
        self.ayudas_iniciales = self.ayudas = 0

        self.vtime = {}
        self.maxSegundos = minutos * 60
        self.segundosJugada = segundos

        # -Aplazamiento 1/2--------------------------------------------------
        if aplazamiento:
            self.game.restore(aplazamiento["JUGADAS"])

            self.datosMotor = self.engineAplazado(aplazamiento["ALIAS"], aplazamiento["BASEELO"])

            self.vtime[True] = Util.Timer(aplazamiento["TIEMPOBLANCAS"])
            self.vtime[False] = Util.Timer(aplazamiento["TIEMPONEGRAS"])

            self.maxSegundos = aplazamiento["MAXSEGUNDOS"]
            self.segundosJugada = aplazamiento["SEGUNDOSJUGADA"]

            self.game.assign_opening()

        else:
            self.datosMotor = datosMotor
            self.vtime[True] = Util.Timer(self.maxSegundos)
            self.vtime[False] = Util.Timer(self.maxSegundos)

        cbook = self.datosMotor.book if self.datosMotor.book else Code.tbook
        self.book = Books.Libro("P", cbook, cbook, True)
        self.book.polyglot()

        elo = self.datosMotor.elo
        self.maxMoveBook = elo / 200 if 0 <= elo <= 1700 else 9999

        eloengine = self.datosMotor.elo
        eloplayer = self.configuration.miceloActivo()
        self.whiteElo = eloplayer if is_white else eloengine
        self.blackElo = eloplayer if not is_white else eloengine

        self.xrival = self.procesador.creaManagerMotor(
            self.datosMotor, None, None, siMultiPV=self.datosMotor.multiPV > 0
        )

        self.pte_tool_resigndraw = False
        if self.is_human_side_white:
            self.pte_tool_resigndraw = True
            self.maxPlyRendirse = 1
        else:
            self.maxPlyRendirse = 0

        if aplazamiento and len(self.game) > self.maxPlyRendirse:
            self.pte_tool_resigndraw = False

        self.pon_toolbar()

        self.main_window.activaJuego(True, True, siAyudas=False)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.last_position)
        self.ponPiezasAbajo(is_white)
        self.quitaAyudas(True, siQuitarAtras=True)
        self.show_side_indicator(True)

        nbsp = "&nbsp;" * 3

        txt = "%s:%+d%s%s:%+d%s%s:%+d" % (
            _("Win"),
            self.datosMotor.pgana,
            nbsp,
            _("Draw"),
            self.datosMotor.ptablas,
            nbsp,
            _("Loss"),
            self.datosMotor.ppierde,
        )
        self.set_label1("<center>%s</center>" % txt)
        self.set_label2("")
        self.pgnRefresh(True)
        self.ponCapInfoPorDefecto()

        # -Aplazamiento 2/2--------------------------------------------------
        if aplazamiento:
            self.mueveJugada(GO_END)
            self.siPrimeraJugadaHecha = True
        else:
            self.siPrimeraJugadaHecha = False

        tpBL = self.vtime[True].etiqueta()
        tpNG = self.vtime[False].etiqueta()
        self.rival = rival = self.datosMotor.alias + " (%d)" % self.datosMotor.elo
        player = self.configuration.x_player + " (%d)" % self.configuration.miceloActivo()
        bl, ng = player, rival
        if self.is_engine_side_white:
            bl, ng = ng, bl
        self.main_window.ponDatosReloj(bl, tpBL, ng, tpNG)
        self.refresh()

        self.check_boards_setposition()

        if not self.is_human_side_white:
            mensaje = _("Press the continue button to start.")
            self.mensajeEnPGN(mensaje)

        self.siguiente_jugada()

    def pon_toolbar(self):
        if self.pte_tool_resigndraw:
            liTool = (TB_CANCEL, TB_ADJOURN, TB_TAKEBACK, TB_CONFIG, TB_UTILITIES)
        else:
            liTool = (TB_RESIGN, TB_DRAW, TB_ADJOURN, TB_CONFIG, TB_UTILITIES)

        self.main_window.pon_toolbar(liTool)

    def run_action(self, key):

        if key in (TB_RESIGN, TB_CANCEL):
            self.rendirse()

        elif key == TB_DRAW:
            self.tablasPlayer()

        elif key == TB_CONFIG:
            self.configurar(siSonidos=True)

        elif key == TB_TAKEBACK:
            self.atras()

        elif key == TB_UTILITIES:
            self.utilidadesElo()

        elif key == TB_ADJOURN:
            self.aplazar()

        elif key in self.procesador.li_opciones_inicio:
            self.procesador.run_action(key)

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def aplazar(self):
        if len(self.game) and QTUtil2.pregunta(self.main_window, _("Do you want to adjourn the game?")):
            aplazamiento = {}
            aplazamiento["TIPOJUEGO"] = self.game_type
            aplazamiento["ISWHITE"] = self.is_human_side_white
            aplazamiento["JUGADAS"] = self.game.save()

            aplazamiento["BASEELO"] = self.datosMotor.baseElo
            aplazamiento["ALIAS"] = self.datosMotor.alias

            aplazamiento["MAXSEGUNDOS"] = self.maxSegundos
            aplazamiento["SEGUNDOSJUGADA"] = self.segundosJugada
            aplazamiento["TIEMPOBLANCAS"] = self.vtime[True].tiempoAplazamiento()
            aplazamiento["TIEMPONEGRAS"] = self.vtime[False].tiempoAplazamiento()

            self.configuration.graba(aplazamiento)
            self.state = ST_ENDGAME
            self.main_window.accept()

    def final_x(self):
        return self.rendirse()

    def rendirse(self):
        if self.state == ST_ENDGAME:
            return True
        if (len(self.game) > 0) and not self.pte_tool_resigndraw:
            if not QTUtil2.pregunta(self.main_window, _("Do you want to resign?") + " (%d)" % self.datosMotor.ppierde):
                return False  # no abandona
            self.game.resign(self.is_human_side_white)
            self.put_result(RS_WIN_OPPONENT)
        else:
            self.procesador.inicio()

        return False

    def siguiente_jugada(self):

        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.human_is_playing = False
        self.put_view()
        is_white = self.game.last_position.is_white

        num_moves = len(self.game)

        if num_moves > 0:
            jgUltima = self.game.last_jg()
            if jgUltima:
                if jgUltima.is_mate:
                    self.put_result(RS_WIN_OPPONENT if self.is_human_side_white == is_white else RS_WIN_PLAYER)
                    return
                if jgUltima.is_draw_stalemate:
                    self.put_result(RS_DRAW)
                    return
                if jgUltima.is_draw_repetition:
                    self.put_result(RS_DRAW_REPETITION)
                    return
                if jgUltima.is_draw_50:
                    self.put_result(RS_DRAW_50)
                    return
                if jgUltima.is_draw_material:
                    self.put_result(RS_DRAW_MATERIAL)
                    return

        siRival = is_white == self.is_engine_side_white
        self.set_side_indicator(is_white)

        self.refresh()

        if siRival:
            self.reloj_start(False)
            self.pensando(True)
            self.disable_all()

            siEncontrada = False

            if self.book:
                if self.game.last_position.num_moves >= self.maxMoveBook:
                    self.book = None
                else:
                    fen = self.last_fen()
                    pv = self.book.eligeJugadaTipo(fen, "ap")
                    if pv:
                        rm_rival = EngineResponse.EngineResponse("Opening", self.is_engine_side_white)
                        rm_rival.from_sq = pv[:2]
                        rm_rival.to_sq = pv[2:4]
                        rm_rival.promotion = pv[4:]
                        siEncontrada = True
                    else:
                        self.book = None
            if not siEncontrada:
                tiempoBlancas = self.vtime[True].tiempoPendiente
                tiempoNegras = self.vtime[False].tiempoPendiente
                mrm = self.xrival.juegaTiempoTorneo(self.game, tiempoBlancas, tiempoNegras, self.segundosJugada)
                if mrm is None:
                    self.pensando(False)
                    return False
                rm_rival = mrm.mejorMov()

            self.reloj_stop(False)

            self.pensando(False)
            if self.mueve_rival(rm_rival):
                self.lirm_engine.append(rm_rival)
                if self.valoraRMrival(rm_rival):
                    self.siguiente_jugada()
            else:
                self.put_result(RS_WIN_PLAYER)
        else:
            self.reloj_start(True)

            self.human_is_playing = True
            self.activate_side(is_white)

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        move = self.checkmueve_humano(from_sq, to_sq, promotion)
        if not move:
            return False

        self.move_the_pieces(move.liMovs)
        self.reloj_stop(True)

        self.add_move(move, True)
        self.siguiente_jugada()
        return True

    def add_move(self, move, siNuestra):

        if not self.siPrimeraJugadaHecha:
            self.siPrimeraJugadaHecha = True

        self.game.li_moves.append(move)
        self.game.comprueba()

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.check_boards_setposition()

        if self.pte_tool_resigndraw:
            if len(self.game) > self.maxPlyRendirse:
                self.pte_tool_resigndraw = False
                self.pon_toolbar()

    def mueve_rival(self, respMotor):
        from_sq = respMotor.from_sq
        to_sq = respMotor.to_sq

        promotion = respMotor.promotion

        siBien, mens, move = Move.get_game_move(self.game, self.game.last_position, from_sq, to_sq, promotion)
        if siBien:
            self.add_move(move, False)
            self.move_the_pieces(move.liMovs, True)

            self.error = ""

            return True
        else:
            self.error = mens
            return False

    def put_result(self, quien):
        if self.puestoResultado:  # Problema doble asignacion de ptos Thomas
            return

        self.resultado = quien
        self.disable_all()
        self.human_is_playing = False

        self.state = ST_ENDGAME

        self.beepResultadoCAMBIAR(quien)

        nombreContrario = self.rival

        mensaje = _("Game ended")
        if quien == RS_WIN_PLAYER:
            mensaje = _X(_("Congratulations you have won against %1."), nombreContrario)

        elif quien == RS_WIN_OPPONENT:
            mensaje = _X(_("Unfortunately you have lost against %1."), nombreContrario)

        elif quien == RS_DRAW:
            mensaje = _X(_("Draw against %1."), nombreContrario)

        elif quien == RS_DRAW_REPETITION:
            mensaje = _X(
                _("Draw due to three times repetition (n. %1) against %2."),
                self.game.rotuloTablasRepeticion,
                nombreContrario,
            )
            self.resultado = RS_DRAW

        elif quien == RS_DRAW_50:
            mensaje = _X(_("Draw according to the 50 move rule against %1."), nombreContrario)
            self.resultado = RS_DRAW

        elif quien == RS_DRAW_MATERIAL:
            mensaje = _X(_("Draw, not enough material to mate %1."), nombreContrario)
            self.resultado = RS_DRAW

        elif quien == RS_WIN_PLAYER_TIME:
            if self.game.last_position.siFaltaMaterialColor(self.is_human_side_white):
                return self.put_result(RS_DRAW_MATERIAL)
            mensaje = _X(_("Congratulations, you win against %1 on time."), nombreContrario)
            self.resultado = RS_WIN_PLAYER

        elif quien == RS_WIN_OPPONENT_TIME:
            if self.game.last_position.siFaltaMaterialColor(not self.is_human_side_white):
                return self.put_result(RS_DRAW_MATERIAL)
            mensaje = _X(_("%1 has won on time."), nombreContrario)
            self.resultado = RS_WIN_OPPONENT

        elo = self.configuration.miceloActivo()
        relo = self.datosMotor.elo
        if self.resultado == RS_WIN_PLAYER:
            difelo = self.datosMotor.pgana

        elif self.resultado == RS_WIN_OPPONENT:
            difelo = self.datosMotor.ppierde

        else:
            difelo = self.datosMotor.ptablas

        nelo = elo + difelo
        if nelo < 0:
            nelo = 0
        self.configuration.ponMiceloActivo(nelo)

        rnelo = relo - difelo
        if rnelo < 100:
            rnelo = 100
        dme = DicMicElos()
        dme.cambia_elo(self.datosMotor.key, rnelo)
        # TODO en el mensaje poner el elo con el que queda el rival, self.rival incluye el elo antiguo, hay que indicar el elo nuevo

        self.historial(elo, nelo)
        self.configuration.graba()

        mensaje += "<br><br>%s : %d<br>" % (_("New Tourney-Elo"), nelo)

        self.guardarGanados(quien == RS_WIN_PLAYER)
        self.puestoResultado = True
        self.mensajeEnPGN(mensaje)
        self.ponFinJuego()

    def historial(self, elo, nelo):
        dic = {}
        dic["FECHA"] = datetime.datetime.now()
        dic["RIVAL"] = self.datosMotor.name
        dic["RESULTADO"] = self.resultado
        dic["AELO"] = elo
        dic["NELO"] = nelo

        lik = UtilSQL.ListSQL(self.configuration.fichEstadMicElo)
        lik.append(dic)
        lik.close()

        dd = UtilSQL.DictSQL(self.configuration.fichEstadMicElo, tabla="color")
        key = self.datosMotor.name
        dd[key] = self.is_human_side_white
        dd.close()

    def determinaColor(self, datosMotor):
        key = datosMotor.name

        dd = UtilSQL.DictSQL(self.configuration.fichEstadMicElo, tabla="color")
        previo = dd.get(key, random.randint(0, 1) == 0)
        dd.close()
        return not previo

    def set_clock(self):

        if (not self.siPrimeraJugadaHecha) or self.state != ST_PLAYING:
            return

        def mira(is_white):
            ot = self.vtime[is_white]

            eti, eti2 = ot.etiquetaDif2()
            if eti:
                if is_white:
                    self.main_window.ponRelojBlancas(eti, eti2)
                else:
                    self.main_window.ponRelojNegras(eti, eti2)

            if ot.siAgotado():
                siJugador = self.is_human_side_white == is_white
                self.put_result(RS_WIN_OPPONENT_TIME if siJugador else RS_WIN_PLAYER_TIME)
                return False

            return True

        if Code.dgt:
            DGT.writeClocks(self.vtime[True].etiquetaDGT(), self.vtime[False].etiquetaDGT())

        if self.human_is_playing:
            is_white = self.is_human_side_white
        else:
            is_white = not self.is_human_side_white
        mira(is_white)

    def reloj_start(self, siUsuario):
        if self.siPrimeraJugadaHecha:
            self.vtime[siUsuario == self.is_human_side_white].iniciaMarcador()
            self.main_window.start_clock(self.set_clock, transicion=200)

    def reloj_stop(self, siUsuario):
        if self.siPrimeraJugadaHecha:
            self.vtime[siUsuario == self.is_human_side_white].paraMarcador(self.segundosJugada)
            self.set_clock()
            self.main_window.stop_clock()
            self.refresh()

    def atras(self):
        if len(self.game) > 2:
            self.game.anulaUltimoMovimiento(self.is_human_side_white)
            self.game.assign_opening()
            self.goto_end()
            self.refresh()
            self.siguiente_jugada()
