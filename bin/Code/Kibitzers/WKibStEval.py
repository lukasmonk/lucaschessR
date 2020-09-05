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

        dicVideo = self.cpu.dic_video
        if not dicVideo:
            dicVideo = {}

        self.siTop = dicVideo.get("SITOP", True)
        self.siShowBoard = dicVideo.get("SHOW_BOARD", True)
        self.position = Position.Position()

        self.fen = ""
        self.almFEN = {}
        self.siPlay = True
        self.is_white = True
        self.siNegras = True

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
            (_("Quit"), Iconos.Kibitzer_Terminar(), self.terminar),
            (_("Continue"), Iconos.Kibitzer_Continuar(), self.play),
            (_("Pause"), Iconos.Kibitzer_Pausa(), self.pause),
            (_("Board"), Iconos.Board(), self.config_board),
            ("%s: %s" % (_("Enable"), _("window on top")), Iconos.Top(), self.windowTop),
            ("%s: %s" % (_("Disable"), _("window on top")), Iconos.Bottom(), self.windowBottom),
        )
        self.tb = Controles.TBrutina(self, li_acciones, with_text=False, icon_size=16)
        self.tb.setAccionVisible(self.play, False)

        ly1 = Colocacion.H().control(self.tb)
        ly2 = Colocacion.V().otro(ly1).control(self.em)

        layout = Colocacion.H().control(self.board).otro(ly2)
        self.setLayout(layout)

        self.engine = self.lanzaMotor()

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.cpu.compruebaInput)
        self.timer.start(200)

        if not self.siShowBoard:
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
        self.ponFen(self.fen)

    def stop(self):
        self.siPlay = False
        self.engine.ac_final(0)

    def closeEvent(self, event):
        self.finalizar()

    def siAnalizar(self):
        siW = " w " in self.fen
        if not self.siPlay or (siW and (not self.is_white)) or ((not siW) and (not self.siNegras)):
            return False
        return True

    def color(self):
        menu = QTVarios.LCMenu(self)
        menu.opcion("blancas", _("White"), Iconos.PuntoNaranja())
        menu.opcion("negras", _("Black"), Iconos.PuntoNegro())
        menu.opcion("blancasnegras", "%s + %s" % (_("White"), _("Black")), Iconos.PuntoVerde())
        resp = menu.lanza()
        if resp:
            self.siNegras = True
            self.is_white = True
            if resp == "blancas":
                self.siNegras = False
            elif resp == "negras":
                self.is_white = False
            if self.siAnalizar():
                self.ponFen(self.fen)

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

        dic["SHOW_BOARD"] = self.siShowBoard

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
        self.pause()
        menu = QTVarios.LCMenu(self)
        if self.siShowBoard:
            menu.opcion("hide", _("Hide"), Iconos.PuntoNaranja())
        else:
            menu.opcion("show", _("Show"), Iconos.PuntoNaranja())
        resp = menu.lanza()
        if resp:
            if resp == "hide":
                self.siShowBoard = False
                self.board.hide()
            elif resp == "show":
                self.siShowBoard = True
                self.board.show()
            self.save_video()
        self.play()

    def lanzaMotor(self):
        confMotor = self.cpu.configMotor
        self.nom_engine = confMotor.name
        exe = confMotor.ejecutable()
        args = confMotor.argumentos()
        liUCI = confMotor.liUCI
        return EngineRun.RunEngine(self.nom_engine, exe, liUCI, 0, priority=self.cpu.prioridad, args=args)

    def ponFen(self, fen):
        txt = ""
        if fen:
            position = Position.Position()
            position.read_fen(fen)
            self.board.set_position(position)
            if self.fen and fen != self.fen:
                txt = self.em.texto()
                if self.fen and txt:
                    self.almFEN[self.fen] = txt

            self.fen = fen
            if fen in self.almFEN:
                txt = self.almFEN[fen]
            elif self.siAnalizar():
                self.engine.set_fen_position(fen)
                self.engine.put_line("eval")
                li, ok = self.engine.wait_list(":", 2000)
                while li and li[-1] == "\n":
                    li = li[:-1]
                if ok:
                    txt = "".join(li)

        self.em.set_text(txt)
