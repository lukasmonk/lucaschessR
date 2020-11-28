import os
import os.path
import copy
import operator

import FasterCode

from PySide2 import QtCore, QtWidgets

from Code import Util
from Code.Base import Game
from Code.Base.Constantes import *
from Code.Analysis import Analysis
from Code.Polyglots import Books
from Code.Engines import EnginesBunch
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Grid
from Code.QT import Iconos
from Code.Openings import WindowOpenings, POLAnalisis, POLBoard, OpeningLines
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code.QT import Delegados
from Code.QT import Voyager
from Code.QT import FormLayout
from Code.QT import WindowSavePGN



class WLines(QTVarios.WDialogo):
    def __init__(self, procesador, dbop):
        self.dbop = dbop
        self.title = dbop.gettitle()

        QTVarios.WDialogo.__init__(self, procesador.main_window, self.title, Iconos.OpeningLines(), "studyOpening")

        self.procesador = procesador
        self.configuration = procesador.configuration
        self.gamebase = self.dbop.getgamebase()
        self.num_jg_inicial = self.gamebase.num_moves()
        self.num_jg_actual = None
        self.game = None

        self.resultado = None
        si_figurines_pgn = self.configuration.x_pgn_withfigurines

        li_acciones = (
            (_("Close"), Iconos.MainMenu(), self.terminar),
            None,
            (_("Remove"), Iconos.Borrar(), self.borrar),
            None,
            (_("Import"), Iconos.Import8(), self.importar),
            None,
            (_("Export"), Iconos.Export8(), self.exportar),
            None,
            (_("Utilities"), Iconos.Utilidades(), self.utilidades),
            None,
            (_("Train"), Iconos.Study(), self.train),
            None,
        )
        self.tb = QTVarios.LCTB(self, li_acciones, icon_size=20)

        o_columns = Columnas.ListaColumnas()
        o_columns.nueva("LINE", _("Line"), 35, edicion=Delegados.EtiquetaPOS(False, True))
        start = self.gamebase.num_moves() // 2 + 1
        ancho_col = int(((self.configuration.x_pgn_width - 35 - 20) / 2) * 80 / 100)
        for x in range(start, 75):
            o_columns.nueva(str(x), str(x), ancho_col, edicion=Delegados.EtiquetaPOS(si_figurines_pgn, True))
        self.glines = Grid.Grid(self, o_columns, siCabeceraMovible=False)
        self.glines.setAlternatingRowColors(False)
        self.glines.tipoLetra(puntos=self.configuration.x_pgn_fontpoints)
        self.glines.ponAltoFila(self.configuration.x_pgn_rowheight)

        self.pboard = POLBoard.BoardLines(self, self.configuration)

        self.tabsanalisis = POLAnalisis.TabsAnalisis(self, self.procesador, self.configuration)

        widget = QtWidgets.QWidget()
        widget.setStyleSheet("background-color:lightgray;")
        widget_layout = Colocacion.V().control(self.glines)
        widget_layout.setSpacing(10)
        widget_layout.margen(3)
        widget.setLayout(widget_layout)

        splitter = QtWidgets.QSplitter(self)
        splitter.setOrientation(QtCore.Qt.Vertical)
        splitter.addWidget(widget)
        splitter.addWidget(self.tabsanalisis)

        sp = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        splitter.setSizePolicy(sp)

        self.register_splitter(splitter, "SPLITTER")

        layout_down = Colocacion.H().control(self.pboard).control(splitter).margen(3)
        layout = Colocacion.V().control(self.tb).otro(layout_down).margen(3)
        self.setLayout(layout)

        self.colorPar = QTUtil.qtColor("#DBDAD9")
        self.colorNon = QTUtil.qtColor("#F1EFE9")
        self.colorLine = QTUtil.qtColor("#CDCCCB")

        self.game = self.gamebase

        self.pboard.MoverFinal()

        self.restore_video()

        self.last_numlines = 0
        self.show_lines()

    def show_lines(self):
        numlines = len(self.dbop)
        if numlines != self.last_numlines:
            self.setWindowTitle("%s [%d]" % (self.title, numlines))
            self.last_numlines = numlines

    def exportar(self):
        menu = QTVarios.LCMenu(self)
        submenu = menu.submenu(_("PGN Format"), Iconos.PGN())
        r = "%s %%s" % _("Result")
        submenu.opcion("1-0", r % "1-0", Iconos.Blancas8())
        submenu.opcion("0-1", r % "0-1", Iconos.Negras8())
        submenu.opcion("1/2-1/2", r % "1/2-1/2", Iconos.Tablas8())
        submenu.opcion("", _("Without Result"), Iconos.Gris())
        resp = menu.lanza()
        if resp is not None:
            w = WindowSavePGN.WSaveVarios(self, self.configuration)
            if w.exec_():
                ws = WindowSavePGN.FileSavePGN(self, w.dic_result)
                if ws.open():
                    self.dbop.exportarPGN(ws, resp)
                    ws.close()
                    ws.um_final()

    def utilidades(self):
        menu = QTVarios.LCMenu(self)
        submenu = menu.submenu(_("Analysis"), Iconos.Analizar())
        submenu.opcion(self.ta_massive, _("Mass analysis"), Iconos.Analizar())
        submenu.separador()
        submenu.opcion(self.ta_remove, _("Delete all previous analysis"), Iconos.Delete())
        menu.separador()
        lihistory = self.dbop.lihistory()
        if lihistory:
            submenu = menu.submenu(_("Backups"), Iconos.Copiar())
            rondo = QTVarios.rondoPuntos()
            for history in lihistory[:30]:
                h = history
                if len(h) > 70:
                    h = h[:70] + "..."
                submenu.opcion(history, h, rondo.otro())
                submenu.separador()

        # submenu = menu.submenu(_("History of this session"), Iconos.Copiar())
        resp = menu.lanza()
        if resp:
            if isinstance(resp, str):
                if QTUtil2.pregunta(self, _("Are you sure you want to restore backup %s ?" % ("\n%s" % resp))):
                    um = QTUtil2.unMomento(self, _("Working..."))
                    self.dbop.rechistory(resp)
                    self.glines.refresh()
                    self.glines.gotop()
                    um.final()
            else:
                resp()

    def ta_massive(self):
        dicVar = self.configuration.leeVariables("MASSIVE_OLINES")

        liGen = [FormLayout.separador]

        config = FormLayout.Combobox(_("Engine"), self.configuration.comboMotoresMultiPV10(4))
        liGen.append((config, dicVar.get("ENGINE", self.configuration.tutor)))

        liGen.append(
            (
                _("Duration of engine analysis (secs)") + ":",
                dicVar.get("SEGUNDOS", float(self.configuration.x_tutor_mstime / 1000.0)),
            )
        )
        liDepths = [("--", 0)]
        for x in range(1, 51):
            liDepths.append((str(x), x))
        config = FormLayout.Combobox(_("Depth"), liDepths)
        liGen.append((config, dicVar.get("DEPTH", self.configuration.x_tutor_depth)))

        li = [(_("Maximum"), 0)]
        for x in (1, 3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200):
            li.append((str(x), x))
        config = FormLayout.Combobox(_("Number of moves evaluated by engine(MultiPV)"), li)
        liGen.append((config, dicVar.get("MULTIPV", self.configuration.x_tutor_multipv)))

        liGen.append(FormLayout.separador)
        liGen.append((_("Redo any existing prior analyses (if they exist)") + ":", dicVar.get("REDO", False)))

        resultado = FormLayout.fedit(
            liGen, title=_("Mass analysis"), parent=self, anchoMinimo=460, icon=Iconos.Analizar()
        )
        if resultado is None:
            return

        claveMotor, vtime, depth, multiPV, redo = resultado[1]
        ms = int(vtime * 1000)
        if ms == 0 and depth == 0:
            return

        dicVar["ENGINE"] = claveMotor
        dicVar["SEGUNDOS"] = vtime
        dicVar["DEPTH"] = depth
        dicVar["MULTIPV"] = multiPV
        dicVar["REDO"] = redo
        self.configuration.escVariables("MASSIVE_OLINES", dicVar)

        um = QTUtil2.unMomento(self)
        stFensM2 = self.dbop.getAllFen()
        if redo is False:
            liBorrar = []
            for fenm2 in stFensM2:
                dic = self.dbop.getfenvalue(fenm2)
                if "ANALISIS" in dic:
                    liBorrar.append(fenm2)
            for fenm2 in liBorrar:
                stFensM2.remove(fenm2)

        conf_engine = copy.deepcopy(self.configuration.buscaRival(claveMotor))
        conf_engine.actMultiPV(multiPV)
        xmanager = self.procesador.creaManagerMotor(conf_engine, ms, depth, True)

        um.final()

        mensaje = _("Move") + "  %d/" + str(len(stFensM2))
        tmpBP = QTUtil2.BarraProgreso(self, _("Mass analysis"), "", len(stFensM2))

        done = 0

        for n, fenm2 in enumerate(stFensM2, 1):

            if tmpBP.is_canceled():
                break

            tmpBP.inc()
            tmpBP.mensaje(mensaje % n)

            mrm = xmanager.analiza(fenm2 + " 0 1")
            dic = self.dbop.getfenvalue(fenm2)
            dic["ANALISIS"] = mrm
            self.dbop.setfenvalue(fenm2, dic)
            done += 1

        tmpBP.cerrar()

    def ta_remove(self):
        if QTUtil2.pregunta(self, _("Are you sure?")):
            total = len(self.dbop.db_fenvalues)
            mensaje = _("Move") + "  %d/" + str(total)
            tmpBP = QTUtil2.BarraProgreso(self, "", "", total)
            self.dbop.removeAnalisis(tmpBP, mensaje)
            tmpBP.cerrar()
            self.glines.refresh()

    def train(self):
        menu = QTVarios.LCMenu(self)
        trSSP, trEng = self.train_test()
        if trSSP:
            menu.opcion("tr_sequential", _("Sequential"), Iconos.TrainSequential())
            menu.separador()
            menu.opcion("tr_static", _("Static"), Iconos.TrainStatic())
            menu.separador()
            menu.opcion("tr_positions", _("Positions"), Iconos.TrainPositions())
            menu.separador()
        if trEng:
            menu.opcion("tr_engines", _("With engines"), Iconos.TrainEngines())
            menu.separador()
        submenu = menu.submenu(_("Configuration"), Iconos.Configurar())
        if trEng or trSSP:
            submenu.opcion("update", _("Update current trainings"), Iconos.Reindexar())
            submenu.separador()
        submenu1 = submenu.submenu(_("Create trainings"), Iconos.Modificar())
        submenu1.opcion(
            "new_ssp", "%s - %s - %s" % (_("Sequential"), _("Static"), _("Positions")), Iconos.TrainSequential()
        )
        submenu1.opcion("new_eng", "With engines", Iconos.TrainEngines())

        resp = menu.lanza()
        if resp is None:
            return
        if resp.startswith("tr_"):
            self.resultado = resp
            self.accept()
        elif resp == "new_ssp":
            self.trainNewSSP()
        elif resp == "new_eng":
            self.trainNewEngines()
        elif resp == "update":
            self.trainUpdateAll()

    def train_test(self):
        if len(self.dbop) == 0:
            return False, False
        training = self.dbop.training()
        trainingEng = self.dbop.trainingEngines()
        return training is not None, trainingEng is not None

    def trainNewSSP(self):
        training = self.dbop.training()
        color = "WHITE"
        random_order = False
        max_moves = 0

        if training is not None:
            color = training["COLOR"]
            random_order = training["RANDOM"]
            max_moves = training["MAXMOVES"]

        separador = FormLayout.separador
        liGen = [separador]

        liJ = [(_("White"), "WHITE"), (_("Black"), "BLACK")]
        config = FormLayout.Combobox(_("Play with"), liJ)
        liGen.append((config, color))

        liGen.append(separador)
        liGen.append((_("Random order"), random_order))

        liGen.append(separador)
        liGen.append((_("Maximum number of moves (0=all)"), max_moves))

        resultado = FormLayout.fedit(liGen, title=_("New training"), parent=self, anchoMinimo=360, icon=Iconos.Study())
        if resultado is None:
            return

        accion, liResp = resultado

        reg = {}

        reg["COLOR"], reg["RANDOM"], reg["MAXMOVES"] = liResp

        self.dbop.createTrainingSSP(reg, self.procesador)

        QTUtil2.message_bold(self, _("The trainings of this opening has been created"))

    def trainNewEngines(self):
        training = self.dbop.trainingEngines()
        color = "WHITE"
        basepv = self.dbop.basePV
        mandatory = basepv.count(" ") + 1 if len(basepv) > 0 else 0
        control = 10
        lost_points = 20
        engine_control = self.configuration.tutor.key
        engine_time = 5.0
        num_engines = 20
        key_engine = "alaric"
        ext_engines = []
        auto_analysis = True
        ask_movesdifferent = False
        times = [500, 1000, 2000, 4000, 8000]
        books = ["", "", "", "", ""]
        books_sel = ["", "", "", "", ""]

        if training is not None:
            color = training["COLOR"]
            mandatory = training.get("MANDATORY", mandatory)
            control = training.get("CONTROL", control)
            lost_points = training.get("LOST_POINTS", lost_points)
            engine_control = training.get("ENGINE_CONTROL", engine_control)
            engine_time = training.get("ENGINE_TIME", engine_time)
            num_engines = training.get("NUM_ENGINES", num_engines)
            key_engine = training.get("KEY_ENGINE", key_engine)
            ext_engines = training.get("EXT_ENGINES", ext_engines)
            auto_analysis = training.get("AUTO_ANALYSIS", auto_analysis)
            ask_movesdifferent = training.get("ASK_MOVESDIFFERENT", ask_movesdifferent)
            times = training.get("TIMES", times)
            books = training.get("BOOKS", books)
            books_sel = training.get("BOOKS_SEL", books_sel)

        separador = FormLayout.separador
        li_gen = [separador]

        liJ = [(_("White"), "WHITE"), (_("Black"), "BLACK")]
        config = FormLayout.Combobox(_("Play with"), liJ)
        li_gen.append((config, color))

        li_gen.append((_("Mandatory moves") + ":", mandatory))
        li_gen.append(separador)
        li_gen.append((_("Moves until the control") + ":", control))
        li_gen.append(separador)
        li_gen.append((_("Maximum number of lost centipawns to pass control") + ":", lost_points))
        li_gen.append(separador)

        dic_engines = self.configuration.dic_engines
        li_engines = EnginesBunch.lista(dic_engines)
        config = FormLayout.Spinbox(
            "%s: %s" % (_("Automatic selection"), _("number of engines")), 0, len(li_engines), 50
        )
        li_gen.append((config, num_engines))

        likeys = [(dic_engines[x].name, x) for x in li_engines]
        config = FormLayout.Combobox("%s: %s" % (_("Automatic selection"), _("bunch of engines")), likeys)
        li_gen.append((config, key_engine))
        li_gen.append(separador)

        config = FormLayout.Combobox(_("Engine that does the control"), self.configuration.comboMotores())
        li_gen.append((config, engine_control))
        li_gen.append((_("Duration of analysis (secs)") + ":", float(engine_time)))

        li_gen.append(separador)

        li_gen.append((_("Automatic analysis") + ":", auto_analysis))

        li_gen.append(separador)

        li_gen.append((_("Ask when the moves are different from the line") + ":", ask_movesdifferent))

        li = [("--", "")]
        for key, cm in self.configuration.dic_engines.items():
            li.append((cm.nombre_ext(), key))
        li = sorted(li, key=operator.itemgetter(1))

        li_ext = []

        for x in range(16):
            config = FormLayout.Combobox("%s %d" % (_("Engine"), x + 1), li)
            key = ext_engines[x] if len(ext_engines) > x else ""
            li_ext.append((config, key))

        liLevels = [separador]
        list_books = Books.ListBooks()
        list_books.restore_pickle(self.configuration.file_books)
        list_books.check()
        libooks = [(bookx.name, bookx) for bookx in list_books.lista]
        libooks.insert(0, ("--", None))
        li_books_sel = (
            ("", ""),
            (_("Uniform random"), "au"),
            (_("Proportional random"), "ap"),
            (_("Always the highest percentage"), "mp"),
        )
        for level in range(5):
            n = level + 1
            title = "%s %d" % (_("Level"), n)
            # liLevels.append((None, title))
            tm = times[level] / 1000.0 if len(times) > level else 0.0
            liLevels.append(("%s. %s:" % (title, _("Time engines think in seconds")), tm))

            bk = books[level] if len(books) > level else ""
            book = list_books.buscaLibro(bk) if bk else None
            config = FormLayout.Combobox(_("Book"), libooks)
            liLevels.append((config, book))

            config = FormLayout.Combobox(_("Book selection mode"), li_books_sel)
            liLevels.append((config, books_sel[level]))

        lista = []
        lista.append((li_gen, _("Basic data"), ""))
        lista.append((li_ext, _("Manual engine selection"), ""))
        lista.append((liLevels, _("Levels"), ""))

        resultado = FormLayout.fedit(lista, title=_("With engines"), parent=self, anchoMinimo=360, icon=Iconos.Study())
        if resultado is None:
            return

        accion, liResp = resultado

        selMotoresExt = []
        li_gen, li_ext, liLevels = liResp

        for key in li_ext:
            if key:
                selMotoresExt.append(key)

        reg = {}

        (
            reg["COLOR"],
            reg["MANDATORY"],
            reg["CONTROL"],
            reg["LOST_POINTS"],
            reg["NUM_ENGINES"],
            reg["KEY_ENGINE"],
            reg["ENGINE_CONTROL"],
            reg["ENGINE_TIME"],
            reg["AUTO_ANALYSIS"],
            reg["ASK_MOVESDIFFERENT"],
        ) = li_gen
        reg["EXT_ENGINES"] = selMotoresExt

        if (len(selMotoresExt) + reg["NUM_ENGINES"]) == 0:
            reg["NUM_ENGINES"] = 1

        times = []
        books = []
        books_sel = []
        for x in range(5):
            tm = int(liLevels[x * 3] * 1000)
            bk = liLevels[x * 3 + 1]
            bk_mode = liLevels[x * 3 + 2]
            if tm:
                times.append(tm)
                books.append(bk.name if bk else "")
                books_sel.append(bk_mode)
        if len(times) == 0:
            times.append(500)
            books.append(None)
        reg["TIMES"] = times
        reg["BOOKS"] = books
        reg["BOOKS_SEL"] = books_sel

        self.dbop.createTrainingEngines(reg, self.procesador)

        QTUtil2.message_bold(self, _("Created"))

    def trainUpdateAll(self):
        self.dbop.updateTraining(self.procesador)
        self.dbop.updateTrainingEngines()
        QTUtil2.message_bold(self, _("The trainings have been updated"))

    def addPartida(self, game):
        if game.pv().startswith(self.gamebase.pv()):
            siNueva, num_linea, siAppend = self.dbop.posPartida(game)
            if siNueva:
                self.dbop.append(game)
            else:
                if siAppend:
                    self.dbop[num_linea] = game
            self.glines.refresh()
        else:
            QTUtil2.message_error(self, _X("New line must begin with %1", self.gamebase.pgn_translated()))
        self.show_lines()

    def gameActual(self):
        game = Game.Game()
        if len(self.dbop) == 0:
            game.leeOtra(self.gamebase)
            return game
        numcol = self.glines.posActualN()[1]
        game.leeOtra(self.game if self.game and numcol > 0 else self.gamebase)
        if self.num_jg_actual is not None and self.num_jg_inicial <= self.num_jg_actual < len(game):
            game.li_moves = game.li_moves[: self.num_jg_actual + 1]
        return game

    def voyager2(self, game):
        ptxt = Voyager.voyagerPartida(self, game)
        if ptxt:
            game = Game.Game()
            game.restore(ptxt)
            self.addPartida(game)
            self.show_lines()

    def importar(self):
        menu = QTVarios.LCMenu(self)

        def haz_menu(frommenu, game_base, all=True):
            if all:
                liOp = self.dbop.getOtras(self.configuration, game_base)
                if liOp:
                    otra = frommenu.submenu(_("Other opening lines"), Iconos.OpeningLines())
                    for file, titulo in liOp:
                        otra.opcion(("ol", (file, game_base)), titulo, Iconos.PuntoVerde())
                    frommenu.separador()
            frommenu.opcion(("pgn", game_base), _("PGN with variations"), Iconos.Board())
            frommenu.separador()
            frommenu.opcion(("polyglot", game_base), _("Polyglot book"), Iconos.Libros())
            frommenu.separador()
            frommenu.opcion(("summary", game_base), _("Database summary"), Iconos.Database())
            if all:
                frommenu.separador()
                frommenu.opcion(("voyager2", game_base), _("Voyager 2"), Iconos.Voyager())
                frommenu.separador()
                frommenu.opcion(("opening", game_base), _("Opening"), Iconos.Opening())

        game = self.gameActual()
        if len(game) > len(self.gamebase):
            sub2 = menu.submenu(_("From base position"), Iconos.MoverInicio())
            haz_menu(sub2, self.gamebase)
            menu.separador()
            sub1 = menu.submenu(_("From current position"), Iconos.MoverLibre())
            haz_menu(sub1, game)
            menu.separador()
            sub1 = menu.submenu(_("From all end positions"), Iconos.MoverFinal())
            sub1.opcion(("polyglot", None), _("Polyglot book"), Iconos.Libros())
            menu.separador()
        else:
            haz_menu(menu, self.gamebase)

        resp = menu.lanza()
        if resp is None:
            return
        tipo, game = resp
        if tipo == "pgn":
            self.importarPGN(game)
        elif tipo == "polyglot":
            self.importarPolyglot(game)
        elif tipo == "summary":
            self.importarSummary(game)
        elif tipo == "voyager2":
            self.voyager2(game)
        elif tipo == "opening":
            self.importarOpening(game)
        elif tipo == "ol":
            file, game = game
            self.importarOtra(file, game)
        self.show_lines()

    def importarOtra(self, file, game):
        um = QTUtil2.unMomento(self)
        pathFichero = os.path.join(self.configuration.folder_openings(), file)
        self.dbop.importarOtra(pathFichero, game)
        um.final()
        self.glines.refresh()
        self.glines.gotop()

    def importarOpening(self, game):
        game.assign_opening()
        w = WindowOpenings.WOpenings(self, self.configuration, game.opening)
        if w.exec_():
            ap = w.resultado()
            game = Game.Game()
            game.read_pv(ap.a1h8)
            self.addPartida(game)

    def importarLeeParam(self, titulo):
        dicData = self.dbop.getconfig("IMPORTAR_LEEPARAM")
        if not dicData:
            dicData = {}
        liGen = [FormLayout.separador]

        liGen.append((None, _("Select a maximum number of moves (plies)<br> to consider from each game")))
        liGen.append((FormLayout.Spinbox(_("Depth"), 3, 99, 50), dicData.get("DEPTH", 30)))
        liGen.append(FormLayout.separador)

        li = [(_("Only white best moves"), True), (_("Only black best moves"), False)]
        config = FormLayout.Combobox(_("Moves"), li)
        liGen.append((config, dicData.get("SIWHITE", True)))
        liGen.append(FormLayout.separador)

        li = [(_("Only one best move"), True), (_("All best moves"), False)]
        config = FormLayout.Combobox(_("Best move"), li)
        liGen.append((config, dicData.get("ONLYONE", True)))
        liGen.append(FormLayout.separador)

        liGen.append(
            (FormLayout.Spinbox(_("Minimum moves must have each line"), 0, 99, 50), dicData.get("MINMOVES", 0))
        )

        resultado = FormLayout.fedit(liGen, title=titulo, parent=self, anchoMinimo=360, icon=Iconos.PuntoNaranja())
        if resultado:
            accion, liResp = resultado
            depth, siWhite, onlyone, minMoves = liResp
            dicData["DEPTH"] = depth
            dicData["SIWHITE"] = siWhite
            dicData["ONLYONE"] = onlyone
            dicData["MINMOVES"] = minMoves
            self.dbop.setconfig("IMPORTAR_LEEPARAM", dicData)
            self.configuration.escVariables("WBG_MOVES", dicData)
            return dicData
        return None

    def importarSummary(self, game):
        nomfichgames = QTVarios.select_db(self, self.configuration, True, False)
        if nomfichgames:
            dicData = self.importarLeeParam(_("Database summary"))
            if dicData:
                ficheroSummary = nomfichgames + ".st1"
                depth, siWhite, onlyone, minMoves = (
                    dicData["DEPTH"],
                    dicData["SIWHITE"],
                    dicData["ONLYONE"],
                    dicData["MINMOVES"],
                )
                self.dbop.importarSummary(self, game, ficheroSummary, depth, siWhite, onlyone, minMoves)
                self.glines.refresh()
                self.glines.gotop()

    def importarPolyglot(self, game):
        list_books = Books.ListBooks()
        list_books.restore_pickle(self.configuration.file_books)
        list_books.check()

        dicData = self.dbop.getconfig("IMPORT_POLYGLOT")
        bookW = list_books.lista[0]
        bookB = list_books.lista[0]
        if dicData:
            book = list_books.buscaLibro(dicData["BOOKW"])
            if book:
                bookW = book
            book = list_books.buscaLibro(dicData["BOOKB"])
            if book:
                bookB = book

        liGen = [FormLayout.separador]

        li = [(bookx.name, bookx) for bookx in list_books.lista]
        config = FormLayout.Combobox(_("Book that plays white side"), li)
        liGen.append((config, bookW))
        liGen.append(FormLayout.separador)
        config = FormLayout.Combobox(_("Book that plays black side"), li)
        liGen.append((config, bookB))
        liGen.append(FormLayout.separador)

        resultado = FormLayout.fedit(
            liGen, title=_("Polyglot book"), parent=self, anchoMinimo=360, icon=Iconos.Libros()
        )
        if resultado:
            accion, liResp = resultado
            bookW, bookB = liResp
            dicData = {"BOOKW": bookW.name, "BOOKB": bookB.name}
            self.dbop.setconfig("IMPORT_POLYGLOT", dicData)
        else:
            return

        bookW.polyglot()
        bookB.polyglot()

        titulo = bookW.name if bookW == bookB else "%s/%s" % (bookW.name, bookB.name)
        dicData = self.importarLeeParam(titulo)
        if dicData:
            depth, siWhite, onlyone, minMoves = (
                dicData["DEPTH"],
                dicData["SIWHITE"],
                dicData["ONLYONE"],
                dicData["MINMOVES"],
            )
            self.dbop.importarPolyglot(self, game, bookW, bookB, titulo, depth, siWhite, onlyone, minMoves)
            self.glines.refresh()
            self.glines.gotop()

    def importarPGN(self, game):
        previo = self.configuration.leeVariables("OPENINGLINES")
        carpeta = previo.get("CARPETAPGN", "")

        ficheroPGN = QTUtil2.leeFichero(self, carpeta, "%s (*.pgn)" % _("PGN Format"), titulo=_("File to import"))
        if not ficheroPGN:
            return
        previo["CARPETAPGN"] = os.path.dirname(ficheroPGN)

        liGen = [(None, None)]

        liGen.append((None, _("Select a maximum number of moves (plies)<br> to consider from each game")))

        liGen.append((FormLayout.Spinbox(_("Depth"), 3, 999, 50), previo.get("IPGN_DEPTH", 30)))
        liGen.append((None, None))

        liVariations = ((_("All"), ALL), (_("None"), NONE), (_("White"), ONLY_WHITE), (_("Black"), ONLY_BLACK))
        config = FormLayout.Combobox(_("Include variations"), liVariations)
        liGen.append((config, previo.get("IPGN_VARIATIONSMODE", "A")))
        liGen.append((None, None))

        resultado = FormLayout.fedit(
            liGen, title=os.path.basename(ficheroPGN), parent=self, anchoMinimo=460, icon=Iconos.PuntoNaranja()
        )

        if resultado:
            accion, liResp = resultado
            previo["IPGN_DEPTH"] = depth = liResp[0]
            previo["IPGN_VARIATIONSMODE"] = variations = liResp[1]

            self.dbop.importarPGN(self, game, ficheroPGN, depth, variations)
            self.glines.refresh()
            self.glines.gotop()
            self.configuration.escVariables("OPENINGLINES", previo)

    def grid_color_fondo(self, grid, row, o_column):
        col = o_column.key
        if col == "LINE":
            return self.colorLine
        else:
            linea = row // 2
            return self.colorPar if linea % 2 == 0 else self.colorNon

    def grid_cambiado_registro(self, grid, row, o_column):
        col = o_column.key
        linea = row // 2
        self.game = self.dbop[linea]
        iswhite = row % 2 == 0
        if col.isdigit():
            njug = (int(col) - 1) * 2
            if not iswhite:
                njug += 1
        else:
            njug = -1
        self.num_jg_actual = njug
        self.pboard.ponPartida(self.game)
        self.pboard.colocatePartida(njug)
        self.glines.setFocus()

    def setJugada(self, njug):
        """Recibimos informacion del panel del board"""
        if njug >= 0:
            self.tabsanalisis.setPosicion(self.game, njug)

    def grid_dato(self, grid, row, o_column):
        col = o_column.key
        linea = row // 2
        iswhite = (row % 2) == 0
        color = None
        info = None
        indicadorInicial = None
        li_nags = []
        siLine = False
        agrisar = False

        if col == "LINE":
            pgn = str(linea + 1) if iswhite else ""
            siLine = True

        else:
            njug = (int(col) - 1) * 2
            if not iswhite:
                njug += 1
            game = self.dbop[linea]
            if self.num_jg_inicial <= njug < len(game):
                move = game.move(njug)
                pgn = move.pgnFigurinesSP()
                if linea:
                    game_ant = self.dbop[linea - 1]
                    if game_ant.pv_hasta(njug) == game.pv_hasta(njug):
                        agrisar = True
                dic = self.dbop.getfenvalue(move.position.fenm2())
                if dic:
                    if "COMENTARIO" in dic:
                        v = dic["COMENTARIO"]
                        if v:
                            indicadorInicial = "C"
                    if "VALORACION" in dic:
                        v = dic["VALORACION"]
                        if v:
                            li_nags.append(str(v))
                    if "VENTAJA" in dic:
                        v = dic["VENTAJA"]
                        if v:
                            li_nags.append(str(v))
            else:
                pgn = ""

        return pgn, iswhite, color, info, indicadorInicial, li_nags, agrisar, siLine

    def grid_num_datos(self, grid):
        return len(self.dbop) * 2

    def grid_tecla_control(self, grid, k, is_shift, is_control, is_alt):
        if k == QtCore.Qt.Key_Left:
            row, col = self.glines.current_position()
            pos = col.posCreacion
            if pos > 1:
                if row % 2 == 0:
                    self.glines.goto(row + 1, pos - 2)
                else:
                    self.glines.goto(row - 1, pos - 1)
                return
        elif k == QtCore.Qt.Key_Right:
            row, col = self.glines.current_position()
            pos = col.posCreacion
            if pos >= 1:
                if row % 2 == 0:
                    self.glines.goto(row + 1, pos - 1)
                else:
                    self.glines.goto(row - 1, pos)
                return
        elif k in (QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace):
            row, col = self.glines.current_position()
            if col.key == "LINE":
                self.borrar()
            else:
                self.borrar_move()
        elif k == QtCore.Qt.Key_Up:
            row, col = self.glines.current_position()
            if row > 0:
                self.glines.goto(row-1, col.posCreacion-1)

        elif k == QtCore.Qt.Key_Down:
            row, col = self.glines.current_position()
            if row < self.grid_num_datos(None)-1:
                self.glines.goto(row+1, col.posCreacion-1)

    def grid_doble_click(self, grid, row, o_column):
        game = self.gameActual()
        if game is not None:
            self.procesador.cambiaXAnalyzer()
            xanalyzer = self.procesador.xanalyzer
            move = game.move(-1)
            fenm2 = move.position_before.fenm2()
            dic = self.dbop.getfenvalue(fenm2)
            if "ANALISIS" in dic:
                mrm = dic["ANALISIS"]
                move.analysis = mrm, 0
            else:
                me = QTUtil2.mensEspera.start(self, _("Analyzing the move...."), physical_pos="ad")

                move.analysis = xanalyzer.analizaJugadaPartida(
                    game, len(game) - 1, xanalyzer.motorTiempoJugada, xanalyzer.motorProfundidad
                )
                me.final()
            Analysis.show_analysis(
                self.procesador,
                xanalyzer,
                move,
                self.pboard.board.is_white_bottom,
                9999,
                len(game) - 1,
                main_window=self,
            )

            dic = self.dbop.getfenvalue(fenm2)
            dic["ANALISIS"] = move.analysis[0]
            self.dbop.setfenvalue(fenm2, dic)

    def borrar_move(self):
        row, col = self.glines.current_position()
        linea = row // 2
        if 0 <= linea < len(self.dbop):
            game = self.dbop[linea]
            njug = (int(col.key) - 1) * 2
            if row % 2 == 1:
                njug += 1
            if linea:
                game_ant = self.dbop[linea - 1]
                if game_ant.pv_hasta(njug - 1) == game.pv_hasta(njug - 1):
                    return self.borrar()
            if linea < len(self.dbop) - 1:
                game_sig = self.dbop[linea + 1]
                if game_sig.pv_hasta(njug - 1) == game.pv_hasta(njug - 1):
                    return self.borrar()

            if njug == self.num_jg_inicial:
                return self.borrar()

            siUltimo = njug == len(game) - 1  # si es el ultimo no se pregunta
            if siUltimo or QTUtil2.pregunta(self, _("Do you want to eliminate this move?")):
                game.li_moves = game.li_moves[:njug]
                self.dbop[linea] = game

                self.goto_end_line()
        self.show_lines()

    def borrar(self):
        tam_dbop = len(self.dbop)
        if tam_dbop == 0:
            return
        menu = QTVarios.LCMenu(self)
        current = self.glines.recno() // 2
        if 0 <= current < tam_dbop:
            menu.opcion("current", _("Remove line %d") % (current + 1,), Iconos.Mover())
            menu.separador()
        if tam_dbop > 1:
            menu.opcion("lines", _("Remove a list of lines"), Iconos.MoverLibre())
            menu.separador()
            menu.opcion("worst", _("Remove worst lines"), Iconos.Borrar())
            menu.separador()
        submenu = menu.submenu(_("Remove last move if the line ends with"), Iconos.Final())
        submenu.opcion("last_white", _("White"), Iconos.Blancas())
        submenu.separador()
        submenu.opcion("last_black", _("Black"), Iconos.Negras())

        resp = menu.lanza()

        if resp == "current":
            self.dbop.saveHistory(_("Remove line %d") % (current + 1,))
            del self.dbop[current]
            self.goto_inilinea()

        elif resp == "lines":
            liGen = [FormLayout.separador]
            config = FormLayout.Editbox(
                '<div align="right">' + _("Lines") + "<br>" + _("By example:") + " -5,8-12,14,19-", rx=r"[0-9,\-,\,]*"
            )
            liGen.append((config, ""))
            resultado = FormLayout.fedit(
                liGen, title=_("Remove a list of lines"), parent=self, anchoMinimo=460, icon=Iconos.OpeningLines()
            )
            if resultado:
                accion, liResp = resultado
                clista = liResp[0]
                if clista:
                    ln = Util.ListaNumerosImpresion(clista)
                    li = ln.selected(range(1, tam_dbop + 1))
                    sli = []
                    cad = ""
                    for num in li:
                        if cad:
                            cad += "," + str(num)
                        else:
                            cad = str(num)
                        if len(cad) > 80:
                            if len(sli) == 4:
                                sli.append("...")
                            elif len(sli) < 4:
                                sli.append(cad)
                            cad = ""
                    if cad:
                        sli.append(cad)
                    cli = "\n".join(sli)
                    if QTUtil2.pregunta(self, _("Do you want to remove the next lines?") + "\n\n" + cli):
                        um = QTUtil2.unMomento(self, _("Working..."))
                        self.dbop.removeLines([x - 1 for x in li], cli)
                        self.glines.refresh()
                        self.goto_inilinea()
                        um.final()
        elif resp == "worst":
            self.remove_worst()
        elif resp == "last_white":
            self.remove_lastmove(True)
        elif resp == "last_black":
            self.remove_lastmove(False)
        self.show_lines()

    def remove_lastmove(self, iswhite):
        um = QTUtil2.unMomento(self, _("Working..."))
        self.dbop.remove_lastmove(
            iswhite, "%s %s" % (_("Remove last move if the line ends with"), _("White") if iswhite else _("Black"))
        )
        um.final()

    def remove_worst(self):
        # color + time
        liGen = [FormLayout.separador]
        liJ = [(_("White"), "WHITE"), (_("Black"), "BLACK")]
        config = FormLayout.Combobox(_("Side"), liJ)
        liGen.append((config, "WHITE"))
        liGen.append((_("Duration of engine analysis (secs)") + ":", float(self.configuration.x_tutor_mstime / 1000.0)))
        resultado = FormLayout.fedit(liGen, title=_("Remove worst lines"), parent=self, icon=Iconos.OpeningLines())
        if resultado:
            color, segs = resultado[1]
            ms = int(segs * 1000)
            if ms == 0:
                return
            si_white = color == "WHITE"
            dic = self.dbop.dicRepeFen(si_white)
            mensaje = _("Move") + "  %d/" + str(len(dic))
            tmpBP = QTUtil2.BarraProgreso(self, _("Remove worst lines"), "", len(dic))

            xmanager = self.procesador.creaManagerMotor(self.configuration.tutor, ms, 0, siMultiPV=False)

            st_borrar = set()

            ok = True

            for n, fen in enumerate(dic, 1):

                if tmpBP.is_canceled():
                    ok = False
                    break

                tmpBP.inc()
                tmpBP.mensaje(mensaje % n)

                max_puntos = -999999
                max_pv = None
                dicPV = dic[fen]
                for pv in dicPV:
                    if tmpBP.is_canceled():
                        ok = False
                        break
                    FasterCode.set_fen(fen)
                    FasterCode.move_pv(pv[:2], pv[2:4], pv[4:])
                    mrm = xmanager.analiza(fen)
                    rm = mrm.mejorMov()
                    pts = rm.centipawns_abs()
                    if not si_white:
                        pts = -pts
                    if pts > max_puntos:
                        max_puntos = pts
                        if max_pv:
                            for nl in dicPV[max_pv]:
                                st_borrar.add(nl)
                        max_pv = pv
                    else:
                        for nl in dicPV[pv]:
                            st_borrar.add(nl)

            tmpBP.cerrar()

            xmanager.terminar()

            if ok:
                li_borrar = list(st_borrar)
                n = len(li_borrar)
                if n:
                    self.dbop.removeLines(li_borrar, _("Remove worst lines"))
                    QTUtil2.message_bold(self, _("Removed %d lines") % n)
                else:
                    QTUtil2.message_bold(self, _("Done"))

    def goto_inilinea(self):
        nlines = len(self.dbop)
        if nlines == 0:
            return

        linea = self.glines.recno() // 2
        if linea >= nlines:
            linea = nlines - 1

        row = linea * 2
        ncol = 0
        self.glines.goto(row, ncol)
        self.glines.refresh()

    def goto_end_line(self):
        nlines = len(self.dbop)
        if nlines == 0:
            return

        linea = self.glines.recno() // 2
        if linea >= nlines:
            linea = nlines - 1

        game = self.dbop[linea]

        row = linea * 2
        njug = len(game)
        if njug % 2 == 0:
            row += 1

        ncol = njug // 2
        if njug % 2 == 1:
            ncol += 1

        ncol -= self.num_jg_inicial // 2
        self.glines.goto(row, ncol)
        self.glines.refresh()

    def goto_next_lipv(self, lipv):
        li = self.dbop.getNumLinesPV(lipv, base=0)
        linea_actual = self.glines.recno() // 2

        if linea_actual in li:
            linea = linea_actual
        else:
            li.sort()
            linea = None
            for l in li:
                if l > linea_actual:
                    linea = l
                    break
            if linea is None:
                linea = li[0]

        njug = len(lipv)

        row = linea * 2
        if njug % 2 == 0:
            row += 1

        ncol = njug // 2
        if njug % 2 == 1:
            ncol += 1

        ncol -= self.num_jg_inicial // 2
        self.glines.goto(row, ncol)
        self.glines.refresh()

    def procesosFinales(self):
        board = self.pboard.board
        board.dbVisual.saveMoviblesBoard(board)
        self.dbop.setconfig("WHITEBOTTOM", board.is_white_bottom)
        self.tabsanalisis.saveConfig()
        self.dbop.close()
        self.save_video()

    def terminar(self):
        self.procesosFinales()
        self.accept()

    def closeEvent(self, event):
        self.procesosFinales()

    def player_has_moved(self, game):
        # Estamos en la misma linea ?
        # recno = self.glines.recno()
        # Buscamos en las lineas si hay alguna que el pv sea parcial o totalmente igual
        game.pending_opening = True
        siNueva, num_linea, siAppend = self.dbop.posPartida(game)
        is_white = game.move(-1).is_white()
        ncol = (len(game) - self.num_jg_inicial + 1) // 2
        if self.num_jg_inicial % 2 == 1 and is_white:
            ncol += 1
        if siNueva:
            self.dbop.append(game)
        else:
            if siAppend:
                self.dbop[num_linea] = game
        if not siAppend:
            siNueva, num_linea, siAppend = self.dbop.posPartida(game)

        row = num_linea * 2
        if not is_white:
            row += 1

        self.glines.refresh()
        self.glines.goto(row, ncol)
        self.show_lines()


def study(procesador, file):
    with QTUtil.EscondeWindow(procesador.main_window):
        dbop = OpeningLines.Opening(os.path.join(procesador.configuration.folder_openings(), file))
        w = WLines(procesador, dbop)
        w.exec_()
        dbop.close()
        return w.resultado
