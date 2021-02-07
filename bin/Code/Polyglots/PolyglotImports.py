import os
import math
import time
import shutil

import FasterCode
from PySide2 import QtCore, QtWidgets

from Code.SQL import UtilSQL
from Code.Databases import DBgames
from Code.QT import Colocacion
from Code.QT import Controles
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code.QT import FormLayout

from Code.Base.Constantes import *


class PolyglotImports:
    def __init__(self, wpolyglot):
        self.wpolyglot = wpolyglot
        self.configuration = wpolyglot.configuration
        self.db_entries = wpolyglot.db_entries
        self.pol_mkbin = wpolyglot.pol_mkbin
        self.path_mkbin = wpolyglot.path_mkbin

    def importar(self):
        menu = QTVarios.LCMenu(self.wpolyglot)
        menu.opcion("pgn", _("PGN"), Iconos.Board())
        menu.separador()
        menu.opcion("database", _("Database"), Iconos.Database())
        menu.separador()
        menu.opcion("polyglot", _("Polyglot book"), Iconos.Libros())
        menu.separador()
        resp = menu.lanza()
        if resp == "pgn":
            self.import_pgn()
        elif resp == "database":
            self.import_db()
        elif resp == "polyglot":
            self.import_polyglot()

    def exportar(self):
        file_def = os.path.basename(self.path_mkbin)[:-5] + "bin"
        resp = export_polyglot_config(self.wpolyglot, self.configuration, file_def)
        if resp is None:
            return None
        path_bin, uniform = resp

        export_create_polyglot(self.wpolyglot, path_bin, uniform, self.fuente_origen)

    def import_config(self, titulo):
        titulo = "%s %s" % (_("Import"), titulo)
        return import_polyglot_config(self.wpolyglot, self.configuration, titulo)

    def import_db(self):
        path_db = QTVarios.select_db(self.wpolyglot, self.configuration, True, False)
        if not path_db:
            return

        resp = self.import_config(os.path.basename(path_db))
        if resp is None:
            return
        plies, st_side, st_results, ru, min_games, min_score, calc_weight, save_score = resp

        db = UtilSQL.DictBig()

        def fsum(keymove, pt):
            num, pts = db.get(keymove, (0, 0))
            num += 1
            pts += pt
            db[keymove] = num, pts

        dltmp = ImportarPGNDB(self.wpolyglot, os.path.basename(path_db))
        dltmp.show()

        db_games = DBgames.DBgames(path_db)

        ok = add_db(db_games, plies, st_results, st_side, ru, time.time, 1.2, dltmp.dispatch, fsum)
        dltmp.close()
        if not ok:
            db.close()
            db_games.close()
            return

        self.merge(db, min_games, min_score, calc_weight, save_score)

    def import_pgn(self):
        path_pgn = QTVarios.select_pgn(self.wpolyglot)
        if not path_pgn:
            return

        resp = self.import_config(os.path.basename(path_pgn))
        if resp is None:
            return
        plies, st_side, st_results, ru, min_games, min_score, calc_weight, save_score = resp

        db = UtilSQL.DictBig()

        def fsum(keymove, pt):
            num, pts = db.get(keymove, (0, 0))
            num += 1
            pts += pt
            db[keymove] = num, pts

        dltmp = ImportarPGNDB(self.wpolyglot, os.path.basename(path_pgn))
        dltmp.show()
        ok = add_pgn(path_pgn, plies, st_results, st_side, ru.encode(), time.time, 1.2, dltmp.dispatch, fsum)
        dltmp.close()
        if not ok:
            db.close()
            return

        self.merge(db, min_games, min_score, calc_weight, save_score)

    def merge(self, db, min_games, min_score, calc_weight, save_score):
        g_nueva = iter(fuente_dbbig(db, min_games, min_score, calc_weight, save_score))
        g_origen = iter(self.fuente_origen())

        n_key, n_data = next(g_nueva)
        o_key, o_data = next(g_origen)

        ftemporal = self.configuration.ficheroTemporal("bin")
        um = QTUtil2.unMomento(self.wpolyglot, _("Saving..."))
        wpoly = FasterCode.PolyglotWriter(ftemporal)

        def write_data(dic_data):
            li = list(dic_data.keys())
            li.sort(key=lambda x: dic_data[x].weight, reverse=True)
            for imv in li:
                ent = dic_data[imv]
                if ent.weight > 0:
                    wpoly.write(ent)

        while not (n_key is None and o_key is None):
            if n_key is None:
                write_data(o_data)
                o_key, o_data = next(g_origen)
            elif o_key is None:
                write_data(n_data)
                n_key, n_data = next(g_nueva)
            else:
                if n_key < o_key:
                    write_data(n_data)
                    n_key, n_data = next(g_nueva)
                elif o_key < n_key:
                    write_data(o_data)
                    o_key, o_data = next(g_origen)
                else:
                    for imove, entry in n_data.items():
                        if imove not in o_data:
                            o_data[imove] = entry
                        elif n_data[imove].weight > 0:
                            o_data[imove].weight = n_data[imove].weight
                            if save_score and n_data[imove].score > 0:
                                o_data[imove].score = n_data[imove].score
                    write_data(o_data)
                    o_key, o_data = next(g_origen)
                    n_key, n_data = next(g_nueva)

        wpoly.close()

        self.pol_mkbin.close()

        shutil.copy(ftemporal, self.path_mkbin)

        self.wpolyglot.pol_mkbin = FasterCode.Polyglot(self.path_mkbin)

        self.db_entries.zap()

        db.close()

        um.final()

        self.wpolyglot.set_position(self.wpolyglot.position, False)

    def fuente_origen(self):
        li_externas = [(FasterCode.str_int(key_10), key_10) for key_10 in self.db_entries.keys()]
        li_externas.sort(key=lambda x:x[0])
        max_externas = len(li_externas)

        pos_externas = 0

        if len(self.pol_mkbin) > 0:
            current_key = 0
            dic_entries = {}
            for entry in self.pol_mkbin:

                if entry.key != current_key:
                    if current_key > 0:
                        # Anteriores externas se mandan
                        while pos_externas < max_externas:
                            ext_int, ext_str = li_externas[pos_externas]
                            if ext_int < current_key:
                                for entry_ext in self.db_entries[ext_str].values():
                                    dic_entries[entry_ext.move] = entry_ext
                                pos_externas += 1
                            else:
                                break
                        # Se juntan externas, internas, preferencia internas
                        while pos_externas < max_externas:
                            ext_int, ext_str = li_externas[pos_externas]
                            if ext_int == current_key:
                                for entry_ext in self.db_entries[ext_str].values():
                                    dic_entries[entry_ext.move] = entry_ext
                                pos_externas += 1
                            else:
                                break

                        # se envian
                        for entry_dic in dic_entries.values():
                            yield entry_dic.key, entry_dic

                    current_key = entry.key
                    dic_entries = {}

                dic_entries[entry.move] = entry

        while pos_externas < max_externas:
            ext_int, ext_str = li_externas[pos_externas]
            for entry_ext in self.db_entries[ext_str].values():
                yield entry_ext.key, entry_ext
            pos_externas += 1

        yield None, None

    def fuente_bin(self, path_bin):
        pol_bin = FasterCode.Polyglot(path_bin)

        key = None
        dic = None
        for entry in pol_bin:
            if key is None:
                key = entry.key
                dic = {}
            elif key != entry.key:
                yield key, dic
                dic = {}
                key = entry.key
            dic[entry.move] = entry
        if key is not None:
            yield key, dic

        yield None, None

    def fuente_origen_acum(self):
        key = None
        dic = None
        for key, entry in self.fuente_origen():
            if key is None:
                if entry is None:
                    yield None, None
                    return
                key = entry.key
                dic = {}
            elif key != entry.key:
                yield key, dic
                dic = {}
                key = entry.key
            dic[entry.move] = entry
        if key is not None:
            yield key, dic

        yield None, None

    def import_polyglot(self):
        dic = self.configuration.read_variables("POLYGLOT_IMPORT")

        folder = dic.get("FOLDER_BIN", "")

        path_bin = QTUtil2.leeFichero(self.wpolyglot, folder, "bin", titulo=_("Polyglot bin file name"))
        if not path_bin:
            return

        dic["FOLDER_BIN"] = os.path.dirname(path_bin)
        self.configuration.write_variables("POLYGLOT_IMPORT", dic)

        g_bin = iter(self.fuente_bin(path_bin))
        g_origen = iter(self.fuente_origen())

        n_key, n_data = next(g_bin)
        o_key, o_data = next(g_origen)

        ftemporal = self.configuration.ficheroTemporal("bin")
        um = QTUtil2.unMomento(self.wpolyglot, _("Saving..."))
        wpoly = FasterCode.PolyglotWriter(ftemporal)

        def write_data(dic_data):
            li = list(dic_data.keys())
            li.sort(key=lambda x: dic_data[x].weight, reverse=True)
            for imv in li:
                ent = dic_data[imv]
                if ent.weight > 0:
                    wpoly.write(ent)

        while not (n_key is None and o_key is None):
            if n_key is None:
                write_data(o_data)
                o_key, o_data = next(g_origen)
            elif o_key is None:
                write_data(n_data)
                n_key, n_data = next(g_bin)
            else:
                if n_key < o_key:
                    write_data(n_data)
                    n_key, n_data = next(g_bin)
                elif o_key < n_key:
                    write_data(o_data)
                    o_key, o_data = next(g_origen)
                else:
                    for imove, entry in n_data.items():
                        if imove not in o_data:
                            o_data[imove] = entry
                        elif n_data[imove].weight > 0:
                            o_data[imove].weight = n_data[imove].weight
                    write_data(o_data)
                    o_key, o_data = next(g_origen)
                    n_key, n_data = next(g_bin)

        wpoly.close()

        self.pol_mkbin.close()

        shutil.copy(ftemporal, self.path_mkbin)

        self.wpolyglot.pol_mkbin = FasterCode.Polyglot(self.path_mkbin)

        self.db_entries.zap()

        um.final()

        self.wpolyglot.set_position(self.wpolyglot.position, False)


class ImportarPGNDB(QtWidgets.QDialog):
    def __init__(self, parent, titulo):
        QtWidgets.QDialog.__init__(self, parent)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)

        self.is_canceled = False

        self.setWindowTitle(titulo)
        self.setWindowIcon(Iconos.Import8())
        self.fontB = Controles.TipoLetra(puntos=10, peso=75)

        self.lbgames_readed = Controles.LB(self).ponFuente(self.fontB)

        self.bp = QtWidgets.QProgressBar()
        self.bp.setFont(self.fontB)

        self.lb_previsto = Controles.LB(self)
        self.li_times = []
        self.time_inicial = None
        self.invalid_prevision = True
        self.total = None

        self.bt_cancelar = Controles.PB(self, _("Cancel"), self.cancelar, plano=False).ponIcono(Iconos.Delete())

        lyBT = Colocacion.H().relleno().control(self.bt_cancelar)

        layout = Colocacion.V()
        layout.control(self.lbgames_readed)
        layout.control(self.bp)
        layout.control(self.lb_previsto)
        layout.espacio(20)
        layout.otro(lyBT)

        self.setLayout(layout)

        self.setMinimumWidth(480)

    def test_invalid_prevision(self):
        if len(self.li_times) < 5:
            return
        ntm = len(self.li_times[-5:])
        media = 0.0
        for tm in self.li_times:
            media += tm
        media /= ntm
        sdev = 0
        for tm in self.li_times:
            sdev += (tm - media) ** 2
        sdev = math.sqrt(sdev / (ntm - 1))

        if sdev < media / 10:
            self.invalid_prevision = False

    def cancelar(self):
        self.is_canceled = True

    def dispatch(self, is_total, valor, num_games):
        if is_total:
            self.bp.setRange(0, valor)
            self.time_inicial = time.time()
            self.total = valor
        elif valor > 0:
            self.bp.setValue(valor)
            self.lbgames_readed.set_text("%s: %d" % (_("Games read"), num_games))
            tm = time.time() - self.time_inicial

            tm1 = tm / valor
            if self.invalid_prevision:
                self.li_times.append(tm1)
                self.test_invalid_prevision()
            else:
                previsto = int(tm1 * (self.total - valor))
                minutos = previsto // 60
                segundos = previsto % 60
                lb_min = _("minutes") if minutos > 1 else _("minute")
                self.lb_previsto.set_text(
                    "%s: %d %s %d %s" % (_("Pending time"), minutos, lb_min, segundos, _("seconds"))
                )

        QTUtil.refresh_gui()
        return not self.is_canceled


def add_db(db, plies, st_results, st_side, unknown_convert, ftime, time_dispatch, dispatch, fsum):
    time_prev = ftime()
    cancelled = False
    st_results = {x.decode() for x in st_results}

    dispatch(True, len(db), 0)
    for num_games, (xpv, result) in enumerate(db.yield_polyglot()):
        if (ftime() - time_prev) >= time_dispatch:
            time_prev = ftime()
            if not dispatch(False, num_games, num_games):
                cancelled = True
                break
        if not (result in st_results):
            continue
        if result == "*":
            result = unknown_convert

        if result == "1-0":
            pw = 2
            pb = 0
        elif result == "0-1":
            pw = 0
            pb = 2
        else:  # if result == b"1/2-1/2":
            pw = 1
            pb = 1

        if xpv.startswith("|"):
            nada, fen, xpv = xpv.split("|")
        else:
            fen = FEN_INITIAL
        lipv = FasterCode.xpv_lipv(xpv)[:plies]
        is_white = " w" in fen
        FasterCode.set_fen(fen)
        for mv in lipv:
            if is_white in st_side:
                move = FasterCode.string_movepolyglot(mv)
                fen = FasterCode.get_fen()
                key = FasterCode.hash_polyglot8(fen)
                keymove = FasterCode.keymove_str(key, move)
                pt = pw if is_white else pb
                fsum(keymove, pt)
            FasterCode.make_move(mv)
            is_white = not is_white

    return not cancelled


def add_pgn(path_pgn, plies, st_results, st_side, bunknown_convert, ftime, time_dispatch, dispatch, fsum):
    time_prev = ftime()
    cancelled = False
    bfen_inicial = FEN_INITIAL.encode()

    with FasterCode.PGNreader(path_pgn, plies) as fpgn:
        bsize = fpgn.size
        dispatch(True, bsize, 0)
        num_games = 0
        for (body, raw, pv, liFens, bdCab, bdCablwr, btell) in fpgn:
            if len(liFens) == 0:
                continue

            if (ftime() - time_prev) >= time_dispatch:
                time_prev = ftime()
                if not dispatch(False, btell, num_games):
                    cancelled = True
                    break

            result = bdCab.get(b"RESULT", b"*")
            if not (result in st_results):
                continue
            if result == b"*":
                result = bunknown_convert

            if result == b"1-0":
                pw = 2
                pb = 0
            elif result == b"0-1":
                pw = 0
                pb = 2
            else:  # if result == b"1/2-1/2":
                pw = 1
                pb = 1

            if b"FEN" in bdCab:
                bfen0 = bdCab[b"FEN"]
            else:
                bfen0 = bfen_inicial
            lipv = pv.split(" ")
            is_white = b" w" in bfen0
            for pos, bfen in enumerate(liFens):
                if is_white in st_side:
                    mv = lipv[pos]
                    move = FasterCode.string_movepolyglot(mv)
                    key = FasterCode.hash_polyglot(bfen0)
                    keymove = FasterCode.keymove_str(key, move)
                    pt = pw if is_white else pb
                    fsum(keymove, pt)

                is_white = not is_white
                bfen0 = bfen

            num_games += 1

    return not cancelled


def import_polyglot_config(owner, configuration, titulo):
    dic = configuration.read_variables("POLYGLOT_IMPORT")

    form = FormLayout.FormLayout(owner, titulo, Iconos.Import8(), anchoMinimo=440)
    form.separador()

    form.spinbox(_("Maximum half moves (plies)"), 1, 999, 60, dic.get("PLIES", 50))
    form.separador()

    li_options = (("%s + %s" % (_("White"), _("Black")), {True, False}), (_("White"), {True}), (_("Black"), {False}))
    form.combobox(_("Side to include"), li_options, dic.get("SIDE", {True, False}))
    form.separador()

    form.apart_simple(_("Include games when result is"))
    form.checkbox("1-0", dic.get("1-0", True))
    form.checkbox("0-1", dic.get("0-1", True))
    form.checkbox("1/2-1/2", dic.get("1/2-1/2", True))
    form.separador()
    li_options = ((_("Discard"), ""), ("1-0", "1-0"), ("0-1", "0-1"), ("1/2-1/2", "1/2-1/2"))
    form.combobox("%s %s" % (_("Unknown result"), _("convert to")), li_options, dic.get("*", ""))
    form.separador()

    form.spinbox(_("Minimum number of games"), 1, 999999, 50, dic.get("MINGAMES", 5))
    form.spinbox(_("Minimum score") + " (0-100)", 0, 100, 50, dic.get("MINSCORE", 0))

    form.separador()
    li_options = (
        (_("Number of games"), CALCWEIGHT_NUMGAMES),
        (_("Number of games") + " * " + _("Score"), CALCWEIGHT_NUMGAMES_SCORE),
        (_("Score") + "% * 100", CALCWEIGHT_SCORE),
    )
    form.combobox(_("Calculation of the weight"), li_options, dic.get("CALCWEIGHT", CALCWEIGHT_NUMGAMES))
    form.separador()
    form.checkbox(_("Save score"), dic.get("SAVESCORE", False))

    resultado = form.run()

    if not resultado:
        return None
    accion, resp = resultado
    plies, st_side, r1_0, r0_1, r1_1, ru, min_games, min_score, calc_weight, save_score = resp
    if not (r1_0 or r0_1 or r1_1 or ru != ""):
        return None

    st_results = set()
    if r1_0:
        st_results.add(b"1-0")
    if r1_1:
        st_results.add(b"1/2-1/2")
    if r0_1:
        st_results.add(b"0-1")
    if ru != "":
        st_results.add(b"*")

    dic["PLIES"] = plies
    dic["SIDE"] = st_side
    dic["1-0"] = r1_0
    dic["0-1"] = r0_1
    dic["1/2-1/2"] = r1_1
    dic["*"] = ru
    dic["MINGAMES"] = min_games
    dic["MINSCORE"] = min_score
    dic["CALCWEIGHT"] = calc_weight
    dic["SAVESCORE"] = save_score
    configuration.write_variables("POLYGLOT_IMPORT", dic)

    return plies, st_side, st_results, ru, min_games, min_score, calc_weight, save_score


def export_polyglot_config(owner, configuration, file_nom_def):
    dic = configuration.read_variables("POLYGLOT_EXPORT")
    form = FormLayout.FormLayout(owner, _("Export to"), Iconos.Export8(), anchoMinimo=440)
    form.separador()

    folder = dic.get("FOLDER", "")
    file_def = os.path.realpath(os.path.join(folder, file_nom_def))
    form.file(_("Polyglot book"), "bin", True, file_def)
    form.separador()
    form.checkbox(_("Uniform distribution"), dic.get("UNIFORM", False))
    form.separador()

    resultado = form.run()

    if not resultado:
        return None
    accion, resp = resultado
    path_bin, uniform = resp
    if not path_bin:
        return None

    path_bin = os.path.realpath(path_bin)
    dic["FOLDER"] = os.path.dirname(path_bin)
    dic["UNIFORM"] = uniform
    configuration.write_variables("POLYGLOT_EXPORT", dic)

    return path_bin, uniform


def export_create_polyglot(owner, path_bin, uniform, fuente_origen):
    um = QTUtil2.unMomento(owner, _("Saving..."))
    wpoly = FasterCode.PolyglotWriter(path_bin)

    for entry in fuente_origen():
        if entry is None:
            break
        if entry.weight > 0:
            if uniform:
                entry.weight = 100
            wpoly.write(entry)

    wpoly.close()

    um.final()

    QTUtil2.message_bold(owner, "%s\n%s" % (_("Saved"), path_bin))


def fuente_dbbig(db, min_games, min_score, calc_weight, save_score):
    db_iter = iter(db.items())
    current_key = None
    dic = None

    def pasa_filtro(dic_act):
        li = []
        max_weight = 0
        for imove, (num, suma) in dic_act.items():
            if (num < min_games) or ((suma / num) < (min_score / 50)):
                li.append(imove)
            elif suma > max_weight:
                max_weight = suma
        if len(li) > 0:
            if len(li) == len(dic_act):
                return False
            for imove in li:
                del dic_act[imove]
        if max_weight > 32767:
            factor = max_weight / 32767
            for imove, (num, suma) in dic.items():
                dic_act[imove] = (num // factor, suma // factor)
        return True

    def dic_entry(key, dic_act):
        d = {}
        for imove, (num, sum) in dic_act.items():
            e = FasterCode.Entry()
            e.key = key
            e.move = imove
            score = (sum / num) / 2.0 if num > 0.0 else 0.0
            if calc_weight == CALCWEIGHT_NUMGAMES:
                e.weight = sum
            elif calc_weight == CALCWEIGHT_NUMGAMES_SCORE:
                e.weight = int(sum * score)
            else:
                e.weight = int(score * 10_000)
            if save_score:
                e.score = int(score * 10_000)
            d[imove] = e
        return d

    while True:
        k, v = next(db_iter, (None, None))
        if k is None:
            break
        key, move = FasterCode.str_keymove(k)
        if key != current_key:
            if current_key is not None:
                if pasa_filtro(dic):
                    yield current_key, dic_entry(current_key, dic)
            current_key = key
            dic = {}
        dic[move] = v
    if current_key is not None:
        if pasa_filtro(dic):
            yield current_key, dic_entry(current_key, dic)

    yield None, None


def create_bin_from_dbbig(owner, path_bin, db, min_games, min_score, calc_weight, save_score):
    g_nueva = iter(fuente_dbbig(db, min_games, min_score, calc_weight, save_score))

    um = QTUtil2.unMomento(owner, _("Saving..."))
    wpoly = FasterCode.PolyglotWriter(path_bin)

    for n_key, dic_data in g_nueva:
        if n_key is not None:
            li = list(dic_data.keys())
            li.sort(key=lambda x: dic_data[x].weight, reverse=True)
            for imv in li:
                ent = dic_data[imv]
                if ent.weight > 0:
                    wpoly.write(ent)

    wpoly.close()

    um.final()
    QTUtil2.message_bold(owner, "%s\n%s" % (_("Saved"), path_bin))
