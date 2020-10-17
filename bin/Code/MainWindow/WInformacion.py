import os

from PySide2 import QtWidgets, QtCore

from Code.Base import Game
from Code import Variations
from Code.QT import Colocacion, Controles, Iconos, QTVarios, ShowPGN, QTUtil2, FormLayout
from Code import TrListas
import Code


class WVariations(QtWidgets.QWidget):
    def __init__(self, owner):
        self.owner = owner
        configuration = Code.configuration
        self.with_figurines = configuration.x_pgn_withfigurines
        puntos = configuration.x_pgn_fontpoints

        QtWidgets.QWidget.__init__(self, self.owner)

        li_acciones = (
            None,
            (_("Append"), Iconos.Mas(), self.tb_mas_variation),
            None,
            ("%s+%s" % (_("Append"), _("Engine")), Iconos.MasR(), self.tb_mas_variation_r),
            None,
            (_("Edit in other board"), Iconos.EditVariation(), self.tb_edit_variation),
            None,
            (_("Remove"), Iconos.Borrar(), self.tb_remove_variation),
            None,
        )
        tb_variations = Controles.TBrutina(self, li_acciones, with_text=False, icon_size=16)

        self.em = ShowPGN.ShowPGN(self, puntos, self.with_figurines)
        self.em.set_link(self.link_variation_pressed)
        self.em.set_edit(self.link_variation_edit)

        f = Controles.TipoLetra(puntos=puntos, peso=750)

        lb_variations = Controles.LB(self.owner, _("Variations")).ponFuente(f)

        ly_head = Colocacion.H().control(lb_variations).relleno().control(tb_variations)

        layout = Colocacion.V().otro(ly_head).control(self.em).margen(0)
        self.setLayout(layout)

        self.move = None
        self.selected_link = None

    def li_variations(self):
        return self.move.variations.list_games() if self.move else []

    def link_variation_pressed(self, selected_link):
        li_variation_move = [int(cnum) for cnum in selected_link.split("|")]
        self.selected_link = selected_link
        is_num_variation = True
        var_move = self.move
        variation = None
        for num in li_variation_move[1:]:
            if is_num_variation:
                variation = var_move.variations.get(num)
            else:
                var_move = variation.move(num)
            is_num_variation = not is_num_variation
        board = self.get_board()
        board.set_base_position(var_move.position, variation_history=selected_link)
        board.put_arrow_sc(var_move.from_sq, var_move.to_sq)
        self.mostrar()

    def link_variation_edit(self, num_variation):
        self.edit(num_variation)

    def det_variation_move(self, li_variation_move):
        var_move = self.move
        variation = None
        is_num_variation = True
        for num in li_variation_move[1:]:
            num = int(num)
            if is_num_variation:
                variation = var_move.variations.get(num)
            else:
                var_move = variation.move(num)
            is_num_variation = not is_num_variation
        return variation, var_move

    def remove_line(self):
        if QTUtil2.pregunta(self, _("Are you sure you want to delete this line?")):
            li_variation_move = self.selected_link.split("|")
            num_line = int(li_variation_move[-2])

            li_variation_move = li_variation_move[:-2]
            selected_link = "|".join(li_variation_move)
            variation, var_move = self.det_variation_move(li_variation_move)

            var_move.variations.remove(num_line)
            self.link_variation_pressed(selected_link)

    def remove_move(self):
        li_variation_move = self.selected_link.split("|")
        li_variation_move[-1] = str(int(li_variation_move[-1])-1)
        variation, var_move = self.det_variation_move(li_variation_move)
        variation.shrink(int(li_variation_move[-1]))
        selected_link = "|".join(li_variation_move)
        self.link_variation_pressed(selected_link)

    def comment_edit(self):
        li_variation_move = self.selected_link.split("|")
        variation, var_move = self.det_variation_move(li_variation_move)
        previo = var_move.comment
        form = FormLayout.FormLayout(self, _("Comments"), Iconos.ComentarioEditar(), anchoMinimo=640)
        form.separador()

        config = FormLayout.Editbox(_("Comment"), alto=5)
        form.base(config, previo)

        resultado = form.run()

        if resultado:
            accion, resp = resultado
            comment = resp[0].strip()
            var_move.comment = comment
            self.link_variation_pressed(self.selected_link)

    def set_move(self, move):
        self.move = move
        self.em.show_variations(move, self.selected_link)

    def get_board(self):
        return self.owner.w_parent.manager.board

    def mostrar(self):
        self.em.show_variations(self.move, self.selected_link)

    def select(self):
        li_variations = self.li_variations()
        if len(li_variations) == 0:
            return None
        menu = QTVarios.LCMenuRondo(self)
        for num, variante in enumerate(li_variations):
            move = variante.move(0)
            menu.opcion(num, "%d. %s" % (num + 1, move.pgn_translated()))
        return menu.lanza()

    def edit(self, number, with_engine_active=False):
        game = None
        if number > -1:
            li_variations = self.li_variations()
            if li_variations:
                game = li_variations[number]
            else:
                number = -1

        if number == -1:
            game = Game.Game(ini_posicion=self.move.position_before)

        change_game = Variations.edit_variation(
            Code.procesador,
            game,
            with_engine_active=with_engine_active,
            is_white_bottom=self.get_board().is_white_bottom,
        )
        if change_game:
            self.move.variations.change(number, change_game)
            self.mostrar()

    def tb_mas_variation(self):
        self.edit(-1, False)

    def tb_mas_variation_r(self):
        self.edit(-1, True)

    def tb_edit_variation(self):
        num = self.select()
        if num is not None:
            self.edit(num)

    def tb_remove_variation(self):
        num = self.select()
        if num is not None:
            self.move.variations.remove(num)
            self.mostrar()


class InformacionPGN(QtWidgets.QWidget):
    def __init__(self, w_parent):
        QtWidgets.QWidget.__init__(self, w_parent)

        self.w_parent = w_parent

        self.move = None
        self.game = None

        configuration = Code.configuration

        puntos = configuration.x_pgn_fontpoints

        f = Controles.TipoLetra(puntos=puntos, peso=75)
        f9 = Controles.TipoLetra(puntos=puntos)
        ftxt = f9

        # Opening
        self.lb_opening = (
            Controles.LB(self, "").ponFuente(f).align_center().set_foreground_backgound("#eeeeee", "#474d59").set_wrap()
        )
        self.lb_opening.hide()

        # Valoracion
        li_options = [("-", None)]
        dic_nags = TrListas.dic_nags()

        nags_folder = Code.path_resource("IntFiles", "NAGs")

        ico_vacio = QTVarios.fsvg2ico("%s/$0.svg" % (nags_folder,), 16)

        for x in dic_nags:
            if x:
                fsvg = "%s/$%d.svg" % (nags_folder, x)
                if os.path.isfile(fsvg):
                    li_options.append(("$%d : %s" % (x, dic_nags[x]), x, QTVarios.fsvg2ico(fsvg, 16)))
                else:
                    li_options.append(("$%d : %s" % (x, dic_nags[x]), x, ico_vacio))
        self.max_nags = 10
        self.li_nags = []
        for x in range(self.max_nags):
            cb = (
                Controles.CB(self, li_options, "")
                .set_widthMinimo()
                .capture_changes(self.valoration_changed)
                .ponFuente(f9)
            )
            if x:
                cb.hide()
            self.li_nags.append(cb)

        bt_nags = Controles.PB(self, "", self.more_nags).ponIcono(Iconos.Mas()).anchoFijo(22)

        ly_h = Colocacion.H().control(self.li_nags[0]).control(bt_nags)
        ly = Colocacion.V().otro(ly_h)
        for x in range(1, self.max_nags):
            ly.control(self.li_nags[x])

        self.gbValoracion = Controles.GB(self, _("Rating"), ly).ponFuente(f)

        # Comentarios
        self.comment = (
            Controles.EM(self, siHTML=False).capturaCambios(self.comment_changed).ponFuente(ftxt).anchoMinimo(200)
        )
        ly = Colocacion.H().control(self.comment).margen(3)
        self.gb_comments = Controles.GB(self, _("Comments"), ly).ponFuente(f)

        # Variations
        self.variantes = WVariations(self)

        self.splitter = splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        splitter.addWidget(self.gb_comments)
        splitter.addWidget(self.variantes)

        layout = Colocacion.V()
        layout.control(self.lb_opening)
        layout.control(self.gbValoracion)
        layout.control(self.splitter)
        layout.margen(1)

        self.setLayout(layout)

        self.setMinimumWidth(220)

    def more_nags(self):
        for cb in self.li_nags:
            if not cb.isVisible():
                cb.ponValor("-")
                cb.show()
                return

    def set_move(self, game, move, opening):
        self.game = game
        self.move = move

        if not opening:
            self.lb_opening.hide()

        is_move = self.move is not None
        self.gbValoracion.setVisible(is_move)
        self.variantes.setVisible(is_move)

        if is_move:
            self.gb_comments.set_text(_("Comments"))
            if opening:
                self.lb_opening.set_text(opening)
                if move.in_the_opening:
                    self.lb_opening.set_foreground_backgound("#eeeeee", "#474d59")
                else:
                    self.lb_opening.set_foreground_backgound("#ffffff", "#aaaaaa")
                self.lb_opening.show()

            self.comment.set_text(move.comment)
            self.variantes.set_move(move)

            self.set_nags(move.li_nags)

        else:
            self.gb_comments.set_text("%s - %s" % (_("Game"), _("Comments")))
            if game is not None:
                self.comment.set_text(game.first_comment)
                if opening:
                    self.lb_opening.set_text(opening)
                    self.lb_opening.set_foreground_backgound("#eeeeee", "#474d59")
                    self.lb_opening.show()

    def set_nags(self, li):
        n = 0
        for nag in li:
            cb = self.li_nags[n]
            cb.ponValor(nag)
            cb.show()
            n += 1
        if n == 0:
            cb = self.li_nags[0]
            cb.ponValor("-")
            cb.show()
        else:
            for x in range(n, self.max_nags):
                cb = self.li_nags[x]
                cb.ponValor("-")
                cb.hide()

    def keyPressEvent(self, event):
        pass  # Para que ESC no cierre el programa

    def comment_changed(self):
        if self.move:
            self.move.comment = self.comment.texto()
        else:
            self.game.first_comment = self.comment.texto()

    def valoration_changed(self):
        if self.move:
            li = []
            for x in range(self.max_nags):
                v = self.li_nags[x].valor()
                if v:
                    li.append(v)
            self.move.li_nags = li
            self.set_nags(li)
