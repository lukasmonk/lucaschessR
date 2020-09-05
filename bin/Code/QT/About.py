from PySide2 import QtCore, QtWidgets
import Code

from Code.QT import Colocacion
from Code.QT import Controles
from Code.QT import Iconos
from Code.QT import AboutBase
from Code.QT import QTUtil


class WAbout(QtWidgets.QDialog):
    def __init__(self, procesador):
        super(WAbout, self).__init__(procesador.main_window)

        self.setWindowTitle(_("About"))
        self.setWindowIcon(Iconos.Aplicacion64())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)
        self.setMaximumWidth(QTUtil.anchoEscritorio())

        f = Controles.TipoLetra(puntos=10)  # 0, peso=75 )

        head = (
            '<span style="font-size:30pt; font-weight="700"; font-family:arial; color:#2D2B2B">%s</span><br>'
            % Code.lucas_chess
        )
        head += '<span style="font-size:15pt;">%s</span><br>' % _X(_("version %1"), procesador.version)
        head += '<span style="font-size:10pt;color:2D2B2B">%s: %s</span>' % (
            _("Author"),
            '<a href="mailto:lukasmonk@gmail.com">Lucas Monge</a>',
        )
        head += ' - <a style="font-size:10pt; color:2D2B2B" href="%s">%s</a>' % (procesador.web, procesador.web)
        head += ' - <a style="font-size:10pt; color:2D2B2B" href="%s">Blog : Fresh news</a>' % (procesador.blog,)
        head += ' - <a style="font-size:10pt; color:2D2B2B" href="%s">Sources: github</a><br>' % (
            procesador.github,
        )
        head += (
            '%s <a style="font-size:10pt; color:2D2B2B" href="http://www.gnu.org/copyleft/gpl.html"> GPL</a>'
            % _("License")
        )

        lb_ico = Controles.LB(self).ponImagen(Iconos.pmAplicacion64())
        lb_titulo = Controles.LB(self, head)

        # Tabs
        tab = Controles.Tab()
        tab.ponFuente(f)

        ib = AboutBase.ThanksTo()

        sub_tab = None
        for n, (k, titulo) in enumerate(ib.dic.items()):
            txt = ib.texto(k)
            lb = Controles.LB(self, txt)
            lb.set_background("#F6F3EE")
            lb.ponFuente(f)
            if "-" in k:
                base, num = k.split("-")
                if num == "1":
                    sub_tab = Controles.Tab()
                    sub_tab.ponFuente(f)
                    sub_tab.set_position("S")
                    tab.addTab(sub_tab, _("Engines"))
                lm = ib.list_engines(num)
                titulo = lm[0][0].split(" ")[1] + " - " + lm[-1][0].split(" ")[1]
                sub_tab.addTab(lb, titulo)
            else:
                tab.addTab(lb, titulo)

        ly_v1 = Colocacion.H().control(lb_ico).espacio(15).control(lb_titulo).relleno()
        layout = Colocacion.V().otro(ly_v1).espacio(10).control(tab).margen(10)

        self.setLayout(layout)


class WInfo(QtWidgets.QDialog):
    def __init__(self, wparent, titulo, head, txt, min_tam, pm_icon):
        super(WInfo, self).__init__(wparent)

        self.setWindowTitle(titulo)
        self.setWindowIcon(Iconos.Aplicacion64())
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)

        f = Controles.TipoLetra(puntos=20)

        lb_ico = Controles.LB(self).ponImagen(pm_icon)
        lb_titulo = Controles.LB(self, head).align_center().ponFuente(f)
        lb_texto = Controles.LB(self, txt)
        lb_texto.setMinimumWidth(min_tam - 84)
        lb_texto.setWordWrap(True)
        lb_texto.setTextFormat(QtCore.Qt.RichText)
        bt_seguir = Controles.PB(self, _("Continue"), self.seguir).ponPlano(False)

        ly_v1 = Colocacion.V().control(lb_ico).relleno()
        ly_v2 = Colocacion.V().control(lb_titulo).control(lb_texto).espacio(10).control(bt_seguir)
        ly_h = Colocacion.H().otro(ly_v1).otro(ly_v2).margen(10)

        self.setLayout(ly_h)

    def seguir(self):
        self.close()


def info(parent, titulo, head, txt, min_tam, pm_icon):
    w = WInfo(parent, titulo, head, txt, min_tam, pm_icon)
    w.exec_()
