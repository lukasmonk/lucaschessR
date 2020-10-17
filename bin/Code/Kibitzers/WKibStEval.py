from PySide2 import QtCore, QtGui, QtWidgets

import Code
from Code.Base import Position
from Code.Engines import EngineRun
from Code.QT import Colocacion
from Code.QT import Controles
from Code.QT import Iconos
from Code.QT import Piezas
from Code.QT import QTUtil
from Code.QT import QTVarios
from Code.Board import Board
from Code.QT import Delegados


class WStEval(QtWidgets.QDialog):
    def __init__(self, cpu):
        QtWidgets.QDialog.__init__(self)

        self.cpu = cpu

        self.kibitzer = cpu.kibitzer

        dicVideo = self.cpu.dic_video
        if not dicVideo:
            dicVideo = {}

        self.siTop = dicVideo.get("SITOP", True)
        self.show_board = dicVideo.get("SHOW_BOARD", True)
        self.position = Position.Position()

        self.game = None
        self.siPlay = True
        self.is_white = True
        self.is_black = True

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
        Delegados.generaPM(self.board.piezas)

        self.em = Controles.EM(self, siHTML=False).read_only()
        f = Controles.TipoLetra(name="Courier New", puntos=10)
        self.em.ponFuente(f)

        li_acciones = (
            (_("Quit"), Iconos.Kibitzer_Close(), self.terminar),
            (_("Continue"), Iconos.Kibitzer_Play(), self.play),
            (_("Pause"), Iconos.Kibitzer_Pause(), self.pause),
            (_("Show/hide board"), Iconos.Kibitzer_Board(), self.config_board),
            ("%s: %s" % (_("Enable"), _("window on top")), Iconos.Top(), self.windowTop),
            ("%s: %s" % (_("Disable"), _("window on top")), Iconos.Bottom(), self.windowBottom),
        )
        self.tb = Controles.TBrutina(self, li_acciones, with_text=False, icon_size=24)
        self.tb.setAccionVisible(self.play, False)

        ly1 = Colocacion.H().control(self.board).control(self.em).margen(3)
        layout = Colocacion.V().control(self.tb).espacio(-10).otro(ly1).margen(3)
        self.setLayout(layout)

        self.engine = self.lanzaMotor()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.cpu.compruebaInput)
        self.timer.start(200)

        if not self.show_board:
            self.board.hide()
        self.restore_video(dicVideo)
        self.ponFlags()

    def ponFlags(self):
        if self.siTop:
            flags = self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint
        else:
            flags = self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | flags)
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
        self.reset()

    def stop(self):
        self.siPlay = False
        self.engine.ac_final(0)

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
                self.reset()

    def finalizar(self):
        self.save_video()
        if self.engine:
            self.engine.close()
            self.engine = None
            self.siPlay = False

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

    def lanzaMotor(self):
        self.numMultiPV = self.kibitzer.multiPV

        self.nom_engine = self.kibitzer.name
        exe = self.kibitzer.path_exe
        args = self.kibitzer.args
        li_uci = self.kibitzer.liUCI
        return EngineRun.RunEngine(self.nom_engine, exe, li_uci, self.numMultiPV, priority=self.cpu.prioridad, args=args)

    def orden_game(self, game):
        txt = ""
        self.game = game
        if game:
            position = game.last_position
            self.board.set_position(position)
            if self.if_to_analyze():
                self.engine.set_fen_position(position.fen())
                self.engine.put_line("eval")
                li, ok = self.engine.wait_list(":", 2000)
                while li and li[-1] == "\n":
                    li = li[:-1]
                if ok:
                    txt = "".join(li)

        self.em.set_text(txt)

    def reset(self):
        self.orden_game(self.game)

