import os

import FasterCode

from Code.Base import Position
from Code.SQL import UtilSQL
from Code import Util
from Code.QT import Colocacion
from Code.QT import Columnas
from Code.QT import Controles
from Code.QT import Grid
from Code.QT import Iconos
from Code.Board import Board
from Code.QT import Delegados
from Code.QT import Voyager
from Code.QT import QTVarios
from Code.Polyglots import PolyglotImports


class WPolyglot(QTVarios.WDialogo):
    def __init__(self, wowner, configuration, path_dbbin):
        title = os.path.basename(path_dbbin)[:-6]
        QTVarios.WDialogo.__init__(self, wowner, title, Iconos.Book(), "polyglot")

        self.configuration = configuration
        self.path_dbbin = path_dbbin
        self.path_mkbin = self.path_dbbin[:-6] + ".mkbin"

        self.owner = wowner
        self.key = None
        self.key_str10 = None

        self.db_entries = UtilSQL.DictSQL(self.path_dbbin)
        if Util.filesize(self.path_mkbin) < 0:
            f = open(self.path_mkbin, "wb")
            f.close()
        self.pol_mkbin = FasterCode.Polyglot(self.path_mkbin)

        self.li_moves = []
        self.history = []

        self.pol_imports = PolyglotImports.PolyglotImports(self)

        conf_board = configuration.config_board("WPOLYGLOT", 48)
        self.board = Board.Board(self, conf_board)
        self.board.crea()
        self.board.set_dispatcher(self.mensajero)
        self.with_figurines = configuration.x_pgn_withfigurines

        o_columnas = Columnas.ListaColumnas()
        delegado = Delegados.EtiquetaPOS(True, siLineas=False) if self.configuration.x_pgn_withfigurines else None
        o_columnas.nueva("move", _("Move"), 80, centered=True, edicion=delegado, siEditable=False)
        o_columnas.nueva("%", "%", 60, siDerecha=True, siEditable=False)
        o_columnas.nueva("weight", _("weight"), 60, siDerecha=True, edicion=Delegados.LineaTexto(siEntero=True))
        o_columnas.nueva("score", _("Score"), 60, siDerecha=True, edicion=Delegados.LineaTexto(siEntero=True))
        o_columnas.nueva("depth", _("Depth"), 60, siDerecha=True, edicion=Delegados.LineaTexto(siEntero=True))
        o_columnas.nueva("learn", _("Learn"), 60, siDerecha=True, edicion=Delegados.LineaTexto(siEntero=True))
        self.grid_moves = Grid.Grid(self, o_columnas, siEditable=True)
        self.grid_moves.setMinimumWidth(self.grid_moves.anchoColumnas() + 20)

        li_acciones = (
            (_("Close"), Iconos.MainMenu(), self.terminar),
            None,
            (_("Takeback"), Iconos.Atras(), self.takeback),
            None,
            (_("Voyager"), Iconos.Voyager(), self.voyager),
            None,
            (_("Import"), Iconos.Import8(), self.pol_imports.importar),
            None,
            (_("Export"), Iconos.Export8(), self.pol_imports.exportar),
            None,
        )
        self.tb = Controles.TBrutina(self, li_acciones)

        ly2 = Colocacion.V().control(self.tb).control(self.grid_moves)

        layout = Colocacion.H().control(self.board).otro(ly2)
        self.setLayout(layout)

        self.restore_video()

        self.position = None
        position = Position.Position()
        position.set_pos_initial()
        self.set_position(position, True)

    def set_position(self, position, save_history):
        self.position = position
        self.position.set_lce()

        self.li_moves = [FasterCode.BinMove(info_move) for info_move in self.position.get_exmoves()]

        self.key, str_key, d_entries = self.pol_mkbin.dict_entries(position.fen())
        self.key_str10 = "%10s" % str_key
        for binmove in self.li_moves:
            mv = binmove.imove()
            if mv in d_entries:
                binmove.set_entry(d_entries[mv])

        dic_db = self.db_entries[self.key_str10]
        if dic_db is not None:
            for binmove in self.li_moves:
                mv = binmove.imove()
                if mv in dic_db:
                    binmove.set_entry(dic_db[mv])

        tt = sum(binmove.weight() for binmove in self.li_moves)
        for binmove in self.li_moves:
            binmove.porc = binmove.weight() * 100.0 / tt if tt > 0 else 0

        self.li_moves.sort(key=lambda x: x.weight(), reverse=True)
        self.grid_moves.refresh()
        self.board.set_position(position)
        self.board.activate_side(position.is_white)
        if save_history:
            self.history.append(self.position.fen())

    def grid_doble_click(self, grid, row, col):
        if col.key == "move":
            bin_move = self.li_moves[row]
            xfrom = bin_move.info_move.xfrom()
            xto = bin_move.info_move.xto()
            promotion = bin_move.info_move.promotion()
            self.mensajero(xfrom, xto, promotion)

    def grid_cambiado_registro(self, grid, row, o_column):
        if -1 < row < len(self.li_moves):
            bin_move = self.li_moves[row]
            self.board.put_arrow_sc(bin_move.info_move.xfrom(), bin_move.info_move.xto())

    def terminar(self):
        self.finalizar()
        self.accept()

    def grid_num_datos(self, grid):
        return len(self.li_moves)

    def grid_dato(self, grid, row, o_column):
        move = self.li_moves[row]
        key = o_column.key
        if key == "move":
            san = move.info_move.san()
            if self.with_figurines:
                is_white = self.position.is_white
                return san, is_white, None, None, None, None, False, True
            else:
                return san
        elif key == "%":
            return "%.1f%%" % move.porc if move.porc > 0 else ""
        else:
            valor = move.get_field(key)
            return str(valor) if valor else ""

    def grid_setvalue(self, grid, row, column, valor):
        binmove = self.li_moves[row]
        field = column.key
        if valor == "":
            valor = 0

        valor = int(valor)

        binmove.set_field(field, valor)
        dic = self.db_entries.get(self.key_str10, {})
        entry = binmove.get_entry()
        if entry.key == 0:
            entry.key = self.key
        if entry.move == 0:
            entry.move = binmove.imove()
        dic[entry.move] = entry
        self.db_entries[self.key_str10] = dic

        if field == "weight":
            tt = sum(binmove.weight() for binmove in self.li_moves)
            for binmove in self.li_moves:
                binmove.porc = binmove.weight() * 100.0 / tt

    def closeEvent(self, event):
        self.finalizar()

    def finalizar(self):
        self.pol_mkbin.close()
        self.db_entries.close()
        self.save_video()

    def mensajero(self, from_sq, to_sq, promocion=""):
        FasterCode.set_fen(self.position.fen())
        if FasterCode.make_move(from_sq + to_sq + promocion):
            fen = FasterCode.get_fen()
            self.position.read_fen(fen)
            self.set_position(self.position, True)

    def takeback(self):
        if len(self.history) > 1:
            self.history = self.history[:-1]
            fen = self.history[-1]
            self.position.read_fen(fen)
            self.set_position(self.position, False)

    def voyager(self):
        position = Voyager.voyager_position(self, self.position, wownerowner=self.owner)
        if position:
            self.set_position(position, True)
