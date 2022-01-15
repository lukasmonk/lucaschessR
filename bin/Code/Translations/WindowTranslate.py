import datetime
import os
import shutil
import traceback

import polib
from PySide2 import QtCore

import Code
from Code import Util
from Code.Base.Constantes import TB_QUIT
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Delegados
from Code.QT import FormLayout
from Code.QT import Grid
from Code.QT import Iconos
from Code.QT import LCDialog
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code.QT import SelectFiles


class WTranslate(LCDialog.LCDialog):
    REORDER_ALL = 1
    REORDER_UNTRANSLATED = 2

    TRANSLATION_HELP = "TRANSLATION_HELP"
    AUTOMATIC_REORDER = "AUTOMATIC_REORDER"
    REORDER_TYPE = "REORDER_TYPE"
    MAIN_REFERENCE = "MAIN_REFERENCE"
    SECONDARY_REFERENCES = "SECONDARY_REFERENCES"

    def __init__(self, owner):
        icono = Iconos.WorldMap()
        titulo = "Translation"
        extparam = "translation"
        LCDialog.LCDialog.__init__(self, None, titulo, icono, extparam)

        self.main_window = owner
        self.configuration = Code.configuration

        self.automatic_reorder = self.get_param(self.AUTOMATIC_REORDER, True)
        self.reorder_type = self.get_param(self.REORDER_TYPE, self.REORDER_ALL)
        self.main_reference = self.get_param(self.MAIN_REFERENCE, "")
        self.secondary_references = self.get_param(self.SECONDARY_REFERENCES, [])

        li_traducciones = self.configuration.list_translations()
        self.tr_actual = self.configuration.translator()
        self.language = "English"
        for key, lng, porc, autor in li_traducciones:
            if key == self.tr_actual:
                self.language = lng

        self.dic_languages = {}
        self.read_languages()
        self.dic_translate = self.read_labels()
        self.li_labels = list(self.dic_translate.keys())
        self.ult_where = ["?", "?", "?"]  # Que no encuentre a nadie

        self.color_new = QTUtil.qtColor("#840C24")
        self.color_ult = QTUtil.qtColor("#90caff")

        li_acciones = (
            ("Close", Iconos.FinPartida(), self.cerrar),
            None,
            ("Edit", Iconos.EditColumns(), self.editar),
            None,
            ("Config", Iconos.Configurar(), self.config),
            None,
            ("Utilities", Iconos.Utilidades(), self.utilities),
        )
        self.tb = QTVarios.LCTB(self, li_acciones, icon_size=24)

        self.lb_porcentage = Controles.LB(self, "").ponTipoLetra(puntos=20, peso=300).anchoFijo(150).align_right()

        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("CURRENT", self.language, 280, edicion=Delegados.LineaTextoUTF8(), siEditable=True)
        o_columns.nueva("BASE", "To translate", 280)

        self.grid = None
        self.grid = Grid.Grid(self, o_columns, altoFila=Code.configuration.x_pgn_rowheight, siEditable=True)
        self.grid.tipoLetra(puntos=10)
        self.grid.setAlternatingRowColors(False)
        self.register_grid(self.grid)

        self.lb_seek = Controles.LB(self, "Find (Ctrl F):").ponTipoLetra(puntos=10).anchoFijo(74)
        self.ed_seek = Controles.ED(self, "").ponTipoLetra(puntos=10).capture_enter(self.siguiente)
        self.f3_seek = Controles.PB(self, "F3", self.siguiente, plano=False).ponTipoLetra(puntos=10).anchoFijo(30)
        ly_seek = Colocacion.H().control(self.lb_seek).control(self.ed_seek).control(self.f3_seek).margen(0)

        laytb = Colocacion.H().control(self.tb).control(self.lb_porcentage)
        layout = Colocacion.V().otro(laytb).control(self.grid).otro(ly_seek).margen(3)
        self.setLayout(layout)

        self.restore_video(anchoDefecto=self.grid.anchoColumnas() + 28, altoDefecto=self.main_window.height())
        self.grid.setFocus()

        self.set_porcentage()

        self.orders = {"BASE": 0, "CURRENT": 0, "WHERE": 0}
        self.order_by_type("CURRENT")
        # self.li_labels.sort(key=lambda x:x.upper())

    def current(self, english_text):
        dic = self.dic_translate[english_text]

        x = traceback.format_stack()[-3]
        x0 = x.split('"')[1]
        li = x0.split(os.sep)
        li = li[li.index("bin") + 1 :]
        where = "\\".join(li)[:-3]
        if where.startswith("Code"):
            where = "." + where[4:] + ".py"
        # xc = x.split(",")[1][6:]

        dic["WHEN"] = datetime.datetime.now()
        where = "|%s|" % where
        if where not in self.ult_where:
            del self.ult_where[0]
            self.ult_where.append(where)

        if dic["NEW"]:
            traduccion = dic["NEW"]
        elif dic["TRANS"]:
            traduccion = dic["TRANS"]
        else:
            traduccion = Code.bridge_translation(english_text)

        if self.automatic_reorder:
            if self.reorder_type == self.REORDER_ALL:
                ok = True
            else:
                ok = not (dic["NEW"] or dic["TRANS"])
            if ok:
                self.li_labels.remove(english_text)
                self.li_labels.insert(0, english_text)

        self.grid.refresh()

        return traduccion

    def read_labels(self):
        path_po = Code.path_resource("IntFiles", "messages.po")
        pofile = polib.pofile(path_po)

        path_mo = Code.path_resource("Locale", self.tr_actual, "LC_MESSAGES", "lucaschess.mo")
        mofile = polib.mofile(path_mo)
        dmo = {entry.msgid: entry.msgstr for entry in mofile}

        path_po_saved = self.configuration.po_saved()
        if os.path.isfile(path_po_saved):
            pofile_saved = polib.pofile(path_po_saved)
            dpo_saved = {entry.msgid: entry.msgstr for entry in pofile_saved}
        else:
            dpo_saved = {}

        dic_translate = {}
        now = datetime.datetime.now()
        for entry in pofile:
            trans = dmo.get(entry.msgid, "")
            new = dpo_saved.get(entry.msgid, "")
            if entry.occurrences:
                li_occurrences = []
                li = []
                for rut, linea in entry.occurrences:
                    if rut in li:
                        li_occurrences[li.index(rut)][1].append(int(linea))
                    else:
                        li.append(rut)
                        li_occurrences.append([rut, [int(linea)]])
            else:
                li_occurrences = [("Web", [])]

            where = "|".join(rut for rut, lineas in li_occurrences)

            if trans == new:
                new = ""
            dic_translate[entry.msgid] = {
                "TRANS": trans,
                "NEW": new,
                "WHERE": "|%s|" % where,
                "LI_OCCURRENCES": li_occurrences,
                "WHEN": now,
            }

        return dic_translate

    def set_porcentage(self):
        total = len(self.dic_translate)
        traducidos = 0
        for key, dic in self.dic_translate.items():
            if dic["TRANS"] or dic["NEW"]:
                traducidos += 1

        self.lb_porcentage.setText("%0.02f%%" % (traducidos * 100 / total))

    def save(self):
        self.create_po(self.configuration.po_saved())

    def create_po(self, path_po):
        po = polib.POFile()
        po.metadata = {
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Transfer-Encoding": "8bit",
        }
        for key, dic in self.dic_translate.items():
            if dic["NEW"]:
                entry = polib.POEntry(msgid=key, msgstr=dic["NEW"])
                po.append(entry)
        po.save(path_po)

    def terminar(self):
        self.save()
        Code.win_translator = None
        self.accept()
        Code.procesador.run_action(TB_QUIT)

    def cerrar(self):
        self.save()
        self.hide()

    def closeEvent(self, event):
        self.save()
        Code.win_translator = None
        Code.procesador.run_action(TB_QUIT)

    def grid_num_datos(self, grid):
        return len(self.li_labels)

    def grid_dato(self, grid, fila, o_col):
        clave = o_col.key
        key = self.li_labels[fila]
        dic = self.dic_translate[key]
        if clave == "BASE":
            if self.main_reference:
                key = self.dic_languages[self.main_reference].get(key, key)
            return key
        elif clave == "CURRENT":
            return dic["NEW"] if dic["NEW"] else dic["TRANS"]

    def grid_setvalue(self, grid, fila, o_col, value):
        auto_reorder = self.automatic_reorder
        self.automatic_reorder = False

        key = self.li_labels[fila]
        dic = self.dic_translate[key]
        if value:
            li_porc = ["%1", "%2", "%3", "%s", "%d"]

            def calc(txt):
                dporc = {}
                for xkey in li_porc:
                    dporc[xkey] = txt.count(xkey)
                return txt.count("%"), dporc

            ori_porc, ori_dic = calc(key)
            tra_porc, tra_dic = calc(value)
            if ori_porc != tra_porc:
                QTUtil2.message_error(self, "The % number does not match the English text.")
                self.automatic_reorder = auto_reorder
                return
            for k in li_porc:
                if ori_dic[k] != tra_dic[k]:
                    QTUtil2.message_error(self, "The command %s does not match the English text." % k)
                    self.automatic_reorder = auto_reorder
                    return
            if "{" in key:
                if "{" in value or "}" in value:
                    QTUtil2.message_error(
                        self,
                        "The text between braces should not be translated, it is only explanatory and to differentiate"
                        " English words that have different meanings depending on the context.",
                    )
                    self.automatic_reorder = auto_reorder
                    return
            if value != dic["TRANS"]:
                dic["NEW"] = value
                self.set_porcentage()
        else:
            dic["NEW"] = ""

        self.automatic_reorder = auto_reorder

    def grid_color_texto(self, grid, row, o_column):
        if o_column.key == "CURRENT":
            key = self.li_labels[row]
            dic = self.dic_translate[key]
            if dic["NEW"]:
                return self.color_new

    def grid_color_fondo(self, grid, row, o_column):
        if o_column.key == "BASE":
            key = self.li_labels[row]
            dic = self.dic_translate[key]
            if (
                self.ult_where[0] in dic["WHERE"]
                or self.ult_where[1] in dic["WHERE"]
                or self.ult_where[2] in dic["WHERE"]
            ):
                return self.color_ult

    def grid_bold(self, grid, row, o_column):
        if o_column.key == "CURRENT":
            key = self.li_labels[row]
            dic = self.dic_translate[key]
            return dic["NEW"]

    def menu_occurrences(self, row):
        key = self.li_labels[row]
        li_occur = self.dic_translate[key]["LI_OCCURRENCES"]
        if not li_occur:
            return
        menu = QTVarios.LCMenu(self)
        menu.opcion("edit", "Edit", Iconos.EditColumns())
        menu.separador()
        submenu = menu.submenu("Show sentences in the same code file", Iconos.Carpeta())
        for txt, linea in li_occur:
            submenu.opcion(txt, "%s %s" % (txt, linea))
        rut = menu.lanza()
        if rut == "edit":
            self.editar()
        elif rut:
            where = "|%s|" % rut
            if where not in self.ult_where:
                del self.ult_where[0]
                self.ult_where.append(where)
            li_rut = []
            li_rest = []
            for key in self.li_labels:
                ok = False
                li_occur = self.dic_translate[key]["LI_OCCURRENCES"]
                if li_occur:
                    for cur_rut, linea in li_occur:
                        if cur_rut == rut:
                            ok = True
                            break
                if ok:
                    li_rut.append(key)
                else:
                    li_rest.append(key)
            self.li_labels = li_rut
            self.li_labels.extend(li_rest)
            self.grid.refresh()
            self.grid.gotop()

    def menu_secondary(self, row):
        auto = self.automatic_reorder
        self.automatic_reorder = False

        def l80(txt):
            if len(txt) > 80:
                return txt[:76] + " ..."
            return txt

        key = self.li_labels[row]
        current_new = self.dic_translate[key]["NEW"]
        current_trans = self.dic_translate[key]["TRANS"]
        current = current_new or current_trans
        li_opciones = []

        def add_opcion(xlng):
            xvalue = self.dic_languages[xlng].get(key)
            if xvalue and xvalue not in li_opciones and xvalue != current:
                li_opciones.append(xvalue)

        for lng in self.secondary_references:
            add_opcion(lng)

        if self.main_reference:
            add_opcion(self.main_reference)

        add_opcion(self.tr_actual)

        if key not in li_opciones:
            li_opciones.append(key)

        if not li_opciones:
            return

        menu = QTVarios.LCMenu(self)

        for xvalue in li_opciones:
            menu.opcion(xvalue, l80(xvalue))
            menu.separador()

        txt = menu.lanza()
        if txt:
            current_new = self.dic_translate[key]["NEW"]
            current_trans = self.dic_translate[key]["TRANS"]
            ask = False
            ok = False
            if current_new:
                ask = current_new != txt
            elif current_trans:
                ask = current_trans != txt
            else:
                ok = True
            if ask:
                ok = QTUtil2.pregunta(self, "Do you want to replace current translation?\n\nChange to:\n%s" % txt)

            if ok:
                self.dic_translate[key]["NEW"] = "" if txt == current_trans else txt
                self.grid.refresh()

        self.automatic_reorder = auto

    def grid_right_button(self, grid, row, o_column, modificadores):
        if row < 0:
            return
        if o_column.key == "CURRENT":
            self.menu_occurrences(row)
        elif o_column.key == "BASE":
            self.menu_secondary(row)

    def order_by_type(self, key_col):
        order = self.orders[key_col]
        if key_col == "BASE":

            def order_english(key):
                return key.upper()

            if order == 0:
                self.li_labels.sort(key=order_english, reverse=True)
            elif order == 1:
                self.li_labels.sort(key=order_english)
                order = -1

        elif key_col == "CURRENT":

            def order_current(key):
                new = self.dic_translate[key]["NEW"].upper()
                trans = self.dic_translate[key]["TRANS"].upper()

                if new:
                    orden = "B" + new
                else:
                    # primero los que no tienen nada
                    if not trans:
                        orden = "A" + key
                    else:
                        orden = "C" + trans
                return orden

            def order_current_new(key):
                new = self.dic_translate[key]["NEW"].upper()
                trans = self.dic_translate[key]["TRANS"].upper()
                if new:
                    orden = "A" + new
                else:
                    if not trans:
                        orden = "B" + key
                    else:
                        orden = "C" + trans
                return orden

            if order == 0:
                self.li_labels.sort(key=order_current)
            elif order == 1:
                self.li_labels.sort(key=order_current_new)
                order = -1

        self.orders[key_col] = order + 1
        self.grid.refresh()
        self.grid.gotop()

    def grid_doubleclick_header(self, grid, o_col):
        key_col = o_col.key
        self.order_by_type(key_col)

    def config(self):
        menu = QTVarios.LCMenu(self)
        submenu = menu.submenu("Reordering", Iconos.SortAZ())
        subsubmenu = submenu.submenu("Automatic reordering", Iconos.PuntoVerde())
        subsubmenu.opcion("enabled", "Enabled", siChecked=self.automatic_reorder)
        subsubmenu.separador()
        subsubmenu.opcion("disabled", "Disabled", siChecked=not self.automatic_reorder)
        submenu.separador()
        subsubmenu = submenu.submenu("What to reorder", Iconos.PuntoAzul())
        subsubmenu.opcion("reorder_all", "Reorder all", siChecked=self.reorder_type == self.REORDER_ALL)
        subsubmenu.opcion(
            "reorder_untranslated",
            "Reorder only untranslated",
            siChecked=self.reorder_type == self.REORDER_UNTRANSLATED,
        )

        li_traducciones = self.configuration.list_translations()
        li_trans = []
        for k, trad, porc, author in li_traducciones:
            li_trans.append((trad, k))

        menu.separador()
        submenu = menu.submenu("Reference language", Iconos.Reference())
        subsubmenu = submenu.submenu("Main reference", Iconos.PuntoMagenta())
        li_ref = [("Default", "")]
        li_ref.extend(li_trans)
        for trad, key in li_ref:
            subsubmenu.opcion("main" + key, trad, siChecked=key == self.main_reference)

        submenu.separador()
        subsubmenu = submenu.submenu("Secondary reference", Iconos.PuntoAmarillo())
        for trad, key in li_trans:
            subsubmenu.opcion("sec" + key, trad, siChecked=key in self.secondary_references)

        resp = menu.lanza()
        if not resp:
            return
        elif resp == "disabled":
            self.automatic_reorder = False
            self.set_param(self.AUTOMATIC_REORDER, self.automatic_reorder)
        elif resp == "enabled":
            self.automatic_reorder = True
            self.set_param(self.AUTOMATIC_REORDER, self.automatic_reorder)
        elif resp == "reorder_all":
            self.reorder_type = self.REORDER_ALL
            self.set_param(self.REORDER_TYPE, self.reorder_type)
        elif resp == "reorder_untranslated":
            self.reorder_type = self.REORDER_UNTRANSLATED
            self.set_param(self.REORDER_TYPE, self.reorder_type)
        elif resp.startswith("main"):
            self.main_reference = resp[4:]
            self.set_param(self.MAIN_REFERENCE, self.main_reference)
            self.read_languages()
            self.grid.refresh()
        elif resp.startswith("sec"):
            ref = resp[3:]
            if ref in self.secondary_references:
                self.secondary_references.remove(ref)
            else:
                self.secondary_references.append(ref)
            self.set_param(self.SECONDARY_REFERENCES, self.secondary_references)
            self.read_languages()

    def siguiente(self):
        pos = self.grid.recno()
        txt = self.ed_seek.texto().strip().upper()
        mirar = list(range(pos + 1, len(self.li_labels)))
        mirar.extend(range(pos + 1))

        for row in mirar:
            key = self.li_labels[row]
            ok = False
            if txt in key.upper():
                ok = True
            else:
                dic = self.dic_translate[key]
                ok = txt in dic["NEW"].upper() or txt in dic["TRANS"].upper()

            if ok:
                self.grid.goto(row, 0)
                self.grid.setFocus()
                return

    def keyPressEvent(self, event):
        k = event.key()
        m = int(event.modifiers())

        if k == QtCore.Qt.Key_F3:
            self.siguiente()

        elif k == QtCore.Qt.Key_F and (m & QtCore.Qt.ControlModifier) > 0:
            self.ed_seek.setFocus()

        elif k == QtCore.Qt.Key_Delete:
            row = self.grid.recno()
            if row >= 0:
                key = self.li_labels[row]
                self.dic_translate[key]["NEW"] = ""
                self.grid.refresh()

    def editar(self):
        row = self.grid.recno()
        label = self.li_labels[row]
        current = self.dic_translate[label]

        form = FormLayout.FormLayout(
            self, "Translate", Iconos.WorldMap(), anchoMinimo=500, font_txt=Controles.TipoLetra(puntos=10)
        )
        form.apart("Original")
        form.apart_nothtml_np(label)
        if "<" in label:
            form.apart("Result")
            form.apart_simple_np(label)
        form.separador()
        form.editbox("Translation", alto=10, init_value=current["NEW"] if current["NEW"] else current["TRANS"])
        form.separador()
        form.apart_simple_np("Remember that you can edit directly in the table by double-clicking on it")
        resultado = form.run()
        if resultado is None:
            return None
        accion, li_resp = resultado
        row = self.li_labels.index(label)  # necesario ya que puede cambiar
        self.grid_setvalue(None, row, None, li_resp[0])

    def utilities(self):
        menu = QTVarios.LCMenu(self)
        menu.opcion(self.export_po, "Export translated labels to a .po file", Iconos.Export8())
        menu.separador()
        menu.opcion(self.import_mo, "Import .mo file downloaded from poeditor", Iconos.Import8())
        menu.separador()

        submenu = menu.submenu("New language", Iconos.LanguageNew())
        submenu.opcion(self.new_lng, "Register a new language", Iconos.Add())
        submenu.separador()

        li_traducciones = self.configuration.list_translations()
        li_remove = []
        for k, trad, porc, author in li_traducciones:
            if k[1].isdigit() and k != self.tr_actual:
                li_remove.append((k, trad))

        if li_remove:
            subsubmenu = submenu.submenu("Remove a created language", Iconos.Remove1())
            for k, trad in li_remove:
                subsubmenu.opcion((k, trad), trad, Iconos.PuntoRojo())
                subsubmenu.separador()

        resp = menu.lanza()
        if resp:
            if type(resp) == tuple:
                self.remove_lng(resp[0], resp[1])
            else:
                resp( )

    def remove_lng(self, lng, name):
        if QTUtil2.pregunta(self, "Are you sure to remove %s?" % name):
            folder_lng = Code.path_resource("Locale", lng)
            folder_mo = os.path.join(folder_lng, "LC_MESSAGES")
            path_po_saved = os.path.join(self.configuration.carpeta_translations(), "%s.po" % lng)
            ok = Util.remove_folder_files(folder_mo)
            if ok:
                ok = Util.remove_folder_files(folder_lng)
            if ok:
                Util.remove_file(path_po_saved)
                QTUtil2.message(self, "Language %s, removed" % name)

            else:
                QTUtil2.message_error(self, "It is not possible to remove %s language" % name)

    def new_lng(self):
        name = ""
        lng_copy = None
        li_traducciones = self.configuration.list_translations()
        li_trans = [("None", None)]
        for k, trad, porc, author in li_traducciones:
            label = "%s (%s%%)" % (trad, porc)
            li_trans.append((label, k))

        while True:
            form = FormLayout.FormLayout(
                self, "New language", Iconos.WorldMap(), anchoMinimo=300, font_txt=Controles.TipoLetra(puntos=10)
            )
            form.separador()
            form.edit("Language name", name)
            form.separador()
            form.combobox("Copy from", li_trans, lng_copy)
            form.separador()
            resultado = form.run()
            if resultado is None:
                return
            accion, li_resp = resultado
            name, lng_copy = li_resp
            name = name.strip()
            if not name:
                return
            problem = False
            for k, trad, porc, author in li_traducciones:
                if name.upper() == trad.upper():
                    problem = True
                    break
            if problem:
                QTUtil2.message_error(self, "This name is already in use")
            else:
                return self.create_lng(name, lng_copy)

    def create_lng(self, name, lng_copy):
        for c1 in "abcdefghijklmnopqrstuvwxyz":
            for c2 in "123456789":
                lng = c1 + c2
                folder = Code.path_resource("Locale", lng)
                if not os.path.isdir(folder) and not os.path.isfile(folder):
                    break
        folder_lng = Code.path_resource("Locale", lng)
        Util.create_folder(folder_lng)
        folder_mo = os.path.join(folder_lng, "LC_MESSAGES")
        Util.create_folder(folder_mo)
        path_mo = os.path.join(folder_mo, "lucaschess.mo")

        po = polib.POFile()
        po.metadata = {
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=utf-8",
            "Content-Transfer-Encoding": "8bit",
        }
        po.save_as_mofile(path_mo)

        path_ini = os.path.join(folder_lng, "lang.ini")
        with open(path_ini, "wt", encoding="utf-8") as q:
            q.write("NAME=%s\n" % name)
            q.write("AUTHOR=%s\n" % self.configuration.nom_player())
            q.write("%=100\n")

        if lng_copy:
            po = polib.POFile()
            po.metadata = {
                "MIME-Version": "1.0",
                "Content-Type": "text/plain; charset=utf-8",
                "Content-Transfer-Encoding": "8bit",
            }

            path_mo = Code.path_resource("Locale", lng_copy, "LC_MESSAGES", "lucaschess.mo")
            mofile = polib.mofile(path_mo)
            for entry in mofile:
                nentry = polib.POEntry(msgid=entry.msgid, msgstr=entry.msgstr)
                po.append(nentry)

            path_po = os.path.join(self.configuration.carpeta_translations(), "%s.po" % lng)
            po.save(path_po)

        self.configuration.set_translator(lng)
        self.configuration.graba()
        QTUtil2.message(self, "Created the new language\n\n")
        Code.win_translator = None
        self.accept()
        Code.procesador.reiniciar()

    def export_po(self):
        message = (
            "This option creates a file that can be imported "
            "from the poeditor website to complete the public translation.\n\n"
            "First the name and location of the file will be requested.\n"
            "Then an explorer is opened in the folder where the file is located "
            "to make it easier to send it to poeditor.com.\n"
        )

        if not QTUtil2.pregunta(self, message, label_yes="Continue", label_no="Cancel"):
            return

        folder = self.configuration.read_variables("PATH_PO")
        if not folder or not os.path.isdir(folder):
            folder = self.configuration.carpeta_translations()
        path_po = SelectFiles.salvaFichero(self, "Save .po file", folder, "po")
        if path_po:
            path_po = os.path.abspath(path_po)
            if not path_po.endswith(".po"):
                path_po += ".po"
            folder = os.path.dirname(path_po)
            self.configuration.write_variables("PATH_PO", folder)
            self.create_po(path_po)
            QTUtil2.message(self, "Created\n%s" % path_po)
            Code.startfile(folder)

    def import_mo(self):
        message = (
            "The utility of this option is to import a .mo file that has been exported from poeditor.com, "
            "and set it as the general translation of the program, "
            "which works when this translation window is not active.\n"
        )

        if not QTUtil2.pregunta(self, message, label_yes="Continue", label_no="Cancel"):
            return

        folder = self.configuration.read_variables("PATH_MO")
        if not folder or not os.path.isdir(folder):
            folder = self.configuration.carpeta_translations()
        path_mo = SelectFiles.leeFichero(self, folder, "mo", ".mo file downloaded from poeditor")
        if path_mo:
            path_mo = os.path.abspath(path_mo)
            folder = os.path.dirname(path_mo)
            self.configuration.write_variables("PATH_MO", folder)
            path_mo_ori = Code.path_resource("Locale", self.tr_actual, "LC_MESSAGES", "lucaschess.mo")
            shutil.copy(path_mo, path_mo_ori)
            self.dic_translate = self.read_labels()
            for dic in self.dic_translate.values():
                if dic["NEW"]:
                    if QTUtil2.pregunta(
                        self,
                        "There are old translations that are different "
                        "from the imported labels, shall we delete them?",
                    ):
                        for dic in self.dic_translate.values():
                            if dic["NEW"]:
                                dic["NEW"] = ""
                    break

            self.li_labels = list(self.dic_translate.keys())
            self.grid.refresh()
            QTUtil2.message(self, "Changed\n%s" % path_mo)

    def get_param(self, key, default):
        dic = self.configuration.read_variables(self.TRANSLATION_HELP)
        return dic.get(key, default)

    def set_param(self, key, value):
        dic = self.configuration.read_variables(self.TRANSLATION_HELP)
        dic[key] = value
        self.configuration.write_variables(self.TRANSLATION_HELP, dic)

    def read_language(self, lng):
        if lng in self.dic_languages:
            return
        path_mo = Code.path_resource("Locale", lng, "LC_MESSAGES", "lucaschess.mo")
        mofile = polib.mofile(path_mo)
        self.dic_languages[lng] = {entry.msgid: entry.msgstr for entry in mofile}

    def read_languages(self):
        if self.main_reference:
            self.read_language(self.main_reference)
        if self.tr_actual not in self.secondary_references:
            self.read_language(self.tr_actual)
        for lng in self.secondary_references:
            self.read_language(lng)
