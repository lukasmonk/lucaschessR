from PySide2 import QtSvg, QtCore

import Code
from Code import Everest
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code import Util


class WNewExpedition(QTVarios.WDialogo):
    def __init__(self, owner, fichero):
        self.litourneys = Everest.str_file(fichero)
        self.configuration = owner.configuration
        titulo = _("New expedition")
        icono = Iconos.Trekking()
        extparam = "newexpedition"
        QTVarios.WDialogo.__init__(self, owner, titulo, icono, extparam)

        self.selected = None

        # Torneo
        li = [("%s (%d)" % (_F(tourney["TOURNEY"]), len(tourney["GAMES"])), tourney) for tourney in self.litourneys]
        li.sort(key=lambda x: x[0])
        self.cbtourney, lbtourney = QTUtil2.comboBoxLB(self, li, li[0], _("Expedition"))

        lytourney = Colocacion.H().control(lbtourney).control(self.cbtourney).relleno(1)

        # tolerance
        self.sbtolerance_min, lbtolerance_min = QTUtil2.spinBoxLB(self, 20, 0, 99999, _("From"))
        self.sbtolerance_min.capture_changes(self.tolerance_changed)
        self.sbtolerance_max, lbtolerance_max = QTUtil2.spinBoxLB(self, 1000, 0, 99999, _("To"))
        lbexplanation = Controles.LB(self, _("Maximum lost points for having to repeat active game"))
        ly = Colocacion.H().relleno(2).control(lbtolerance_min).control(self.sbtolerance_min).relleno(1)
        ly.control(lbtolerance_max).control(self.sbtolerance_max).relleno(2)
        layout = Colocacion.V().otro(ly).control(lbexplanation)
        gbtolerance = Controles.GB(self, _("Tolerance"), layout)

        # tries
        self.sbtries_min, lbtries_min = QTUtil2.spinBoxLB(self, 2, 1, 99999, _("From"))
        self.sbtries_min.capture_changes(self.tries_changed)
        self.sbtries_max, lbtries_max = QTUtil2.spinBoxLB(self, 15, 1, 99999, _("To"))
        lbexplanation = Controles.LB(self, _("Maximum repetitions to return to the previous game"))
        ly = Colocacion.H().relleno(2).control(lbtries_min).control(self.sbtries_min).relleno(1)
        ly.control(lbtries_max).control(self.sbtries_max).relleno(2)
        layout = Colocacion.V().otro(ly).control(lbexplanation)
        gbtries = Controles.GB(self, _("Tries"), layout)

        # color
        liColors = ((_("Default"), "D"), (_("White"), "W"), (_("Black"), "B"))
        self.cbcolor = Controles.CB(self, liColors, "D")
        layout = Colocacion.H().relleno(1).control(self.cbcolor).relleno(1)
        gbcolor = Controles.GB(self, _("Color"), layout)

        tb = QTVarios.LCTB(self)
        tb.new(_("Accept"), Iconos.Aceptar(), self.aceptar)
        tb.new(_("Cancel"), Iconos.Cancelar(), self.cancelar)

        layout = Colocacion.V().control(tb).otro(lytourney).control(gbtolerance).control(gbtries).control(gbcolor)

        self.setLayout(layout)

    def aceptar(self):
        self.selected = alm = Util.Record()
        alm.tourney = self.cbtourney.valor()
        alm.tolerance_min = self.sbtolerance_min.valor()
        alm.tolerance_max = self.sbtolerance_max.valor()
        alm.tries_min = self.sbtries_min.valor()
        alm.tries_max = self.sbtries_max.valor()
        alm.color = self.cbcolor.valor()
        self.accept()

    def cancelar(self):
        self.reject()

    def tolerance_changed(self):
        tolerance_min = self.sbtolerance_min.valor()
        self.sbtolerance_max.setMinimum(tolerance_min)
        if self.sbtolerance_max.valor() < tolerance_min:
            self.sbtolerance_max.ponValor(tolerance_min)

    def tries_changed(self):
        tries_min = self.sbtries_min.valor()
        self.sbtries_max.setMinimum(tries_min)
        if self.sbtries_max.valor() < tries_min:
            self.sbtries_max.ponValor(tries_min)


class WExpedition(QTVarios.WDialogo):
    def __init__(self, wowner, configuration, recno):
        expedition = Everest.Expedition(configuration, recno)
        self.li_routes, self.current, svg, label = expedition.gen_routes()

        titulo = _("Everest")
        icono = Iconos.Trekking()
        extparam = "expedition"
        QTVarios.WDialogo.__init__(self, wowner, titulo, icono, extparam)

        self.selected = False

        wsvg = QtSvg.QSvgWidget()
        wsvg.load(QtCore.QByteArray(svg))
        wsvg.setFixedSize(762, int(762.0 * 520.0 / 1172.0))
        lySVG = Colocacion.H().relleno(1).control(wsvg).relleno(1)

        li_acciones = (
            (_("Climb"), Iconos.Empezar(), self.climb),
            None,
            (_("Close"), Iconos.MainMenu(), self.cancel),
            None,
        )
        tb = Controles.TBrutina(self, li_acciones).vertical()
        if self.current is None:
            tb.setAccionVisible(self.climb, False)

        lyRot = Colocacion.H()
        for elem in label:
            lb_rotulo = Controles.LB(self, elem).align_center()
            lb_rotulo.setStyleSheet(
                "QWidget { border-style: groove; border-width: 2px; border-color: LightSlateGray ;}"
            )
            lb_rotulo.ponTipoLetra(puntos=12, peso=700)
            lyRot.control(lb_rotulo)

        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("ROUTE", _("Route"), 240, centered=True)
        o_columns.nueva("GAMES", _("Games"), 80, centered=True)
        o_columns.nueva("DONE", _("Done"), 80, centered=True)
        o_columns.nueva("TIME", _("Time"), 80, centered=True)
        o_columns.nueva("MTIME", _("Average time"), 80, centered=True)
        o_columns.nueva("MPOINTS", _("Av. lost points"), 80, centered=True)
        o_columns.nueva("TRIES", _("Max tries"), 80, centered=True)
        o_columns.nueva("TOLERANCE", _("Tolerance"), 80, centered=True)
        grid = Grid.Grid(self, o_columns, siSelecFilas=True, siSeleccionMultiple=False)
        grid.setMinimumWidth(grid.anchoColumnas() + 20)
        grid.coloresAlternados()

        lyG = Colocacion.V().otro(lyRot).control(grid).margen(0)

        lyR = Colocacion.H().control(tb).otro(lyG).margen(0)

        ly = Colocacion.V().otro(lySVG).otro(lyR).margen(3)

        self.setLayout(ly)

        self.restore_video(siTam=True, anchoDefecto=784, altoDefecto=670)

    def grid_num_datos(self, grid):
        return 12

    def grid_dato(self, grid, row, o_column):
        return self.li_routes[row][o_column.key]

    def grid_bold(self, grid, row, o_column):
        return self.current is not None and row == self.current

    def grid_doble_click(self, grid, row, o_column):
        if self.current is not None and row == self.current:
            self.climb()

    def gen_routes(self, ev, li_distribution, done_game, tries, tolerances, times):
        li_p = ev.li_points
        li_routes = []
        xgame = done_game + 1
        xcurrent = None
        for x in range(12):
            d = {}
            d["ROUTE"] = "%s - %s" % (li_p[x][4], li_p[x + 1][4])
            xc = li_distribution[x]
            d["GAMES"] = str(xc)
            done = xgame if xc >= xgame else xc
            xgame -= xc
            if xcurrent is None and xgame < 0:
                xcurrent = x

            d["DONE"] = str(done if done > 0 else "0")
            d["TRIES"] = str(tries[x])
            d["TOLERANCE"] = str(tolerances[x])
            seconds = times[x]
            d["TIME"] = "%d' %d\"" % (seconds / 60, seconds % 60)
            mseconds = seconds / done if done > 0 else 0
            d["MTIME"] = "%d' %d\"" % (mseconds / 60, mseconds % 60)
            li_routes.append(d)

        return li_routes, xcurrent

    def climb(self):
        self.save_video()
        self.selected = True
        self.accept()

    def cancel(self):
        self.save_video()
        self.reject()


class WEverest(QTVarios.WDialogo):
    def __init__(self, procesador):

        QTVarios.WDialogo.__init__(
            self, procesador.main_window, _("Expeditions to the Everest"), Iconos.Trekking(), "everestBase"
        )

        self.procesador = procesador
        self.configuration = procesador.configuration

        self.db = Everest.Expeditions(self.configuration)

        self.selected = None

        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("NAME", _("Expedition"), 120, centered=True)
        o_columns.nueva("DATE_INIT", _("Start date"), 120, centered=True)
        o_columns.nueva("DATE_END", _("Final date"), 100, centered=True)
        o_columns.nueva("NUM_GAMES", _("Games"), 80, centered=True)
        o_columns.nueva("TIMES", _("Time"), 120, centered=True)
        o_columns.nueva("TOLERANCE", _("Tolerance"), 90, centered=True)
        o_columns.nueva("TRIES", _("Tries"), 90, centered=True)
        self.grid = Grid.Grid(self, o_columns, siSelecFilas=True, siSeleccionMultiple=True)
        self.grid.setMinimumWidth(self.grid.anchoColumnas() + 20)

        li_acciones = (
            (_("Close"), Iconos.MainMenu(), self.terminar),
            None,
            (_("Start"), Iconos.Empezar(), self.start),
            None,
            (_("New"), Iconos.Nuevo(), self.nuevo),
            None,
            (_("Remove"), Iconos.Borrar(), self.borrar),
            None,
        )
        self.tb = QTVarios.LCTB(self, li_acciones)

        # Colocamos
        lyTB = Colocacion.H().control(self.tb).margen(0)
        ly = Colocacion.V().otro(lyTB).control(self.grid).margen(3)

        self.setLayout(ly)

        self.register_grid(self.grid)
        self.restore_video(siTam=False)

        self.grid.gotop()

    def grid_doble_click(self, grid, fil, col):
        if fil >= 0:
            self.start()

    def grid_num_datos(self, grid):
        return self.db.reccount()

    def grid_dato(self, grid, row, o_column):
        col = o_column.key
        v = self.db.field(row, col)

        # if col in ("NAME", "TOLERANCE", "TRIES"):return v
        if col in ("DATE_INIT", "DATE_END"):
            d = Util.stodext(v)
            v = Util.localDateT(d) if d else ""

        elif col == "TIMES":
            li = eval(v)
            seconds = sum(x for x, p in li)
            done_games = self.db.field(row, "NEXT_GAME")  # next_game is 0 based
            mseconds = seconds // done_games if done_games > 0 else 0
            v = "%d' %d\" / %d' %d\"" % (mseconds // 60, mseconds % 60, seconds // 60, seconds % 60)

        elif col == "NUM_GAMES":
            next_game = self.db.field(row, "NEXT_GAME")
            v = "%d / %d" % (next_game, v)

        return v

    def terminar(self):
        self.save_video()
        self.db.close()
        self.reject()

    def borrar(self):
        li = self.grid.recnosSeleccionados()
        if len(li) > 0:
            if QTUtil2.pregunta(self, _("Do you want to delete all selected records?")):
                self.db.borrar_lista(li)
                self.grid.gotop()
                self.grid.refresh()

    def start(self):
        recno = self.grid.recno()
        if recno >= 0:
            self.save_video()
            self.db.close()
            self.selected = recno
            self.accept()

    def nuevo(self):
        menu = QTVarios.LCMenu(self)

        menu.opcion("tourneys", _("Tourneys"), Iconos.Torneos())
        menu.separador()
        menu.opcion("fide_openings", _("Openings from progressive elo games"), Iconos.Opening())
        menu.separador()
        menu.opcion("gm_openings", _("Openings from GM games"), Iconos.GranMaestro())

        resp = menu.lanza()
        if not resp:
            return
        fichero = Code.path_resource("IntFiles", "Everest", "%s.str" % resp)
        w = WNewExpedition(self, fichero)
        if w.exec_():
            reg = w.selected
            self.db.new(reg)
            self.grid.refresh()


def everest(procesador):
    w = WEverest(procesador)
    if w.exec_():
        procesador.showEverest(w.selected)


def show_expedition(wowner, configuration, recno):
    wexp = WExpedition(wowner, configuration, recno)
    return wexp.exec_()
