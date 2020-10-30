from Code.Base import Game, Position
from Code import Manager
from Code.QT import Controles
from Code.QT import Iconos
from Code.PlayAgainstEngine import PlayAgainstEngine
from Code.QT import WindowSolo
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code import TrListas
from Code.QT import Voyager
from Code.Base.Constantes import *


class ManagerPartida(Manager.Manager):
    def inicio(self, game, si_completa, si_solo_consultar):
        self.game_type = GT_ALONE

        self.game = game
        self.reinicio = self.game.save()
        self.si_completa = si_completa

        self.human_is_playing = True
        self.is_human_side_white = True

        self.changed = False

        self.state = ST_PLAYING

        if si_solo_consultar:
            li = [TB_CLOSE, TB_PGN_LABELS, TB_TAKEBACK, TB_REINIT, TB_CONFIG, TB_UTILITIES]
        else:
            li = [TB_SAVE, TB_CANCEL, TB_PGN_LABELS, TB_TAKEBACK, TB_REINIT, TB_CONFIG, TB_UTILITIES]
        self.main_window.pon_toolbar(li)

        self.main_window.activaJuego(True, False, siAyudas=False)
        self.quitaAyudas(True, False)
        self.main_window.set_label1(None)
        self.main_window.set_label2(None)
        self.set_dispatcher(self.player_has_moved)
        self.set_position(self.game.first_position)
        self.show_side_indicator(True)
        self.ponPiezasAbajo(game.iswhite())
        self.pgnRefresh(True)
        self.ponCapInfoPorDefecto()
        self.ponteAlPrincipio()

        self.check_boards_setposition()

        self.ponInformacion()

        self.refresh()

        self.siguiente_jugada()

    def ponInformacion(self):
        white = black = result = None
        for key, valor in self.game.li_tags:
            key = key.upper()
            if key == "WHITE":
                white = valor
            elif key == "BLACK":
                black = valor
            elif key == "RESULT":
                result = valor
        self.set_label1(
            "%s : <b>%s</b><br>%s : <b>%s</b>" % (_("White"), white, _("Black"), black) if white and black else ""
        )
        self.set_label2("%s : <b>%s</b>" % (_("Result"), result) if result else "")

    def reiniciar(self):
        if self.changed and not QTUtil2.pregunta(self.main_window, _("You will loose all changes, are you sure?")):
            return
        p = Game.Game()
        p.restore(self.reinicio)
        self.inicio(p, self.si_completa)

    def run_action(self, key):
        if key == TB_REINIT:
            self.reiniciar()

        elif key == TB_TAKEBACK:
            self.atras()

        elif key == TB_SAVE:
            self.main_window.accept()

        elif key == TB_CONFIG:
            self.configurarGS()

        elif key == TB_UTILITIES:
            liMasOpciones = (
                ("libros", _("Consult a book"), Iconos.Libros()),
                (None, None, None),
                ("play", _("Play current position"), Iconos.MoverJugar()),
            )

            resp = self.utilidades(liMasOpciones)
            if resp == "libros":
                liMovs = self.librosConsulta(True)
                if liMovs:
                    for x in range(len(liMovs) - 1, -1, -1):
                        from_sq, to_sq, promotion = liMovs[x]
                        self.player_has_moved(from_sq, to_sq, promotion)
            elif resp == "play":
                self.jugarPosicionActual()

        elif key == TB_PGN_LABELS:
            self.informacion()

        elif key in (TB_CANCEL, TB_END_GAME, TB_CLOSE):
            self.finPartida()

        else:
            Manager.Manager.rutinaAccionDef(self, key)

    def finPartida(self):
        # Comprobamos que no haya habido cambios from_sq el ultimo grabado
        if self.changed:
            resp = QTUtil2.preguntaCancelar(self.main_window, _("Do you want to cancel changes?"), _("Yes"), _("No"))
            if not resp:
                return False

        self.main_window.reject()
        return True

    def final_x(self):
        return self.finPartida()

    def siguiente_jugada(self):
        if self.state == ST_ENDGAME:
            return

        self.state = ST_PLAYING

        self.put_view()

        is_white = self.game.last_position.is_white
        self.is_human_side_white = is_white  # Compatibilidad, sino no funciona el cambio en pgn

        if self.game.is_finished():
            self.muestra_resultado()
            return

        self.set_side_indicator(is_white)
        self.refresh()

        self.human_is_playing = True
        self.activate_side(is_white)

    def muestra_resultado(self):
        self.state = ST_ENDGAME
        self.disable_all()

    def player_has_moved(self, from_sq, to_sq, promotion=""):
        self.human_is_playing = True
        move = self.checkmueve_humano(from_sq, to_sq, promotion)
        if not move:
            return False

        self.move_the_pieces(move.liMovs)

        self.add_move(move, True)

        self.siguiente_jugada()
        return True

    def add_move(self, move, siNuestra):
        self.changed = True

        self.game.add_move(move)

        self.put_arrow_sc(move.from_sq, move.to_sq)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.game.last_position.is_white)
        self.refresh()

        self.check_boards_setposition()

    def current_pgn(self):
        resp = ""
        st = set()
        for eti, valor in self.game.li_tags:
            etiU = eti.upper()
            if etiU in st:
                continue
            st.add(etiU)
            resp += '[%s "%s"]\n' % (eti, valor)
            if etiU == "RESULT":
                result = valor

        if not ("RESULT" in st):
            if self.resultado == RS_UNKNOWN:
                result = "*"

            elif self.resultado == RS_DRAW:
                result = "1/2-1/2"

            else:
                result = "1-0" if self.resultadoSiBlancas else "0-1"

            resp += '[Result "%s"]\n' % result

        if self.fen:
            resp += '[FEN "%s"]\n' % self.fen

        ap = self.game.opening
        if ap:
            if not ("ECO" in st):
                resp += '[ECO "%s"]\n' % ap.eco
            if not ("OPENING" in st):
                resp += '[Opening "%s"]\n' % ap.trNombre

        resp += "\n" + self.game.pgnBase() + " " + result

        return resp

    def editEtiquetasPGN(self):
        resp = WindowSolo.editEtiquetasPGN(self.procesador, self.game.li_tags)
        if resp:
            self.game.li_tags = resp
            self.changed = True
            self.ponInformacion()

    def informacion(self):
        menu = QTVarios.LCMenu(self.main_window)
        f = Controles.TipoLetra(puntos=10, peso=75)
        menu.ponFuente(f)

        siOpening = False
        for key, valor in self.game.li_tags:
            trad = TrListas.pgnLabel(key)
            if trad != key:
                key = trad
            menu.opcion(key, "%s : %s" % (key, valor), Iconos.PuntoAzul())
            if key.upper() == "OPENING":
                siOpening = True

        if not siOpening:
            opening = self.game.opening
            if opening:
                menu.separador()
                nom = opening.trNombre
                ape = _("Opening")
                label = nom if ape.upper() in nom.upper() else ("%s : %s" % (ape, nom))
                menu.opcion("opening", label, Iconos.PuntoNaranja())

        menu.separador()
        menu.opcion("pgn", _("Edit PGN labels"), Iconos.PGN())

        resp = menu.lanza()
        if resp:
            self.editEtiquetasPGN()

    def configurarGS(self):
        sep = (None, None, None)

        liMasOpciones = [
            ("rotacion", _("Auto-rotate board"), Iconos.JS_Rotacion()),
            sep,
            ("leerpgn", _("Read PGN"), Iconos.PGN_Importar()),
            sep,
            ("pastepgn", _("Paste PGN"), Iconos.Pegar16()),
            sep,
        ]
        if not self.si_completa:
            liMasOpciones.extend(
                [
                    ("position", _("Edit start position"), Iconos.Datos()),
                    sep,
                    ("pasteposicion", _("Paste FEN position"), Iconos.Pegar16()),
                    sep,
                    ("voyager", _("Voyager 2"), Iconos.Voyager()),
                ]
            )

        resp = self.configurar(liMasOpciones, siCambioTutor=True, siSonidos=True)

        if resp == "rotacion":
            self.auto_rotate = not self.auto_rotate
            is_white = self.game.last_position.is_white
            if self.auto_rotate:
                if is_white != self.board.is_white_bottom:
                    self.board.rotaBoard()

        elif resp == "position":
            ini_position = self.game.first_position
            new_position = Voyager.voyager_position(self.main_window, ini_position)
            if new_position and new_position != ini_position:
                self.game.set_position(new_position)
                self.inicio(self.game, self.si_completa)

        elif resp == "pasteposicion":
            texto = QTUtil.traePortapapeles()
            if texto:
                cp = Position.Position()
                try:
                    cp.read_fen(str(texto))
                    self.fen = cp.fen()
                    self.posicOpening = None
                    self.reiniciar()
                except:
                    pass

        elif resp == "leerpgn":
            game = self.procesador.select_1_pgn(self.main_window)
            if game is not None:
                if self.si_completa and not game.siFenInicial():
                    return
                p = Game.Game()
                p.leeOtra(game)
                p.assign_opening()
                self.reinicio = p.save()
                self.reiniciar()

        elif resp == "pastepgn":
            texto = QTUtil.traePortapapeles()
            if texto:
                ok, game = Game.pgn_game(texto)
                if not ok:
                    QTUtil2.message_error(
                        self.main_window, _("The text from the clipboard does not contain a chess game in PGN format")
                    )
                    return
                if self.si_completa and not game.siFenInicial():
                    return
                self.reinicio = game.save()
                self.reiniciar()

        elif resp == "voyager":
            ptxt = Voyager.voyagerPartida(self.main_window, self.game)
            if ptxt:
                dic = self.creaDic()
                dic["GAME"] = ptxt.save()
                dic["FEN"] = None if ptxt.siFenInicial() else ptxt.first_position.fen()
                dic["WHITEBOTTOM"] = self.board.is_white_bottom
                self.reiniciar(dic)

    def control_teclado(self, nkey):
        if nkey == ord("V"):  # V
            self.paste(QTUtil.traePortapapeles())

    def listHelpTeclado(self):
        return [("V", _("Paste position"))]

    def juegaRival(self):
        if not self.is_finished():
            self.pensando(True)
            rm = self.xrival.juega(nAjustado=self.xrival.nAjustarFuerza)
            self.pensando(False)
            if rm.from_sq:
                self.player_has_moved(rm.from_sq, rm.to_sq, rm.promotion)

    def cambioRival(self):
        if self.dicRival:
            dicBase = self.dicRival
        else:
            dicBase = self.configuration.leeVariables("ENG_MANAGERSOLO")

        dic = self.dicRival = PlayAgainstEngine.cambioRival(
            self.main_window, self.configuration, dicBase, siManagerSolo=True
        )

        if dic:
            for k, v in dic.items():
                self.reinicio[k] = v

            dr = dic["RIVAL"]
            rival = dr["CM"]
            r_t = dr["TIME"] * 100  # Se guarda en decimas -> milesimas
            r_p = dr["PROFUNDIDAD"]
            if r_t <= 0:
                r_t = None
            if r_p <= 0:
                r_p = None
            if r_t is None and r_p is None and not dic["SITIEMPO"]:
                r_t = 1000

            nAjustarFuerza = dic["AJUSTAR"]
            self.xrival = self.procesador.creaManagerMotor(rival, r_t, r_p, nAjustarFuerza != ADJUST_BETTER)
            self.xrival.nAjustarFuerza = nAjustarFuerza

            dic["ROTULO1"] = _("Opponent") + ": <b>" + self.xrival.name
            self.set_label1(dic["ROTULO1"])
            self.play_against_engine = True
            self.configuration.escVariables("ENG_MANAGERSOLO", dic)

    def tituloVentana(self):
        white = ""
        black = ""
        event = ""
        date = ""
        result = ""
        for key, valor in self.game.li_tags:
            if key.upper() == "WHITE":
                white = valor
            elif key.upper() == "BLACK":
                black = valor
            elif key.upper() == "EVENT":
                event = valor
            elif key.upper() == "DATE":
                date = valor
            elif key.upper() == "RESULT":
                result = valor
        return "%s-%s (%s, %s,%s)" % (white, black, event, date, result)

    def atras(self):
        if len(self.game):
            self.game.anulaSoloUltimoMovimiento()
            self.game.assign_opening()
            self.goto_end()
            self.state = ST_PLAYING
            self.refresh()
            self.siguiente_jugada()
