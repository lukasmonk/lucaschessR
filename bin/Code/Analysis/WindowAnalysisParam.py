from Code.Polyglots import Books
from Code.QT import FormLayout
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code import Util
from Code.Engines import Priorities

SEPARADOR = FormLayout.separador


def leeDicParametros(configuration):
    file = configuration.file_param_analysis()
    dic = Util.restore_pickle(file)
    if not dic:
        dic = {}
    alm = Util.Record()
    alm.engine = dic.get("engine", configuration.tutor.key)
    alm.vtime = dic.get("vtime", configuration.x_tutor_mstime)
    alm.depth = dic.get("depth", configuration.x_tutor_depth)
    alm.timedepth = dic.get("timedepth", False)
    alm.kblunders = dic.get("kblunders", 50)
    alm.ptbrilliancies = dic.get("ptbrilliancies", 100)
    alm.dpbrilliancies = dic.get("dpbrilliancies", 7)
    alm.from_last_move = dic.get("from_last_move", False)
    alm.multiPV = dic.get("multipv", "PD")
    alm.priority = dic.get("priority", Priorities.priorities.normal)

    alm.book_name = dic.get("book_name", None)

    alm.include_variations = dic.get("include_variations", True)
    alm.limit_include_variations = dic.get("limit_include_variations", 0)
    alm.best_variation = dic.get("best_variation", False)
    alm.info_variation = dic.get("info_variation", True)
    alm.one_move_variation = dic.get("one_move_variation", False)
    alm.delete_previous = dic.get("delete_previous", True)
    alm.si_pdt = dic.get("si_pdt", False)

    alm.show_graphs = dic.get("show_graphs", True)

    alm.stability = dic.get("stability", False)
    alm.st_centipawns = dic.get("st_centipawns", 5)
    alm.st_depths = dic.get("st_depths", 3)
    alm.st_timelimit = dic.get("st_timelimit", 5)

    alm.white = dic.get("white", True)
    alm.black = dic.get("black", True)

    return alm


def formBlundersBrilliancies(alm, configuration):
    liBlunders = [SEPARADOR]

    liBlunders.append((FormLayout.Editbox(_("Is considered wrong move when the loss of points is greater than"), tipo=int, ancho=50), alm.kblunders))
    liBlunders.append(SEPARADOR)

    def fileNext(base, ext):
        return Util.file_next(configuration.personal_training_folder, base, ext)

    path_pgn = fileNext("Blunders", "pgn")

    liBlunders.append((None, _("Generate a training file with these moves")))

    config = FormLayout.Editbox(_("Tactics name"), rx="[^\\:/|?*^%><()]*")
    liBlunders.append((config, ""))

    config = FormLayout.Fichero(_("PGN Format"), "%s (*.pgn)" % _("PGN Format"), True, anchoMinimo=280, ficheroDefecto=path_pgn)
    liBlunders.append((config, ""))

    liBlunders.append((_("Also add complete game to PGN") + ":", False))

    liBlunders.append(SEPARADOR)

    eti = '"%s"' % _("Find best move")
    liBlunders.append((_X(_("Add to the training %1 with the name"), eti) + ":", ""))

    liBrilliancies = [SEPARADOR]

    liBrilliancies.append((FormLayout.Spinbox(_("Minimum depth"), 3, 30, 50), alm.dpbrilliancies))

    liBrilliancies.append((FormLayout.Spinbox(_("Minimum gain points"), 30, 30000, 50), alm.ptbrilliancies))
    liBrilliancies.append(SEPARADOR)

    path_fns = fileNext("Brilliancies", "fns")
    path_pgn = fileNext("Brilliancies", "pgn")

    liBrilliancies.append((None, _("Generate a training file with these moves")))

    config = FormLayout.Fichero(_("List of FENs"), "%s (*.fns)" % _("List of FENs"), True, anchoMinimo=280, ficheroDefecto=path_fns)
    liBrilliancies.append((config, ""))

    config = FormLayout.Fichero(_("PGN Format"), "%s (*.pgn)" % _("PGN Format"), True, anchoMinimo=280, ficheroDefecto=path_pgn)
    liBrilliancies.append((config, ""))

    liBrilliancies.append((_("Also add complete game to PGN"), False))

    liBrilliancies.append(SEPARADOR)

    eti = '"%s"' % _("Find best move")
    liBrilliancies.append((_X(_("Add to the training %1 with the name"), eti) + ":", ""))

    return liBlunders, liBrilliancies


def form_variations(alm):
    li_var = [SEPARADOR]
    li_var.append((_("Add analysis to variations") + ":", alm.include_variations))
    li_var.append(SEPARADOR)

    li_var.append((FormLayout.Spinbox(_("Minimum points lost"), 0, 1000, 60), alm.limit_include_variations))
    li_var.append(SEPARADOR)

    li_var.append((_("Only add better variation") + ":", alm.best_variation))
    li_var.append(SEPARADOR)

    li_var.append((_("Include info about engine") + ":", alm.info_variation))
    li_var.append(SEPARADOR)

    li_var.append(("%s %s/%s/%s:" % (_("Format"), _("Points"), _("Depth"), _("Time")), alm.si_pdt))
    li_var.append(SEPARADOR)

    li_var.append((_("Only one move of each variation") + ":", alm.one_move_variation))
    return li_var


def analysis_parameters(parent, configuration, siModoAmpliado, siTodosMotores=False):
    alm = leeDicParametros(configuration)

    # Datos
    liGen = [SEPARADOR]

    # # Tutor
    if siTodosMotores:
        li = configuration.ayudaCambioCompleto(alm.engine)
    else:
        li = configuration.ayudaCambioTutor()
        li[0] = alm.engine
    liGen.append((_("Engine") + ":", li))

    # # Time
    liGen.append(SEPARADOR)
    config = FormLayout.Editbox(_("Duration of engine analysis (secs)"), 40, tipo=float)
    liGen.append((config, alm.vtime / 1000.0))

    # Depth
    liDepths = [("--", 0)]
    for x in range(1, 51):
        liDepths.append((str(x), x))
    config = FormLayout.Combobox(_("Depth"), liDepths)
    liGen.append((config, alm.depth))

    # Time+Depth
    liGen.append(("%s+%s:" % (_("Time"), _("Depth")), alm.timedepth))

    # MultiPV
    liGen.append(SEPARADOR)
    li = [(_("Default"), "PD"), (_("Maximum"), "MX")]
    for x in (1, 3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200):
        li.append((str(x), str(x)))
    config = FormLayout.Combobox(_("Number of moves evaluated by engine(MultiPV)"), li)
    liGen.append((config, alm.multiPV))

    # Priority
    liGen.append(SEPARADOR)
    config = FormLayout.Combobox(_("Process priority"), Priorities.priorities.combo())
    liGen.append((config, alm.priority))

    # Completo
    if siModoAmpliado:
        liGen.append(SEPARADOR)

        liJ = [(_("White"), "WHITE"), (_("Black"), "BLACK"), (_("White & Black"), "BOTH")]
        config = FormLayout.Combobox(_("Analyze only color"), liJ)
        if alm.white and alm.black:
            color = "BOTH"
        elif alm.black:
            color = "BLACK"
        elif alm.white:
            color = "WHITE"
        else:
            color = "BOTH"
        liGen.append((config, color))

        config = FormLayout.Editbox('<div align="right">' + _("Moves") + "<br>" + _("By example:") + " -5,8-12,14,19-", rx="[0-9,\-,\,]*")
        liGen.append((config, ""))

        fvar = configuration.file_books
        list_books = Books.ListBooks()
        list_books.restore_pickle(fvar)
        # Comprobamos que todos esten accesibles
        list_books.check()
        li = [("--", None)]
        defecto = list_books.lista[0] if alm.book_name else None
        for book in list_books.lista:
            if alm.book_name == book.name:
                defecto = book
            li.append((book.name, book))
        config = FormLayout.Combobox(_("Do not scan the opening moves based on book"), li)
        liGen.append((config, defecto))
        liGen.append(SEPARADOR)

        liGen.append((_("Redo any existing prior analyses (if they exist)") + ":", alm.delete_previous))

        liGen.append((_("Start from the end of the game") + ":", alm.from_last_move))

        liGen.append(SEPARADOR)

        liGen.append((_("Show graphics") + ":", alm.show_graphs))

        liVar = form_variations(alm)

        liBlunders, liBrilliancies = formBlundersBrilliancies(alm, configuration)

        liST = [SEPARADOR]
        liST.append((_("Activate") + ":", alm.stability))
        liST.append(SEPARADOR)
        liST.append((FormLayout.Spinbox(_("Last depths to control same best move"), 2, 10, 40), alm.st_depths))
        liST.append(SEPARADOR)
        liST.append((FormLayout.Spinbox(_("Maximum difference among last evaluations"), 0, 99999, 60), alm.st_centipawns))
        liST.append(SEPARADOR)
        liST.append((FormLayout.Spinbox(_("Additional time limit"), 0, 99999, 60), alm.st_timelimit))

        lista = []
        lista.append((liGen, _("General options"), ""))
        lista.append((liVar, _("Variations"), ""))
        lista.append((liBlunders, _("Wrong moves"), ""))
        lista.append((liBrilliancies, _("Brilliancies"), ""))
        lista.append((liST, _("Stability control"), ""))

    else:
        lista = liGen

    reg = Util.Record()
    reg.form = None

    def dispatchR(valor):
        if reg.form is None:
            if isinstance(valor, FormLayout.FormTabWidget):
                reg.form = valor
                reg.wtime = valor.getWidget(0, 1)
                reg.wdepth = valor.getWidget(0, 2)
                reg.wdt = valor.getWidget(0, 3)
            elif isinstance(valor, FormLayout.FormWidget):
                reg.form = valor
                reg.wtime = valor.getWidget(1)
                reg.wdepth = valor.getWidget(2)
                reg.wdt = valor.getWidget(3)
        else:
            sender = reg.form.sender()
            if not reg.wdt.isChecked():
                if sender == reg.wtime:
                    if reg.wtime.textoFloat() > 0:
                        reg.wdepth.setCurrentIndex(0)
                elif sender == reg.wdepth:
                    if reg.wdepth.currentIndex() > 0:
                        reg.wtime.ponFloat(0.0)
                elif sender == reg.wdt:
                    if reg.wtime.textoFloat() > 0:
                        reg.wdepth.setCurrentIndex(0)
                    elif reg.wdepth.currentIndex() > 0:
                        reg.wtime.ponFloat(0.0)

                QTUtil.refresh_gui()

    resultado = FormLayout.fedit(lista, title=_("Analysis Configuration"), parent=parent, anchoMinimo=460, icon=Iconos.Opciones(), dispatch=dispatchR)

    if resultado:
        accion, liResp = resultado

        if siModoAmpliado:
            liGen, liVar, liBlunders, liBrilliancies, liST = liResp
        else:
            liGen = liResp

        alm.engine = liGen[0]
        alm.vtime = int(liGen[1] * 1000)
        alm.depth = liGen[2]
        alm.timedepth = liGen[3]
        alm.multiPV = liGen[4]
        alm.priority = liGen[5]

        if siModoAmpliado:
            color = liGen[6]
            alm.white = color != "BLACK"
            alm.black = color != "WHITE"
            alm.num_moves = liGen[7]
            alm.book = liGen[8]
            alm.book_name = alm.book.name if alm.book else None
            alm.delete_previous = liGen[9]
            alm.from_last_move = liGen[10]
            alm.show_graphs = liGen[11]

            (alm.include_variations, alm.limit_include_variations, alm.best_variation, alm.info_variation, alm.si_pdt, alm.one_move_variation) = liVar

            (alm.kblunders, alm.tacticblunders, alm.pgnblunders, alm.oriblunders, alm.bmtblunders) = liBlunders

            (alm.dpbrilliancies, alm.ptbrilliancies, alm.fnsbrilliancies, alm.pgnbrilliancies, alm.oribrilliancies, alm.bmtbrilliancies) = liBrilliancies

            (alm.stability, alm.st_depths, alm.st_centipawns, alm.st_timelimit) = liST

        dic = {}
        for x in dir(alm):
            if not x.startswith("__"):
                dic[x] = getattr(alm, x)
        Util.save_pickle(configuration.file_param_analysis(), dic)

        return alm
    else:
        return None


def massive_analysis_parameters(parent, configuration, siVariosSeleccionados, siDatabase=False):
    alm = leeDicParametros(configuration)

    # Datos
    liGen = [SEPARADOR]

    # # Tutor
    li = configuration.ayudaCambioTutor()
    li[0] = alm.engine
    liGen.append((_("Engine") + ":", li))

    liGen.append(SEPARADOR)

    # # Time
    config = FormLayout.Editbox(_("Duration of engine analysis (secs)"), 40, tipo=float)
    liGen.append((config, alm.vtime / 1000.0))

    # Depth
    liDepths = [("--", 0)]
    for x in range(1, 31):
        liDepths.append((str(x), x))
    config = FormLayout.Combobox(_("Depth"), liDepths)
    liGen.append((config, alm.depth))

    # Time+Depth
    liGen.append(("%s+%s:" % (_("Time"), _("Depth")), alm.timedepth))

    # MultiPV
    liGen.append(SEPARADOR)
    li = [(_("Default"), "PD"), (_("Maximum"), "MX")]
    for x in (1, 3, 5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200):
        li.append((str(x), str(x)))
    config = FormLayout.Combobox(_("Number of moves evaluated by engine(MultiPV)"), li)
    liGen.append((config, alm.multiPV))
    liGen.append(SEPARADOR)

    liJ = [(_("White"), "WHITE"), (_("Black"), "BLACK"), (_("White & Black"), "BOTH")]
    config = FormLayout.Combobox(_("Analyze only color"), liJ)
    if alm.white and alm.black:
        color = "BOTH"
    elif alm.black:
        color = "BLACK"
    elif alm.white:
        color = "WHITE"
    else:
        color = "BOTH"
    liGen.append((config, color))

    liGen.append(('<div align="right">' + _("Only player moves") + ":<br>%s</div>" % _("(You can add multiple aliases separated by ; and wildcard * )"), ""))

    fvar = configuration.file_books
    list_books = Books.ListBooks()
    list_books.restore_pickle(fvar)
    # Comprobamos que todos esten accesibles
    list_books.check()
    defecto = list_books.lista[0]
    li = [("--", None)]
    for book in list_books.lista:
        if book.name == alm.book_name:
            defecto = book
        li.append((book.name, book))
    config = FormLayout.Combobox(_("Do not scan the opening moves based on book"), li)
    liGen.append((config, defecto))

    liGen.append((_("Start from the end of the game") + ":", alm.from_last_move))

    liGen.append(SEPARADOR)
    liGen.append((_("Redo any existing prior analyses (if they exist)") + ":", alm.delete_previous))

    liGen.append(SEPARADOR)
    liGen.append((_("Only selected games") + ":", siVariosSeleccionados))

    liVar = form_variations(alm)

    liBlunders, liBrilliancies = formBlundersBrilliancies(alm, configuration)

    lista = []
    lista.append((liGen, _("General options"), ""))
    lista.append((liVar, _("Variations"), ""))
    lista.append((liBlunders, _("Wrong moves"), ""))
    lista.append((liBrilliancies, _("Brilliancies"), ""))

    reg = Util.Record()
    reg.form = None

    def dispatchR(valor):
        if reg.form is None:
            if isinstance(valor, FormLayout.FormTabWidget):
                reg.form = valor
                reg.wtime = valor.getWidget(0, 1)
                reg.wdepth = valor.getWidget(0, 2)
                reg.wdt = valor.getWidget(0, 3)
            elif isinstance(valor, FormLayout.FormWidget):
                reg.form = valor
                reg.wtime = valor.getWidget(1)
                reg.wdepth = valor.getWidget(2)
                reg.wdt = valor.getWidget(3)
        else:
            sender = reg.form.sender()
            if not reg.wdt.isChecked():
                if sender == reg.wtime:
                    if reg.wtime.textoFloat() > 0:
                        reg.wdepth.setCurrentIndex(0)
                elif sender == reg.wdepth:
                    if reg.wdepth.currentIndex() > 0:
                        reg.wtime.ponFloat(0.0)
                elif sender == reg.wdt:
                    if reg.wtime.textoFloat() > 0:
                        reg.wdepth.setCurrentIndex(0)
                    elif reg.wdepth.currentIndex() > 0:
                        reg.wtime.ponFloat(0.0)

                QTUtil.refresh_gui()

    resultado = FormLayout.fedit(lista, title=_("Mass analysis"), parent=parent, anchoMinimo=460, icon=Iconos.Opciones(), dispatch=dispatchR)

    if resultado:
        accion, liResp = resultado

        liGen, liVar, liBlunders, liBrilliancies = liResp

        alm.engine, vtime, alm.depth, alm.timedepth, alm.multiPV, color, cjug, alm.book, alm.from_last_move, alm.delete_previous, alm.siVariosSeleccionados = liGen

        alm.vtime = int(vtime * 1000)
        alm.white = color != "BLACK"
        alm.black = color != "WHITE"
        cjug = cjug.strip()
        alm.li_players = cjug.upper().split(";") if cjug else None
        alm.book_name = alm.book.name if alm.book else None

        alm.kblunders, alm.tacticblunders, alm.pgnblunders, alm.oriblunders, alm.bmtblunders = liBlunders

        alm.include_variations, alm.limiteinclude_variations, alm.best_variation, alm.info_variation, alm.si_pdt, alm.one_move_variation = liVar

        alm.dpbrilliancies, alm.ptbrilliancies, alm.fnsbrilliancies, alm.pgnbrilliancies, alm.oribrilliancies, alm.bmtbrilliancies = liBrilliancies

        dic = {}
        for x in dir(alm):
            if not x.startswith("__"):
                dic[x.upper()] = getattr(alm, x)
        Util.save_pickle(configuration.file_param_analysis(), dic)

        if not (alm.tacticblunders or alm.pgnblunders or alm.bmtblunders or alm.fnsbrilliancies or alm.pgnbrilliancies or alm.bmtbrilliancies or siDatabase):
            QTUtil2.message_error(parent, _("No file was specified where to save results"))
            return

        return alm
    else:
        return None
