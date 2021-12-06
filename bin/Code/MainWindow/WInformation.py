from PySide2 import QtWidgets, QtCore

import Code
from Code import Variations
from Code.Base import Game
from Code.QT import Colocacion, Controles, Iconos, QTVarios, ShowPGN, QTUtil2, FormLayout
from Code.Themes import WThemes, Themes
from Code.Nags import WNags, Nags


class Information(QtWidgets.QWidget):
    def __init__(self, w_parent):
        QtWidgets.QWidget.__init__(self, w_parent)

        self.w_parent = w_parent

        self.move = None
        self.game = None

        configuration = Code.configuration

        puntos = configuration.x_pgn_fontpoints

        font = Controles.TipoLetra(puntos=puntos)
        font_bold = Controles.TipoLetra(puntos=puntos, peso=75)

        self.themes = Themes.Themes()
        self.nags = Nags.Nags()

        # Opening
        self.lb_opening = Controles.LB(self, "").ponFuente(font).align_center().set_foreground_backgound("#eeeeee", "#474d59").set_wrap()
        self.lb_opening.hide()

        # Valoracion
        self.w_rating = QtWidgets.QWidget(self)
        ly_rating = Colocacion.V().margen(0)

        li_acciones = [(_("Rating"), Iconos.Mas(), self.edit_rating), None, (_("Theme"), Iconos.MasR(), self.edit_theme)]
        tb = QTVarios.LCTB(self, li_acciones, icon_size=16, style=QtCore.Qt.ToolButtonTextBesideIcon)
        ly_rating.control(tb)

        self.lb_cpws_lost = Controles.LB(self).ponFuente(font_bold).set_wrap()
        self.lb_cpws_lost.hide()
        self.lb_cpws_lost.setStyleSheet("*{ border: 1px solid lightgray; padding:2px; background: #f7f2f0}")
        ly_rating.control(self.lb_cpws_lost)
        self.lb_rating = Controles.LB(self).ponFuente(font_bold).set_wrap()
        self.lb_rating.hide()
        self.lb_rating.setStyleSheet("*{ border: 1px solid lightgray; padding:2px; background: #f7f2f0}")
        self.lb_rating.mousePressEvent = self.edit_rating
        ly_rating.control(self.lb_rating)

        self.lb_theme = Controles.LB(self).ponFuente(font_bold).set_wrap()
        self.lb_theme.hide()
        self.lb_theme.setStyleSheet("*{ border: 1px solid lightgray; padding:2px; background: #fdfae8}")
        self.lb_theme.mousePressEvent = self.edit_theme
        ly_rating.control(self.lb_theme)
        self.w_rating.setLayout(ly_rating)

        # Comentarios
        self.comment = Controles.EM(self, siHTML=False).capturaCambios(self.comment_changed).ponFuente(font).anchoMinimo(200)
        ly = Colocacion.H().control(self.comment).margen(3)
        self.gb_comments = Controles.GB(self, _("Comments"), ly).ponFuente(font_bold)

        # Variations
        self.variantes = WVariations(self)

        self.splitter = splitter = QtWidgets.QSplitter(self)
        splitter.setOrientation(QtCore.Qt.Vertical)
        splitter.addWidget(self.gb_comments)
        splitter.addWidget(self.variantes)
        splitter.setSizes([1, 1])
        self.sp_sizes = None

        layout = Colocacion.V()
        layout.control(self.lb_opening)
        layout.control(self.w_rating)
        layout.control(splitter)
        layout.margen(1)

        self.setLayout(layout)

        self.setMinimumWidth(220)

    def edit_theme(self, event=None):
        if event:
            event.ignore()
        w = WThemes.WThemes(self, self.themes, self.move)
        if w.exec_():
            self.show_themes()

    def show_themes(self):
        if self.move:
            str_themes = self.themes.str_themes(self.move)
        else:
            str_themes = ""
        self.lb_theme.set_text(str_themes)
        self.lb_theme.setVisible(len(str_themes) > 0)

    def show_cpws_lost(self):
        visible = False
        if self.move:
            cpws_lost = self.move.get_points_lost()
            if cpws_lost is not None and cpws_lost > 0:
                analysis_depth = self.move.analysis[0].li_rm[0].depth
                str_cpws_lost = "%.02f %s (%s %s)" % (cpws_lost / 100.0, _("pawns lost"), _("Depth"), analysis_depth)
                self.lb_cpws_lost.set_text(str_cpws_lost)
                visible = True
        self.lb_cpws_lost.setVisible(visible)

    def edit_rating(self, event=None):
        if event:
            event.ignore()
        w = WNags.WNags(self, self.nags, self.move)
        if w.exec_():
            self.show_rating()

    def show_rating(self):
        if self.move:
            str_nags = self.nags.str_move(self.move)
        else:
            str_nags = ""
        self.lb_rating.set_text(str_nags)
        self.lb_rating.setVisible(len(str_nags) > 0)

    def set_move(self, game, move, opening):
        sps = self.splitter.sizes()
        if sps[1] > 0:
            self.sp_sizes = sps

        self.game = game
        self.move = move

        if not opening:
            self.lb_opening.hide()

        is_move = self.move is not None
        self.w_rating.setVisible(is_move)
        self.variantes.setVisible(is_move)

        self.show_themes()
        self.show_rating()
        self.show_cpws_lost()
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
            num_moves, nj, row, is_white = self.w_parent.manager.jugadaActual()

        else:
            self.gb_comments.set_text("%s - %s" % (_("Game"), _("Comments")))
            if game is not None:
                self.comment.set_text(game.first_comment)

                if opening:
                    self.lb_opening.set_text(opening)
                    self.lb_opening.set_foreground_backgound("#eeeeee", "#474d59")
                    self.lb_opening.show()

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
        num_var_move = 0
        variation = None
        for num in li_variation_move[1:]:
            if is_num_variation:
                variation = var_move.variations.get(num)
            else:
                var_move = variation.move(num)
                num_var_move = num
            is_num_variation = not is_num_variation
        board = self.get_board()
        board.set_base_position(var_move.position, variation_history=selected_link)
        board.put_arrow_sc(var_move.from_sq, var_move.to_sq)
        self.mostrar()

        if variation is not None:
            manager = self.owner.w_parent.manager
            manager.kibitzers_manager.put_game(variation.copia(num_var_move))

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
        li_variation_move[-1] = str(int(li_variation_move[-1]) - 1)
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
            game = Game.Game(first_position=self.move.position_before)

        change_game = Variations.edit_variation(
            Code.procesador, game, with_engine_active=with_engine_active, is_white_bottom=self.get_board().is_white_bottom
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
