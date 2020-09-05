import os

from PySide2 import QtCore, QtGui, QtWidgets

from Code.Config import Configuration
from Code.QT import Colocacion
from Code.QT import Controles
from Code.QT import Iconos
from Code.QT import QTUtil
from Code.QT import QTVarios
from Code import Usuarios
from Code import Util
import Code


def run_gui(procesador):
    app = QtWidgets.QApplication([])

    # Usuarios
    list_users = Usuarios.Usuarios().list_users
    if list_users:
        user = pide_usuario(list_users)
        if user is None:
            return
        if user == list_users[0]:
            user = None
    else:
        user = None

    active_folder = Configuration.active_folder()
    askfor_language = not os.path.isdir(active_folder) or not os.listdir(active_folder)

    procesador.start_with_user(user)
    configuration = procesador.configuration
    if user:
        if not configuration.x_player:
            configuration.x_player = user.name
            configuration.graba()
        elif configuration.x_player != user.name:
            for usu in list_users:
                if usu.number == user.number:
                    usu.name = configuration.x_player
                    Usuarios.Usuarios().save_list(list_users)

    # Comprobamos el lenguaje
    if askfor_language and not configuration.translator:
        if user:
            conf_main = Configuration.Configuration("")
            ori = conf_main.file_external_engines()
            conf_main.lee()
            conf_main.limpia(user.name)
            conf_main.set_folders()
            conf_main.graba()
            procesador.configuration = conf_main

            Util.file_copy(ori, conf_main.file_external_engines())

        else:
            li = configuration.list_translations()
            menu = QTVarios.LCMenuRondo(None)
            for k, name, porc, author in li:
                if porc != 100:
                    name += " (%d%%)" % porc
                menu.opcion(k, name)
            resp = menu.lanza()
            if resp:
                configuration.translator = resp
                configuration.graba()
                configuration.releeTRA()

    # Estilo
    # https://github.com/gmarull/qtmodern/blob/master/qtmodern/styles.py
    # https://stackoverflow.com/questions/15035767/is-the-qt-5-dark-fusion-theme-available-for-windows
    # darkPalette.setColor(QPalette.Window, QColor(53, 53, 53))
    # darkPalette.setColor(QPalette.WindowText, QColor(180, 180, 180))
    # darkPalette.setColor(QPalette.Base, QColor(42, 42, 42))
    # darkPalette.setColor(QPalette.Text, QColor(180, 180, 180))
    # darkPalette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    # darkPalette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
    # darkPalette.setColor(QPalette.ToolTipText, QColor(180, 180, 180))
    # darkPalette.setColor(QPalette.Button, QColor(53, 53, 53))
    # darkPalette.setColor(QPalette.ButtonText, QColor(180, 180, 180))
    # darkPalette.setColor(QPalette.BrightText, QColor(180, 180, 180))
    # darkPalette.setColor(QPalette.Link, QColor(56, 252, 196))
    #
    # darkPalette.setColor(QPalette.Light, QColor(180, 180, 180))
    # darkPalette.setColor(QPalette.Midlight, QColor(90, 90, 90))
    # darkPalette.setColor(QPalette.Dark, QColor(35, 35, 35))
    # darkPalette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    # darkPalette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    # darkPalette.setColor(QPalette.HighlightedText, QColor(180, 180, 180))
    #
    # # disabled
    # darkPalette.setColor(QPalette.Disabled, QPalette.WindowText,
    #                      QColor(127, 127, 127))
    # darkPalette.setColor(QPalette.Disabled, QPalette.Text,
    #                      QColor(127, 127, 127))
    # darkPalette.setColor(QPalette.Disabled, QPalette.ButtonText,
    #                      QColor(127, 127, 127))
    # darkPalette.setColor(QPalette.Disabled, QPalette.Highlight,
    #                      QColor(80, 80, 80))
    # darkPalette.setColor(QPalette.Disabled, QPalette.HighlightedText,
    #                      QColor(127, 127, 127))
    # app.setStyle(QtWidgets.QStyleFactory.create(configuration.x_style))

    if configuration.palette:
        qpalette = QtGui.QPalette(QtGui.QPalette.Dark)
        palette = configuration.palette

        for key, tp in (
            (QtGui.QPalette.Window, "Window"),
            (QtGui.QPalette.WindowText, "WindowText"),
            (QtGui.QPalette.Base, "Base"),
            (QtGui.QPalette.Text, "Text"),
            (QtGui.QPalette.AlternateBase, "AlternateBase"),
            (QtGui.QPalette.ToolTipBase, "ToolTipBase"),
            (QtGui.QPalette.ToolTipText, "ToolTipText"),
            (QtGui.QPalette.Button, "Button"),
            (QtGui.QPalette.ButtonText, "ButtonText"),
            (QtGui.QPalette.BrightText, "BrightText"),
            (QtGui.QPalette.Link, "Link"),
        ):
            qpalette.setColor(key, QtGui.QColor(palette[tp]))
    else:
        qpalette = QtWidgets.QApplication.style().standardPalette()

    app.setPalette(qpalette)

    app.setEffectEnabled(QtCore.Qt.UI_AnimateMenu)

    QtGui.QFontDatabase.addApplicationFont(Code.path_resource("IntFiles", "ChessAlpha2.ttf"))

    if configuration.x_font_family:
        font = Controles.TipoLetra(configuration.x_font_family)
        app.setFont(font)

    Code.gc = QTUtil.GarbageCollector()

    procesador.iniciar_gui()

    resp = app.exec_()

    return resp


class WPassword(QtWidgets.QDialog):
    def __init__(self, liUsuarios):
        QtWidgets.QDialog.__init__(self, None)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)

        self.setWindowTitle(Code.lucas_chess)
        self.setWindowIcon(Iconos.Aplicacion64())

        self.liUsuarios = liUsuarios

        li_options = [(usuario.name, nusuario) for nusuario, usuario in enumerate(liUsuarios)]
        lbU = Controles.LB(self, _("User") + ":")
        self.cbU = Controles.CB(self, li_options, liUsuarios[0])

        lbP = Controles.LB(self, _("Password") + ":")
        self.edP = Controles.ED(self).password()

        btaceptar = Controles.PB(self, _("Accept"), rutina=self.accept, plano=False)
        btcancelar = Controles.PB(self, _("Cancel"), rutina=self.reject, plano=False)

        ly = Colocacion.G()
        ly.controld(lbU, 0, 0).control(self.cbU, 0, 1)
        ly.controld(lbP, 1, 0).control(self.edP, 1, 1)

        lybt = Colocacion.H().relleno().control(btaceptar).espacio(10).control(btcancelar)

        layout = Colocacion.V().otro(ly).espacio(10).otro(lybt).margen(10)

        self.setLayout(layout)
        self.edP.setFocus()

    def resultado(self):
        nusuario = self.cbU.valor()
        usuario = self.liUsuarios[nusuario]
        return usuario if self.edP.texto().strip() == usuario.password else None


def pide_usuario(liUsuarios):
    # Miramos si alguno tiene key, si es asi, lanzamos ventana
    siPass = False
    for usuario in liUsuarios:
        if usuario.password:
            siPass = True
    if siPass:
        intentos = 3
        while True:
            w = WPassword(liUsuarios)
            if w.exec_():
                usuario = w.resultado()
                if usuario:
                    break
            else:
                return None
            intentos -= 1
            if intentos == 0:
                return None
    else:
        if len(liUsuarios) == 1:
            usuario = liUsuarios[0]
        else:
            menu = Controles.Menu(None)  # No puede ser LCmenu, ya que todavia no existe la configuration
            menu.separador()

            for usuario in liUsuarios:
                menu.opcion(usuario, usuario.name, Iconos.PuntoNaranja())
                menu.separador()

            usuario = menu.lanza()
            if usuario is None:
                return None

    return usuario
