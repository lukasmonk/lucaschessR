import base64
import os
import pickle
import shutil
import sqlite3
import subprocess

import Code
from Code import Util
from Code.Base import Game, Move
from Code.Base.Constantes import *
from Code.Databases import DBgames
from Code.Engines import EngineResponse
from Code.QT import QTUtil2
from Code.SQL import UtilSQL

class DicSQLV11(object):
    def __init__(self, nomDB, tabla="Data"):
        self.table = tabla

        self._conexion = sqlite3.connect(nomDB)

        cursor = self._conexion.cursor()
        cursor.execute("pragma table_info(%s)" % tabla)
        if not cursor.fetchall():
            sql = "CREATE TABLE %s( KEY TEXT PRIMARY KEY, VALUE TEXT );" % tabla
            cursor.execute(sql)
            self._conexion.commit()
            cursor.close()

        self.stKeys = set()
        cursor = self._conexion.cursor()
        sql = "SELECT KEY FROM %s" % self.table
        cursor.execute(sql)
        li = cursor.fetchall()
        for reg in li:
            self.stKeys.add(reg[0])
        cursor.close()

    def __getitem__(self, key):
        key = str(key)
        if key in self.stKeys:
            cursor = self._conexion.cursor()
            sql = "SELECT VALUE FROM %s WHERE KEY= ?" % self.table
            cursor.execute(sql, (key,))
            li = cursor.fetchone()
            cursor.close()
            dato = base64.decodestring(li[0].encode("utf-8", errors="ignore"))
            obj = pickle.loads(dato)
            return obj
        else:
            return None

    def __len__(self):
        return len(self.stKeys)

    def close(self):
        if self._conexion:
            self._conexion.close()
            self._conexion = None

    def keys(self, siOrdenados=False, siReverse=False):
        li = list(self.stKeys)
        return sorted(li, reverse=siReverse) if siOrdenados else li

    def get(self, key, default):
        key = str(key)
        if key in self.stKeys:
            return self.__getitem__(key)
        else:
            return default

    def __enter__(self):
        return self

    def __exit__(self, xtype, value, traceback):
        self.close()


class LIVersion11:
    def __init__(self, nomFichero):
        self.nomFichero = nomFichero
        self._conexion = sqlite3.connect(nomFichero)
        # self._conexion.text_factory = lambda x: str(x, "utf-8", "ignore")

    def __getitem__(self, xid):
        sql = "select DATO from datos where ROWID=%d" % (xid + 1,)
        cursor = self._conexion.cursor()
        cursor.execute(sql)
        dato = cursor.fetchone()
        value = dato[0]
        return eval(value)

    def __len__(self):
        sql = "select COUNT(DATO) from datos"
        cursor = self._conexion.cursor()
        cursor.execute(sql)
        resp = cursor.fetchone()
        cursor.close()
        return resp[0]

    def close(self):
        if self._conexion:
            self._conexion.close()
            self._conexion = None


class Version11:
    def __init__(self, procesador):
        self.procesador = procesador
        self.configuration = procesador.configuration
        self.wowner = procesador.main_window
        self.dic_cnags = self.dic_cnag_nag()

    @staticmethod
    def py27(*args):
        pt = os.path.join(Code.folder_OS, "Version11", "python.exe")
        li = [pt]
        li.extend(args)
        return subprocess.call(li)

    def dic_cnag_nag(self):
        d = {}
        for k, v in dicHTMLnags.items():
            d[v] = k
        for k, v in dicHTMLnagsTxt.items():
            d[v] = k
        return d

    def phase2(self, pb: QTUtil2.BarraProgreso1, entry: os.DirEntry):
        dest = entry.name

        name = ".".join(entry.name.split(".")[:-2])
        pb.ponRotulo(name)

        li = dest.split(".")
        dest = ".".join(li[:-2])
        path_dest = os.path.join(Code.configuration.folder_databases(), dest + ".lcdb")
        db_dest = DBgames.DBgames(path_dest)
        db_ori = LIVersion11(entry.path)
        total = len(db_ori)
        pb.ponTotal(total)
        for x in range(total):
            pb.pon(x + 1)
            if pb.is_canceled():
                break
            dic = db_ori[x]
            g = Game.Game(fen=dic.get("INIFEN"))
            g.set_tags(dic["LITAGS"])
            result = g.get_tag("Result")
            g.set_termination(dic["TERMINATION"], result if result else RESULT_UNKNOWN)
            li_moves = dic["MOVES"]
            current_position = g.last_position.copia()
            for dic_mv in li_moves:
                pv = dic_mv["M"]
                position = current_position.copia()
                position.moverPV(pv)
                move = Move.Move(g, position_before=current_position, position=position, from_sq=pv[:2], to_sq=pv[2:4], promotion=pv[4:])
                if "VARIATIONS" in dic_mv:
                    li_varpgn = dic_mv["VARIATIONS"]
                    fen_base = current_position.fen()
                    for varpgn in li_varpgn:
                        gv = Game.fen_game(fen_base, varpgn)
                        if gv:
                            move.add_variation(gv)
                if "COMMENT" in dic_mv:
                    move.comment = dic_mv["COMMENT"]
                if "$NAGS" in dic_mv:
                    nags = dic_mv["$NAGS"]
                    for nag in nags.split(" "):
                        if nag.isdigit():
                            move.add_nag(int(nag))
                if "NAGS" in dic_mv:
                    nags = dic_mv["NAGS"]
                    for nag in nags.split(" "):
                        if nag in self.dic_cnags:
                            move.add_nag(self.dic_cnags[nag])
                if "AMRM" in dic_mv:
                    mrm_pos = dic_mv["APOS"]
                    mrm_save = dic_mv["AMRM"]
                    mrm = EngineResponse.MultiEngineResponse(None, True)
                    mrm.restore(mrm_save)
                    move.analysis = mrm, mrm_pos

                current_position = position.copia()
                g.add_move(move)

            db_dest.insert(g)
        db_ori.close()
        if pb.is_canceled():
            db_dest.close()
            return False

        db_dest.commit()
        db_dest.close()

        shutil.move(entry.path, entry.path + ".imported")
        return True

    def databases(self):
        dic = self.configuration.read_variables("VERSION11")
        titulo = _("Select the folder with the %s to be imported") % _("Databases")
        QTUtil2.message(self.wowner, titulo)
        folder = QTUtil2.leeCarpeta(self.wowner, dic.get("FOLDER", "../.."), titulo=titulo)
        if not folder:
            return
        um = QTUtil2.unMomento(self.wowner, _("Working...") + "\n This is a very slow process")
        dic["FOLDER"] = folder
        self.configuration.write_variables("VERSION11", dic)

        ini_curdir = os.curdir
        os.chdir(os.path.join(Code.folder_OS, "Version11"))
        self.py27("ConversionDB.py", "folder", folder)
        os.chdir(ini_curdir)
        um.final()

        pb = QTUtil2.BarraProgreso1(self.wowner, _("Importing"), formato1="%p%")
        pb.mostrar()

        entry: os.DirEntry
        for entry in os.scandir(folder):
            if entry.name.endswith(".convert_end"):
                if not self.phase2(pb, entry):
                    break

        pb.cerrar()

    def import_openingline(self, base_folder, ori_path: str):
        ori_path = os.path.abspath(ori_path)
        ori_folder = os.path.dirname(ori_path)
        subfolder = os.path.relpath(ori_folder, base_folder)
        if subfolder == ".":
            dest_path = os.path.join(Code.configuration.folder_base_openings, os.path.basename(ori_path))
            op_idx = os.path.join(Code.configuration.folder_base_openings, "openinglines.pk")
        else:
            dest_path = os.path.join(Code.configuration.folder_base_openings, subfolder, os.path.basename(ori_path))

            folder_dest = os.path.dirname(dest_path)
            if not Util.create_folder(folder_dest):
                try:
                    os.makedirs(folder_dest)
                except:
                    pass
            op_idx = os.path.join(Code.configuration.folder_base_openings, subfolder, "openinglines.pk")
        Util.remove_file(op_idx)
        dest_path = Util.filename_unique(dest_path)
        for tabla in ("CONFIG", "FEN", "FENVALUES"):
            db11 = DicSQLV11(ori_path, tabla=tabla)
            if len(db11) > 0:
                db = UtilSQL.DictSQL(dest_path, tabla=tabla)
                li_keys = db11.keys()
                for key in li_keys:
                    try:
                        db[key] = db11[key]
                    except:
                        pass
                db.close()
            db11.close()

        conexion_dest = sqlite3.connect(dest_path)
        conexion_dest.execute("CREATE TABLE IF NOT EXISTS LINES( XPV TEXT PRIMARY KEY );")
        conexion_dest.commit()

        conexion_ori = sqlite3.connect(ori_path)
        cursor_ori = conexion_ori.execute("SELECT XPV FROM LINES")
        for raw in cursor_ori.fetchall():
            conexion_dest.execute("INSERT INTO LINES( XPV ) VALUES( ? )", raw)
        conexion_dest.commit()

        conexion_ori.close()
        conexion_dest.close()

    def import_openinglines_folder(self, base_folder, folder):
        li_folders = []
        entry: os.DirEntry
        for entry in os.scandir(folder):
            if entry.name.endswith(".opk"):
                self.import_openingline(base_folder, entry.path)
            elif entry.is_dir():
                li_folders.append(entry)

        for entry in li_folders:
            self.import_openinglines_folder(base_folder, entry.path)

    def openinglines(self):
        dic = self.configuration.read_variables("VERSION11")
        titulo = _("Select the folder with the %s to be imported") % _("Opening lines")
        QTUtil2.message(self.wowner, titulo)
        folder = QTUtil2.leeCarpeta(self.wowner, dic.get("FOLDER_OPENINGLINES", "../.."), titulo=titulo)
        if not folder:
            return
        dic["FOLDER_OPENINGLINES"] = os.path.abspath(folder)
        self.configuration.write_variables("VERSION11", dic)
        self.import_openinglines_folder(folder, folder)
        QTUtil2.message(self.wowner, _("Imported"))

    def run(self, tipo):
        if tipo == "databases":
            self.databases()
        elif tipo == "openinglines":
            self.openinglines()
