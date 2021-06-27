import FasterCode

from operator import attrgetter

import Code
from Code.Config import TrListas
from Code import Util


class OpeningStd:
    def __init__(self, key):
        self.name = key
        self.trNombre = key
        self.nivel = 0
        self.padre = None
        self.hijos = []
        self.a1h8 = ""
        self.pgn = ""
        self.eco = ""
        self.siBasic = False

    def tr_pgn(self):
        p = ""
        pzs = "KQRBNPkqrbnp"
        pgn = self.pgn
        for n, c in enumerate(pgn):
            if c in pzs and not pgn[n + 1].isdigit():
                c = TrListas.letterPiece(c)
            p += c
        return p

    def __str__(self):
        return self.name + " " + self.pgn


class ListaOpeningsStd:
    def __init__(self):
        self.dic = None
        self.dic_fenm2 = None
        self.hijos = None
        self.lia1h8 = None
        self.max_ply = None

    def reset(self, configuration, si_basic, si_entrenar):
        self.dic = {}
        self.hijos = []
        fichero_pers = configuration.file_pers_openings()
        self.lee(fichero_pers, si_entrenar)
        self.lia1h8 = list(self.dic.keys())

        if si_basic:
            for bl in self.dic.values():
                bl.trOrdena = ("A" if bl.siBasic else "B") + bl.trNombre.upper()
            self.hijos = self.ordena(self.hijos, 0)

        dfen = {}
        make_pv = FasterCode.make_pv
        fen_fenm2 = FasterCode.fen_fenm2

        mx = 0
        for n, (pv, o_ap) in enumerate(self.dic.items(), 1):
            fen = make_pv(pv)
            dfen[fen_fenm2(fen)] = o_ap
            if n > mx:
                mx = n
        self.dic_fenm2 = dfen
        self.max_ply = mx

    def ordena(self, hijos, n):
        if hijos:
            hijos = sorted(hijos, key=attrgetter("trOrdena"))
            for hijo in hijos:
                hijo.hijos = self.ordena(hijo.hijos, n + 8)
        return hijos

    @staticmethod
    def read_standard(dic):
        list_std = TrListas.list_std()

        for name, eco, a1h8, pgn, siBasic in list_std:
            bloque = OpeningStd(name)
            bloque.eco = eco
            bloque.a1h8 = a1h8
            bloque.pgn = pgn
            bloque.siBasic = siBasic
            dic[bloque.a1h8] = bloque

    @staticmethod
    def read_personal(fichero_pers, si_entrenar):
        lista = Util.restore_pickle(fichero_pers)
        txt = ""
        if lista:
            for reg in lista:
                estandar = reg["ESTANDAR"]
                if si_entrenar or estandar:
                    txt += "\n[%(NOMBRE)s]\nECO=%(ECO)s\nA1H8=%(A1H8)s\nPGN=%(PGN)s\nBASIC=True" % reg
        return txt

    def lee(self, fichero_pers, si_entrenar):
        d = {}
        self.read_standard(d)
        txt = self.read_personal(fichero_pers, si_entrenar)

        li = txt.split("\n")

        bloque = None
        for linea in li:
            linea = linea.strip()
            if linea:
                if linea.startswith("["):
                    if bloque:
                        d[bloque.a1h8] = bloque
                    bloque = OpeningStd(linea.strip()[1:-1].strip())
                else:
                    c, v = linea.split("=")
                    if c == "A1H8":
                        bloque.a1h8 = v
                    elif c == "PGN":
                        bloque.pgn = v
                    elif c == "BASIC":
                        bloque.siBasic = v == "True"
                    elif c == "ECO":
                        bloque.eco = v
        if bloque:
            d[bloque.a1h8] = bloque

        self.dic = d

        li = sorted(d.keys())
        for k in li:
            bloque = d[k]
            a1h8 = bloque.a1h8
            n = a1h8.rfind(" ")
            while n > 0:
                a1h8 = a1h8[:n]
                if a1h8 in d:
                    bloque_padre = d[a1h8]
                    nivel = bloque_padre.nivel + 1
                    if nivel > 8:
                        bloque_padre = bloque_padre.padre
                        nivel = bloque_padre.nivel + 1
                    hijos = bloque_padre.hijos
                    if hijos is None:
                        bloque_padre.hijos = hijos = []
                    hijos.append(bloque)
                    bloque.padre = bloque_padre
                    bloque.nivel = nivel
                    break
                n = a1h8.rfind(" ")
            if n <= 0:
                self.hijos.append(bloque)

    def assign_transposition(self, game):
        game.transposition = None
        if not (game.opening is None or game.pending_opening):
            for nj, move in enumerate(game.li_moves):
                if not move.in_the_opening:
                    fenm2 = move.position.fenm2()
                    if fenm2 in self.dic_fenm2:
                        game.transposition = self.dic_fenm2[fenm2]
                        game.jg_transposition = move

    def assign_opening(self, game):
        game.opening = None
        if not game.siFenInicial():
            game.pending_opening = False
            return
        game.pending_opening = True
        a1h8 = ""
        for nj, move in enumerate(game.li_moves):
            if move.in_the_opening:
                move.in_the_opening = False
            a1h8 += move.movimiento()
            if a1h8 in self.dic:
                game.opening = self.dic[a1h8]
                for nP in range(nj + 1):
                    game.move(nP).in_the_opening = True
                no_hay_mas = True
                for k in self.dic:
                    if k.startswith(a1h8) and k != a1h8:
                        no_hay_mas = False
                        break
                if no_hay_mas:
                    game.pending_opening = False  # la ponemos como definitiva
                    return
            a1h8 += " "
        # Hay alguna posible ?
        a1h8 = a1h8.strip()
        for k in self.dic:
            if k.startswith(a1h8):
                return  # volvemos con la opening pendiente aun
        game.pending_opening = False  # No hay ninguna aplicable

    def list_possible_openings(self, game, si_todas=False):
        a1h8 = ""
        for move in game.li_moves:
            a1h8 += " " + move.movimiento()
        a1h8 = a1h8[1:]
        li = []

        # Las ordenamos para que esten antes las principales que las variantes
        lik = sorted(self.dic.keys())

        si_basic = len(game) == 0
        if si_todas:
            si_basic = False

        for k in lik:
            if k.startswith(a1h8) and len(k) > len(a1h8):
                # Comprobamos que no sea una variante de las a_adidas, no nos interesan para mostrar options al usuario
                si_mas = True
                for xap in li:
                    if k.startswith(xap.a1h8):
                        si_mas = False
                        break
                if si_mas:
                    xap = self.dic[k]
                    xap.liMovs = a1h8[len(k) :].strip().split(" ")
                    if si_basic and not xap.siBasic:
                        continue
                    li.append(xap)

        return li if li else None

    def base_xpv(self, xpv):
        lipv = FasterCode.xpv_pv(xpv).split(" ")
        last_ap = None

        FasterCode.set_init_fen()
        mx = self.max_ply + 3
        for n, pv in enumerate(lipv):
            if n > mx:
                break
            FasterCode.make_move(pv)
            fen = FasterCode.get_fen()
            fenm2 = FasterCode.fen_fenm2(fen)
            if fenm2 in self.dic_fenm2:
                last_ap = self.dic_fenm2[fenm2]
        return last_ap

    def xpv(self, xpv):
        last_ap = self.base_xpv(xpv)
        return last_ap.trNombre if last_ap else ""


ap = ListaOpeningsStd()
apTrain = ListaOpeningsStd()


def reset():
    configuration = Code.configuration
    ap.reset(configuration, False, False)
    apTrain.reset(configuration, True, True)
