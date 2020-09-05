import os
import os.path
import datetime
import shutil

from Code import Util
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code.QT import FormLayout
from Code.Polyglots import WPolyglot


class WFactoryPolyglots(QTVarios.WDialogo):
    def __init__(self, procesador):

        self.procesador = procesador
        self.configuration = procesador.configuration
        self.resultado = None
        self.lista_names, self.dict_data = self.lee_lista()

        QTVarios.WDialogo.__init__(
            self, procesador.main_window, "Polyglot book factory", Iconos.FactoryPolyglot(), "factorypolyglots"
        )

        o_columnas = Columnas.ListaColumnas()
        o_columnas.nueva("NAME", _("Name"), 240)
        o_columnas.nueva("MTIME", _("Last modification"), 100, centered=True)
        o_columnas.nueva("SIZE", _("Size"), 100, siDerecha=True)
        self.glista = Grid.Grid(self, o_columnas, siSelecFilas=True, siSeleccionMultiple=True)

        li_acciones = (
            (_("Close"), Iconos.MainMenu(), self.terminar),
            None,
            (_("Edit"), Iconos.Modificar(), self.edit),
            None,
            (_("New"), Iconos.Nuevo(), self.new),
            None,
            (_("Copy"), Iconos.Copiar(), self.copy),
            None,
            (_("Rename"), Iconos.Modificar(), self.renombrar),
            None,
            (_("Remove"), Iconos.Borrar(), self.borrar),
            None,
        )
        tb = QTVarios.LCTB(self, li_acciones)

        ly = Colocacion.V().control(tb).control(self.glista).margen(4)
        self.setLayout(ly)

        self.register_grid(self.glista)
        self.restore_video(anchoDefecto=self.glista.anchoColumnas() + 20)

        self.glista.gotop()

    def lee_lista(self):
        d = {}
        with os.scandir(self.configuration.folder_polyglots_factory()) as it:
            for entry in it:
                if entry.is_file():
                    name = entry.name
                    name_base = entry.name[:-6]
                    ns = entry.stat().st_mtime
                    if name.endswith(".dbbin") or name.endswith(".mkbin"):
                        if not (name_base in d):
                            d[name_base] = [None, None, ns]
                        d[name_base][0 if name.endswith(".dbbin") else 1] = entry
                        if d[name_base][2] < ns:
                            d[name_base][2] = ns
        li = list(d.keys())
        li.sort(key=lambda x: d[x][2], reverse=True)

        return li, d

    def edit(self):
        recno = self.glista.recno()
        if recno >= 0:
            self.run_edit(self.dict_data[self.lista_names[recno]][0].path)

    def grid_doble_click(self, grid, row, o_columna):
        self.edit()

    def run_edit(self, path):
        self.resultado = path
        self.save_video()
        self.accept()

    def get_new_path(self, name):
        while True:
            form = FormLayout.FormLayout(self, _("New polyglot book"), Iconos.Book(), anchoMinimo=340)
            form.separador()
            form.filename(_("Name"), name)
            form.separador()
            resp = form.run()
            if resp:
                name = resp[1][0]
                path = os.path.join(self.configuration.folder_polyglots_factory(), name + ".dbbin")
                if os.path.isfile(path):
                    QTUtil2.message_error(self, "%s/n%s" % (_("This file already exists"), path))
                else:
                    return os.path.realpath(path)
            else:
                return None

    def new(self):
        path = self.get_new_path("")
        if path:
            self.run_edit(path)

    def copy(self):
        recno = self.glista.recno()
        if recno >= 0:
            path = self.get_new_path(self.lista_names[recno].name)
            if path:
                shutil.copy(self.lista_names[recno].path, path)
                self.glista.refresh()

    def renombrar(self):
        row = self.glista.recno()
        if row >= 0:
            op = self.listaOpenings[row]
            name = self.get_nombre(op["title"])
            if name:
                self.listaOpenings.change_title(row, name)
                self.glista.refresh()

    def borrar(self):
        li = self.glista.recnosSeleccionados()
        if len(li) > 0:
            mens = _("Do you want to delete all selected records?")
            mens += "\n"
            for num, row in enumerate(li, 1):
                mens += "\n%d. %s" % (num, self.lista_names[row])
            if QTUtil2.pregunta(self, mens):
                li.sort(reverse=True)
                for row in li:
                    name = self.lista_names[row]
                    entry_dbbin, entry_mkbin, ms = self.dict_data[name]
                    Util.remove_file(entry_dbbin.path)
                    if entry_mkbin:
                        Util.remove_file(entry_mkbin.path)
                    del self.lista_names[row]
                self.glista.refresh()

    def grid_num_datos(self, grid):
        return len(self.lista_names)

    def grid_dato(self, grid, row, o_columna):
        col = o_columna.key
        name = self.lista_names[row]
        entry_dbbin, entry_mkbin, ms = self.dict_data[name]
        if col == "NAME":
            return name
        elif col == "MTIME":
            return Util.localDateT(datetime.datetime.fromtimestamp(ms))
        elif col == "SIZE":
            sz_mk = entry_mkbin.stat().st_size if entry_mkbin else 0
            return "{:,}".format(sz_mk // 16).replace(",", ".")

    def closeEvent(self, event):  # Cierre con X
        self.save_video()

    def terminar(self):
        self.save_video()
        self.accept()


def polyglots_factory(procesador):
    w = WFactoryPolyglots(procesador)
    return w.resultado if w.exec_() else None


def edit_polyglot(procesador, path_dbbin):
    w = WPolyglot.WPolyglot(procesador.main_window, procesador.configuration, path_dbbin)
    w.exec_()
