from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import FormLayout
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import QTUtil2
from Code.QT import QTVarios


class WResistance(QTVarios.WDialogo):
    def __init__(self, owner, resistance):

        self.resistance = resistance

        # Dialogo ---------------------------------------------------------------
        icono = Iconos.Resistencia()
        titulo = _("Resistance Test")
        tipo = resistance.tipo
        if tipo:
            titulo += "-" + _("Blindfold chess")
            if tipo == "p1":
                titulo += "-" + _("Hide only our pieces")
            elif tipo == "p2":
                titulo += "-" + _("Hide only opponent pieces")
        extparam = "boxing"
        QTVarios.WDialogo.__init__(self, owner, titulo, icono, extparam)
        # self.setStyleSheet("QWidget { background: #AFC3D7 }")

        # Tool bar ---------------------------------------------------------------
        li_acciones = [
            (_("Close"), Iconos.MainMenu(), self.terminar),
            None,
            (_("Remove data"), Iconos.Borrar(), self.borrar),
            None,
            (_("Config"), Iconos.Configurar(), self.configurar),
        ]
        tb = Controles.TBrutina(self, li_acciones, background="#AFC3D7")

        # Texto explicativo ----------------------------------------------------
        self.lb = Controles.LB(self)
        self.set_textAyuda()
        self.lb.set_background("#F5F0CF")

        # Lista
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("ENGINE", _("Engine"), 198)
        o_columns.nueva("WHITE", _("White"), 200, centered=True)
        o_columns.nueva("BLACK", _("Black"), 200, centered=True)

        self.grid = grid = Grid.Grid(self, o_columns, siSelecFilas=True, background=None)
        self.grid.coloresAlternados()
        self.register_grid(grid)

        # Layout
        lyB = Colocacion.V().controlc(self.lb).control(self.grid).margen(3)
        layout = Colocacion.V().control(tb).otro(lyB).margen(0)
        self.setLayout(layout)

        self.restore_video(siTam=True, anchoDefecto=677, altoDefecto=562)

        self.grid.gotop()

        self.grid.setFocus()
        self.resultado = None

    def set_textAyuda(self):
        txt = self.resistance.rotuloActual()
        self.lb.set_text(
            '<center><b>%s<br><font color="red">%s</red></b></center>'
            % (txt, _("Double click in any cell to begin to play"))
        )

    def grid_num_datos(self, grid):
        return self.resistance.num_engines()

    def grid_dato(self, grid, row, o_column):
        key = o_column.key
        if key == "ENGINE":
            return self.resistance.dameEtiEngine(row)
        else:
            return self.resistance.dameEtiRecord(key, row)

    def grid_doble_click(self, grid, row, column):
        key = column.key
        if key != "ENGINE":
            self.play(key)

    def play(self, key):
        self.save_video()
        self.resultado = self.grid.recno(), key
        self.accept()

    def borrar(self):
        numEngine = self.grid.recno()
        if QTUtil2.pregunta(self, _X(_("Remove data from %1 ?"), self.resistance.dameEtiEngine(numEngine))):
            self.resistance.borraRegistros(numEngine)

    def terminar(self):
        self.save_video()
        self.accept()

    def configurar(self):
        segundos, puntos, maxerror = self.resistance.actual()

        separador = FormLayout.separador

        liGen = [separador]

        config = FormLayout.Spinbox(_("Time in seconds"), 1, 99999, 80)
        liGen.append((config, segundos))

        liGen.append(separador)

        config = FormLayout.Spinbox(_("Max lost points in total"), 10, 99999, 80)
        liGen.append((config, puntos))

        liGen.append(separador)

        config = FormLayout.Spinbox(
            _("Max lost points in a single move") + ":\n" + _("0 = not consider this limit"), 0, 1000, 80
        )
        liGen.append((config, maxerror))

        resultado = FormLayout.fedit(liGen, title=_("Config"), parent=self, icon=Iconos.Configurar())
        if resultado:
            accion, liResp = resultado
            segundos, puntos, maxerror = liResp
            self.resistance.cambiaconfiguration(segundos, puntos, maxerror)
            self.set_textAyuda()
            self.grid.refresh()
            return liResp[0]


def windowResistance(window, resistance):
    w = WResistance(window, resistance)
    if w.exec_():
        return w.resultado
    else:
        return None