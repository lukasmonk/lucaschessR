import os
import sys
import sqlite3
import time
from imp import reload

reload(sys)
sys.setdefaultencoding("latin-1")
sys.path.insert(0, os.curdir)

current_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
if current_dir:
    os.chdir(current_dir)

from Code import DBgames, Util, DBgamesFEN

sys.path.append(os.path.join(current_dir, "Code"))

import Code.Traducir as Traducir
Traducir.install()

(
    RS_WIN_PLAYER,
    RS_WIN_OPPONENT,
    RS_DRAW,
    RS_DRAW_REPETITION,
    RS_DRAW_50,
    RS_DRAW_MATERIAL,
    RS_WIN_PLAYER_TIME,
    RS_WIN_OPPONENT_TIME,
    RS_UNKNOWN,
    RS_WIN_WHITE,
    RS_WIN_BLACK,
) = range(11)

RESULT_UNKNOWN, RESULT_WIN_WHITE, RESULT_WIN_BLACK, RESULT_DRAW = ("*", "1-0", "0-1", "1/2-1/2")

(
    TERMINATION_MATE,
    TERMINATION_DRAW_STALEMATE,
    TERMINATION_DRAW_REPETITION,
    TERMINATION_DRAW_MATERIAL,
    TERMINATION_DRAW_50,
    TERMINATION_DRAW_AGREEMENT,
    TERMINATION_RESIGN,
    TERMINATION_ADJUDICATION,
    TERMINATION_WIN_ON_TIME,
    TERMINATION_UNKNOWN,
) = ("MT", "DS", "DR", "DM", "D5", "DA", "RS", "AD", "LT", "UN")

class LIdisk:
    def __init__(self, nomFichero):
        self.nomFichero = nomFichero
        self._conexion = sqlite3.connect(nomFichero)
        # self._conexion.text_factory = lambda x: unicode(x, "utf-8", "ignore")

        try:
            sql = "CREATE TABLE datos( DATO TEXT );"
            self._conexion.cursor().execute(sql)
        except:
            pass

    def append_fast(self, valor):
        sql = "INSERT INTO datos( DATO ) VALUES( ? )"
        liValores = [str(valor)]
        self._conexion.execute(sql, liValores)

    def __len__(self):
        sql = "select COUNT(DATO) from datos"
        cursor = self._conexion.cursor()
        cursor.execute(sql)
        resp = cursor.fetchone()
        cursor.close()
        return resp[0]

    def close_fast(self):
        self._conexion.commit()
        self._conexion.close()

    def commit(self):
        self._conexion.commit()


def conversion(db):
    # type: (object) -> object
    filepath = db.nomFichero
    convertpath = filepath + ".convert"
    db_conv = LIdisk(convertpath)

    hechos = len(db_conv)

    dic_tags = {}

    total = db.all_reccount() - hechos
    t0 = time.time()
    if total > 0:
        nom = os.path.basename(filepath)
        for n, pc in enumerate(db.yield_todas(hechos), 1):
            if n%100 == 0 or (total -n) < 100:
                t = time.time() - t0
                t1 = t/n
                x = t1*(total-n)
                xt = t1*total
                s = "\r%3d' %2d\" | %3d' %2d\" |%8d/%8d " % (int(x/60), int(x) % 60, int(xt/60), int(xt) % 60, n if n < total else total, total)
                print s, "|", nom, "      ",
                if n % 1000:
                    db_conv.commit()

            if pc is None:
                continue
            dic = {"LITAGS": pc.liTags, "FIRSTCOMMENT": pc.firstComment, "INIFEN":pc.iniPosicion.fen()}
            for tag, valor in pc.liTags:
                dic_tags[tag.upper()] = tag
            termination = TERMINATION_UNKNOWN
            result = None
            li_moves = []

            def add(dc, key, value):
                if value:
                    dc[key] = value

            for jg in pc.liJugadas:
                move = jg.movimiento()
                dic_jg = {"M": move}
                add(dic_jg, "VARIATIONS", jg.variantes)
                add(dic_jg, "COMMENTS", jg.comentario)
                add(dic_jg, "$NAGS", jg.critica)
                add(dic_jg, "NAGS", jg.criticaDirecta)
                add(dic_jg, "COMMENT", jg.comentario)
                if jg.siJaqueMate:
                    termination = TERMINATION_MATE
                if jg.siAhogado:
                    termination = TERMINATION_DRAW_STALEMATE
                if jg.siTablasRepeticion:
                    termination = TERMINATION_DRAW_REPETITION
                if jg.siTablasFaltaMaterial:
                    termination = TERMINATION_DRAW_MATERIAL
                if jg.siTablas50:
                    termination = TERMINATION_DRAW_50
                if jg.siAbandono:
                    termination = TERMINATION_RESIGN
                if jg.siTablasAcuerdo:
                    termination = TERMINATION_DRAW_AGREEMENT

                if jg.analisis:
                    mrm, pos = jg.analisis
                    dic_jg["AMRM"] = mrm.save()
                    dic_jg["APOS"] = pos

                li_moves.append(dic_jg)

            dic["MOVES"] = li_moves
            dic["TERMINATION"] = termination
            db_conv.append_fast(dic)

        db_config = Util.DicSQL(convertpath, tabla="config")
        db_config["DIC_TAGS"] = dic_tags
        db_config.close()

    print
    print "---------+----------+-----------------------------------"
    db.close()
    db_conv.close_fast()

    for x in range(5):
        try:
            os.rename(convertpath, convertpath + "_end")
            return
        except:
            time.sleep(1.0)


def conversion_complete(filepath):
    db = DBgames.DBgames(filepath)
    conversion(db)


def conversion_positions(filepath):
    db = DBgamesFEN.DBgamesFEN(filepath)
    conversion(db)


def conversion_folder(folder, extension, rutina_conversion):
    li = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            if path.endswith(extension):
                convert_end = path + ".convert_end"
                imported = path + ".convert_end.imported"
                if not (os.path.isfile(convert_end) or os.path.isfile(imported)):
                    rutina_conversion(path)
        elif os.path.isdir(path):
            li.append(path)

    for folder in li:
        conversion_folder(folder, extension, rutina_conversion)


def conversion_folder_base(folder):
    print "Folder:", folder
    print "---------+----------+-------------------+---------------"
    print "PENDING  |   TOTAL  |     REGISTERS     | FILE"
    print "---------+----------+-------------------+---------------"
    conversion_folder(folder, "lcg", conversion_complete)
    conversion_folder(folder, "lcf", conversion_positions)


if sys.argv[1] == "folder":
    path = sys.argv[2]
    conversion_folder_base(path)
