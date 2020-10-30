import os
import zipfile

import Code
from Code.Polyglots import Books
from Code.GM import GM
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Grid
from Code.QT import Iconos
from Code.Openings import WindowOpenings
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code import Util
from Code.SQL import UtilSQL


class WGM(QTVarios.WDialogo):
    def __init__(self, procesador):
        self.configuration = procesador.configuration
        self.procesador = procesador

        self.dbHisto = UtilSQL.DictSQL(self.configuration.ficheroGMhisto)
        self.opening_block = None
        self.liOpeningsFavoritas = []

        w_parent = procesador.main_window
        titulo = _("Play like a Grandmaster")
        icono = Iconos.GranMaestro()

        extparam = "gm"
        QTVarios.WDialogo.__init__(self, w_parent, titulo, icono, extparam)

        flb = Controles.TipoLetra(puntos=10)

        # Toolbar
        li_acciones = [
            (_("Accept"), Iconos.Aceptar(), self.aceptar),
            None,
            (_("Cancel"), Iconos.Cancelar(), self.cancelar),
            None,
            (_("One game"), Iconos.Uno(), self.unJuego),
            None,
            (_("Import"), Iconos.ImportarGM(), self.importar),
        ]
        tb = Controles.TBrutina(self, li_acciones)

        # Grandes maestros
        self.liGM = GM.lista_gm()
        li = [(x[0], x[1]) for x in self.liGM]
        li.insert(0, ("-", None))
        self.cbGM = QTUtil2.comboBoxLB(self, li, li[0][1] if len(self.liGM) == 0 else li[1][1])
        self.cbGM.capture_changes(self.compruebaGM)
        hbox = Colocacion.H().relleno().control(self.cbGM).relleno()
        gbGM = Controles.GB(self, _("Choose a Grandmaster"), hbox).ponFuente(flb)

        # Personales
        self.liPersonal = GM.lista_gm_personal(self.procesador.configuration.personal_training_folder)
        if self.liPersonal:
            li = [(x[0], x[1]) for x in self.liPersonal]
            li.insert(0, ("-", None))
            self.cbPersonal = QTUtil2.comboBoxLB(self, li, li[0][1])
            self.cbPersonal.capture_changes(self.compruebaP)
            btBorrar = Controles.PB(self, "", self.borrarPersonal, plano=False).ponIcono(Iconos.Borrar(), icon_size=16)
            hbox = Colocacion.H().relleno().control(self.cbPersonal).control(btBorrar).relleno()
            gbPersonal = Controles.GB(self, _("Personal games"), hbox).ponFuente(flb)

        # Color
        self.rbBlancas = Controles.RB(self, _("White"), rutina=self.check_color)
        self.rbBlancas.activa(True)
        self.rbNegras = Controles.RB(self, _("Black"), rutina=self.check_color)
        self.rbNegras.activa(False)

        # Contrario
        self.chContrario = Controles.CHB(
            self, _("Choose the opponent's move, when there are multiple possible answers"), False
        )

        # Juez
        liDepths = [("--", 0)]
        for x in range(1, 31):
            liDepths.append((str(x), x))
        self.liMotores = self.configuration.comboMotoresMultiPV10()
        self.cbJmotor, self.lbJmotor = QTUtil2.comboBoxLB(
            self, self.liMotores, self.configuration.tutor_inicial, _("Engine")
        )
        self.edJtiempo = Controles.ED(self).tipoFloat().ponFloat(1.0).anchoFijo(50)
        self.lbJtiempo = Controles.LB2P(self, _("Time in seconds"))
        self.cbJdepth = Controles.CB(self, liDepths, 0).capture_changes(self.cambiadoDepth)
        self.lbJdepth = Controles.LB2P(self, _("Depth"))
        self.lbJshow = Controles.LB2P(self, _("Show rating"))
        self.chbEvals = Controles.CHB(self, _("Show all evaluations"), False)
        liOptions = [(_("All moves"), None), (_("Moves are different"), True), (_("Never"), False)]
        self.cbJshow = Controles.CB(self, liOptions, True)
        self.lbJmultiPV = Controles.LB2P(self, _("Number of moves evaluated by engine(MultiPV)"))
        li = [(_("Default"), "PD"), (_("Maximum"), "MX")]
        for x in (1, 3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200):
            li.append((str(x), str(x)))
        self.cbJmultiPV = Controles.CB(self, li, "PD")

        # Inicial
        self.edJugInicial, lbInicial = QTUtil2.spinBoxLB(self, 1, 1, 99, etiqueta=_("Initial move"), maxTam=40)

        # Libros
        fvar = self.configuration.file_books
        self.listaLibros = Books.ListaLibros()
        self.listaLibros.restore_pickle(fvar)
        # # Comprobamos que todos esten accesibles
        self.listaLibros.comprueba()
        li = [(x.name, x) for x in self.listaLibros.lista]
        li.insert(0, ("--", None))
        self.cbBooks, lbBooks = QTUtil2.comboBoxLB(self, li, None, _("Bypass moves in the book"))

        # Openings

        self.btOpening = Controles.PB(self, " " * 5 + _("Undetermined") + " " * 5, self.aperturasEditar).ponPlano(
            False
        )
        self.btOpeningsFavoritas = Controles.PB(self, "", self.aperturasFavoritas).ponIcono(Iconos.Favoritos())
        self.btOpeningsQuitar = Controles.PB(self, "", self.aperturasQuitar).ponIcono(Iconos.Motor_No())
        hbox = (
            Colocacion.H()
            .control(self.btOpeningsQuitar)
            .control(self.btOpening)
            .control(self.btOpeningsFavoritas)
            .relleno()
        )
        gbOpening = Controles.GB(self, _("Opening"), hbox)

        # gbBasic
        # # Color
        hbox = Colocacion.H().relleno().control(self.rbBlancas).espacio(10).control(self.rbNegras).relleno()
        gbColor = Controles.GB(self, _("Play with"), hbox).ponFuente(flb)

        # Tiempo
        ly1 = (
            Colocacion.H()
            .control(self.lbJmotor)
            .control(self.cbJmotor)
            .control(self.lbJshow)
            .control(self.cbJshow)
            .relleno()
        )
        ly2 = Colocacion.H().control(self.lbJtiempo).control(self.edJtiempo)
        ly2.control(self.lbJdepth).control(self.cbJdepth).espacio(15).control(self.chbEvals).relleno()
        ly3 = Colocacion.H().control(self.lbJmultiPV).control(self.cbJmultiPV).relleno()
        ly = Colocacion.V().otro(ly1).otro(ly2).otro(ly3)
        self.gbJ = Controles.GB(self, _("Adjudicator"), ly).to_connect(self.cambiaJuez)

        # Opciones
        vlayout = Colocacion.V().control(gbColor)
        vlayout.espacio(5).control(self.gbJ)
        vlayout.margen(20)
        gbBasic = Controles.GB(self, "", vlayout)
        gbBasic.setFlat(True)

        # Opciones avanzadas
        lyInicial = (
            Colocacion.H()
            .control(lbInicial)
            .control(self.edJugInicial)
            .relleno()
            .control(lbBooks)
            .control(self.cbBooks)
            .relleno()
        )
        vlayout = Colocacion.V().relleno().otro(lyInicial).control(gbOpening)
        vlayout.espacio(5).control(self.chContrario).margen(20).relleno()
        gbAdvanced = Controles.GB(self, "", vlayout)
        gbAdvanced.setFlat(True)

        # Historico
        self.liHisto = []
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("FECHA", _("Date"), 80, centered=True)
        o_columns.nueva("PACIERTOS", _("Hints"), 90, centered=True)
        o_columns.nueva("PUNTOS", _("Points accumulated"), 120, centered=True)
        o_columns.nueva("ENGINE", _("Adjudicator"), 100, centered=True)
        o_columns.nueva("RESUMEN", _("Game played"), 150)

        self.grid = grid = Grid.Grid(self, o_columns, siSelecFilas=True, background=None)
        self.grid.coloresAlternados()
        self.register_grid(grid)

        # Tabs
        self.tab = Controles.Tab().set_position("S")
        self.tab.nuevaTab(gbBasic, _("Basic"))
        self.tab.nuevaTab(gbAdvanced, _("Advanced"))
        self.tab.nuevaTab(self.grid, _("Track record"))

        # Cabecera
        lyCab = Colocacion.H().control(gbGM)
        if self.liPersonal:
            lyCab.control(gbPersonal)

        layout = Colocacion.V().control(tb).otro(lyCab).control(self.tab).margen(6)

        self.setLayout(layout)

        self.recuperaDic()
        self.cambiaJuez()
        self.compruebaGM()
        self.compruebaP()
        self.compruebaHisto()
        self.aperturaMuestra()
        self.btOpeningsFavoritas.hide()

        self.restore_video(anchoDefecto=450)

    def cambiadoDepth(self, num):
        vtime = self.edJtiempo.textoFloat()
        if int(vtime) * 10 == 0:
            vtime = 3.0
        self.edJtiempo.ponFloat(0.0 if num > 0 else vtime)
        self.edJtiempo.setEnabled(num == 0)

    def closeEvent(self, event):
        self.save_video()
        self.dbHisto.close()

    def compruebaGM_P(self, liGMP, tgm):
        tsiw = self.rbBlancas.isChecked()

        for nom, gm, siw, sib in liGMP:
            if gm == tgm:
                self.rbBlancas.setEnabled(siw)
                self.rbNegras.setEnabled(sib)
                if tsiw:
                    if not siw:
                        self.rbBlancas.activa(False)
                        self.rbNegras.activa(True)
                else:
                    if not sib:
                        self.rbBlancas.activa(True)
                        self.rbNegras.activa(False)
                break
        self.compruebaHisto()

    def compruebaGM(self):
        tgm = self.cbGM.valor()
        if tgm:
            if self.liPersonal:
                self.cbPersonal.ponValor(None)
            self.compruebaGM_P(self.liGM, tgm)

    def compruebaP(self):
        if not self.liPersonal:
            return
        tgm = self.cbPersonal.valor()
        if tgm:
            if self.liGM:
                self.cbGM.ponValor(None)
            self.compruebaGM_P(self.liPersonal, tgm)

    def compruebaHisto(self):
        tgmGM = self.cbGM.valor()
        tgmP = self.cbPersonal.valor() if self.liPersonal else None

        if tgmGM is None and tgmP is None:
            if len(self.liGM) > 1:
                tgmGM = self.liGM[1][1]
                self.cbGM.ponValor(tgmGM)
            else:
                self.liHisto = []
                return

        if tgmGM and tgmP:
            self.cbPersonal.ponValor(None)
            tgmP = None

        if tgmGM:
            tgm = tgmGM
        else:
            tgm = "P_" + tgmP

        self.liHisto = self.dbHisto[tgm]
        if self.liHisto is None:
            self.liHisto = []
        self.grid.refresh()

    def grid_num_datos(self, grid):
        return len(self.liHisto)

    def grid_dato(self, grid, row, o_column):
        key = o_column.key
        dic = self.liHisto[row]
        if key == "FECHA":
            f = dic["FECHA"]
            return "%d/%02d/%d" % (f.day, f.month, f.year)
        elif key == "PACIERTOS":
            return "%d%%" % dic["PACIERTOS"]
        elif key == "PUNTOS":
            return "%d" % dic["PUNTOS"]
        elif key == "JUEZ":
            return "%s (%d)" % (dic["JUEZ"], dic["TIME"])
        elif key == "RESUMEN":
            return dic.get("RESUMEN", "")

    def borrarPersonal(self):
        tgm = self.cbPersonal.valor()
        if tgm is None:
            return
        if not QTUtil2.pregunta(self, _X(_("Delete %1?"), tgm)):
            return

        base = os.path.join(self.configuration.personal_training_folder, "%s.gm" % tgm)
        for x in "wbi":
            Util.remove_file(base + x)

        self.liPersonal = GM.lista_gm_personal(self.configuration.personal_training_folder)

        li = [(x[0], x[1]) for x in self.liPersonal]
        li.insert(0, ("-", None))
        self.cbPersonal.rehacer(li, li[0][1])

        self.compruebaP()

    def check_color(self):
        tgm = self.cbGM.valor()
        tsiw = self.rbBlancas.isChecked()

        for nom, gm, siw, sib in self.liGM:
            if gm == tgm:
                if tsiw:
                    if not siw:
                        self.rbBlancas.activa(False)
                        self.rbNegras.activa(True)
                else:
                    if not sib:
                        self.rbBlancas.activa(True)
                        self.rbNegras.activa(False)

    def aceptar(self):
        if self.grabaDic():
            self.accept()
        else:
            self.reject()

    def unJuego(self):
        if not self.grabaDic():  # crea self.ogm
            return

        w = SelectGame(self, self.ogm)
        if w.exec_():
            if w.partidaElegida is not None:
                self.record.partidaElegida = w.partidaElegida

                self.accept()

    def cancelar(self):
        self.reject()

    def importar(self):
        if importar_gm(self):
            liC = GM.lista_gm()
            self.cbGM.clear()
            for tp in liC:
                self.cbGM.addItem(tp[0], tp[1])
            self.cbGM.setCurrentIndex(0)

    def cambiaJuez(self):
        si = self.gbJ.isChecked()
        for control in (
            self.cbJmotor,
            self.lbJmotor,
            self.edJtiempo,
            self.lbJtiempo,
            self.lbJdepth,
            self.cbJdepth,
            self.lbJshow,
            self.cbJshow,
            self.lbJmultiPV,
            self.cbJmultiPV,
            self.chbEvals,
        ):
            control.setVisible(si)

    def grabaDic(self):
        rk = Util.Record()
        rk.gm = self.cbGM.valor()
        if rk.gm is None:
            rk.modo = "personal"
            rk.gm = self.cbPersonal.valor()
            if rk.gm is None:
                return False
        else:
            rk.modo = "estandar"
        rk.partidaElegida = None
        rk.is_white = self.rbBlancas.isChecked()
        rk.siJuez = self.gbJ.isChecked()
        rk.showevals = self.chbEvals.valor()
        rk.engine = self.cbJmotor.valor()
        rk.vtime = int(self.edJtiempo.textoFloat() * 10)
        rk.mostrar = self.cbJshow.valor()
        rk.depth = self.cbJdepth.valor()
        rk.multiPV = self.cbJmultiPV.valor()
        rk.jugContrario = self.chContrario.isChecked()
        rk.jugInicial = self.edJugInicial.valor()
        if rk.siJuez and rk.vtime <= 0 and rk.depth == 0:
            rk.siJuez = False
        rk.bypassBook = self.cbBooks.valor()
        rk.opening = self.opening_block

        default = Code.path_resource("GM")

        carpeta = default if rk.modo == "estandar" else self.configuration.personal_training_folder
        self.ogm = GM.GM(carpeta, rk.gm)
        self.ogm.filter_side(rk.is_white)
        if not len(self.ogm):
            QTUtil2.message_error(self, _("There are no games to play with this color"))
            return False

        self.ogm.isErasable = rk.modo == "personal"  # para saber si se puede borrar
        self.record = rk
        dic = {}

        for atr in dir(self.record):
            if not atr.startswith("_"):
                dic[atr.upper()] = getattr(self.record, atr)
        dic["APERTURASFAVORITAS"] = self.liOpeningsFavoritas

        Util.save_pickle(self.configuration.file_gms(), dic)

        return True

    def recuperaDic(self):
        dic = Util.restore_pickle(self.configuration.file_gms())
        if dic:

            gm = dic["GM"]
            modo = dic.get("MODO", "estandar")
            is_white = dic.get("IS_WHITE", True)
            siJuez = dic["SIJUEZ"]
            showevals = dic.get("SHOWEVALS", False)
            engine = dic["ENGINE"]
            vtime = dic["VTIME"]
            depth = dic.get("DEPTH", 0)
            multiPV = dic.get("MULTIPV", "PD")
            mostrar = dic["MOSTRAR"]
            jugContrario = dic.get("JUGCONTRARIO", False)
            jugInicial = dic.get("JUGINICIAL", 1)
            self.liOpeningsFavoritas = dic.get("APERTURASFAVORITAS", [])
            self.opening_block = dic.get("APERTURA", None)
            if self.opening_block:
                nEsta = -1
                for npos, bl in enumerate(self.liOpeningsFavoritas):
                    if bl.a1h8 == self.opening_block.a1h8:
                        nEsta = npos
                        break
                if nEsta != 0:
                    if nEsta != -1:
                        del self.liOpeningsFavoritas[nEsta]
                    self.liOpeningsFavoritas.insert(0, self.opening_block)
                while len(self.liOpeningsFavoritas) > 10:
                    del self.liOpeningsFavoritas[10]
            if len(self.liOpeningsFavoritas):
                self.btOpeningsFavoritas.show()
            bypassBook = dic.get("BYPASSBOOK", None)

            self.rbBlancas.setChecked(is_white)
            self.rbNegras.setChecked(not is_white)

            self.gbJ.setChecked(siJuez)
            self.cbJmotor.ponValor(engine)
            self.edJtiempo.ponFloat(float(vtime / 10.0))
            self.cbJshow.ponValor(mostrar)
            self.chbEvals.ponValor(showevals)
            self.cbJdepth.ponValor(depth)
            self.cambiadoDepth(depth)
            self.cbJmultiPV.ponValor(multiPV)

            self.chContrario.setChecked(jugContrario)

            self.edJugInicial.ponValor(jugInicial)

            li = self.liGM
            cb = self.cbGM
            if modo == "personal":
                if self.liPersonal:
                    li = self.liPersonal
                    cb = self.cbGM
            for v in li:
                if v[1] == gm:
                    cb.ponValor(gm)
                    break
            if bypassBook:
                for book in self.listaLibros.lista:
                    if book.path == bypassBook.path:
                        self.cbBooks.ponValor(book)
                        break
            self.aperturaMuestra()

    def aperturasEditar(self):
        self.btOpening.setDisabled(True)  # Puede tardar bastante vtime
        me = QTUtil2.unMomento(self)
        w = WindowOpenings.WOpenings(self, self.configuration, self.opening_block)
        me.final()
        self.btOpening.setDisabled(False)
        if w.exec_():
            self.opening_block = w.resultado()
            self.aperturaMuestra()

    def aperturasFavoritas(self):
        if len(self.liOpeningsFavoritas) == 0:
            return
        menu = QTVarios.LCMenu(self)
        menu.setToolTip(_("To choose: <b>left button</b> <br>To erase: <b>right button</b>"))
        f = Controles.TipoLetra(puntos=8, peso=75)
        menu.ponFuente(f)
        nPos = 0
        for nli, bloque in enumerate(self.liOpeningsFavoritas):
            if type(bloque) == tuple:  # compatibilidad con versiones anteriores
                bloque = bloque[0]
                self.liOpeningsFavoritas[nli] = bloque
            menu.opcion(bloque, bloque.trNombre, Iconos.PuntoVerde())
            nPos += 1

        resp = menu.lanza()
        if resp:
            if menu.siIzq:
                self.opening_block = resp
                self.aperturaMuestra()
            elif menu.siDer:
                opening_block = resp
                if QTUtil2.pregunta(
                    self,
                    _X(
                        _("Do you want to delete the opening %1 from the list of favourite openings?"),
                        opening_block.trNombre,
                    ),
                ):
                    del self.liOpeningsFavoritas[nPos]

    def aperturaMuestra(self):
        if self.opening_block:
            label = self.opening_block.trNombre + "\n" + self.opening_block.pgn
            self.btOpeningsQuitar.show()
        else:
            label = " " * 3 + _("Undetermined") + " " * 3
            self.btOpeningsQuitar.hide()
        self.btOpening.set_text(label)

    def aperturasQuitar(self):
        self.opening_block = None
        self.aperturaMuestra()


def eligeJugada(manager, li_moves, is_gm):
    menu = QTVarios.LCMenu(manager.main_window)

    if is_gm:
        titulo = manager.nombreGM
        icono = Iconos.GranMaestro()
    else:
        titulo = _("Opponent's move")
        icono = Iconos.Carpeta()
    menu.opcion(None, titulo, icono)
    menu.separador()

    icono = Iconos.PuntoAzul() if is_gm else Iconos.PuntoNaranja()

    for from_sq, to_sq, promotion, label, pgn in li_moves:

        if label and (len(li_moves) > 1):
            txt = "%s - %s" % (pgn, label)
        else:
            txt = pgn
        menu.opcion((from_sq, to_sq, promotion), txt, icono)
        menu.separador()

    resp = menu.lanza()
    if resp:
        return resp
    else:
        from_sq, to_sq, promotion, label, pgn = li_moves[0]
        return from_sq, to_sq, promotion


class WImportar(QTVarios.WDialogo):
    def __init__(self, w_parent, liGM):

        self.liGM = liGM

        titulo = _("Import")
        icono = Iconos.ImportarGM()

        self.qtColor = {"w": QTUtil.qtColorRGB(221, 255, 221), "m": QTUtil.qtColorRGB(247, 247, 247)}

        extparam = "imp_gm"
        QTVarios.WDialogo.__init__(self, w_parent, titulo, icono, extparam)

        li_acciones = [
            (_("Import"), Iconos.Aceptar(), self.importar),
            None,
            (_("Cancel"), Iconos.Cancelar(), self.reject),
            None,
            (_("Mark"), Iconos.Marcar(), self.marcar),
            None,
        ]
        tb = Controles.TBrutina(self, li_acciones)

        # Lista
        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("ELEGIDO", "", 22, siChecked=True)
        o_columns.nueva("NOMBRE", _("Grandmaster"), 140)
        o_columns.nueva("PARTIDAS", _("Games"), 60, siDerecha=True)
        o_columns.nueva("BORN", _("Birth date"), 60, centered=True)

        self.grid = Grid.Grid(self, o_columns)
        n = self.grid.anchoColumnas()
        self.grid.setMinimumWidth(n + 20)

        self.register_grid(self.grid)

        # Layout
        layout = Colocacion.V().control(tb).control(self.grid).margen(3)
        self.setLayout(layout)

        self.last_order = "NOMBRE", False

        self.restore_video(anchoDefecto=n + 26)

    def importar(self):
        self.save_video()
        self.accept()

    def marcar(self):
        menu = QTVarios.LCMenu(self)
        f = Controles.TipoLetra(puntos=8, peso=75)
        menu.ponFuente(f)
        menu.opcion(1, _("All"), Iconos.PuntoVerde())
        menu.opcion(2, _("None"), Iconos.PuntoNaranja())
        resp = menu.lanza()
        if resp:
            for obj in self.liGM:
                obj["ELEGIDO"] = resp == 1
            self.grid.refresh()

    def grid_num_datos(self, grid):
        return len(self.liGM)

    def grid_setvalue(self, grid, row, column, valor):
        self.liGM[row][column.key] = valor

    def grid_dato(self, grid, row, o_column):
        return self.liGM[row][o_column.key]

    def grid_color_fondo(self, grid, row, col):
        return self.qtColor[self.liGM[row]["WM"]]

    def grid_doble_clickCabecera(self, grid, oCol):
        cab, si_rev = self.last_order
        col_clave = oCol.key
        key = lambda x: str(x[col_clave])
        if cab == col_clave:
            si_rev = not si_rev
        else:
            si_rev = False
        self.liGM.sort(key=key, reverse=si_rev)
        self.last_order = col_clave, si_rev
        self.grid.refresh()
        self.grid.gotop()


def importar_gm(owner_gm):
    web = "https://lucaschess.pythonanywhere.com/static/gm_mw"

    message = _("Reading the list of Grandmasters from the web")
    me = QTUtil2.mensEspera.inicio(owner_gm, message)

    fich_name = "_listaGM.txt"
    url_lista = "%s/%s" % (web, fich_name)
    fich_tmp = Code.configuration.ficheroTemporal("txt")
    fich_lista = Code.path_resource("GM", fich_name)
    si_bien = Util.urlretrieve(url_lista, fich_tmp)
    me.final()

    if not si_bien:
        QTUtil2.message_error(
            owner_gm, _("List of Grandmasters currently unavailable; please check Internet connectivity")
        )
        return False

    with open(fich_tmp, "rt") as f:
        li_gm = []
        for linea in f:
            linea = linea.strip()
            if linea:
                gm, name, ctam, cpart, wm, cyear = linea.split("|")
                fichero = Code.path_resource("GM/%s.xgm" % gm)
                if Util.filesize(fichero) != int(ctam):  # si no existe tam = -1
                    dic = {"GM": gm, "NOMBRE": name, "PARTIDAS": cpart, "ELEGIDO": False, "BORN": cyear, "WM": wm}
                    li_gm.append(dic)

        if len(li_gm) == 0:
            QTUtil2.message_bold(owner_gm, _("You have all Grandmasters installed."))
            return False

    Util.remove_file(fich_lista)
    Util.file_copy(fich_tmp, fich_lista)

    w = WImportar(owner_gm, li_gm)
    if w.exec_():
        for dic in li_gm:
            if dic["ELEGIDO"]:
                gm = dic["GM"]
                gm = gm[0].upper() + gm[1:].lower()
                me = QTUtil2.mensEspera.inicio(owner_gm, _X(_("Import %1"), gm), opacity=1.0)

                # Descargamos
                fzip = gm + ".zip"
                si_bien = Util.urlretrieve("%s/%s.zip" % (web, gm), fzip)

                if si_bien:
                    zfobj = zipfile.ZipFile(fzip)
                    for name in zfobj.namelist():
                        fichero = Code.path_resource("GM/%s" % name)
                        with open(fichero, "wb") as outfile:
                            outfile.write(zfobj.read(name))
                    zfobj.close()
                    os.remove(fzip)

                me.final()

        return True

    return False


class SelectGame(QTVarios.WDialogo):
    def __init__(self, wgm, ogm):
        self.ogm = ogm
        self.liRegs = ogm.gen_toselect()
        self.si_reverse = False
        self.claveSort = None

        dgm = GM.dic_gm()
        name = dgm.get(ogm.gm, ogm.gm)
        titulo = "%s - %s" % (_("One game"), name)
        icono = Iconos.Uno()
        extparam = "gm1g"
        QTVarios.WDialogo.__init__(self, wgm, titulo, icono, extparam)

        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("NOMBRE", _("Opponent"), 180)
        o_columns.nueva("FECHA", _("Date"), 90, centered=True)
        o_columns.nueva("EVENT", _("Event"), 140, centered=True)
        o_columns.nueva("ECO", _("ECO"), 40, centered=True)
        o_columns.nueva("RESULT", _("Result"), 64, centered=True)
        self.grid = Grid.Grid(self, o_columns, siSelecFilas=True, siSeleccionMultiple=True)
        nAnchoPgn = self.grid.anchoColumnas() + 20
        self.grid.setMinimumWidth(nAnchoPgn)
        self.grid.coloresAlternados()

        self.register_grid(self.grid)

        li_acciones = [
            (_("Accept"), Iconos.Aceptar(), self.aceptar),
            None,
            (_("Cancel"), Iconos.Cancelar(), self.cancelar),
            None,
        ]
        if ogm.isErasable:
            li_acciones.append((_("Remove"), Iconos.Borrar(), self.remove))
            li_acciones.append(None)

        tb = Controles.TBrutina(self, li_acciones)

        layout = Colocacion.V().control(tb).control(self.grid).margen(3)
        self.setLayout(layout)

        self.restore_video(anchoDefecto=400)
        self.partidaElegida = None

    def grid_num_datos(self, grid):
        return len(self.liRegs)

    def grid_dato(self, grid, row, o_column):
        return self.liRegs[row][o_column.key]

    def grid_doble_click(self, grid, row, column):
        self.aceptar()

    def grid_doble_clickCabecera(self, grid, o_column):
        key = o_column.key

        self.liRegs = sorted(self.liRegs, key=lambda x: x[key].upper())

        if self.claveSort == key:
            if self.si_reverse:
                self.liRegs.reverse()

            self.si_reverse = not self.si_reverse
        else:
            self.si_reverse = True

        self.grid.refresh()
        self.grid.gotop()

    def aceptar(self):
        self.partidaElegida = self.liRegs[self.grid.recno()]["NUMBER"]
        self.save_video()
        self.accept()

    def cancelar(self):
        self.save_video()
        self.reject()

    def remove(self):
        li = self.grid.recnosSeleccionados()
        if len(li) > 0:
            if QTUtil2.pregunta(self, _("Do you want to delete all selected records?")):
                li.sort(reverse=True)
                for x in li:
                    self.ogm.remove(x)
                    del self.liRegs[x]
                self.grid.refresh()
