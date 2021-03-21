import os
import subprocess
import sqlite3

import Code
from Code.Base.Constantes import *
from Code.Base import Game, Move, Position
from Code.Engines import EngineResponse
from Code.QT import QTVarios, QTUtil2, Iconos


class LIBridge:
    def __init__(self, nomFichero):
        self.nomFichero = nomFichero
        self._conexion = sqlite3.connect(nomFichero)
        self._conexion.text_factory = lambda x: str(x, "utf-8", "ignore")

    def __getitem__(self, xid):
        sql = "select DATO from datos where ROWID=%d" % (xid + 1,)
        cursor = self._conexion.cursor()
        cursor.execute(sql)
        dato = cursor.fetchone()
        return dato[0]

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


class Bridge11:
    def __init__(self, procesador):
        self.procesador = procesador
        self.configuration = procesador.configuration
        self.wowner = procesador.main_window
        self.dic_cnags = self.dic_cnag_nag()

    @staticmethod
    def py27(*args):
        pt = os.path.join(Code.folder_resources, "Bridge11", "python.exe")
        li = [pt,]
        li.extend(args)
        return subprocess.call(li)

    def dic_cnag_nag(self):
        d = {}
        for k, v in dicHTMLnags.items():
            d[v] = k
        for k, v in dicHTMLnagsTxt.items():
            d[v] = k
        return d

    def phase2(self, entry:os.DirEntry):
        db = LIBridge(entry.path)
        for x in range(len(db)):
            dato = db[x]
            dic = eval(dato)
            if "INIFEN" in dic:
                g = Game.Game(fen=dic["INIFEN"])
            else:
                g = Game.Game()
            g.set_tags(dic["LITAGS"])
            result = g.get_tag("Result")
            g.set_termination(dic["TERMINATION"], result if result else RESULT_UNKNOWN)
            li_moves = dic["MOVES"]
            current_position = g.last_position.copia()
            for dic_mv in li_moves:
                pv = dic_mv["MV"]
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
                if "MRM" in dic_mv:
                    mrm_pos =  dic_mv["MRM_POS"]
                    mrm_save = dic_mv["MRM"]
                    mrm = EngineResponse.MultiEngineResponse(None, True)
                    mrm.restore(mrm_save)
                    move.analysis = mrm, mrm_pos

                current_position = position.copia()
                g.add_move(move)
            print(dic)

        db.close()

    def run(self):
        dic = self.configuration.read_variables("BRIDGE11")
        menu = QTVarios.LCMenu(self.wowner)
        menu.opcion("db_folder", _("Import databases in a folder"), Iconos.Carpeta())
        menu.opcion("db_file", _("Import a database"), Iconos.Database())
        resp = menu.lanza()
        if resp == "db_folder":
            folder = QTUtil2.leeCarpeta(self.wowner, dic.get("FOLDER", "../.."))
            if not folder:
                return
            dic["FOLDER"] = folder
            self.configuration.write_variables("BRIDGE11", dic)

            ini_folder = os.curdir
            os.chdir(os.path.join(Code.folder_resources, "Bridge11"))
            self.py27("ImportDatabases.py", "folder", folder)
            os.chdir(ini_folder)

            entry: os.DirEntry
            for entry in os.scandir(folder):
                if entry.name.endswith(".convert_end"):
                    self.phase2(entry)




