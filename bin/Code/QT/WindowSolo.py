from Code import TrListas
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Delegados
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import QTVarios
from Code.Base.Constantes import STANDARD_TAGS


class WEtiquetasPGN(QTVarios.WDialogo):
    def __init__(self, procesador, liPGN):
        titulo = _("Edit PGN labels")
        icono = Iconos.PGN()
        extparam = "editlabels"
        self.listandard = STANDARD_TAGS

        QTVarios.WDialogo.__init__(self, procesador.main_window, titulo, icono, extparam)
        self.procesador = procesador
        self.creaLista(liPGN)

        # Toolbar
        liAccionesWork = (
            (_("Accept"), Iconos.Aceptar(), self.aceptar),
            None,
            (_("Cancel"), Iconos.Cancelar(), self.cancelar),
            None,
            (_("Up"), Iconos.Arriba(), self.arriba),
            None,
            (_("Down"), Iconos.Abajo(), self.abajo),
            None,
        )
        tbWork = QTVarios.LCTB(self, liAccionesWork, icon_size=24)

        # Lista
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("ETIQUETA", _("Label"), 150, edicion=Delegados.LineaTextoUTF8())
        o_columns.nueva("VALOR", _("Value"), 400, edicion=Delegados.LineaTextoUTF8())

        self.grid = Grid.Grid(self, o_columns, siEditable=True)
        n = self.grid.anchoColumnas()
        self.grid.setFixedWidth(n + 20)
        self.register_grid(self.grid)

        # Layout
        layout = Colocacion.V().control(tbWork).control(self.grid).margen(3)
        self.setLayout(layout)

        self.restore_video()

    def creaLista(self, liPGN):
        st = {eti for eti, val in liPGN}

        li = [[k, v] for k, v in liPGN]
        for eti in self.listandard:
            if not (eti in st):
                li.append([eti, ""])
        while len(li) < 30:
            li.append(["", ""])
        self.liPGN = li

    def aceptar(self):
        dic_rev = {}
        for eti in self.listandard:
            dic_rev[TrListas.pgnLabel(eti.upper())] = eti

        for n, (eti, val) in enumerate(self.liPGN):
            if eti in dic_rev:
                self.liPGN[n][0] = dic_rev[eti]

        li = []
        st = set()
        for n, (eti, val) in enumerate(self.liPGN):
            val = val.strip()
            if not (eti in st) and val:
                st.add(eti)
                li.append((eti, val))
        self.liPGN = li

        self.save_video()
        self.accept()

    def closeEvent(self, event):
        self.save_video()

    def cancelar(self):
        self.save_video()
        self.reject()

    def grid_num_datos(self, grid):
        return len(self.liPGN)

    def grid_setvalue(self, grid, row, o_column, valor):
        col = 0 if o_column.key == "ETIQUETA" else 1
        try:
            self.liPGN[row][col] = valor
        except:
            pass

    def grid_dato(self, grid, row, o_column):
        if o_column.key == "ETIQUETA":
            lb = self.liPGN[row][0]
            ctra = lb.upper()
            trad = TrListas.pgnLabel(lb)
            if trad != ctra:
                key = trad
            else:
                if lb:
                    key = lb  # [0].upper()+lb[1:].lower()
                else:
                    key = ""
            return key
        return self.liPGN[row][1]

    def arriba(self):
        recno = self.grid.recno()
        if recno:
            self.liPGN[recno], self.liPGN[recno - 1] = self.liPGN[recno - 1], self.liPGN[recno]
            self.grid.goto(recno - 1, 0)
            self.grid.refresh()

    def abajo(self):
        n0 = self.grid.recno()
        if n0 < len(self.liPGN) - 1:
            n1 = n0 + 1
            self.liPGN[n0], self.liPGN[n1] = self.liPGN[n1], self.liPGN[n0]
            self.grid.goto(n1, 0)
            self.grid.refresh()


def editEtiquetasPGN(procesador, liPGN):
    w = WEtiquetasPGN(procesador, liPGN)
    if w.exec_():
        li = []
        for eti, valor in w.liPGN:
            if (len(eti.strip()) > 0) and (len(valor.strip()) > 0):
                li.append([eti, valor])
        return li
    else:
        return None
