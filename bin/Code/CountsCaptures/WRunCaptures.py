import time

from PySide2 import QtCore

import FasterCode

import Code
from Code.QT import Colocacion, Controles, Iconos, QTUtil, QTVarios, Tablero, QTUtil2

from Code.CountsCaptures import WRunCommon


class WRunCaptures(QTVarios.WDialogo):
    def __init__(self, owner, db_captures, capture):

        QTVarios.WDialogo.__init__(self, owner, _("Captures and threats in a game"), Iconos.Captures(), "runcaptures")

        self.configuracion = Code.configuracion
        self.capture = capture
        self.db_captures = db_captures

        conf_board = self.configuracion.config_board("RUNCAPTURES", 64)

        self.board = Tablero.TableroEstaticoMensaje(self, conf_board, None)
        self.board.crea()

        # Rotulo informacion
        self.lb_info_game = Controles.LB(
            self, self.capture.game.titulo("DATE", "EVENT", "WHITE", "BLACK", "RESULT")
        ).ponTipoLetra(puntos=self.configuracion.x_pgn_fontpoints)

        # Movimientos
        self.liwm_captures = []
        ly = Colocacion.G().margen(4)
        for i in range(16):
            f = i // 2
            c = i % 2
            wm = WRunCommon.WEdMove(self)
            self.liwm_captures.append(wm)
            ly.control(wm, f, c)

        self.gb_captures = Controles.GB(self, _("Captures"), ly).ponFuente(Controles.TipoLetra(puntos=10, peso=75))

        self.liwm_threats = []
        ly = Colocacion.G().margen(4)
        for i in range(16):
            f = i // 2
            c = i % 2
            wm = WRunCommon.WEdMove(self)
            self.liwm_threats.append(wm)
            ly.control(wm, f, c)

        self.gb_threats = Controles.GB(self, _("Threats"), ly).ponFuente(Controles.TipoLetra(puntos=10, peso=75))

        self.lb_result = Controles.LB(self).ponTipoLetra(puntos=10, peso=500).anchoFijo(254).altoFijo(32).ponWrap()
        self.lb_info = (
            Controles.LB(self).ponTipoLetra(puntos=14, peso=500).anchoFijo(254).ponColorFondoN("white", "#496075").alinCentrado()
        )

        # Botones
        li_acciones = (
            (_("Close"), Iconos.MainMenu(), self.terminar),
            None,
            (_("Begin"), Iconos.Empezar(), self.begin),
            (_("Check"), Iconos.Check(), self.check),
            (_("Continue"), Iconos.Pelicula_Seguir(), self.seguir),
        )
        self.tb = QTVarios.LCTB(self, li_acciones, style=QtCore.Qt.ToolButtonTextBesideIcon, tamIcon=32)
        self.show_tb(self.terminar, self.begin)

        ly_right = (
            Colocacion.V()
            .control(self.tb)
            .controlc(self.lb_info)
            .relleno()
            .control(self.gb_captures)
            .relleno()
            .control(self.gb_threats)
            .control(self.lb_result)
            .relleno()
        )

        ly_center = Colocacion.H().control(self.board).otro(ly_right)

        ly = Colocacion.V().otro(ly_center).control(self.lb_info_game).margen(3)

        self.setLayout(ly)

        self.restore_video()
        self.adjustSize()

        # Tiempo
        self.time_base = time.time()

        self.gb_captures.setDisabled(True)
        self.gb_threats.setDisabled(True)

        self.liwm_captures[0].activa()

        self.ultimaCelda = None

        self.pon_info_posic()
        self.set_position()

    def set_position(self):
        self.move_base = self.capture.game.move(self.capture.current_posmove)
        self.move_obj = self.capture.game.move(self.capture.current_posmove + self.capture.current_depth)
        self.board.ponPosicion(self.move_base.position_before)

    def pon_info_posic(self):
        self.lb_info.ponTexto(
            "%d+%d / %d"
            % (self.capture.current_posmove + 1, self.capture.current_depth, len(self.capture.game), )
        )

    def pulsada_celda(self, celda):
        if self.ultimaCelda:
            self.ultimaCelda.ponTexto(celda)

            ucld = self.ultimaCelda
            for liwm in (self.liwm_captures, self.liwm_threats):
                for num, wm in enumerate(liwm):
                    if wm.origen == ucld:
                        wm.activaDestino()
                        self.ultimaCelda = wm.destino
                        return
                    elif wm.destino == ucld:
                        if num < (len(liwm) - 1):
                            x = num + 1
                        else:
                            x = 0
                        wm = liwm[x]
                        wm.activa()
                        self.ultimaCelda = wm.origen
                        return

    def ponUltimaCelda(self, wmcelda):
        self.ultimaCelda = wmcelda

    def closeEvent(self, event):
        self.save_video()
        event.accept()

    def terminar(self):
        self.save_video()
        self.reject()

    def show_tb(self, *lista):
        for opc in self.tb.dicTB:
            self.tb.setAccionVisible(opc, opc in lista)
        QTUtil.refresh_gui()

    def begin(self):
        self.seguir()

    def seguir(self):
        self.set_position()
        self.lb_result.ponTexto("")
        for wm in self.liwm_captures:
            wm.limpia()
        for wm in self.liwm_threats:
            wm.limpia()

        self.show_tb()

        # Mostramos los movimientos según depth
        depth = self.capture.current_depth
        if depth:
            for x in range(depth):
                move = self.capture.game.move(self.capture.current_posmove + x)
                txt = move.pgnBaseSP()
                self.board.pon_texto(txt, 0.9)
                QTUtil.refresh_gui()
                dif = depth - x
                factor = 1.0 - dif * 0.1
                if factor < 0.7:
                    factor = 0.7

                time.sleep(2.6*factor*factor)
                self.board.pon_texto("", 1)
                QTUtil.refresh_gui()

        # Ponemos el toolbar
        self.show_tb(self.check, self.terminar)

        # Activamos capturas
        self.gb_captures.setEnabled(True)
        self.gb_threats.setEnabled(True)

        # Marcamos el tiempo
        self.time_base = time.time()

        self.liwm_captures[0].activa()

    def check(self):
        tiempo = time.time() - self.time_base

        position_obj = self.move_obj.position_before

        def test(liwm, si_mb):
            st_busca = {mv.xfrom() + mv.xto() for mv in FasterCode.get_captures(position_obj.fen(), si_mb)}
            st_sel = set()
            ok = True
            for wm in liwm:
                wm.deshabilita()
                mv = wm.movimiento()
                if mv:
                    if mv in st_sel:
                        wm.repetida()
                    elif mv in st_busca:
                        wm.correcta()
                        st_sel.add(mv)
                    else:
                        wm.error()
                        ok = False
            if ok:
                ok = (len(st_busca) == len(st_sel)) or st_sel == 16
            return ok

        ok_captures = test(self.liwm_captures, True)
        ok_threats = test(self.liwm_threats, False)

        ok = ok_captures and ok_threats
        xtry = self.capture.current_posmove, self.capture.current_depth, ok, tiempo
        self.capture.tries.append(xtry)

        if ok:
            self.capture.current_depth += 1
            if (self.capture.current_posmove + self.capture.current_depth) >= len(self.capture.game):
                QTUtil2.message(self, _("Training finished"))
                self.capture.current_posmove = len(self.capture.game)-1
                self.db_captures.change_count_capture(self.capture)
                self.terminar()
                return
            self.lb_result.ponTexto("%s (%d)" % (_("Right, go to the next level of depth"), self.capture.current_depth))
            self.lb_result.ponColorN("green")

        else:
            if self.capture.current_depth >= 1:
                self.capture.current_posmove += self.capture.current_depth - 1
                if self.capture.current_posmove < 0:
                    self.capture.current_posmove = 0
                self.capture.current_depth = 0
                self.lb_result.ponTexto(
                    "%s (%d)" % (_("Wrong, you advance to the last position solved"), self.capture.current_posmove + 1)
                )
                self.lb_result.ponColorN("red")
            else:
                self.lb_result.ponTexto(_("Wrong, you must repeat this position"))
                self.lb_result.ponColorN("red")
            self.board.ponPosicion(position_obj)

        self.db_captures.change_count_capture(self.capture)
        self.pon_info_posic()
        self.show_tb(self.terminar, self.seguir)
