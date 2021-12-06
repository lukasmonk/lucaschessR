from PySide2 import QtCore, QtWidgets

import Code
from Code.Base.Constantes import (
    TB_CLOSE,
    TB_REINIT,
    TB_TAKEBACK,
    TB_CONFIG,
    TB_ACCEPT,
    TB_ADJOURN,
    TB_Adjournments,
    TB_BOXROOMS_PGN,
    TB_CANCEL,
    TB_CHANGE,
    TB_COMPETE,
    TB_CONTINUE,
    TB_CONTINUE_REPLAY,
    TB_DRAW,
    TB_END_GAME,
    TB_END_REPLAY,
    TB_FAST_REPLAY,
    TB_FILE,
    TB_HELP,
    TB_HELP_TO_MOVE,
    TB_INFORMATION,
    TB_LEVEL,
    TB_MY_GAMES,
    TB_NEXT,
    TB_OPEN,
    TB_OPTIONS,
    TB_OTHER_GAME,
    TB_PASTE_PGN,
    TB_PAUSE,
    TB_PAUSE_REPLAY,
    TB_PGN_LABELS,
    TB_PGN_REPLAY,
    TB_PLAY,
    TB_PREVIOUS,
    TB_QUIT,
    TB_READ_PGN,
    TB_REPEAT,
    TB_REPEAT_REPLAY,
    TB_RESIGN,
    TB_SAVE,
    TB_SAVE_AS,
    TB_SEND,
    TB_SHOW_TEXT,
    TB_SLOW_REPLAY,
    TB_STOP,
    TB_TOOLS,
    TB_TRAIN,
    TB_UTILITIES,
    TB_VARIATIONS,
    NAG_0,
    NAG_1,
    NAG_2,
    NAG_3,
    NAG_4,
    NAG_5,
    NAG_6,
)
from Code.Board import Board
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Delegados
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTUtil2


class WBase(QtWidgets.QWidget):
    def __init__(self, parent, manager):
        super(WBase, self).__init__(parent)

        self.parent = parent
        self.manager = manager

        self.configuration = Code.configuration

        self.procesandoEventos = None

        self.setWindowIcon(Iconos.Aplicacion64())

        self.create_toolbar()
        self.create_board()

        ly_bi = self.creaBloqueInformacion()

        ly_t = Colocacion.V().control(self.board).relleno()

        self.conAtajos = True

        self.si_tutor = False
        self.num_hints = 0

        self.li_hide_replay = []

        ly_ai = Colocacion.H().relleno(1).otroi(ly_t).otroi(ly_bi).relleno(1).margen(0)
        ly = Colocacion.V().control(self.tb).relleno().otro(ly_ai).relleno().margen(2)

        self.setLayout(ly)

        self.setAutoFillBackground(True)

    def set_manager_active(self, manager):
        self.manager = manager

    def create_toolbar(self):
        self.tb = QtWidgets.QToolBar("BASIC", self)
        iconsTB = self.configuration.tipoIconos()
        self.tb.setToolButtonStyle(iconsTB)
        sz = 32 if iconsTB == QtCore.Qt.ToolButtonTextUnderIcon else 16
        self.tb.setIconSize(QtCore.QSize(sz, sz))
        style = "QToolBar {border-bottom: 1px solid gray; border-top: 1px solid gray;}"
        self.tb.setStyleSheet(style)
        # sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtGui, QtWidgets.QSizePolicy.Expanding)
        # self.tb.setSizePolicy(sp)
        self.tb.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tb.customContextMenuRequested.connect(self.lanzaAtajos)

        self.dic_toolbar = {}

        dic_opciones = {
            TB_PLAY: (_("Play"), Iconos.Libre()),
            TB_COMPETE: (_("Compete"), Iconos.NuevaPartida()),
            TB_TRAIN: (_("Train"), Iconos.Entrenamiento()),
            TB_OPTIONS: (_("Options"), Iconos.Opciones()),
            TB_INFORMATION: (_("Information"), Iconos.Informacion()),
            TB_FILE: (_("File"), Iconos.File()),
            TB_SAVE: (_("Save"), Iconos.Grabar()),
            TB_SAVE_AS: (_("Save as"), Iconos.GrabarComo()),
            TB_OPEN: (_("Open"), Iconos.Recuperar()),
            TB_RESIGN: (_("Resign"), Iconos.Abandonar()),
            TB_REINIT: (_("Reinit"), Iconos.Reiniciar()),
            TB_TAKEBACK: (_("Takeback"), Iconos.Atras()),
            TB_ADJOURN: (_("Adjourn"), Iconos.Aplazar()),
            TB_Adjournments: (_("Adjournments"), Iconos.Aplazamientos()),
            TB_END_GAME: (_("End game"), Iconos.FinPartida()),
            TB_CLOSE: (_("Close"), Iconos.MainMenu()),
            TB_PREVIOUS: (_("Previous"), Iconos.Anterior()),
            TB_NEXT: (_("Next"), Iconos.Siguiente()),
            TB_QUIT: (_("Quit"), Iconos.FinPartida()),
            TB_PASTE_PGN: (_("Paste PGN"), Iconos.Pegar()),
            TB_READ_PGN: (_("Read PGN file"), Iconos.Fichero()),
            TB_PGN_LABELS: (_("PGN Labels"), Iconos.InformacionPGN()),
            TB_OTHER_GAME: (_("Other game"), Iconos.FicheroRepite()),
            TB_MY_GAMES: (_("My games"), Iconos.NuestroFichero()),
            TB_DRAW: (_("Draw"), Iconos.Tablas()),
            TB_BOXROOMS_PGN: (_("Boxrooms PGN"), Iconos.BoxRooms()),
            TB_END_REPLAY: (_("End"), Iconos.MainMenu()),
            TB_SLOW_REPLAY: (_("Slow"), Iconos.Pelicula_Lento()),
            TB_PAUSE: (_("Pause"), Iconos.Pelicula_Pausa()),
            TB_PAUSE_REPLAY: (_("Pause"), Iconos.Pelicula_Pausa()),
            TB_CONTINUE: (_("Continue"), Iconos.Pelicula_Seguir()),
            TB_CONTINUE_REPLAY: (_("Continue"), Iconos.Pelicula_Seguir()),
            TB_FAST_REPLAY: (_("Fast"), Iconos.Pelicula_Rapido()),
            TB_REPEAT: (_("Repeat"), Iconos.Pelicula_Repetir()),
            TB_REPEAT_REPLAY: (_("Repeat"), Iconos.Pelicula_Repetir()),
            TB_PGN_REPLAY: (_("PGN"), Iconos.Pelicula_PGN()),
            TB_HELP: (_("Help"), Iconos.AyudaGR()),
            TB_LEVEL: (_("Level"), Iconos.Jugar()),
            TB_ACCEPT: (_("Accept"), Iconos.Aceptar()),
            TB_CANCEL: (_("Cancel"), Iconos.Cancelar()),
            TB_CONFIG: (_("Config"), Iconos.Configurar()),
            TB_UTILITIES: (_("Utilities"), Iconos.Utilidades()),
            TB_VARIATIONS: (_("Variations"), Iconos.VariationsG()),
            TB_TOOLS: (_("Tools"), Iconos.Tools()),
            TB_CHANGE: (_("Change"), Iconos.Cambiar()),
            TB_SHOW_TEXT: (_("Show text"), Iconos.Modificar()),
            TB_HELP_TO_MOVE: (_("Help to move"), Iconos.BotonAyuda()),
            TB_SEND: (_("Send"), Iconos.Enviar()),
            TB_STOP: (_("Play now"), Iconos.Stop()),
        }

        cf = self.manager.configuration
        peso = 75 if cf.x_tb_bold else 50
        puntos = cf.x_tb_fontpoints
        font = Controles.TipoLetra(puntos=puntos, peso=peso)

        for key, (titulo, icono) in dic_opciones.items():
            accion = QtWidgets.QAction(titulo, None)
            accion.setIcon(icono)
            accion.setIconText(titulo)
            accion.setFont(font)
            accion.triggered.connect(self.run_action)
            accion.key = key
            self.dic_toolbar[key] = accion

    def lanzaAtajos(self):
        if self.conAtajos:
            self.manager.lanza_atajos()

    def lanzaAtajosALT(self, key):
        if self.conAtajos:
            self.manager.lanzaAtajosALT(key)

    def create_board(self):
        ae = QTUtil.altoEscritorio()
        mx = int(ae * 0.08)
        config_board = self.manager.configuration.config_board("BASE", mx)
        self.board = Board.Board(self, config_board)
        self.board.crea()
        self.board.setFocus()

        Delegados.generaPM(self.board.piezas)

    def columnas60(self, siPoner, cNivel):
        o_columns = self.pgn.o_columns
        o_columns.li_columns[0].head = cNivel if siPoner else _("N.")
        o_columns.li_columns[1].head = _("Errors") if siPoner else _("White")
        o_columns.li_columns[2].head = _("Second(s)") if siPoner else _("Black")
        o_columns.li_columns[0].key = "LEVEL" if siPoner else "NUMBER"
        o_columns.li_columns[1].key = "ERRORS" if siPoner else "WHITE"
        o_columns.li_columns[2].key = "TIME" if siPoner else "BLACK"
        self.pgn.releerColumnas()

        self.pgn.seleccionaFilas(siPoner, False)

    def ponWhiteBlack(self, white, black):
        o_columns = self.pgn.o_columns
        o_columns.li_columns[1].head = white if white else _("White")
        o_columns.li_columns[2].head = black if black else _("Black")

    def creaBloqueInformacion(self):
        configuration = self.manager.configuration
        width_pgn = configuration.x_pgn_width
        with_each_color = (width_pgn - 52 - 24) // 2
        nAnchoLabels = max(int((width_pgn - 3) // 2), 140)
        # # Pgn
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("NUMBER", _("N."), 52, centered=True)
        with_figurines = configuration.x_pgn_withfigurines
        o_columns.nueva(
            "WHITE", _("White"), with_each_color, edicion=Delegados.EtiquetaPGN(True if with_figurines else None)
        )
        o_columns.nueva(
            "BLACK", _("Black"), with_each_color, edicion=Delegados.EtiquetaPGN(False if with_figurines else None)
        )
        self.pgn = Grid.Grid(self, o_columns, siCabeceraMovible=False)
        self.pgn.setMinimumWidth(width_pgn)
        self.pgn.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.pgn.tipoLetra(puntos=configuration.x_pgn_fontpoints)
        self.pgn.ponAltoFila(configuration.x_pgn_rowheight)
        self.pgn.set_right_button_without_rows(True)

        # # Blancas y negras
        f = Controles.TipoLetra(puntos=configuration.x_sizefont_infolabels + 2, peso=75)
        self.lb_player_white = Controles.LB(self).anchoFijo(nAnchoLabels).align_center().ponFuente(f).set_wrap()
        style = "QWidget { border-style: groove; border-width: 2px; border-color: Gray; padding: 4px 4px 4px 4px;background-color:%s;color:%s;}"
        self.lb_player_white.setStyleSheet(style % ("white", "black"))

        self.lb_player_black = Controles.LB(self).anchoFijo(nAnchoLabels).align_center().ponFuente(f).set_wrap()
        self.lb_player_black.setStyleSheet(style % ("black", "white"))

        # # Capturas
        n_alto_fijo = 3 * (configuration.x_sizefont_infolabels + 2)
        self.lb_capt_white = Controles.LB(self).anchoFijo(nAnchoLabels).set_wrap().altoFijo(n_alto_fijo)
        style = "QWidget { border-style: groove; border-width: 1px; border-color: LightGray; padding: 2px 0px 2px 0px;}"
        self.lb_capt_white.setStyleSheet(style)

        self.lb_capt_black = Controles.LB(self).anchoFijo(nAnchoLabels).set_wrap().altoFijo(n_alto_fijo)
        self.lb_capt_black.setStyleSheet(style)

        # Relojes
        f = Controles.TipoLetra("Arial Black" if Code.is_windows else Code.font_mono, puntos=26, peso=500)

        def lbReloj():
            lb = (
                Controles.LB(self, "00:00")
                .ponFuente(f)
                .align_center()
                .set_foreground_backgound("#076C9F", "#EFEFEF")
                .anchoMinimo(nAnchoLabels)
            )
            lb.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Raised)
            return lb

        self.lb_clock_white = lbReloj()
        self.lb_clock_black = lbReloj()

        f = Controles.TipoLetra(puntos=12)
        # Boton de tutor activo
        self.bt_active_tutor = Controles.PB(self, "", rutina=self.change_tutor_active, plano=False).ponFuente(f)

        # Rotulos de informacion
        f = Controles.TipoLetra(puntos=configuration.x_sizefont_infolabels)
        self.lbRotulo1 = Controles.LB(self).set_wrap().ponFuente(f)
        self.lbRotulo2 = Controles.LB(self).set_wrap().ponFuente(f)
        f9 = Controles.TipoLetra(puntos=9)
        self.lbRotulo3 = Controles.LB(self).set_wrap().ponFuente(f9)
        self.lbRotulo3.setStyleSheet("*{ border: 1px solid darkgray }")
        self.lbRotulo3.altoFijo(48)

        # Lo escondemos
        self.lb_player_white.hide()
        self.lb_player_black.hide()
        self.lb_capt_white.hide()
        self.lb_capt_black.hide()
        self.lb_clock_white.hide()
        self.lb_clock_black.hide()
        self.lb_capt_white.hide()
        self.lb_capt_black.hide()
        self.pgn.hide()
        self.bt_active_tutor.hide()
        self.lbRotulo1.hide()
        self.lbRotulo2.hide()
        self.lbRotulo3.hide()

        # Layout

        # Arriba
        ly_color = Colocacion.G()
        ly_color.controlc(self.lb_player_white, 0, 0).controlc(self.lb_player_black, 0, 1)
        ly_color.controlc(self.lb_clock_white, 2, 0).controlc(self.lb_clock_black, 2, 1)

        # Abajo
        ly_capturas = Colocacion.H().control(self.lb_capt_white).control(self.lb_capt_black)

        ly_abajo = Colocacion.V()
        ly_abajo.setSizeConstraint(ly_abajo.SetFixedSize)
        ly_abajo.otro(ly_capturas)
        ly_abajo.control(self.bt_active_tutor)
        ly_abajo.control(self.lbRotulo1).control(self.lbRotulo2).control(self.lbRotulo3)

        ly_v = Colocacion.V().otro(ly_color).control(self.pgn)
        ly_v.otro(ly_abajo)

        return ly_v

    def run_action(self):
        self.manager.run_action(self.sender().key)

    def pon_toolbar(self, li_acciones, separator=False, conAtajos=False):
        self.conAtajos = conAtajos

        self.tb.clear()
        last = len(li_acciones) - 1
        for n, k in enumerate(li_acciones):
            self.dic_toolbar[k].setVisible(True)
            self.dic_toolbar[k].setEnabled(True)
            self.tb.addAction(self.dic_toolbar[k])
            if separator and n != last:
                self.tb.addSeparator()

        self.tb.li_acciones = li_acciones
        self.tb.update()
        QTUtil.refresh_gui()
        return self.tb

    def get_toolbar(self):
        return self.tb.li_acciones

    def is_enabled_option_toolbar(self, kopcion):
        return kopcion in self.dic_toolbar and self.dic_toolbar[kopcion].isEnabled()

    def enable_option_toolbar(self, kopcion, siHabilitar):
        self.dic_toolbar[kopcion].setEnabled(siHabilitar)

    def show_option_toolbar(self, kopcion, must_show):
        self.dic_toolbar[kopcion].setVisible(must_show)

    def set_activate_tutor(self, siActivar):
        self.si_tutor = siActivar
        self.set_label_tutor()

    def set_label_tutor(self):
        if self.si_tutor:
            mens = _("Tutor enabled")
        else:
            mens = _("Tutor disabled")
        if 0 < self.num_hints < 99:
            mens += " [%d]" % self.num_hints
        self.bt_active_tutor.setText(mens)

    def change_tutor_active(self):
        self.manager.change_tutor_active()

    def grid_num_datos(self, grid):
        return self.manager.num_rows()

    def grid_left_button(self, grid, row, column):
        self.manager.pgnMueveBase(row, column.key)

    def grid_right_button(self, grid, row, column, modificadores):
        self.manager.gridRightMouse(modificadores.is_shift, modificadores.is_control, modificadores.is_alt)
        self.manager.pgnMueveBase(row, column.key)

    def boardRightMouse(self, is_shift, is_control, is_alt):
        if hasattr(self.manager, "boardRightMouse"):
            self.manager.boardRightMouse(is_shift, is_control, is_alt)

    def grid_doble_click(self, grid, row, column):
        if column.key == "NUMBER":
            return
        self.manager.analizaPosicion(row, column.key)

    def grid_pulsada_cabecera(self, grid, column):
        col_white = self.pgn.o_columns.column(1)
        col_black = self.pgn.o_columns.column(2)
        new_width = 0
        if col_white.ancho != self.pgn.columnWidth(1):
            new_width = self.pgn.columnWidth(1)
        elif col_black.ancho != self.pgn.columnWidth(2):
            new_width = self.pgn.columnWidth(2)

        if new_width:
            col_white.ancho = new_width
            col_black.ancho = new_width
            self.pgn.set_widthsColumnas()
            nAnchoPgn = new_width * 2 + self.pgn.columnWidth(0) + 28
            self.pgn.setMinimumWidth(nAnchoPgn)
            QTUtil.refresh_gui()
            self.manager.configuration.x_pgn_width = nAnchoPgn
            self.manager.configuration.graba()

    def grid_tecla_control(self, grid, k, is_shift, is_control, is_alt):
        self.teclaPulsada("G", k)

    def grid_wheel_event(self, ogrid, forward):
        self.teclaPulsada("T", 16777236 if not forward else 16777234)

    def grid_dato(self, grid, row, o_columna):
        controlPGN = self.manager.pgn

        col = o_columna.key
        if col == "NUMBER":
            return controlPGN.dato(row, col)

        move = controlPGN.only_move(row, col)
        if not move:
            return self.manager.pgn.dato(row, col)  # ManagerMate,...

        if not controlPGN.must_show:
            return "-"

        color = None
        info = ""
        indicadorInicial = None

        color_nag = NAG_0
        st_nags = set(move.li_nags)
        for nag in st_nags:
            if 0 < nag < 7:
                color_nag = nag
                break

        if move.analysis:
            mrm, pos = move.analysis
            rm = mrm.li_rm[pos]
            mate = rm.mate
            siW = move.position_before.is_white
            if mate:
                if mate == 1:
                    info = ""
                else:
                    if not siW:
                        mate = -mate
                    if (mate > 1) and siW:
                        mate -= 1
                    elif (mate < -1) and not siW:
                        mate += 1

                    info = "(M%+d)" % mate
            else:
                pts = rm.puntos
                if not siW:
                    pts = -pts
                info = "(%+0.2f)" % float(pts / 100.0)

            if color_nag == NAG_0:  # Son prioritarios los nags manuales
                nag, color_nag = mrm.set_nag_color(self.configuration, rm)
                st_nags.add(nag)

        if move.in_the_opening or move.comment or move.variations:
            indicadorInicial = "O" if move.in_the_opening else ""
            if len(move.variations) > 0:
                indicadorInicial += "V"
            if move.comment:
                indicadorInicial += "C"

        pgn = move.pgnFigurinesSP() if self.manager.configuration.x_pgn_withfigurines else move.pgn_translated()
        if color_nag:
            c = self.manager.configuration
            color = {
                NAG_1: c.x_color_nag1,
                NAG_2: c.x_color_nag2,
                NAG_3: c.x_color_nag3,
                NAG_4: c.x_color_nag4,
                NAG_5: c.x_color_nag5,
                NAG_6: c.x_color_nag6,
            }[color_nag]

        if move.has_themes():
            indicadorInicial = "T"

        return pgn, color, info, indicadorInicial, st_nags

    def grid_setvalue(self, grid, row, o_column, valor):
        pass

    def keyPressEvent(self, event):
        k = event.key()
        if self.conAtajos:
            if 49 <= k <= 57:
                m = int(event.modifiers())
                if (m & QtCore.Qt.AltModifier) > 0:
                    self.lanzaAtajosALT(k - 48)
                    return
        self.teclaPulsada("V", event.key(), int(event.modifiers()))

    def boardWheelEvent(self, board, forward):
        self.teclaPulsada("T", 16777236 if forward else 16777234)

    def teclaPulsada(self, tipo, tecla, modifiers=None):
        if self.procesandoEventos:
            QTUtil.refresh_gui()
            return
        self.procesandoEventos = True

        dic = QTUtil2.dic_keys()
        if tecla in dic:
            if hasattr(self.manager, "mueveJugada"):
                self.manager.mueveJugada(dic[tecla])
        elif tecla in (16777220, 16777221):  # intros
            row, column = self.pgn.current_position()
            if column.key != "NUMBER":
                if hasattr(self.manager, "analizaPosicion"):
                    self.manager.analizaPosicion(row, column.key)
        else:
            if hasattr(self.manager, "control_teclado"):

                self.manager.control_teclado(tecla, modifiers)
        self.procesandoEventos = False

    def pgnRefresh(self):
        self.pgn.refresh()

    def activaJuego(self, siActivar, siReloj, siAyudas=None):
        self.pgn.setVisible(siActivar)
        if siAyudas is None:
            siAyudas = siActivar
        self.bt_active_tutor.setVisible(siActivar)
        self.lbRotulo1.setVisible(False)
        self.lbRotulo2.setVisible(False)
        self.lbRotulo3.setVisible(False)
        self.lb_capt_white.setVisible(False)
        self.lb_capt_black.setVisible(False)

        self.lb_player_white.setVisible(siReloj)
        self.lb_player_black.setVisible(siReloj)
        self.lb_clock_white.setVisible(siReloj)
        self.lb_clock_black.setVisible(siReloj)

    def hide_replay(self):
        self.li_hide_replay = []
        for control in (
            self.pgn,
            self.bt_active_tutor,
            self.lbRotulo1,
            self.lbRotulo2,
            self.lbRotulo3,
            self.lb_capt_white,
            self.lb_capt_black,
            self.lb_player_white,
            self.lb_player_black,
            self.lb_clock_white,
            self.lb_clock_black,
        ):
            if control.isVisible():
                self.li_hide_replay.append(control)
                control.hide()

    def show_replay(self):
        for control in self.li_hide_replay:
            control.show()

    def nonDistractMode(self, nonDistract):
        if nonDistract:
            for widget in nonDistract:
                widget.setVisible(True)
            nonDistract = None
        else:
            nonDistract = []
            for widget in (
                self.tb,
                self.pgn,
                self.bt_active_tutor,
                self.lbRotulo1,
                self.lbRotulo2,
                self.lbRotulo3,
                self.lb_player_white,
                self.lb_player_black,
                self.lb_clock_white,
                self.lb_clock_black,
                self.lb_capt_white,
                self.lb_capt_black,
                self.parent().parent().informacionPGN,
            ):
                if widget.isVisible():
                    nonDistract.append(widget)
                    widget.setVisible(False)
        return nonDistract

    def ponDatosReloj(self, bl, rb, ng, rn):
        self.ponRelojBlancas(rb, "00:00")
        self.ponRelojNegras(rn, "00:00")
        self.change_player_labels(bl, ng)

    def change_player_labels(self, bl, ng):
        self.lb_player_white.altoMinimo(0)
        self.lb_player_black.altoMinimo(0)
        self.lb_player_white.set_text(bl)
        self.lb_player_black.set_text(ng)
        self.lb_player_white.show()
        self.lb_player_black.show()
        QTUtil.refresh_gui()

        hb = self.lb_player_white.height()
        hn = self.lb_player_black.height()
        if hb > hn:
            self.lb_player_black.altoMinimo(hb)
        elif hb < hn:
            self.lb_player_white.altoMinimo(hn)

    def put_captures(self, dic):
        d = {True: [], False: []}
        for pz, num in dic.items():
            for x in range(num):
                d[pz.isupper()].append(pz)

        value = {"q": 1, "r": 2, "b": 3, "n": 4, "p": 5}

        def xshow(max_num, tp, li, lb):
            html = ""
            li.sort(key=lambda x: value[x.lower()])
            for n, pz in enumerate(li):
                # if n >= max_num: # la situación en la que sobran
                #     html += "+++"
                #     break
                # html += '<img src="../Resources/IntFiles/Figs/%s%s.png">' % (tp, pz.lower())
                html += '<img src="../Resources/IntFiles/Figs/%s%s.png" width="30" height="30">' % (tp, pz.lower())
            lb.set_text(html)

        max_num = self.lb_capt_white.width() // 27
        xshow(max_num, "b", d[True], self.lb_capt_white)
        xshow(max_num, "w", d[False], self.lb_capt_black)
        if self.lb_capt_white.isVisible():
            self.lb_capt_white.show()
            self.lb_capt_black.show()

    def ponAyudas(self, puntos, siQuitarAtras=True):
        self.num_hints = puntos
        self.set_label_tutor()

        if (puntos == 0) and siQuitarAtras:
            if TB_TAKEBACK in self.tb.li_acciones:
                self.dic_toolbar[TB_TAKEBACK].setVisible(False)

    def remove_hints(self, siTambienTutorAtras, siQuitarAtras=True):
        if siTambienTutorAtras:
            self.bt_active_tutor.setVisible(False)
            if siQuitarAtras and (TB_TAKEBACK in self.tb.li_acciones):
                self.dic_toolbar[TB_TAKEBACK].setVisible(False)

    def set_label1(self, label):
        if label:
            self.lbRotulo1.set_text(label)
            self.lbRotulo1.show()
        else:
            self.lbRotulo1.hide()
        return self.lbRotulo1

    def set_label2(self, label):
        if label:
            self.lbRotulo2.set_text(label)
            self.lbRotulo2.show()
        else:
            self.lbRotulo2.hide()
        return self.lbRotulo2

    def set_hight_label3(self, px):
        self.lbRotulo3.altoFijo(px)

    def set_label3(self, label):
        if label is not None:
            self.lbRotulo3.set_text(label)
            self.lbRotulo3.show()
        else:
            self.lbRotulo3.hide()
        return self.lbRotulo3

    def get_labels(self):
        def get(lb):
            return lb.texto() if lb.isVisible() else None

        return get(self.lbRotulo1), get(self.lbRotulo2), get(self.lbRotulo3)

    def ponRelojBlancas(self, tm, tm2):
        if tm2 is not None:
            tm += '<br><FONT SIZE="-4">' + tm2
        self.lb_clock_white.set_text(tm)

    def ponRelojNegras(self, tm, tm2):
        if tm2 is not None:
            tm += '<br><FONT SIZE="-4">' + tm2
        self.lb_clock_black.set_text(tm)

    # def creaCapturas(self):
    #     self.capturas = WCapturas.CapturaLista(self, self.board)
