import os.path
import time

from PySide2 import QtCore

from Code import BMT
from Code import ControlPGN
from Code import TrListas
from Code import Util
from Code.Analysis import Analysis
from Code.Base import Game, Position
from Code.Base.Constantes import *
from Code.Board import Board
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Delegados
from Code.QT import FormLayout
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios


class WHistorialBMT(QTVarios.WDialogo):
    def __init__(self, owner, dbf):

        # Variables
        self.procesador = owner.procesador
        self.configuration = owner.configuration

        # Datos ----------------------------------------------------------------
        self.dbf = dbf
        self.recnoActual = self.dbf.recno
        bmt_lista = Util.zip2var(dbf.leeOtroCampo(self.recnoActual, "BMT_LISTA"))
        self.liHistorial = Util.zip2var(dbf.leeOtroCampo(self.recnoActual, "HISTORIAL"))
        self.max_puntos = dbf.MAXPUNTOS

        if bmt_lista.is_finished():
            dic = {"FFINAL": dbf.FFINAL, "STATE": dbf.ESTADO, "PUNTOS": dbf.PUNTOS, "SEGUNDOS": dbf.SEGUNDOS}
            self.liHistorial.append(dic)

        # Dialogo ---------------------------------------------------------------
        icono = Iconos.Historial()
        titulo = _("Track record") + ": " + dbf.NOMBRE
        extparam = "bmthistorial"
        QTVarios.WDialogo.__init__(self, owner, titulo, icono, extparam)

        # Toolbar
        tb = QTVarios.LCTB(self)
        tb.new(_("Close"), Iconos.MainMenu(), self.terminar)

        # Lista
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("STATE", "", 26, edicion=Delegados.PmIconosBMT(), centered=True)
        o_columns.nueva("PUNTOS", _("Score"), 104, centered=True)
        o_columns.nueva("TIME", _("Time"), 80, centered=True)
        o_columns.nueva("FFINAL", _("End date"), 90, centered=True)

        self.grid = grid = Grid.Grid(self, o_columns, xid=False, siEditable=True)
        # n = grid.anchoColumnas()
        # grid.setMinimumWidth( n + 20 )
        self.register_grid(grid)

        # Colocamos ---------------------------------------------------------------
        ly = Colocacion.V().control(tb).control(self.grid)

        self.setLayout(ly)

        self.restore_video(siTam=True)

    def terminar(self):
        self.save_video()
        self.accept()

    def grid_num_datos(self, grid):
        return len(self.liHistorial)

    def grid_dato(self, grid, row, o_column):
        dic = self.liHistorial[row]
        col = o_column.key
        if col == "STATE":
            return dic["STATE"]

        elif col == "HECHOS":
            return "%d" % (dic["HECHOS"])

        elif col == "PUNTOS":
            p = dic["PUNTOS"]
            m = self.max_puntos
            porc = p * 100 / m
            return "%d/%d=%d" % (p, m, porc) + "%"

        elif col == "FFINAL":
            f = dic["FFINAL"]
            return "%s-%s-%s" % (f[6:], f[4:6], f[:4]) if f else ""

        elif col == "TIME":
            s = dic["SEGUNDOS"]
            if not s:
                s = 0
            m = s / 60
            s %= 60
            return "%d' %d\"" % (m, s) if m else '%d"' % s


class WEntrenarBMT(QTVarios.WDialogo):
    def __init__(self, owner, dbf):

        # Variables
        self.procesador = owner.procesador
        self.configuration = owner.configuration

        self.iniTiempo = None
        self.antTxtSegundos = ""
        self.pts_tolerance = 0

        self.game = Game.Game()
        self.siMostrarPGN = False

        self.position = Position.Position()
        self.actualP = 0  # Posicion actual

        self.game_type = GT_BMT
        self.controlPGN = ControlPGN.ControlPGN(self)

        self.state = None  # compatibilidad con ControlPGN
        self.human_is_playing = False  # compatibilidad con ControlPGN
        self.borrar_fen_lista = set()

        # Datos ----------------------------------------------------------------
        self.dbf = dbf
        self.recnoActual = self.dbf.recno
        x = dbf.leeOtroCampo(self.recnoActual, "BMT_LISTA")
        self.bmt_lista = Util.zip2var(dbf.leeOtroCampo(self.recnoActual, "BMT_LISTA"))
        self.bmt_lista.check_color()
        self.historial = Util.zip2var(dbf.leeOtroCampo(self.recnoActual, "HISTORIAL"))
        self.siTerminadaAntes = self.is_finished = self.bmt_lista.is_finished()
        self.timer = None
        self.datosInicio = self.bmt_lista.calc_thpse()

        # Dialogo ---------------------------------------------------------------
        icono = Iconos.BMT()
        titulo = dbf.NOMBRE
        extparam = "bmtentrenar"
        QTVarios.WDialogo.__init__(self, owner, titulo, icono, extparam)

        # Juegan ---------------------------------------------------------------
        self.lbJuegan = Controles.LB(self, "").set_foreground_backgound("white", "black").align_center()

        # Board ---------------------------------------------------------------
        config_board = self.configuration.config_board("BMT", 32)

        self.board = Board.Board(self, config_board)
        self.board.crea()
        self.board.set_dispatcher(self.player_has_moved)

        # Info -------------------------------------------------------------------
        colorFondo = QTUtil.qtColor(config_board.colorNegras())
        self.trPuntos = "<big><b>" + _("Score") + "<br>%s</b></big>"
        self.trSegundos = "<big><b>" + _("Time") + "<br>%s</b></big>"
        self.lbPuntos = Controles.LB(self, "").set_color_background(colorFondo).align_center().anchoMinimo(80)
        self.lbSegundos = Controles.LB(self, "").set_color_background(colorFondo).align_center().anchoMinimo(80)
        self.texto_lbPrimera = _("* indicates actual move played in game")
        self.ptsMejor = 0
        self.ptsPrimero = 0
        self.lbPrimera = Controles.LB(self, self.texto_lbPrimera)
        f = Controles.TipoLetra(puntos=8)
        self.lbCondiciones = Controles.LB(self, "").ponFuente(f)

        # Grid-PGN ---------------------------------------------------------------
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("NUMBER", _("N."), 35, centered=True)
        si_figurines_pgn = self.configuration.x_pgn_withfigurines
        o_columns.nueva("WHITE", _("White"), 100, edicion=Delegados.EtiquetaPGN(True if si_figurines_pgn else None))
        o_columns.nueva("BLACK", _("Black"), 100, edicion=Delegados.EtiquetaPGN(False if si_figurines_pgn else None))
        self.pgn = Grid.Grid(self, o_columns, siCabeceraMovible=False)
        nAnchoPgn = self.pgn.anchoColumnas() + 20
        self.pgn.setMinimumWidth(nAnchoPgn)

        self.pgn.setVisible(False)

        # BT posiciones ---------------------------------------------------------------
        self.liBT = []
        nSalto = (self.board.ancho + 34) // 26
        self.dicIconos = {
            0: Iconos.PuntoBlanco(),
            1: Iconos.PuntoNegro(),
            2: Iconos.PuntoAmarillo(),
            3: Iconos.PuntoNaranja(),
            4: Iconos.PuntoVerde(),
            5: Iconos.PuntoAzul(),
            6: Iconos.PuntoMagenta(),
            7: Iconos.PuntoRojo(),
            8: Iconos.PuntoEstrella(),
        }
        nfila = 0
        ncolumna = 0
        lyBT = Colocacion.G()
        number = 0
        nposic = len(self.bmt_lista)
        for x in range(nposic):
            bt = Controles.PB(self, str(x + 1), rutina=self.number).anchoFijo(36).altoFijo(20)
            bt.number = number
            number += 1
            estado = self.bmt_lista.state(x)
            bt.ponIcono(self.dicIconos[estado])
            self.liBT.append(bt)

            lyBT.controlc(bt, nfila, ncolumna)
            nfila += 1
            if nfila == nSalto:
                ncolumna += 1
                nfila = 0
        # if ncolumna == 0:
        lyBT = Colocacion.V().otro(lyBT).relleno()

        gbBT = Controles.GB(self, _("Positions"), lyBT)

        # Lista de RM max 16 ---------------------------------------------------------------
        self.liBTrm = []
        nfila = 0
        ncolumna = 0
        lyRM = Colocacion.G()
        number = 0
        for x in range(16):
            btRM = Controles.PB(self, "", rutina=self.pulsadoRM).anchoFijo(180).altoFijo(24).ponPlano(True)
            btRM.number = number
            btRM.setEnabled(False)
            number += 1
            self.liBTrm.append(btRM)
            lyRM.controlc(btRM, nfila, ncolumna)
            ncolumna += 1
            if ncolumna == 2:
                nfila += 1
                ncolumna = 0

        self.gbRM = Controles.GB(self, _("Moves"), lyRM)

        # Tool bar ---------------------------------------------------------------
        li_acciones = (
            (_("Close"), Iconos.MainMenu(), "terminar"),
            (_("Repeat"), Iconos.Pelicula_Repetir(), "repetir"),
            (_("Resign"), Iconos.Abandonar(), "abandonar"),
            (_("Remove"), Iconos.Borrar(), "borrar"),
            (_("Options"), Iconos.Opciones(), "opciones"),
            (_("Start"), Iconos.Empezar(), "empezar"),
            (_("Actual game"), Iconos.PartidaOriginal(), "original"),
            (_("Next"), Iconos.Siguiente(), "seguir"),
        )
        self.tb = Controles.TB(self, li_acciones)

        self.restore_video(siTam=False)

        # Colocamos ---------------------------------------------------------------
        lyPS = Colocacion.H().relleno().control(self.lbPuntos).relleno(2).control(self.lbSegundos).relleno()
        lyV = Colocacion.V().otro(lyPS).control(self.pgn).control(self.gbRM).control(self.lbPrimera)
        lyT = Colocacion.V().control(self.lbJuegan).control(self.board).control(self.lbCondiciones).relleno()
        lyTV = Colocacion.H().otro(lyT).otro(lyV).control(gbBT).margen(5)
        ly = Colocacion.V().control(self.tb).otro(lyTV).margen(2).relleno()

        self.setLayout(ly)

        if self.is_finished:
            self.empezar()
        else:
            self.pon_toolbar(["terminar", "empezar"])

        self.muestraControles(False)

    def muestraControles(self, si):
        for control in (self.lbJuegan, self.board, self.lbPuntos, self.lbSegundos, self.lbPrimera, self.lbCondiciones, self.pgn, self.gbRM):
            control.setVisible(si)

    def seguir(self):
        self.muestraControles(True)
        pos = self.actualP + 1
        if pos >= len(self.liBT):
            pos = 0
        self.buscaPrimero(pos)

    def opciones(self):
        # Se pide name y extra
        li_gen = [(None, None)]

        # # Nombre del entrenamiento
        li_gen.append((FormLayout.Editbox(_("Tolerance: How many centipawns below the best move are accepted"), tipo=int, ancho=50), self.pts_tolerance))

        titulo = "Training settings"
        resultado = FormLayout.fedit(li_gen, title=titulo, parent=self, anchoMinimo=560, icon=Iconos.Opciones())
        if not resultado:
            return
        accion, li_gen = resultado
        self.pts_tolerance = li_gen[0]

    def abandonar(self):
        self.bmt_uno.puntos = 0
        self.activaJugada(0)
        self.ponPuntos(0)
        self.pon_toolbar()

    def borrar(self):
        if QTUtil2.pregunta(self, _("Do you want to delete this position?")):
            self.borrar_fen_lista.add(self.bmt_uno.fen)
            QTUtil2.message(self, _("This position will be deleted on exit."))
            self.seguir()

    def process_toolbar(self):
        accion = self.sender().key
        if accion == "terminar":
            self.terminar()
            self.accept()
        elif accion == "seguir":
            self.seguir()
        elif accion == "abandonar":
            self.abandonar()
        elif accion == "borrar":
            self.borrar()
        elif accion == "repetir":
            self.muestraControles(True)
            self.repetir()
        elif accion == "empezar":
            self.muestraControles(True)
            self.empezar()
        elif accion == "original":
            self.original()
        elif accion == "opciones":
            self.opciones()

    def closeEvent(self, event):
        self.terminar()

    def empezar(self):
        self.buscaPrimero(0)
        self.ponPuntos(0)
        self.ponSegundos()
        self.set_clock()

    def terminar(self):
        self.finalizaTiempo()

        if len(self.borrar_fen_lista) > 0:
            self.bmt_lista.borrar_fen_lista(self.borrar_fen_lista)

        atotal, ahechos, at_puntos, at_segundos, at_estado = self.datosInicio

        total, hechos, t_puntos, t_segundos, t_estado = self.bmt_lista.calc_thpse()

        if (hechos != ahechos) or (t_puntos != at_puntos) or (t_segundos != at_segundos) or (t_estado != at_estado) or len(self.borrar_fen_lista) > 0:

            reg = self.dbf.baseRegistro()

            reg.BMT_LISTA = Util.var2zip(self.bmt_lista)

            reg.HECHOS = hechos
            reg.SEGUNDOS = t_segundos
            reg.PUNTOS = t_puntos
            # Si hay posiciones borradas, tenemos que actualizar TOTAL y MAXPUNTOS
            reg.TOTAL = len(self.bmt_lista)
            reg.MAXPUNTOS = self.bmt_lista.max_puntos()

            if self.historial:
                reg.HISTORIAL = Util.var2zip(self.historial)
                reg.REPE = len(reg.HISTORIAL)

            if self.is_finished:
                if not self.siTerminadaAntes:
                    reg.ESTADO = str(t_estado / total)
                    reg.FFINAL = Util.dtos(Util.today())

            self.dbf.modificarReg(self.recnoActual, reg)

        self.save_video()

    def repetir(self):
        # # Opcion de repetir solo las posiciones dificiles
        # Contamos las posiciones debajo un cierto state para el combobox

        num_pos_estate = {}
        for y in range(0, 9):
            num_pos_estate[y] = 0

        nposic = len(self.bmt_lista)
        for x in range(nposic):
            estado = self.bmt_lista.state(x)
            for y in range(0, 9):
                if estado < y:
                    num_pos_estate[y] += 1

        num_pos_estate[9] = nposic
        labels_score = {9: "Repeat all", 8: "Best move", 7: "Excellent", 6: "Very good", 5: "Good", 4: "Acceptable"}

        li_gen = [(None, None)]
        liJ = []

        for x in reversed(range(5, 10)):
            if num_pos_estate[x] > 0:
                label = "%s (%s)" % (labels_score[x], num_pos_estate[x])
                liJ.append((label, x))

        config = FormLayout.Combobox(_("Repeat only below score"), liJ)
        li_gen.append((config, 9))

        titulo = "%s" % (_("Do you want to repeat this training?"))
        resultado = FormLayout.fedit(li_gen, title=titulo, parent=self, anchoMinimo=560, icon=Iconos.Opciones())
        if not resultado:
            return

        accion, li_gen = resultado
        reiniciar_debajo_state = li_gen[0]

        self.quitaReloj()

        total, hechos, t_puntos, t_segundos, t_estado = self.bmt_lista.calc_thpse()

        dic = {}
        dic["FFINAL"] = self.dbf.FFINAL if self.siTerminadaAntes else Util.dtos(Util.today())
        dic["STATE"] = str(t_estado / total)
        dic["PUNTOS"] = t_puntos
        dic["SEGUNDOS"] = t_segundos

        self.historial.append(dic)

        self.bmt_lista.reiniciar(reiniciar_debajo_state)

        for x in range(nposic):
            estado = self.bmt_lista.state(x)
            self.liBT[x].ponIcono(self.dicIconos[estado])

        # for bt in self.liBT:
        #    bt.ponIcono(self.dicIconos[0])

        self.siTerminadaAntes = self.is_finished = False
        self.board.set_position(Position.Position().logo())
        for bt in self.liBTrm:
            bt.set_text("")
        self.siMostrarPGN = False
        self.pgn.refresh()
        self.lbPuntos.set_text("")
        self.lbSegundos.set_text("")
        self.lbJuegan.set_text("")
        self.lbPrimera.set_text(self.texto_lbPrimera)
        self.lbPrimera.setVisible(False)
        self.pon_toolbar(["terminar", "empezar"])
        # Ahora la ventana se queda vacia - por eso lo cierro
        self.terminar()
        self.accept()

    def disable_all(self):  # compatibilidad ControlPGN
        return

    def refresh(self):  # compatibilidad ControlPGN
        self.board.escena.update()
        self.update()
        QTUtil.refresh_gui()

    def set_position(self, position):
        self.board.set_position(position)

    def put_arrow_sc(self, from_sq, to_sq, liVar=None):  # liVar incluido por compatibilidad
        self.board.put_arrow_sc(from_sq, to_sq)

    def grid_num_datos(self, grid):
        if self.siMostrarPGN:
            return self.controlPGN.num_rows()
        else:
            return 0

    def ponteAlPrincipio(self):
        self.board.set_position(self.game.first_position)
        self.pgn.goto(0, 0)
        self.pgn.refresh()

    def pgnMueveBase(self, row, column):
        if column == "NUMBER":
            if row == 0:
                self.ponteAlPrincipio()
                return
            else:
                row -= 1
        self.controlPGN.mueve(row, column == "WHITE")

    def keyPressEvent(self, event):
        self.teclaPulsada("V", event.key())

    def boardWheelEvent(self, nada, forward):
        self.teclaPulsada("T", 16777234 if forward else 16777236)

    def grid_dato(self, grid, row, o_column):
        return self.controlPGN.dato(row, o_column.key)

    def grid_left_button(self, grid, row, column):
        self.pgnMueveBase(row, column.key)

    def grid_right_button(self, grid, row, column, modificadores):
        self.pgnMueveBase(row, column.key)

    def grid_doble_click(self, grid, row, column):
        if column.key == "NUMBER":
            return
        self.analizaPosicion(row, column.key)

    def grid_tecla_control(self, grid, k, is_shift, is_control, is_alt):
        self.teclaPulsada("G", k)

    def grid_wheel_event(self, ogrid, forward):
        self.teclaPulsada("T", 16777236 if not forward else 16777234)

    def teclaPulsada(self, tipo, tecla):
        if self.siMostrarPGN:
            dic = QTUtil2.dicTeclas()
            if tecla in dic:
                self.mueveJugada(dic[tecla])
        if tecla == 82 and tipo == "V":  # R = resign
            self.abandonar()
        elif tecla == 78 and tipo == "V":  # N = next
            self.seguir()
        elif tecla == 16777223:  # Del
            self.borrar()

    def mueveJugada(self, tipo):
        game = self.game
        row, column = self.pgn.current_position()

        key = column.key
        if key == "NUMBER":
            is_white = tipo == GO_BACK
            row -= 1
        else:
            is_white = key != "BLACK"

        if_starts_with_black = game.if_starts_with_black

        lj = len(game)
        if if_starts_with_black:
            lj += 1
        ultFila = (lj - 1) / 2
        siUltBlancas = lj % 2 == 1

        if tipo == GO_BACK:
            if is_white:
                row -= 1
            is_white = not is_white
            pos = row * 2
            if not is_white:
                pos += 1
            if row < 0 or (row == 0 and pos == 0 and if_starts_with_black):
                self.ponteAlPrincipio()
                return
        elif tipo == GO_FORWARD:
            if not is_white:
                row += 1
            is_white = not is_white
        elif tipo == GO_START:  # Inicio
            self.ponteAlPrincipio()
            return
        elif tipo == GO_END:
            row = ultFila
            is_white = not game.last_position.is_white

        if row == ultFila:
            if siUltBlancas and not is_white:
                return

        if row < 0 or row > ultFila:
            self.refresh()
            return
        if row == 0 and is_white and if_starts_with_black:
            is_white = False

        self.pgnColocate(row, is_white)
        self.pgnMueveBase(row, "WHITE" if is_white else "BLACK")

    def pgnColocate(self, fil, is_white):
        col = 1 if is_white else 2
        self.pgn.goto(fil, col)

    def number(self):
        bt = self.sender()
        self.activaPosicion(bt.number)
        return 0

    def pulsadoRM(self):
        if self.siMostrarPGN:
            bt = self.sender()
            self.muestra(bt.number)

    def pon_toolbar(self, li=None):
        if not li:
            li = ["terminar"]

            if not self.bmt_uno.finished:
                li.append("abandonar")

            li.append("borrar")
            li.append("opciones")

            if self.bmt_uno.finished:
                if self.is_finished:
                    li.append("repetir")
                if self.bmt_uno.cl_game:
                    li.append("original")
            li.append("seguir")
        self.tb.clear()
        for k in li:
            self.tb.dic_toolbar[k].setVisible(True)
            self.tb.dic_toolbar[k].setEnabled(True)
            self.tb.addAction(self.tb.dic_toolbar[k])

        self.tb.li_acciones = li
        self.tb.update()

    def ponPuntos(self, descontar):
        self.bmt_uno.puntos -= descontar
        if self.bmt_uno.puntos < 0:
            self.bmt_uno.puntos = 0
        self.bmt_uno.update_state()

        eti = "%d/%d" % (self.bmt_uno.puntos, self.bmt_uno.max_puntos)
        self.lbPuntos.set_text(self.trPuntos % eti)

    def ponSegundos(self):
        seconds = self.bmt_uno.seconds
        if self.iniTiempo:
            seconds += int(time.time() - self.iniTiempo)
        minutos = seconds // 60
        seconds -= minutos * 60

        if minutos:
            eti = "%d'%d\"" % (minutos, seconds)
        else:
            eti = '%d"' % (seconds,)
        eti = self.trSegundos % eti

        if eti != self.antTxtSegundos:
            self.antTxtSegundos = eti
            self.lbSegundos.set_text(eti)

    def buscaPrimero(self, from_sq):
        # Buscamos el primero que no se ha terminado
        n = len(self.bmt_lista)
        for x in range(n):
            t = from_sq + x
            if t >= n:
                t = 0
            if not self.bmt_lista.finished(t):
                self.activaPosicion(t)
                return

        self.activaPosicion(from_sq)

    def activaJugada1(self, num):
        rm = self.bmt_uno.mrm.li_rm[num]
        if num == 0:
            self.ptsMejor = rm.centipawns_abs()
        game = Game.Game()
        game.restore(rm.txtPartida)

        bt = self.liBTrm[num]
        txt = "%d: %s = %s" % (rm.nivelBMT + 1, game.move(0).pgn_translated(), rm.abrTexto())
        if rm.siPrimero:
            txt = "%s *" % txt
            self.lbPrimera.setVisible(True)
            self.ptsPrimero = rm.centipawns_abs()

        bt.set_text(txt)
        bt.setEnabled(True)
        bt.ponPlano(False)

    def activaJugada(self, num):
        rm = self.bmt_uno.mrm.li_rm[num]
        mm = self.bmt_uno.mrm.li_rm[0]
        if rm.nivelBMT == 0 or abs(rm.centipawns_abs() - mm.centipawns_abs()) <= self.pts_tolerance:
            self.finalizaTiempo()
            for n in range(len(self.bmt_uno.mrm.li_rm)):
                self.activaJugada1(n)
            self.bmt_uno.finished = True
            diferenciaPtsPrimero = self.ptsPrimero - self.ptsMejor
            self.lbPrimera.set_text("%s (difference: %s pts)" % (self.texto_lbPrimera, "%+0.2f" % (diferenciaPtsPrimero / 100.0)))
            self.muestra(num)
            self.ponPuntos(0)
            bt = self.liBT[self.actualP]
            bt.ponIcono(self.dicIconos[self.bmt_uno.state])

            self.is_finished = self.bmt_lista.is_finished()

            self.pon_toolbar()

        else:
            self.activaJugada1(num)

    def activaPosicion(self, num):

        self.finalizaTiempo()  # Para que guarde el vtime, si no es el primero

        self.bmt_uno = bmt_uno = self.bmt_lista.dame_uno(num)
        mrm = bmt_uno.mrm
        tm = mrm.max_time
        dp = mrm.max_depth
        if tm > 0:
            txt = " %d %s" % (tm / 1000, _("Second(s)"))
        elif dp > 0:
            txt = " %s %d" % (_("depth"), dp)
        else:
            txt = ""

        self.position.read_fen(bmt_uno.fen)

        mens = ""
        if self.position.castles:
            color, colorR = _("White"), _("Black")
            cK, cQ, cKR, cQR = "K", "Q", "k", "q"

            def menr(ck, cq):
                enr = ""
                if ck in self.position.castles:
                    enr += "O-O"
                if cq in self.position.castles:
                    if enr:
                        enr += "  +  "
                    enr += "O-O-O"
                return enr

            enr = menr(cK, cQ)
            if enr:
                mens += "  %s : %s" % (color, enr)
            enr = menr(cKR, cQR)
            if enr:
                mens += " %s : %s" % (colorR, enr)
        if self.position.en_passant != "-":
            mens += "     %s : %s" % (_("En passant"), self.position.en_passant)

        if mens:
            txt += "  - " + mens

        self.lbCondiciones.set_text(mrm.name + txt)
        self.lbPrimera.set_text(self.texto_lbPrimera)

        self.board.set_position(self.position)

        self.liBT[self.actualP].ponPlano(True)
        self.liBT[num].ponPlano(False)
        self.actualP = num

        nliRM = len(mrm.li_rm)
        game = Game.Game()
        for x in range(16):
            bt = self.liBTrm[x]
            if x < nliRM:
                rm = mrm.li_rm[x]
                bt.setVisible(True)
                bt.ponPlano(not rm.siElegida)
                baseTxt = str(rm.nivelBMT + 1)
                if rm.siElegida:
                    game.set_position(self.position)
                    game.read_pv(rm.pv)
                    baseTxt += " - " + game.move(0).pgn_translated()
                bt.set_text(baseTxt)
            else:
                bt.setVisible(False)

        self.ponPuntos(0)
        self.ponSegundos()

        self.pon_toolbar()
        if bmt_uno.finished:
            self.activaJugada(0)
            self.muestra(0)
        else:
            self.lbPrimera.setVisible(False)
            self.iniciaTiempo()
            self.sigueHumano()

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        self.paraHumano()

        movimiento = from_sq + to_sq

        # Peon coronando
        if not promotion and self.position.siPeonCoronando(from_sq, to_sq):
            promotion = self.board.peonCoronando(self.position.is_white)
        if promotion:
            movimiento += promotion

        nElegido = None
        puntosDescontar = self.bmt_uno.mrm.li_rm[-1].nivelBMT
        for n, rm in enumerate(self.bmt_uno.mrm.li_rm):
            if rm.pv.lower().startswith(movimiento.lower()):
                nElegido = n
                puntosDescontar = rm.nivelBMT
                break

        self.ponPuntos(puntosDescontar)

        if nElegido is not None:
            self.activaJugada(nElegido)

        if not self.bmt_uno.finished:
            self.sigueHumano()
        return True

    def paraHumano(self):
        self.board.disable_all()

    def sigueHumano(self):
        self.siMostrarPGN = False
        self.pgn.refresh()
        siW = self.position.is_white
        self.board.set_position(self.position)
        self.board.ponerPiezasAbajo(siW)
        self.board.set_side_indicator(siW)
        self.board.activate_side(siW)
        self.lbJuegan.set_text(_("White to play") if siW else _("Black to play"))

    def set_clock(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.enlaceReloj)
        self.timer.start(500)

    def quitaReloj(self):
        if self.timer:
            self.timer.stop()
            self.timer = None

    def enlaceReloj(self):
        self.ponSegundos()

    def original(self):
        self.siMostrarPGN = True
        self.lbJuegan.set_text(_("Actual game"))
        txtPartida = self.bmt_lista.dic_games[self.bmt_uno.cl_game]
        self.game.restore(txtPartida)

        siW = self.position.is_white
        fen = self.position.fen()
        row = 0
        for move in self.game.li_moves:
            if move.position_before.fen() == fen:
                break
            if not move.position_before.is_white:
                row += 1
        self.pgnMueveBase(row, "WHITE" if siW else "BLACK")
        self.pgn.goto(row, 1 if siW else 2)

        self.board.ponerPiezasAbajo(siW)

        self.pgn.refresh()

    def muestra(self, num):

        for n, bt in enumerate(self.liBTrm):
            f = bt.font()
            siBold = f.bold()
            if (num == n and not siBold) or (num != n and siBold):
                f.setBold(not siBold)
                bt.setFont(f)
            bt.setAutoDefault(num == n)
            bt.setDefault(num == n)

        self.siMostrarPGN = True
        self.lbJuegan.set_text(self.liBTrm[num].text())
        self.game.set_position(self.position)
        rm = self.bmt_uno.mrm.li_rm[num]
        self.game.restore(rm.txtPartida)

        siW = self.position.is_white
        self.pgnMueveBase(0, "WHITE" if siW else "BLACK")
        self.pgn.goto(0, 1 if siW else 2)

        self.board.ponerPiezasAbajo(siW)

        self.pgn.refresh()

    def iniciaTiempo(self):
        self.iniTiempo = time.time()
        if not self.timer:
            self.set_clock()

    def finalizaTiempo(self):
        if self.iniTiempo:
            vtime = time.time() - self.iniTiempo
            self.bmt_uno.seconds += int(vtime)
        self.iniTiempo = None
        self.quitaReloj()

    def dameJugadaEn(self, row, key):
        is_white = key != "BLACK"

        pos = row * 2
        if not is_white:
            pos += 1
        if self.game.if_starts_with_black:
            pos -= 1
        tam_lj = len(self.game)
        if tam_lj == 0:
            return
        siUltimo = (pos + 1) >= tam_lj

        move = self.game.move(pos)
        return move, is_white, siUltimo, tam_lj, pos

    def analizaPosicion(self, row, key):

        if row < 0:
            return

        move, is_white, siUltimo, tam_lj, pos = self.dameJugadaEn(row, key)
        if move.is_mate:
            return

        max_recursion = 9999
        Analysis.show_analysis(self.procesador, self.procesador.XTutor(), move, is_white, max_recursion, pos, main_window=self)


class WBMT(QTVarios.WDialogo):
    def __init__(self, procesador):

        self.procesador = procesador
        self.configuration = procesador.configuration
        self.configuration.compruebaBMT()

        self.bmt = BMT.BMT(self.configuration.ficheroBMT)
        self.read_dbf()

        owner = procesador.main_window
        icono = Iconos.BMT()
        titulo = self.titulo()
        extparam = "bmt"
        QTVarios.WDialogo.__init__(self, owner, titulo, icono, extparam)

        # Toolbar
        li_acciones = [
            (_("Close"), Iconos.MainMenu(), self.terminar),
            None,
            (_("Play"), Iconos.Empezar(), self.entrenar),
            None,
            (_("New"), Iconos.Nuevo(), self.nuevo),
            None,
            (_("Modify"), Iconos.Modificar(), self.modificar),
            None,
            (_("Remove"), Iconos.Borrar(), self.borrar),
            None,
            (_("Track record"), Iconos.Historial(), self.historial),
            None,
            (_("Utilities"), Iconos.Utilidades(), self.utilidades),
        ]
        tb = QTVarios.LCTB(self, li_acciones)

        self.tab = tab = Controles.Tab()

        # Lista
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("NOMBRE", _("Name"), 274, edicion=Delegados.LineaTextoUTF8())
        o_columns.nueva("EXTRA", _("Extra info."), 64, centered=True)
        o_columns.nueva("HECHOS", _("Made"), 84, centered=True)
        o_columns.nueva("PUNTOS", _("Score"), 84, centered=True)
        o_columns.nueva("TIME", _("Time"), 80, centered=True)
        o_columns.nueva("REPETICIONES", _("Rep."), 50, centered=True)
        o_columns.nueva("ORDEN", _("Order"), 70, centered=True)

        self.grid = grid = Grid.Grid(self, o_columns, xid="P", siEditable=False, siSelecFilas=True, siSeleccionMultiple=True)
        self.register_grid(grid)
        tab.nuevaTab(grid, _("Pending"))

        # Terminados
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("STATE", "", 26, edicion=Delegados.PmIconosBMT(), centered=True)
        o_columns.nueva("NOMBRE", _("Name"), 240)
        o_columns.nueva("EXTRA", _("Extra info."), 64, centered=True)
        o_columns.nueva("HECHOS", _("Positions"), 64, centered=True)
        o_columns.nueva("PUNTOS", _("Score"), 84, centered=True)
        o_columns.nueva("FFINAL", _("End date"), 90, centered=True)
        o_columns.nueva("TIME", _("Time"), 80, centered=True)
        o_columns.nueva("REPETICIONES", _("Rep."), 50, centered=True)
        o_columns.nueva("ORDEN", _("Order"), 70, centered=True)

        self.gridT = gridT = Grid.Grid(self, o_columns, xid="T", siEditable=True, siSelecFilas=True, siSeleccionMultiple=True)
        self.register_grid(gridT)
        tab.nuevaTab(gridT, _("Finished"))

        self.dicReverse = {}

        # Layout
        layout = Colocacion.V().control(tb).control(tab).margen(8)
        self.setLayout(layout)

        self.restore_video(siTam=True, anchoDefecto=760, altoDefecto=500)

        self.grid.gotop()
        self.gridT.gotop()

        self.grid.setFocus()

    def titulo(self):
        fdir, fnam = os.path.split(self.configuration.ficheroBMT)
        return "%s : %s (%s)" % (_("Find best move"), fnam, Util.relative_path(fdir))

    def terminar(self):
        self.bmt.cerrar()
        self.save_video()
        self.reject()
        return

    def actual(self):
        if self.tab.current_position() == 0:
            grid = self.grid
            dbf = self.dbf
        else:
            grid = self.gridT
            dbf = self.dbfT
        recno = grid.recno()
        if recno >= 0:
            dbf.goto(recno)

        return grid, dbf, recno

    def historial(self):
        grid, dbf, recno = self.actual()
        if recno >= 0:
            if dbf.REPE > 0:
                w = WHistorialBMT(self, dbf)
                w.exec_()

    def utilidades(self):
        menu = QTVarios.LCMenu(self)

        menu.opcion("cambiar", _("Select/create another file of training"), Iconos.BMT())

        menu.separador()
        menu1 = menu.submenu(_("Import") + "/" + _("Export"), Iconos.PuntoMagenta())
        menu1.opcion("exportar", _("Export the current training"), Iconos.PuntoVerde())
        menu1.separador()
        menu1.opcion("exportarLimpio", _("Export Current training with no history"), Iconos.PuntoAzul())
        menu1.separador()
        menu1.opcion("importar", _("Import a training"), Iconos.PuntoNaranja())

        menu.separador()
        menu2 = menu.submenu(_("Generate new trainings"), Iconos.PuntoRojo())
        menu2.opcion("dividir", _("Dividing the active training"), Iconos.PuntoVerde())
        menu2.separador()
        menu2.opcion("extraer", _("Extract a range of positions"), Iconos.PuntoAzul())
        menu2.separador()
        menu2.opcion("juntar", _("Joining selected training"), Iconos.PuntoNaranja())
        menu2.separador()
        menu2.opcion("rehacer", _("Analyze again"), Iconos.PuntoAmarillo())

        resp = menu.lanza()
        if resp:
            if resp == "cambiar":
                self.cambiar()
            elif resp == "importar":
                self.importar()
            elif resp.startswith("exportar"):
                self.exportar(resp == "exportarLimpio")
            elif resp == "dividir":
                self.dividir()
            elif resp == "extraer":
                self.extraer()
            elif resp == "juntar":
                self.juntar()
            elif resp == "pack":
                self.pack()
            elif resp == "rehacer":
                self.rehacer()

    def pack(self):
        um = QTUtil2.unMomento(self)
        self.dbf.pack()
        self.releer()
        um.final()

    def rehacer(self):
        grid, dbf, recno = self.actual()
        if recno < 0:
            return
        name = dbf.NOMBRE
        extra = dbf.EXTRA
        bmt_lista = Util.zip2var(dbf.leeOtroCampo(recno, "BMT_LISTA"))

        # Motor y vtime, cogemos los estandars de analysis
        file = self.configuration.file_param_analysis()
        dic = Util.restore_pickle(file)
        if dic:
            engine = dic["ENGINE"]
            vtime = dic["TIME"]
        else:
            engine = self.configuration.tutor.key
            vtime = self.configuration.x_tutor_mstime

        # Bucle para control de errores
        li_gen = [(None, None)]

        # # Nombre del entrenamiento
        li_gen.append((_("Name") + ":", name))
        li_gen.append((_("Extra info.") + ":", extra))

        # # Tutor
        li = self.configuration.ayudaCambioTutor()
        li[0] = engine
        li_gen.append((_("Engine") + ":", li))

        # Decimas de segundo a pensar el tutor
        li_gen.append((_("Duration of engine analysis (secs)") + ":", vtime / 1000.0))

        li_gen.append((None, None))

        resultado = FormLayout.fedit(li_gen, title=name, parent=self, anchoMinimo=560, icon=Iconos.Opciones())
        if not resultado:
            return
        accion, li_gen = resultado

        name = li_gen[0]
        extra = li_gen[1]
        engine = li_gen[2]
        vtime = int(li_gen[3] * 1000)

        if not vtime or not name:
            return

        dic = {"ENGINE": engine, "TIME": vtime}
        Util.save_pickle(file, dic)

        # Analizamos todos, creamos las games, y lo salvamos
        confMotor = self.configuration.buscaRival(engine)
        confMotor.multiPV = 16
        xmanager = self.procesador.creaManagerMotor(confMotor, vtime, None, True)

        tamLista = len(bmt_lista.li_bmt_uno)

        mensaje = _("Analyzing the move....")
        tmpBP = QTUtil2.BarraProgreso(self.procesador.main_window, name, mensaje, tamLista).mostrar()

        cp = Position.Position()
        is_canceled = False

        game = Game.Game()

        for pos in range(tamLista):

            uno = bmt_lista.dame_uno(pos)

            fen = uno.fen
            ant_movimiento = ""
            for rm in uno.mrm.li_rm:
                if rm.siPrimero:
                    ant_movimiento = rm.movimiento()
                    break

            tmpBP.mensaje(mensaje + " %d/%d" % (pos, tamLista))
            tmpBP.pon(pos)
            if tmpBP.is_canceled():
                is_canceled = True
                break

            mrm = xmanager.analiza(fen)

            cp.read_fen(fen)

            previa = 999999999
            nprevia = -1
            tniv = 0

            for rm in mrm.li_rm:
                if tmpBP.is_canceled():
                    is_canceled = True
                    break
                pts = rm.centipawns_abs()
                if pts != previa:
                    previa = pts
                    nprevia += 1
                tniv += nprevia
                rm.nivelBMT = nprevia
                rm.siElegida = False
                rm.siPrimero = rm.movimiento() == ant_movimiento
                game.set_position(cp)
                game.read_pv(rm.pv)
                rm.txtPartida = game.save()

            if is_canceled:
                break

            uno.mrm = mrm  # lo cambiamos y ya esta

        xmanager.terminar()

        if not is_canceled:
            # Grabamos

            bmt_lista.reiniciar()

            reg = self.dbf.baseRegistro()
            reg.ESTADO = "0"
            reg.NOMBRE = name
            reg.EXTRA = extra
            reg.TOTAL = len(bmt_lista)
            reg.HECHOS = 0
            reg.PUNTOS = 0
            reg.MAXPUNTOS = bmt_lista.max_puntos()
            reg.FINICIAL = Util.dtos(Util.today())
            reg.FFINAL = ""
            reg.SEGUNDOS = 0
            reg.BMT_LISTA = Util.var2zip(bmt_lista)
            reg.HISTORIAL = Util.var2zip([])
            reg.REPE = 0

            reg.ORDEN = 0

            self.dbf.insertarReg(reg, siReleer=True)

        tmpBP.cerrar()
        self.grid.refresh()

    def grid_doble_clickCabecera(self, grid, o_column):
        key = o_column.key
        if key != "NOMBRE":
            return

        grid, dbf, recno = self.actual()

        li = []
        for x in range(dbf.reccount()):
            dbf.goto(x)
            li.append((dbf.NOMBRE, x))

        li.sort(key=lambda x: x[0])

        si_reverse = self.dicReverse.get(grid.id, False)
        self.dicReverse[grid.id] = not si_reverse

        if si_reverse:
            li.reverse()

        order = 0
        reg = dbf.baseRegistro()
        for nom, recno in li:
            reg.ORDEN = order
            dbf.modificarReg(recno, reg)
            order += 1
        dbf.commit()
        dbf.leer()
        grid.refresh()
        grid.gotop()

    def dividir(self):
        grid, dbf, recno = self.actual()
        if recno < 0:
            return
        reg = dbf.registroActual()  # Importante ya que dbf puede cambiarse mientras se edita

        li_gen = [(None, None)]

        mx = dbf.TOTAL
        if mx <= 1:
            return
        bl = mx / 2

        li_gen.append((FormLayout.Spinbox(_("Block Size"), 1, mx - 1, 50), bl))

        resultado = FormLayout.fedit(li_gen, title="%s %s" % (reg.NOMBRE, reg.EXTRA), parent=self, icon=Iconos.Opciones())

        if resultado:
            accion, li_gen = resultado
            bl = li_gen[0]

            um = QTUtil2.unMomento(self)
            bmt_lista = Util.zip2var(dbf.leeOtroCampo(recno, "BMT_LISTA"))

            from_sq = 0
            pos = 1
            extra = reg.EXTRA
            while from_sq < mx:
                to_sq = from_sq + bl
                if to_sq >= mx:
                    to_sq = mx
                bmt_listaNV = bmt_lista.extrae(from_sq, to_sq)
                reg.TOTAL = to_sq - from_sq
                reg.BMT_LISTA = Util.var2zip(bmt_listaNV)
                reg.HISTORIAL = Util.var2zip([])
                reg.REPE = 0
                reg.ESTADO = "0"
                reg.EXTRA = (extra + " (%d)" % pos).strip()
                pos += 1
                reg.HECHOS = 0
                reg.PUNTOS = 0
                reg.MAXPUNTOS = bmt_listaNV.max_puntos()
                reg.FFINAL = ""
                reg.SEGUNDOS = 0

                dbf.insertarReg(reg, siReleer=False)

                from_sq = to_sq

            self.releer()
            um.final()

    def extraer(self):
        grid, dbf, recno = self.actual()
        if recno < 0:
            return
        reg = dbf.registroActual()  # Importante ya que dbf puede cambiarse mientras se edita
        li_gen = [(None, None)]
        config = FormLayout.Editbox('<div align="right">' + _("List of positions") + "<br>" + _("By example:") + " -5,7-9,14,19-", rx=r"[0-9,\-,\,]*")
        li_gen.append((config, ""))

        resultado = FormLayout.fedit(li_gen, title=reg.NOMBRE, parent=self, anchoMinimo=200, icon=Iconos.Opciones())

        if resultado:
            accion, li_gen = resultado

            bmt_lista = Util.zip2var(dbf.leeOtroCampo(recno, "BMT_LISTA"))
            clista = li_gen[0]
            if clista:
                lni = Util.ListaNumerosImpresion(clista)
                bmt_listaNV = bmt_lista.extrae_lista(lni)

                reg.TOTAL = len(bmt_listaNV)
                reg.BMT_LISTA = Util.var2zip(bmt_listaNV)
                reg.HISTORIAL = Util.var2zip([])
                reg.REPE = 0
                reg.ESTADO = "0"
                reg.EXTRA = clista
                reg.HECHOS = 0
                reg.PUNTOS = 0
                reg.MAXPUNTOS = bmt_listaNV.max_puntos()
                reg.FFINAL = ""
                reg.SEGUNDOS = 0

                um = QTUtil2.unMomento(self)
                dbf.insertarReg(reg, siReleer=False)

                self.releer()
                um.final()

    def juntar(self):
        grid, dbf, recno = self.actual()
        orden = dbf.ORDEN
        name = dbf.NOMBRE
        extra = dbf.EXTRA

        # Lista de recnos
        li = grid.recnosSeleccionados()

        if len(li) < 1:
            return

        # Se pide name y extra
        li_gen = [(None, None)]

        # # Nombre del entrenamiento
        li_gen.append((_("Name") + ":", name))

        li_gen.append((_("Extra info.") + ":", extra))

        li_gen.append((FormLayout.Editbox(_("Order"), tipo=int, ancho=50), orden))

        liJ = [("--", 9), (_("Best move"), 8), (_("Excellent"), 7), (_("Very good"), 6), (_("Good"), 5), (_("Acceptable"), 4)]
        config = FormLayout.Combobox(_("Drop answers with minimum score"), liJ)
        li_gen.append((config, 9))

        titulo = "%s (%d)" % (_("Joining selected training"), len(li))
        resultado = FormLayout.fedit(li_gen, title=titulo, parent=self, anchoMinimo=560, icon=Iconos.Opciones())
        if not resultado:
            return

        um = QTUtil2.unMomento(self)

        accion, li_gen = resultado
        name = li_gen[0].strip()
        extra = li_gen[1]
        orden = li_gen[2]
        eliminar_state_minimo = li_gen[3]

        # Se crea una bmt_lista, suma de todas
        bmt_lista = BMT.BMTLista()

        li_unos = []
        dic_games = {}
        for recno in li:
            bmt_lista1 = Util.zip2var(dbf.leeOtroCampo(recno, "BMT_LISTA"))
            li_unos.extend(bmt_lista1.li_bmt_uno)
            dic_games.update(bmt_lista1.dic_games)

        st_fen = set()
        if eliminar_state_minimo < 9:
            for uno in li_unos:
                if uno.state >= eliminar_state_minimo:
                    st_fen.add(uno.fen)

        for uno in li_unos:
            if uno.fen not in st_fen:
                st_fen.add(uno.fen)
                bmt_lista.nuevo(uno)
                if uno.cl_game:
                    bmt_lista.check_game(uno.cl_game, dic_games[uno.cl_game])

        if len(bmt_lista) == 0:
            return

        bmt_lista.reiniciar()

        # Se graba el registro
        reg = dbf.baseRegistro()
        reg.ESTADO = "0"
        reg.NOMBRE = name
        reg.EXTRA = extra
        reg.TOTAL = len(bmt_lista)
        reg.HECHOS = 0
        reg.PUNTOS = 0
        reg.MAXPUNTOS = bmt_lista.max_puntos()
        reg.FINICIAL = Util.dtos(Util.today())
        reg.FFINAL = ""
        reg.SEGUNDOS = 0
        reg.BMT_LISTA = Util.var2zip(bmt_lista)
        reg.HISTORIAL = Util.var2zip([])
        reg.REPE = 0

        reg.ORDEN = orden

        dbf.insertarReg(reg, siReleer=False)

        self.releer()

        um.final()

    def cambiar(self):
        fbmt = QTUtil2.salvaFichero(self, _("Select/create another file of training"), self.configuration.ficheroBMT, _("File") + " bmt (*.bmt)", siConfirmarSobreescritura=False)
        if fbmt:
            fbmt = Util.relative_path(fbmt)
            abmt = self.bmt
            try:
                self.bmt = BMT.BMT(fbmt)
            except:
                QTUtil2.message_error(self, _X(_("Unable to read file %1"), fbmt))
                return
            abmt.cerrar()
            self.read_dbf()
            self.configuration.ficheroBMT = fbmt
            self.configuration.graba()
            self.setWindowTitle(self.titulo())
            self.grid.refresh()
            self.gridT.refresh()

    def exportar(self, siLimpiar):
        grid, dbf, recno = self.actual()

        if recno >= 0:
            regActual = dbf.registroActual()
            carpeta = "%s/%s.bm1" % (os.path.dirname(self.configuration.ficheroBMT), dbf.NOMBRE)  # @Lucas: ya tienes este cambio
            filtro = _("File") + " bm1 (*.bm1)"
            fbm1 = QTUtil2.salvaFichero(self, _("Export the current training"), carpeta, filtro, siConfirmarSobreescritura=True)
            if fbm1:
                if siLimpiar:
                    regActual.ESTADO = "0"
                    regActual.HECHOS = 0
                    regActual.PUNTOS = 0
                    regActual.FFINAL = ""
                    regActual.SEGUNDOS = 0
                    bmt_lista = Util.zip2var(dbf.leeOtroCampo(recno, "BMT_LISTA"))
                    bmt_lista.reiniciar()
                    regActual.BMT_LISTA = bmt_lista
                    regActual.HISTORIAL = []
                    regActual.REPE = 0
                else:
                    regActual.BMT_LISTA = Util.zip2var(dbf.leeOtroCampo(recno, "BMT_LISTA"))
                    regActual.HISTORIAL = Util.zip2var(dbf.leeOtroCampo(recno, "HISTORIAL"))

                Util.save_pickle(fbm1, regActual)

    def modificar(self):
        grid, dbf, recno = self.actual()

        if recno >= 0:
            dbf.goto(recno)

            name = dbf.NOMBRE
            extra = dbf.EXTRA
            orden = dbf.ORDEN

            li_gen = [(None, None)]

            # # Nombre del entrenamiento
            li_gen.append((_("Name") + ":", name))

            li_gen.append((_("Extra info.") + ":", extra))

            li_gen.append((FormLayout.Editbox(_("Order"), tipo=int, ancho=50), orden))

            resultado = FormLayout.fedit(li_gen, title=name, parent=self, anchoMinimo=560, icon=Iconos.Opciones())

            if resultado:
                accion, li_gen = resultado
                li_fieldsValor = (("NOMBRE", li_gen[0].strip()), ("EXTRA", li_gen[1]), ("ORDEN", li_gen[2]))
                self.grabaCampos(grid, recno, li_fieldsValor)

    def releer(self):
        self.dbf.leer()
        self.dbfT.leer()
        self.grid.refresh()
        self.gridT.refresh()
        QTUtil.refresh_gui()

    def importar(self):
        carpeta = os.path.dirname(self.configuration.ficheroBMT)
        filtro = _("File") + " bm1 (*.bm1)"
        fbm1 = QTUtil2.leeFichero(self, carpeta, filtro, titulo=_("Import a training"))
        if fbm1:

            reg = Util.restore_pickle(fbm1)
            if hasattr(reg, "BMT_LISTA"):
                reg.BMT_LISTA = Util.var2zip(reg.BMT_LISTA)
                reg.HISTORIAL = Util.var2zip(reg.HISTORIAL)
                self.dbf.insertarReg(reg, siReleer=False)
                self.releer()
            else:
                QTUtil2.message_error(self, _X(_("Unable to read file %1"), fbm1))

    def entrenar(self):
        grid, dbf, recno = self.actual()
        if recno >= 0:
            w = WEntrenarBMT(self, dbf)
            w.exec_()
            self.releer()

    def borrar(self):
        grid, dbf, recno = self.actual()
        li = grid.recnosSeleccionados()
        if len(li) > 0:
            tit = "<br><ul>"
            for x in li:
                dbf.goto(x)
                tit += "<li>%s %s</li>" % (dbf.NOMBRE, dbf.EXTRA)
            base = _("the following training")
            if QTUtil2.pregunta(self, _X(_("Delete %1?"), base) + tit):
                um = QTUtil2.unMomento(self)
                dbf.remove_list_recnos(li)
                dbf.pack()
                self.releer()
                um.final()

    def grabaCampos(self, grid, row, li_fieldsValor):
        dbf = self.dbfT if grid.id == "T" else self.dbf
        reg = dbf.baseRegistro()
        for campo, valor in li_fieldsValor:
            setattr(reg, campo, valor)
        dbf.modificarReg(row, reg)
        dbf.commit()
        dbf.leer()
        grid.refresh()

    def grid_setvalue(self, grid, row, o_column, valor):  # ? necesario al haber delegados
        pass

    def grid_num_datos(self, grid):
        dbf = self.dbfT if grid.id == "T" else self.dbf
        return dbf.reccount()

    def grid_doble_click(self, grid, row, column):
        self.entrenar()

    def grid_dato(self, grid, row, o_column):
        dbf = self.dbfT if grid.id == "T" else self.dbf
        col = o_column.key

        dbf.goto(row)

        if col == "NOMBRE":
            return dbf.NOMBRE

        elif col == "ORDEN":
            return dbf.ORDEN if dbf.ORDEN else 0

        elif col == "STATE":
            return dbf.ESTADO

        elif col == "HECHOS":
            if grid.id == "T":
                return "%d" % dbf.TOTAL
            else:
                return "%d/%d" % (dbf.HECHOS, dbf.TOTAL)

        elif col == "PUNTOS":
            p = dbf.PUNTOS
            m = dbf.MAXPUNTOS
            if grid.id == "T":
                porc = p * 100 / m
                return "%d/%d=%d" % (p, m, porc) + "%"
            else:
                return "%d/%d" % (p, m)

        elif col == "EXTRA":
            return dbf.EXTRA

        elif col == "FFINAL":
            f = dbf.FFINAL
            return "%s-%s-%s" % (f[6:], f[4:6], f[:4]) if f else ""

        elif col == "TIME":
            s = dbf.SEGUNDOS
            if not s:
                s = 0
            m = s / 60
            s %= 60
            return "%d' %d\"" % (m, s) if m else '%d"' % s

        elif col == "REPETICIONES":
            return str(dbf.REPE)

    def read_dbf(self):
        self.dbf = self.bmt.read_dbf(False)
        self.dbfT = self.bmt.read_dbf(True)

    def nuevo(self):
        talpha = Controles.TipoLetra("Chess Alpha 2", self.configuration.x_menu_points + 4)

        def xopcion(menu, key, texto, icono, is_disabled=False):
            if "KP" in texto:
                # d = {"K": "n", "P": "i", "k": "N", "p": "I"}
                k2 = texto.index("K", 2)
                texto = texto[:k2] + texto[k2:].lower()
                # texton = ""
                # for c in texto:
                #     texton += d[c]
                menu.opcion(key, texto, icono, is_disabled, tipoLetra=talpha)
            else:
                menu.opcion(key, texto, icono, is_disabled)

        # Elegimos el entrenamiento
        menu = QTVarios.LCMenu(self)
        self.procesador.entrenamientos.menuFNS(menu, _("Select the training positions you want to use as a base"), xopcion)
        resp = menu.lanza()
        if resp is None:
            return

        fns = resp[3:]
        with open(fns, "rt", encoding="utf-8", errors="ignore") as f:
            liFEN = []
            for linea in f:
                linea = linea.strip()
                if linea:
                    if "|" in linea:
                        linea = linea.split("|")[0]
                    liFEN.append(linea)
        nFEN = len(liFEN)
        if not nFEN:
            return

        name = os.path.basename(fns)[:-4]
        name = TrListas.dicTraining().get(name, name)

        # Motor y vtime, cogemos los estandars de analysis
        file = self.configuration.file_param_analysis()
        dic = Util.restore_pickle(file)
        engine = self.configuration.tutor.key
        vtime = self.configuration.x_tutor_mstime
        if dic:
            engine = dic.get("ENGINE", engine)
            vtime = dic.get("TIME", vtime)

        if not vtime:
            vtime = 3.0

        # Bucle para control de errores
        while True:
            # Datos
            li_gen = [(None, None)]

            # # Nombre del entrenamiento
            li_gen.append((_("Name") + ":", name))

            # # Tutor
            li = self.configuration.ayudaCambioTutor()
            li[0] = engine
            li_gen.append((_("Engine") + ":", li))

            # Decimas de segundo a pensar el tutor
            li_gen.append((_("Duration of engine analysis (secs)") + ":", vtime / 1000.0))

            li_gen.append((None, None))

            li_gen.append((FormLayout.Spinbox(_("From number"), 1, nFEN, 50), 1))
            li_gen.append((FormLayout.Spinbox(_("To number"), 1, nFEN, 50), nFEN if nFEN < 20 else 20))

            resultado = FormLayout.fedit(li_gen, title=name, parent=self, anchoMinimo=560, icon=Iconos.Opciones())

            if resultado:
                accion, li_gen = resultado

                name = li_gen[0]
                engine = li_gen[1]
                vtime = int(li_gen[2] * 1000)

                if not vtime or not name:
                    return

                dic = {"ENGINE": engine, "TIME": vtime}
                Util.save_pickle(file, dic)

                from_sq = li_gen[3]
                to_sq = li_gen[4]
                nDH = to_sq - from_sq + 1
                if nDH <= 0:
                    return
                break

            else:
                return

        # Analizamos todos, creamos las games, y lo salvamos
        confMotor = self.configuration.buscaRival(engine)
        confMotor.multiPV = 16
        xmanager = self.procesador.creaManagerMotor(confMotor, vtime, None, True)

        mensaje = _("Analyzing the move....")
        tmpBP = QTUtil2.BarraProgreso(self.procesador.main_window, name, mensaje, nDH).mostrar()

        cp = Position.Position()
        is_canceled = False

        bmt_lista = BMT.BMTLista()

        game = Game.Game()

        for n in range(from_sq - 1, to_sq):

            fen = liFEN[n]

            tmpBP.mensaje(mensaje + " %d/%d" % (n + 2 - from_sq, nDH))
            tmpBP.pon(n + 2 - from_sq)
            if tmpBP.is_canceled():
                is_canceled = True
                break

            mrm = xmanager.analiza(fen)

            cp.read_fen(fen)

            previa = 999999999
            nprevia = -1
            tniv = 0

            for rm in mrm.li_rm:
                if tmpBP.is_canceled():
                    is_canceled = True
                    break
                pts = rm.centipawns_abs()
                if pts != previa:
                    previa = pts
                    nprevia += 1
                tniv += nprevia
                rm.nivelBMT = nprevia
                rm.siElegida = False
                rm.siPrimero = False
                game.set_position(cp)
                game.read_pv(rm.pv)
                game.is_finished()
                rm.txtPartida = game.save()

            if is_canceled:
                break

            bmt_uno = BMT.BMTUno(fen, mrm, tniv, None)

            bmt_lista.nuevo(bmt_uno)

        xmanager.terminar()

        if not is_canceled:
            # Grabamos

            reg = self.dbf.baseRegistro()
            reg.ESTADO = "0"
            reg.NOMBRE = name
            reg.EXTRA = "%d-%d" % (from_sq, to_sq)
            reg.TOTAL = len(bmt_lista)
            reg.HECHOS = 0
            reg.PUNTOS = 0
            reg.MAXPUNTOS = bmt_lista.max_puntos()
            reg.FINICIAL = Util.dtos(Util.today())
            reg.FFINAL = ""
            reg.SEGUNDOS = 0
            reg.BMT_LISTA = Util.var2zip(bmt_lista)
            reg.HISTORIAL = Util.var2zip([])
            reg.REPE = 0

            reg.ORDEN = 0

            self.dbf.insertarReg(reg, siReleer=True)

        self.releer()
        tmpBP.cerrar()


def windowBMT(procesador):
    w = WBMT(procesador)
    w.exec_()
