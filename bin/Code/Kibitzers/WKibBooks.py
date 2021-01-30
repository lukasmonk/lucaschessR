import FasterCode
from PySide2 import QtCore, QtGui, QtWidgets

import Code
from Code.Base import Position, Game
from Code.Polyglots import Books
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import Piezas
from Code.QT import QTUtil
from Code.QT import QTVarios
from Code.Board import Board
from Code.QT import Delegados
from Code.QT import Voyager


class WPolyglot(QtWidgets.QDialog):
    def __init__(self, cpu):
        QtWidgets.QDialog.__init__(self)

        self.cpu = cpu

        dicVideo = self.cpu.dic_video
        if not dicVideo:
            dicVideo = {}

        self.siTop = dicVideo.get("SITOP", True)
        self.show_board = dicVideo.get("SHOW_BOARD", True)
        self.position = Position.Position()

        self.game = None
        self.siPlay = True
        self.li_moves = []
        self.history = []

        self.setWindowTitle(cpu.titulo)
        self.setWindowIcon(Iconos.Book())

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
        Delegados.generaPM(self.board.piezas)

        self.book = Books.Book("P", cpu.kibitzer.name, cpu.kibitzer.path_exe, True)
        self.book.polyglot()

        self.with_figurines = cpu.configuration.x_pgn_withfigurines

        o_columns = Columnas.ListaColumnas()
        delegado = Delegados.EtiquetaPOS(True, siLineas=False) if self.with_figurines else None
        o_columns.nueva("MOVE", _("Move"), 80, centered=True, edicion=delegado)
        o_columns.nueva("PORC", "%", 60, centered=True)
        o_columns.nueva("WEIGHT", _("Weight"), 80, siDerecha=True)
        self.grid_moves = Grid.Grid(self, o_columns, dicVideo=dicVideo, siSelecFilas=True)

        li_acciones = (
            (_("Quit"), Iconos.Kibitzer_Close(), self.terminar),
            (_("Continue"), Iconos.Kibitzer_Play(), self.play),
            (_("Pause"), Iconos.Kibitzer_Pause(), self.pause),
            (_("Takeback"), Iconos.pmKibitzer_Back(), self.takeback),
            (_("Manual position"), Iconos.Kibitzer_Voyager(), self.set_position),
            (_("Show/hide board"), Iconos.Kibitzer_Board(), self.config_board),
            ("%s: %s" % (_("Enable"), _("window on top")), Iconos.Top(), self.windowTop),
            ("%s: %s" % (_("Disable"), _("window on top")), Iconos.Bottom(), self.windowBottom),
        )
        self.tb = Controles.TBrutina(self, li_acciones, with_text=False, icon_size=24)
        self.tb.setAccionVisible(self.play, False)

        ly1 = Colocacion.H().control(self.board).control(self.grid_moves)
        layout = Colocacion.V().control(self.tb).espacio(-8).otro(ly1).margen(3)
        self.setLayout(layout)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.cpu.compruebaInput)
        self.timer.start(500)

        if not self.show_board:
            self.board.hide()
        self.restore_video(dicVideo)
        self.ponFlags()

    def grid_doble_click(self, grid, row, o_column):
        if 0 <= row < len(self.li_moves):
            alm = self.li_moves[row]
            mov = alm.from_sq + alm.to_sq + alm.promotion
            self.game.read_pv(mov)
            self.reset()

    def grid_cambiado_registro(self, grid, row, o_column):
        self.ponFlecha(row)

    def ponFlecha(self, row):
        if -1 < row < len(self.li_moves):
            alm = self.li_moves[row]
            self.board.put_arrow_sc(alm.from_sq, alm.to_sq)

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

    def play(self):
        self.siPlay = True
        self.tb.setPosVisible(1, False)
        self.tb.setPosVisible(2, True)
        self.orden_game(self.game)

    def grid_num_datos(self, grid):
        return len(self.li_moves)

    def grid_dato(self, grid, row, o_column):
        alm = self.li_moves[row]

        # alm = Util.Record()
        # alm.from_sq, alm.to_sq, alm.promotion = pv[:2], pv[2:4], pv[4:]
        # alm.pgn = position.pgn_translated(alm.from_sq, alm.to_sq, alm.promotion)
        # alm.pgnRaw = position.pgn(alm.from_sq, alm.to_sq, alm.promotion)
        # alm.porc = "%0.02f%%" % (w * 100.0 / total,) if total else ""
        # alm.weight = w

        key = o_column.key
        if key == "MOVE":
            if self.with_figurines:
                is_white = self.game.last_position.is_white
                return alm.pgnRaw, is_white, None, None, None, None, False, True
            else:
                return alm.pgn
        elif key == "PORC":
            return alm.porc
        elif key == "WEIGHT":
            return "%d" % alm.weight

    def closeEvent(self, event):
        self.finalizar()

    def if_to_analyze(self):
        siW = self.game.last_position.is_white
        if not self.siPlay or (siW and (not self.is_white)) or ((not siW) and (not self.is_black)):
            return False
        return True

    def color(self):
        menu = QTVarios.LCMenu(self)
        menu.opcion("blancas", _("White"), Iconos.PuntoNaranja())
        menu.opcion("negras", _("Black"), Iconos.PuntoNegro())
        menu.opcion("blancasnegras", "%s + %s" % (_("White"), _("Black")), Iconos.PuntoVerde())
        resp = menu.lanza()
        if resp:
            self.is_black = True
            self.is_white = True
            if resp == "blancas":
                self.is_black = False
            elif resp == "negras":
                self.is_white = False
            if self.if_to_analyze():
                self.orden_game(self.game)

    def finalizar(self):
        self.save_video()

    def save_video(self):
        dic = {}

        pos = self.pos()
        dic["_POSICION_"] = "%d,%d" % (pos.x(), pos.y())

        tam = self.size()
        dic["_SIZE_"] = "%d,%d" % (tam.width(), tam.height())

        dic["SHOW_BOARD"] = self.show_board

        dic["SITOP"] = self.siTop

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

    def config_board(self):
        self.show_board = not self.show_board
        self.board.setVisible(self.show_board)
        self.save_video()

    def takeback(self):
        nmoves = len(self.game)
        if nmoves:
            self.game.shrink(nmoves-2)
            self.orden_game(self.game)

    def set_position(self):
        resp = Voyager.voyager_position(self, self.game.last_position)
        if resp is not None:
            game = Game.Game(ini_posicion=resp)
            self.orden_game(game)

    def orden_game(self, game):
        self.game = game
        if self.siPlay:

            position = game.last_position
            self.siW = position.is_white
            self.board.set_position(position)
            self.board.activate_side(self.siW)
            self.li_moves = self.book.almListaJugadas(position.fen())
            self.grid_moves.gotop()
            self.grid_moves.refresh()
            self.ponFlecha(0)

    def mensajero(self, from_sq, to_sq, promocion=""):
        FasterCode.set_fen(self.game.last_position.fen())
        if FasterCode.make_move(from_sq + to_sq + promocion):
            self.game.read_pv(from_sq + to_sq + promocion)
            self.reset()

    def reset(self):
        self.orden_game(self.game)
