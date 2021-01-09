import collections
import os
import time

from PySide2 import QtCore, QtGui, QtWidgets

import Code
from Code.SQL import UtilSQL
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code.Board import BoardElements, BoardTypes
from Code.Sound import Sound
from Code import TrListas
from Code import Util


class MesaSonido(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        QtWidgets.QGraphicsView.__init__(self)

        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setTransformationAnchor(self.NoAnchor)
        self.escena = QtWidgets.QGraphicsScene(self)
        self.escena.setItemIndexMethod(self.escena.NoIndex)
        self.setScene(self.escena)

        self.main_window = parent
        self.crea()

    def crea(self):
        # base
        cajon = BoardTypes.Caja()
        cajon.physical_pos.orden = 1
        cajon.colorRelleno = 4294243572
        ancho, alto = 544, 100
        cajon.physical_pos.ancho, cajon.physical_pos.alto = ancho, alto
        cajon.physical_pos.x, cajon.physical_pos.y = 0, 0
        cajon.tipo = QtCore.Qt.NoPen

        self.cajonSC = BoardElements.CajaSC(self.escena, cajon)

        def tiempoSC(x, y, linea, minim, maxim, rutina, color):
            tt = BoardTypes.Texto()
            tt.tipoLetra = BoardTypes.TipoLetra("Courier New", 10)
            tt.physical_pos.ancho = 68
            tt.physical_pos.alto = 12
            tt.physical_pos.orden = 5
            tt.colorFondo = color
            tt.valor = "00:00:00"
            tt.physical_pos.x = x
            tt.physical_pos.y = y
            tt.linea = linea
            tt.min = x + minim
            tt.max = x + maxim
            tt.rutina = rutina
            sc = BoardElements.TiempoSC(self.escena, tt)
            sc.ponCentesimas(0)
            return sc

        self.txtInicio = tiempoSC(2, 40, "d", 0, 400, self.mv_inicio, 4294242784)
        self.txtFinal = tiempoSC(ancho - 6 - 68, 40, "i", -400, 0, self.mv_final, 4294242784)
        self.txtActual = tiempoSC(68 + 2, 10, "a", 0, 400, None, 4294242784)
        self.txtDuracion = tiempoSC(236, 78, None, 0, 0, None, 4289509046)

        tf = BoardTypes.Caja()
        tf.physical_pos.orden = 2
        tf.physical_pos.x = 70
        tf.physical_pos.y = 44
        tf.physical_pos.ancho = 400
        tf.physical_pos.alto = 4
        tf.grosor = 0
        tf.colorRelleno = 4281413888
        self.linMain = BoardElements.CajaSC(self.escena, tf)

        tf = BoardTypes.Caja()
        tf.physical_pos.orden = 2
        tf.physical_pos.x = 70
        tf.physical_pos.y = 32
        tf.physical_pos.ancho = 0
        tf.physical_pos.alto = 26
        tf.colorRelleno = 4281413888
        BoardElements.CajaSC(self.escena, tf)

        tf = BoardTypes.Caja()
        tf.physical_pos.orden = 2
        tf.physical_pos.x = 470
        tf.physical_pos.y = 32
        tf.physical_pos.ancho = 0
        tf.physical_pos.alto = 26
        tf.colorRelleno = 4281413888
        BoardElements.CajaSC(self.escena, tf)

        self.setFixedSize(ancho, alto)

    def mv_inicio(self, posx):
        self.txtFinal.minimo = self.txtFinal.inicialx - 400 + posx
        self.txtActual.minimo = self.txtActual.inicialx + posx
        self.txtActual.compruebaPos()

        self.txtDuracion.ponCentesimas(self.txtFinal.calcCentesimas() - self.txtInicio.calcCentesimas())

    def mv_final(self, posx):
        self.txtInicio.maximo = self.txtInicio.inicialx + 400 + posx
        self.txtActual.maximo = self.txtActual.inicialx + 400 + posx
        self.txtActual.compruebaPos()

        self.txtDuracion.ponCentesimas(self.txtFinal.calcCentesimas() - self.txtInicio.calcCentesimas())

    def ponCentesimas(self, centesimas):
        for x in (self.txtActual, self.txtDuracion, self.txtFinal, self.txtInicio):
            x.ponCentesimas(centesimas)
            if centesimas == 0:
                x.posInicial()
        self.escena.update()

    def ponCentesimasActual(self, centesimas):
        self.txtActual.setphysical_pos(centesimas)
        self.escena.update()

    def limites(self, siTotal):
        to_sq = self.txtFinal.calcCentesimas()
        if siTotal:
            from_sq = self.txtInicio.calcCentesimas()
        else:
            from_sq = self.txtActual.calcCentesimas()
        return from_sq, to_sq

    def siHayQueRecortar(self):
        return self.txtInicio.siMovido() or self.txtFinal.siMovido()

    def activaEdicion(self, siActivar):
        for x in (self.txtActual, self.txtFinal, self.txtInicio):
            x.activa(siActivar)


class WEdicionSonido(QTVarios.WDialogo):
    ks_aceptar, ks_cancelar, ks_microfono, ks_wav, ks_play, ks_stopplay, ks_stopmic, ks_record, ks_cancelmic, ks_limpiar, ks_grabar = range(
        11
    )

    def __init__(self, owner, titulo, wav=None, maxTime=None, name=None):

        # titulo = _("Sound edition" )
        icono = Iconos.S_Play()
        extparam = "sound"
        QTVarios.WDialogo.__init__(self, owner, titulo, icono, extparam)

        self.confich = Code.configuration.ficheroDirSound

        # toolbar
        self.tb = QtWidgets.QToolBar("BASIC", self)
        self.tb.setIconSize(QtCore.QSize(32, 32))
        self.tb.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.prepare_toolbar()

        # Nombre
        siNombre = name is not None
        if siNombre:
            lbNom = Controles.LB(self, _("Name") + ":")
            self.edNom = Controles.ED(self, name).anchoMinimo(180)
            lyNom = Colocacion.H().control(lbNom).control(self.edNom).relleno()

        # MesaSonido
        self.mesa = MesaSonido(self)
        self.taller = Sound.TallerSonido(wav)

        self.mesa.ponCentesimas(self.taller.centesimas)

        self.maxTime = maxTime if maxTime else 300.0  # segundos=5 minutos

        layout = Colocacion.V().control(self.tb)
        if siNombre:
            layout.otro(lyNom)
        layout.control(self.mesa).margen(3)

        self.setLayout(layout)

        self.ponBaseTB()

        self.restore_video(siTam=False)

    def name(self):  # Para los guiones
        return self.edNom.texto()

    def closeEvent(self, event):  # Cierre con X
        self.siGrabando = False
        self.is_canceled = True
        self.save_video()

    def ponBaseTB(self):
        li = [self.ks_aceptar, self.ks_cancelar, None]
        if self.taller.siDatos():
            li.extend([self.ks_limpiar, None, self.ks_play, None, self.ks_grabar])
            self.mesa.activaEdicion(True)
        else:
            li.extend([self.ks_microfono, None, self.ks_wav])
            self.mesa.activaEdicion(False)
        self.pon_toolbar(li)

    def prepare_toolbar(self):

        self.dic_toolbar = {}

        li_options = (
            (_("Accept"), Iconos.S_Aceptar(), self.ks_aceptar),
            (_("Cancel"), Iconos.S_Cancelar(), self.ks_cancelar),
            (_("Recording Mic"), Iconos.S_Microfono(), self.ks_microfono),
            (_("Read wav"), Iconos.S_LeerWav(), self.ks_wav),
            (_("Listen"), Iconos.S_Play(), self.ks_play),
            (_("End"), Iconos.S_StopPlay(), self.ks_stopplay),
            (_("End"), Iconos.S_StopMicrofono(), self.ks_stopmic),
            (_("Begin"), Iconos.S_Record(), self.ks_record),
            (_("Cancel"), Iconos.S_Cancelar(), self.ks_cancelmic),
            (_("Delete"), Iconos.S_Limpiar(), self.ks_limpiar),
            (_("Save wav"), Iconos.Grabar(), self.ks_grabar),
        )

        for titulo, icono, key in li_options:
            accion = QtWidgets.QAction(titulo, None)
            accion.setIcon(icono)
            accion.setIconText(titulo)
            accion.triggered.connect(self.procesaTB)
            accion.key = key
            self.dic_toolbar[key] = accion

    def pon_toolbar(self, li_acciones):

        self.tb.clear()
        for k in li_acciones:
            if k is None:
                self.tb.addSeparator()
            else:
                self.dic_toolbar[k].setVisible(True)
                self.dic_toolbar[k].setEnabled(True)
                self.tb.addAction(self.dic_toolbar[k])

        self.tb.li_acciones = li_acciones
        self.tb.update()

    def habilitaTB(self, kopcion, siHabilitar):
        self.dic_toolbar[kopcion].setEnabled(siHabilitar)

    def procesaTB(self):
        accion = self.sender().key
        if accion == self.ks_aceptar:
            if self.mesa.siHayQueRecortar():
                from_sq, to_sq = self.mesa.limites(True)
                self.taller.recorta(from_sq, to_sq)
            self.wav = self.taller.wav
            self.centesimas = self.taller.centesimas
            self.accept()
            self.save_video()
            return
        elif accion == self.ks_cancelar:
            self.reject()
            return

        elif accion == self.ks_limpiar:
            self.limpiar()

        elif accion == self.ks_microfono:
            self.microfono()
        elif accion == self.ks_cancelmic:
            self.siGrabando = False
            self.is_canceled = True
            self.ponBaseTB()

        elif accion == self.ks_record:
            self.micRecord()
        elif accion == self.ks_stopmic:
            self.siGrabando = False
        elif accion == self.ks_wav:
            self.wav()
        elif accion == self.ks_grabar:
            self.grabar()
        elif accion == self.ks_play:
            self.play()
        elif accion == self.ks_stopplay:
            self.siPlay = False

    def microfono(self):
        self.pon_toolbar((self.ks_cancelmic, None, self.ks_record))

    def micRecord(self):
        self.pon_toolbar((self.ks_cancelmic, None, self.ks_stopmic))
        self.siGrabando = True
        self.is_canceled = False

        self.mesa.ponCentesimas(0)

        self.taller.micInicio()

        iniTime = time.time()

        while self.siGrabando:
            self.taller.micGraba()
            QTUtil.refresh_gui()
            t = time.time() - iniTime
            self.mesa.ponCentesimas(t * 100)
            if t > self.maxTime:
                break

        self.siGrabando = False
        self.taller.micFinal()
        if self.is_canceled:
            self.taller.limpiar()
            self.mesa.ponCentesimas(0)
        else:
            self.mesa.ponCentesimas(self.taller.centesimas)

        self.ponBaseTB()

    def limpiar(self):
        self.taller.limpiar()
        self.mesa.ponCentesimas(0)
        self.ponBaseTB()

    def wav(self):
        carpeta = Util.restore_pickle(self.confich)
        file = QTUtil2.leeFichero(self, carpeta, "wav")
        if file:
            carpeta = os.path.dirname(file)
            Util.save_pickle(self.confich, carpeta)
            if self.taller.leeWAV(file):
                self.mesa.ponCentesimas(self.taller.centesimas)
            else:
                QTUtil2.message_error(self, _("It is impossible to read this file, it is not compatible."))
            self.ponBaseTB()

    def grabar(self):
        carpeta = Util.restore_pickle(self.confich)
        filtro = _("File") + " wav (*.wav)"
        file = QTUtil2.salvaFichero(self, _("Save wav"), carpeta, filtro, siConfirmarSobreescritura=True)
        if file:
            carpeta = os.path.dirname(file)
            Util.save_pickle(self.confich, carpeta)
            f = open(file, "wb")
            f.write(self.taller.wav)
            f.close()
            self.ponBaseTB()

    def play(self):
        self.mesa.activaEdicion(False)
        self.pon_toolbar((self.ks_stopplay,))

        centDesde, centHasta = self.mesa.limites(False)
        self.taller.playInicio(centDesde, centHasta)

        self.siPlay = True

        while self.siPlay:
            siSeguir, centActual = self.taller.play()
            if siSeguir:
                self.mesa.ponCentesimasActual(centActual)
                QTUtil.refresh_gui()
            else:
                self.mesa.ponCentesimasActual(centDesde)
                QTUtil.refresh_gui()
                break

        self.siPlay = False

        self.taller.playFinal()

        self.ponBaseTB()


def editSonido(owner, titulo, wav):
    w = WEdicionSonido(owner, titulo, wav)
    if w.exec_():
        return w.wav, w.centesimas
    else:
        return None


class WSonidos(QTVarios.WDialogo):
    def __init__(self, procesador):

        self.procesador = procesador

        self.db = UtilSQL.DictSQL(procesador.configuration.file_sounds(), "general")
        self.creaListaSonidos()

        titulo = _("Custom sounds")
        icono = Iconos.S_Play()
        extparam = "sounds"
        QTVarios.WDialogo.__init__(self, procesador.main_window, titulo, icono, extparam)

        # Toolbar
        li_acciones = (
            (_("Close"), Iconos.MainMenu(), "terminar"),
            None,
            (_("Modify"), Iconos.Modificar(), "modificar"),
            None,
            (_("Listen"), Iconos.S_Play(), "play"),
        )
        tb = Controles.TB(self, li_acciones)

        # Lista
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("SONIDO", _("Sound"), 300, centered=True)
        o_columns.nueva("DURACION", _("Duration"), 60, centered=True)

        self.grid = Grid.Grid(self, o_columns, siSelecFilas=True)

        # Layout
        layout = Colocacion.V().control(tb).control(self.grid).margen(3)
        self.setLayout(layout)

        self.grid.gotop()
        self.grid.setFocus()

        self.siPlay = False

        self.register_grid(self.grid)

        if not self.restore_video():
            self.resize(self.grid.anchoColumnas() + 30, 600)

    def closeEvent(self, event):
        self.save_video()

    def process_toolbar(self):
        self.siPlay = False
        accion = self.sender().key
        if accion == "terminar":
            self.save_video()
            self.accept()
            self.db.close()

        elif accion == "modificar":
            self.grid_doble_click(None, self.grid.recno(), None)

        elif accion == "play":
            self.play()

    def grid_num_datos(self, grid):
        return len(self.liSonidos)

    def grid_doble_click(self, grid, row, o_column):
        self.siPlay = False

        cl = self.liSonidos[row][0]
        if cl is None:
            return

        wav = self.db[cl]

        resp = editSonido(self, self.liSonidos[row][1], wav)
        if resp is not None:
            wav, cent = resp
            if wav is None:
                self.liSonidos[row][2] = None
                del self.db[cl]
            else:
                self.db[cl] = wav
                self.liSonidos[row][2] = cent
            self.grid.refresh()

    def grid_dato(self, grid, row, o_column):
        key = o_column.key
        li = self.liSonidos[row]
        if key == "DURACION":
            if li[0] is None:
                return ""
            else:
                t = li[2]
                if t is None:

                    wav = self.db[li[0]]
                    if wav is None:
                        t = 0
                    else:
                        ts = Sound.TallerSonido(wav)
                        t = ts.centesimas
                return "%02d:%02d:%02d" % Sound.msc(t)

        else:
            return li[1]

    def play(self):
        li = self.liSonidos[self.grid.recno()]
        if li[0]:
            wav = self.db[li[0]]
            if wav is not None:
                ts = Sound.TallerSonido(wav)
                ts.playInicio(0, ts.centesimas)
                self.siPlay = True
                while self.siPlay:
                    siSeguir, pos = ts.play()
                    if not siSeguir:
                        break
                ts.playFinal()

    def grid_color_fondo(self, grid, row, o_column):
        li = self.liSonidos[row]
        if li[0] is None:
            return QTUtil.qtColor(4294836181)
        else:
            return None

    def creaListaSonidos(self):

        self.liSonidos = [["MC", _("After rival move"), None]]

        # self.liSonidos.append( [ None, "", None ] )
        self.liSonidos.append([None, "- " + _("Results") + " -", None])

        d = collections.OrderedDict()
        d["GANAMOS"] = _("You win")
        d["GANARIVAL"] = _("Opponent wins")
        d["TABLAS"] = _("Stalemate")
        d["TABLASREPETICION"] = _("Draw due to three times repetition")
        d["TABLAS50"] = _("Draw according to the 50 move rule")
        d["TABLASFALTAMATERIAL"] = _("Draw, not enough material")
        d["GANAMOSTIEMPO"] = _("You win on time")
        d["GANARIVALTIEMPO"] = _("Opponent has won on time")

        for c, tr in d.items():
            self.liSonidos.append([c, tr, None])

        # self.liSonidos.append( [ None, "", None ] )
        self.liSonidos.append([None, "- " + _("Rival moves") + " -", None])

        for c in "abcdefgh12345678":
            self.liSonidos.append([c, c, None])

        for c in "KQRBNP":
            t = TrListas.letterPiece(c)
            self.liSonidos.append([c, t, None])

        for c in ("O-O", "O-O-O", "=", "x", "#", "+"):
            self.liSonidos.append([c, c, None])

        self.liSonidos.append([None, "", None])
        self.liSonidos.append(["ZEITNOT", _("Zeitnot"), None])

        # for c in "abcdefgh":
        # for f in "12345678":
        # self.liSonidos.append( [ c+f, c+f, None ] )


class WSonidosGuion(QTVarios.WDialogo):
    def __init__(self, owner, db):

        self.db = db

        self.liSonidos = owner.listaSonidos()

        titulo = _("Custom sounds")
        icono = Iconos.S_Play()
        extparam = "sounds"
        QTVarios.WDialogo.__init__(self, owner, titulo, icono, extparam)

        # Toolbar
        li_acciones = (
            (_("Close"), Iconos.MainMenu(), "terminar"),
            None,
            (_("New"), Iconos.Nuevo(), "nuevo"),
            (_("Modify"), Iconos.Modificar(), "modificar"),
            None,
            (_("Remove"), Iconos.Borrar(), "borrar"),
            None,
            (_("Up"), Iconos.Arriba(), "arriba"),
            (_("Down"), Iconos.Abajo(), "abajo"),
            None,
            (_("Listen"), Iconos.S_Play(), "play"),
        )
        tb = Controles.TB(self, li_acciones)

        # Lista
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("NOMBRE", _("Sound"), 300, centered=True)
        o_columns.nueva("DURACION", _("Duration"), 60, centered=True)

        self.grid = Grid.Grid(self, o_columns, siSelecFilas=True)

        # Layout
        layout = Colocacion.V().control(tb).control(self.grid).margen(3)
        self.setLayout(layout)

        self.grid.gotop()
        self.grid.setFocus()

        self.siPlay = False

        self.register_grid(self.grid)

        if not self.restore_video():
            self.resize(self.grid.anchoColumnas() + 30, 600)

    def closeEvent(self, event):
        self.save_video()

    def grid_num_datos(self, grid):
        return len(self.liSonidos)

    def process_toolbar(self):
        accion = self.sender().key
        eval("self.%s()" % accion)

    def terminar(self):
        self.save_video()
        self.accept()

    def modificar(self):
        pass
        # self.grid_doble_click( None, self.grid.recno(), None )

    def nuevo(self):
        wav = None
        name = ""
        while True:
            w = WEdicionSonido(self, _("New"), wav=wav, maxTime=600000, name=name)
            resp = w.exec_()
            if resp:
                centesimas = w.centesimas
                if not centesimas:
                    return
                name = w.name().strip()
                if not name:
                    QTUtil2.message_error(self, _("Name missing"))
                    continue

                reg = Util.Record()
                reg.name = name
                reg.centesimas = centesimas
                reg.id = Util.new_id()
                reg.wav = w.wav
                reg.ordenVista = (self.liSonidos[-1].ordenVista + 1) if self.liSonidos else 1
                self.db[reg.id] = reg
                self.liSonidos.append(reg)
                self.grid.refresh()
                return

    def grid_doble_click(self, grid, row, o_column):
        self.siPlay = False

        cl = self.db[row][0]
        if cl is None:
            return

        wav = self.db[cl]

        resp = editSonido(self, self.liSonidos[row][1], wav)
        if resp is not None:
            wav, cent = resp
            self.db[cl] = wav
            self.liSonidos[row][2] = cent
            self.grid.refresh()

    def grid_dato(self, grid, row, o_column):
        key = o_column.key
        reg = self.liSonidos[row]
        if key == "DURACION":
            return "%02d:%02d:%02d" % Sound.msc(reg.centesimas)
        elif key == "NOMBRE":
            return reg.name

    def play(self):
        if self.grid.recno() >= 0:
            reg = self.db[self.grid.recno()]
            wav = reg.wav
            ts = Sound.TallerSonido(wav)
            ts.playInicio(0, ts.centesimas)
            self.siPlay = True
            while self.siPlay:
                siSeguir, pos = ts.play()
                if not siSeguir:
                    break
            ts.playFinal()
