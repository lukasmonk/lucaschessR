from PySide2 import QtCore, QtGui, QtWidgets

import struct
import psutil
import FasterCode

from Code.Base import Game, Position
import Code
from Code.Engines import EngineRun
from Code.QT import Voyager
from Code.Kibitzers import Kibitzers
from Code.QT import Colocacion
from Code.QT import Delegados
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import Piezas
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code.Board import Board
from Code.Kibitzers import WindowKibitzers


class WKibEngine(QtWidgets.QDialog):
    def __init__(self, cpu):
        QtWidgets.QDialog.__init__(self)

        self.cpu = cpu

        self.kibitzer = cpu.kibitzer

        self.siCandidates = cpu.tipo == Kibitzers.KIB_CANDIDATES

        self.type = cpu.tipo

        dicVideo = self.cpu.dic_video
        if not dicVideo:
            dicVideo = {}

        self.siTop = dicVideo.get("SITOP", True)
        self.show_board = dicVideo.get("SHOW_BOARD", True)
        self.nArrows = dicVideo.get("NARROWS", 2)

        self.game = None
        self.li_moves = []

        self.setWindowTitle(cpu.titulo)
        self.setWindowIcon(Iconos.Kibitzer())

        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint
            | QtCore.Qt.Dialog
            | QtCore.Qt.WindowTitleHint
            | QtCore.Qt.WindowMinimizeButtonHint
        )

        self.setBackgroundRole(QtGui.QPalette.Light)

        Code.configuration = cpu.configuration

        Code.todasPiezas = Piezas.TodasPiezas()
        config_board = cpu.configuration.config_board("kib" + cpu.kibitzer.huella, 24)
        self.board = Board.Board(self, config_board)
        self.board.crea()
        self.board.set_dispatcher(self.mensajero)

        self.with_figurines = cpu.configuration.x_pgn_withfigurines

        Delegados.generaPM(self.board.piezas)
        delegado = Delegados.EtiquetaPOS(True, siLineas=False) if self.with_figurines else None

        o_columns = Columnas.ListaColumnas()
        if not self.siCandidates:
            o_columns.nueva("DEPTH", "^", 40, centered=True)
        o_columns.nueva("BESTMOVE", _("Alternatives"), 80, centered=True, edicion=delegado)
        o_columns.nueva("EVALUATION", _("Evaluation"), 85, centered=True)
        o_columns.nueva("MAINLINE", _("Main line"), 400)
        self.grid = Grid.Grid(self, o_columns, dicVideo=dicVideo, siSelecFilas=True)

        self.lbDepth = Controles.LB(self)

        li_acciones = (
            (_("Quit"), Iconos.Kibitzer_Close(), self.terminar),
            (_("Continue"), Iconos.Kibitzer_Play(), self.play),
            (_("Pause"), Iconos.Kibitzer_Pause(), self.pause),
            (_("Takeback"), Iconos.Kibitzer_Back(), self.takeback),
            (_("The line selected is saved on clipboard"), Iconos.Kibitzer_Clipboard(), self.portapapelesJugSelected),
            (_("Analyze only color"), Iconos.Kibitzer_Side(), self.color),
            (_("Show/hide board"), Iconos.Kibitzer_Board(), self.config_board),
            (_("Manual position"), Iconos.Kibitzer_Voyager(), self.set_position),
            ("%s: %s" % (_("Enable"), _("window on top")), Iconos.Kibitzer_Up(), self.windowTop),
            ("%s: %s" % (_("Disable"), _("window on top")), Iconos.Kibitzer_Down(), self.windowBottom),
            (_("Options"), Iconos.Kibitzer_Options(), self.change_options),
        )
        self.tb = Controles.TBrutina(self, li_acciones, with_text=False, icon_size=24)
        self.tb.setAccionVisible(self.play, False)

        ly1 = Colocacion.H().control(self.tb).relleno().control(self.lbDepth).margen(0)
        ly2 = Colocacion.H().control(self.board).control(self.grid).margen(0)
        layout = Colocacion.V().otro(ly1).espacio(-10).otro(ly2).margen(3)
        self.setLayout(layout)

        self.siPlay = True
        self.is_white = True
        self.is_black = True

        if not self.show_board:
            self.board.hide()
        self.restore_video(dicVideo)
        self.ponFlags()

        self.engine = self.lanzaMotor()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.compruebaInput)
        self.timer.start(500)
        self.depth = 0
        self.veces = 0

    def takeback(self):
        nmoves = len(self.game)
        if nmoves:
            self.game.shrink(nmoves-2)
            self.reset()

    def compruebaInput(self):
        if not self.engine:
            return
        self.veces += 1
        if self.veces == 3:
            self.veces = 0
            if self.valid_to_play():
                mrm = self.engine.ac_estado()
                rm = mrm.rmBest()
                if rm and rm.depth > self.depth:
                    self.depth = rm.depth
                    if self.siCandidates:
                        self.li_moves = mrm.li_rm
                        self.lbDepth.set_text("%s: %d" % (_("Depth"), rm.depth))
                    else:
                        self.li_moves.insert(0, rm.copia())
                        if len(self.li_moves) > 256:
                            self.li_moves = self.li_moves[:128]

                    # TODO mirar si es de posicion previa o porterior
                    game = Game.Game(ini_posicion=self.game.last_position)
                    game.read_pv(rm.pv)
                    if len(game):
                        self.board.remove_arrows()
                        tipo = "mt"
                        opacity = 100
                        salto = (80 - 15) * 2 // (self.nArrows - 1) if self.nArrows > 1 else 1
                        cambio = max(30, salto)

                        for njg in range(min(len(game), self.nArrows)):
                            tipo = "ms" if tipo == "mt" else "mt"
                            move = game.move(njg)
                            self.board.creaFlechaMov(move.from_sq, move.to_sq, tipo + str(opacity))
                            if njg % 2 == 1:
                                opacity -= cambio
                                cambio = salto

                    self.grid.refresh()

                QTUtil.refresh_gui()

        self.cpu.compruebaInput()

    def change_options(self):
        self.pause()
        w = WindowKibitzers.WKibitzerLive(self, self.cpu.configuration, self.cpu.numkibitzer)
        if w.exec_():
            xprioridad = w.result_xprioridad
            if xprioridad is not None:
                pid = self.engine.pid()
                if Code.is_windows:
                    hp, ht, pid, dt = struct.unpack("PPII", pid.asstring(16))
                p = psutil.Process(pid)
                p.nice(xprioridad)
            if w.result_opciones:
                for opcion, valor in w.result_opciones:
                    if valor is None:
                        orden = "setoption name %s" % opcion
                    else:
                        if type(valor) == bool:
                            valor = str(valor).lower()
                        orden = "setoption name %s value %s" % (opcion, valor)
                    self.engine.put_line(orden)
        self.play()

    def ponFlags(self):
        flags = self.windowFlags()
        if self.siTop:
            flags |= QtCore.Qt.WindowStaysOnTopHint
        else:
            flags &= ~QtCore.Qt.WindowStaysOnTopHint
        flags |= QtCore.Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        self.tb.setAccionVisible(self.windowTop, not self.siTop)
        self.tb.setAccionVisible(self.windowBottom, self.siTop)
        self.show()

    def windowTop(self):
        self.siTop = True
        self.ponFlags()

    def windowBottom(self):
        self.siTop = False
        self.ponFlags()

    def terminar(self):
        self.finalizar()
        self.accept()

    def pause(self):
        self.siPlay = False
        self.tb.setPosVisible(1, True)
        self.tb.setPosVisible(2, False)
        self.stop()

    def play(self):
        self.siPlay = True
        self.tb.setPosVisible(1, False)
        self.tb.setPosVisible(2, True)
        self.reset()

    def stop(self):
        self.engine.ac_final(0)

    def grid_num_datos(self, grid):
        return len(self.li_moves)

    def grid_dato(self, grid, row, o_column):
        rm = self.li_moves[row]
        key = o_column.key
        if key == "EVALUATION":
            return rm.abrTexto()

        elif key == "BESTMOVE":
            p = Game.Game(ini_posicion=self.game.last_position)
            p.read_pv(rm.pv)
            pgn = p.pgnBaseRAW() if self.with_figurines else p.pgn_translated()
            li = pgn.split(" ")
            resp = ""
            if li:
                if ".." in li[0]:
                    if len(li) > 1:
                        resp = li[1]
                else:
                    resp = li[0].lstrip("1234567890.")
            if self.with_figurines:
                is_white = self.game.last_position.is_white
                return resp, is_white, None, None, None, None, False, True
            else:
                return resp

        elif key == "DEPTH":
            return "%d" % rm.depth

        else:
            p = Game.Game(ini_posicion=self.game.last_position)
            p.read_pv(rm.pv)
            li = p.pgn_translated().split(" ")
            if ".." in li[0]:
                li = li[1:]
            return " ".join(li[1:])

    def grid_doble_click(self, grid, row, o_column):
        if 0 <= row < len(self.li_moves):
            rm = self.li_moves[row]
            self.game.read_pv(rm.movimiento())
            self.reset()

    def grid_bold(self, grid, row, o_column):
        return o_column.key in ("EVALUATION", "BESTMOVE", "DEPTH")

    def lanzaMotor(self):
        if self.siCandidates:
            self.numMultiPV = self.kibitzer.current_multipv()
            if self.numMultiPV <= 1:
                self.numMultiPV = min(self.kibitzer.maxMultiPV, 20)
        else:
            self.numMultiPV = 0

        self.nom_engine = self.kibitzer.name
        exe = self.kibitzer.path_exe
        args = self.kibitzer.args
        li_uci = self.kibitzer.liUCI
        return EngineRun.RunEngine(self.nom_engine, exe, li_uci, self.numMultiPV, priority=self.cpu.prioridad, args=args)

    def closeEvent(self, event):
        self.finalizar()

    def valid_to_play(self):
        siw = self.game.last_position.is_white
        if not self.siPlay or (siw and not self.is_white) or (not siw and not self.is_black):
            return False
        return True

    def color(self):
        menu = QTVarios.LCMenu(self)
        menu.opcion("blancas", _("White"), siChecked=self.is_white)
        menu.opcion("negras", _("Black"), siChecked=self.is_black)
        resp = menu.lanza()
        if resp:
            if resp == "blancas":
                self.is_white = not self.is_white
            elif resp == "negras":
                self.is_black = not self.is_black
            self.reset()

    def finalizar(self):
        self.save_video()
        if self.engine:
            self.engine.ac_final(0)
            self.engine.close()
            self.engine = None
            self.siPlay = False

    def portapapelesJugSelected(self):
        if self.li_moves:
            n = self.grid.recno()
            if n < 0 or n >= len(self.li_moves):
                n = 0
            rm = self.li_moves[n]
            fen = self.game.last_position.fen()
            p = Game.Game(fen=fen)
            p.read_pv(rm.pv)
            jg0 = p.move(0)
            jg0.comment = rm.abrTextoPDT() + " " + self.nom_engine
            pgn = p.pgnBaseRAW()
            resp = '["FEN", "%s"]\n\n%s' % (fen, pgn)
            QTUtil.ponPortapapeles(resp)
            QTUtil2.mensajeTemporal(self, _("The line selected is saved to the clipboard"), 0.7)

    def save_video(self):
        dic = {}

        pos = self.pos()
        dic["_POSICION_"] = "%d,%d" % (pos.x(), pos.y())

        tam = self.size()
        dic["_SIZE_"] = "%d,%d" % (tam.width(), tam.height())

        dic["SHOW_BOARD"] = self.show_board
        dic["NARROWS"] = self.nArrows

        dic["SITOP"] = self.siTop

        self.grid.save_video(dic)

        self.cpu.save_video(dic)

    def restore_video(self, dicVideo):
        if dicVideo:
            wE, hE = QTUtil.tamEscritorio()
            x, y = dicVideo["_POSICION_"].split(",")
            x = int(x)
            y = int(y)
            if not (0 <= x <= (wE - 50)):
                x = 0
            if not (0 <= y <= (hE - 50)):
                y = 0
            self.move(x, y)
            if not ("_SIZE_" in dicVideo):
                w, h = self.width(), self.height()
                for k in dicVideo:
                    if k.startswith("_TAMA"):
                        w, h = dicVideo[k].split(",")
            else:
                w, h = dicVideo["_SIZE_"].split(",")
            w = int(w)
            h = int(h)
            if w > wE:
                w = wE
            elif w < 20:
                w = 20
            if h > hE:
                h = hE
            elif h < 20:
                h = 20
            self.resize(w, h)

    def orden_game(self, game: Game.Game):
        posicion = game.last_position

        is_white = posicion.is_white

        self.board.set_position(posicion)
        self.board.activate_side(is_white)

        self.stop()

        self.game = game
        self.depth = 0
        self.li_moves = []

        if self.valid_to_play():
            self.engine.ac_inicio(game)
        self.grid.refresh()

    def config_board(self):
        self.show_board = not self.show_board
        self.board.setVisible(self.show_board)
        self.save_video()

    def set_position(self):
        resp = Voyager.voyager_position(self, self.game.last_position)
        if resp is not None:
            game = Game.Game(ini_posicion=resp)
            self.orden_game(game)

    def mensajero(self, from_sq, to_sq, promocion=""):
        FasterCode.set_fen(self.game.last_position.fen())
        if FasterCode.make_move(from_sq + to_sq + promocion):
            self.game.read_pv(from_sq + to_sq + promocion)
            self.reset()

    def reset(self):
        self.orden_game(self.game)
