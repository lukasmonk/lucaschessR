"""
Rutinas basicas para la edicion en las listas de registros.
"""

import os

from PySide2 import QtCore, QtGui, QtWidgets, QtSvg

import Code
from Code.QT import Iconos


dicPM = {}
dicPZ = {}
dicNG = {}


def generaPM(piezas):
    dicPM["V"] = Iconos.pmComentario()
    dicPM["R"] = Iconos.pmOpening()
    dicPM["M"] = Iconos.pmComentarioMas()
    dicPM["S"] = Iconos.pmOpeningComentario()

    dicPM["O"] = Iconos.pmOpening()
    dicPM["C"] = Iconos.pmComment()
    dicPM["V"] = Iconos.pmVariation()
    dicPM["OC"] = Iconos.pmOpeningComment()
    dicPM["OV"] = Iconos.pmOpeningVariation()
    dicPM["VC"] = Iconos.pmVariationComment()
    dicPM["OVC"] = Iconos.pmOpeningVariationComment()

    for k in "KQRNBkqrnb":
        dicPZ[k] = piezas.render(k)

    nags_folder = Code.path_resource("IntFiles", "NAGs")
    for f in os.listdir(nags_folder):
        if f.endswith(".svg") and f.startswith("$") and len(f) > 5:
            nag = f[1:-4]
            if nag.isdigit():
                fsvg = nags_folder + "/" + f
                dicNG[nag] = QtSvg.QSvgRenderer(fsvg)


class ComboBox(QtWidgets.QItemDelegate):
    def __init__(self, liTextos):
        QtWidgets.QItemDelegate.__init__(self)
        self.li_textos = liTextos

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QComboBox(parent)
        editor.addItems(self.li_textos)
        editor.installEventFilter(self)
        return editor

    def setEditorData(self, cb, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        num = self.li_textos.index(value)
        cb.setCurrentIndex(num)

    def setModelData(self, cb, model, index):
        num = cb.currentIndex()
        model.setData(index, self.li_textos[num])

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class LineaTexto(QtWidgets.QItemDelegate):
    def __init__(self, parent=None, siPassword=False, siEntero=False, rx=None):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.siPassword = siPassword
        self.siEntero = siEntero
        self.rx = rx

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        if self.siPassword:
            editor.setEchoMode(QtWidgets.QLineEdit.Password)
        if self.siEntero:
            editor.setValidator(QtGui.QIntValidator(self))
            editor.setAlignment(QtCore.Qt.AlignRight)
        if self.rx:
            xrx = QtCore.QRegExp(self.rx)
            validator = QtGui.QRegExpValidator(xrx, self)
            editor.setValidator(validator)
        editor.installEventFilter(self)
        return editor

    def setEditorData(self, sle, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        sle.setText(value)

    def setModelData(self, sle, model, index):
        value = str(sle.text())
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class LineaTextoUTF8(QtWidgets.QItemDelegate):
    def __init__(self, parent=None, siPassword=False):
        QtWidgets.QItemDelegate.__init__(self, parent)
        self.siPassword = siPassword

    def createEditor(self, parent, option, index):
        editor = QtWidgets.QLineEdit(parent)
        if self.siPassword:
            editor.setEchoMode(QtWidgets.QLineEdit.Password)
        editor.installEventFilter(self)
        return editor

    def setEditorData(self, sle, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        sle.setText(value)

    def setModelData(self, sle, model, index):
        value = sle.text()
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class EtiquetaPGN(QtWidgets.QStyledItemDelegate):
    def __init__(self, is_white, siAlineacion=False, siFondo=False):
        self.is_white = is_white  # None = no hacer
        self.si_figurines_pgn = is_white is not None
        self.siAlineacion = siAlineacion
        self.siFondo = siFondo
        QtWidgets.QStyledItemDelegate.__init__(self, None)

    def setWhite(self, is_white):
        self.is_white = is_white

    def rehazPosicion(self):
        position = self.bloquePieza.position
        self.setPos(position.x, position.y)

    def paint(self, painter, option, index):
        data = index.model().data(index, QtCore.Qt.DisplayRole)
        if type(data) == tuple:
            pgn, color, info, indicadorInicial, li_nags = data
            if li_nags:
                li = []
                st = set()
                for x in li_nags:
                    x = str(x)
                    if x in st:
                        continue
                    st.add(x)
                    if x in dicNG:
                        li.append(dicNG[x])
                li_nags = li
        else:
            pgn, color, info, indicadorInicial, li_nags = data, None, None, None, None

        iniPZ = None
        finPZ = None
        salto_finPZ = 0
        if self.si_figurines_pgn and len(pgn) > 2:
            if pgn[0] in "QBKRN":
                iniPZ = pgn[0] if self.is_white else pgn[0].lower()
                pgn = pgn[1:]
            elif pgn[-1] in "QBRN":
                finPZ = pgn[-1] if self.is_white else pgn[-1].lower()
                pgn = pgn[:-1]
            elif pgn[-2] in "QBRN":
                finPZ = pgn[-2] if self.is_white else pgn[-2].lower()
                if info:
                    info = pgn[-1] + info
                else:
                    info = pgn[-1]
                pgn = pgn[:-2]
                salto_finPZ = -6

        if info and not finPZ:
            pgn += info
            info = None

        rect = option.rect
        wTotal = rect.width()
        hTotal = rect.height()
        xTotal = rect.x()
        yTotal = rect.y()

        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(
                rect, QtGui.QColor(Code.configuration.pgn_selbackground())
            )  # sino no se ve en CDE-Motif-Windows
        elif self.siFondo:
            fondo = index.model().getFondo(index)
            if fondo:
                painter.fillRect(rect, fondo)

        if indicadorInicial:
            painter.save()
            painter.translate(xTotal, yTotal)
            painter.drawPixmap(0, 0, dicPM[indicadorInicial])
            painter.restore()

        documentPGN = QtGui.QTextDocument()
        documentPGN.setDefaultFont(option.font)
        if color:
            pgn = '<font color="%s"><b>%s</b></font>' % (color, pgn)
        documentPGN.setHtml(pgn)
        wPGN = documentPGN.idealWidth()
        hPGN = documentPGN.size().height()
        hx = hPGN * 80 / 100
        wpz = int(hx * 0.8)

        if info:
            documentINFO = QtGui.QTextDocument()
            documentINFO.setDefaultFont(option.font)
            if color:
                info = '<font color="%s"><b>%s</b></font>' % (color, info)
            documentINFO.setHtml(info)
            wINFO = documentINFO.idealWidth()

        ancho = wPGN
        if iniPZ:
            ancho += wpz
        if finPZ:
            ancho += wpz + salto_finPZ
        if info:
            ancho += wINFO
        if li_nags:
            ancho += wpz * len(li_nags)

        x = xTotal + (wTotal - ancho) / 2
        if self.siAlineacion:
            alineacion = index.model().getAlineacion(index)
            if alineacion == "i":
                x = xTotal + 3
            elif alineacion == "d":
                x = xTotal + (wTotal - ancho - 3)

        x = xTotal + 20
        y = yTotal + (hTotal - hPGN * 0.9) / 2

        if iniPZ:
            painter.save()
            painter.translate(x, y)
            pm = dicPZ[iniPZ]
            pmRect = QtCore.QRectF(0, 0, hx, hx)
            pm.render(painter, pmRect)
            painter.restore()
            x += wpz

        painter.save()
        painter.translate(x, y)
        documentPGN.drawContents(painter)
        painter.restore()
        x += wPGN

        if finPZ:
            painter.save()
            painter.translate(x - 0.3 * wpz, y)
            pm = dicPZ[finPZ]
            pmRect = QtCore.QRectF(0, 0, hx, hx)
            pm.render(painter, pmRect)
            painter.restore()
            x += wpz + salto_finPZ

        if info:
            painter.save()
            painter.translate(x, y)
            documentINFO.drawContents(painter)
            painter.restore()
            x += wINFO

        if li_nags:
            for rndr in li_nags:
                painter.save()
                painter.translate(x - 0.2 * wpz, y)
                pmRect = QtCore.QRectF(0, 0, hx, hx)
                rndr.render(painter, pmRect)
                painter.restore()
                x += wpz


class PmIconosBMT(QtWidgets.QStyledItemDelegate):
    """
    Delegado para la muestra con html
    """

    def __init__(self, parent=None, dicIconos=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

        if dicIconos:
            self.dicIconos = dicIconos
        else:
            self.dicIconos = {
                "0": Iconos.pmPuntoBlanco(),
                "1": Iconos.pmPuntoNegro(),
                "2": Iconos.pmPuntoAmarillo(),
                "3": Iconos.pmPuntoNaranja(),
                "4": Iconos.pmPuntoVerde(),
                "5": Iconos.pmPuntoAzul(),
                "6": Iconos.pmPuntoMagenta(),
                "7": Iconos.pmPuntoRojo(),
                "8": Iconos.pmPuntoEstrella(),
            }

    def paint(self, painter, option, index):
        pos = str(index.model().data(index, QtCore.Qt.DisplayRole))
        if not (pos in self.dicIconos):
            return
        painter.save()
        painter.translate(option.rect.x(), option.rect.y())
        painter.drawPixmap(4, 1, self.dicIconos[pos])
        painter.restore()


class PmIconosColor(QtWidgets.QStyledItemDelegate):
    """ Usado en TurnOnLigths"""

    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

        self.dicpmIconos = {
            "0": Iconos.pmGris32(),
            "1": Iconos.pmAmarillo32(),
            "2": Iconos.pmNaranja32(),
            "3": Iconos.pmVerde32(),
            "4": Iconos.pmAzul32(),
            "5": Iconos.pmMagenta32(),
            "6": Iconos.pmRojo32(),
            "7": Iconos.pmLight32(),
        }

    def paint(self, painter, option, index):
        pos = str(index.model().data(index, QtCore.Qt.DisplayRole))
        if not (pos in self.dicpmIconos):
            return
        painter.save()
        painter.translate(option.rect.x(), option.rect.y())
        painter.drawPixmap(4, 4, self.dicpmIconos[pos])
        painter.restore()


class PmIconosWeather(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

        self.dicIconos = {
            "0": Iconos.pmInvierno(),
            "1": Iconos.pmLluvia(),
            "2": Iconos.pmSolNubesLluvia(),
            "3": Iconos.pmSolNubes(),
            "4": Iconos.pmSol(),
        }

    def paint(self, painter, option, index):
        pos = str(index.model().data(index, QtCore.Qt.DisplayRole))
        if not (pos in self.dicIconos):
            if pos.isdigit():
                pos = "4" if int(pos) > 4 else "0"
            else:
                return
        painter.save()
        painter.translate(option.rect.x(), option.rect.y())
        painter.drawPixmap(4, 4, self.dicIconos[pos])
        painter.restore()


class PmIconosCheck(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        QtWidgets.QStyledItemDelegate.__init__(self, parent)

        self.dicIconos = {True: Iconos.pmChecked(), False: Iconos.pmUnchecked()}

    def paint(self, painter, option, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole) is True

        rect = option.rect
        width = rect.width()
        height = rect.height()
        x = rect.x() + (width - 16) / 2
        y = rect.y() + (height - 16) / 2

        painter.save()
        painter.drawPixmap(x, y, self.dicIconos[value])
        painter.restore()

    def createEditor(self, parent, option, index):
        return None


# class HTMLDelegate(QtWidgets.QStyledItemDelegate):
#     def paint(self, painter, option, index):
#         options = QtWidgets.QStyleOptionViewItemV4(option)
#         self.initStyleOption(options, index)
#
#         style = QtWidgets.QApplication.style() if options.widget is None else options.widget.style()
#
#         doc = QtWidgets.QTextDocument()
#         doc.setHtml(options.text)
#
#         options.text = ""
#         style.drawControl(QtWidgets.QStyle.CE_ItemViewItem, options, painter)
#
#         ctx = QtWidgets.QAbstractTextDocumentLayout.PaintContext()
#         # if option.state & QtWidgets.QStyle.State_Selected:
#         #     ctx.palette.setColor(QtGui.QPalette.Text, option.palette.color(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText))
#         # else:
#         #     ctx.palette.setColor(QtGui.QPalette.Text, option.palette.color(QtGui.QPalette.Active, QtGui.QPalette.HighlightedText))
#
#         textRect = style.subElementRect(QtWidgets.QStyle.SE_ItemViewItemText, options)
#         painter.save()
#         p = textRect.topLeft()
#         painter.translate(p.x(), p.y() - 3)
#         painter.setClipRect(textRect.translated(-textRect.topLeft()))
#         doc.documentLayout().draw(painter, ctx)
#
#         painter.restore()
#
#     def sizeHint(self, option, index):
#         options = QtWidgets.QStyleOptionViewItemV4(option)
#         self.initStyleOption(options, index)
#
#         doc = QtGui.QTextDocument()
#         doc.setHtml(options.text)
#         doc.setTextWidth(options.rect.width())
#         return QtCore.QSize(doc.idealWidth(), doc.size().height())


class MultiEditor(QtWidgets.QItemDelegate):
    def __init__(self, wparent):
        QtWidgets.QItemDelegate.__init__(self, None)
        self.win_me = wparent

    def createEditor(self, parent, option, index):
        editor = self.win_me.me_set_editor(parent)
        if editor:
            editor.installEventFilter(self)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, QtCore.Qt.DisplayRole)
        self.win_me.me_ponValor(editor, value)

    def setModelData(self, editor, model, index):
        value = self.win_me.me_leeValor(editor)
        model.setData(index, value)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class EtiquetaPOS(QtWidgets.QStyledItemDelegate):
    def __init__(self, with_figurines, siFondo=False, siLineas=True):
        self.si_figurines_pgn = with_figurines
        self.siAlineacion = False
        self.siLineas = siLineas
        self.siFondo = siFondo
        QtWidgets.QStyledItemDelegate.__init__(self, None)

    def rehazPosicion(self):
        position = self.bloquePieza.position
        self.setPos(position.x, position.y)

    def paint(self, painter, option, index):
        data = index.model().data(index, QtCore.Qt.DisplayRole)
        pgn, is_white, color, info, indicadorInicial, li_nags, agrisar, siLine = data
        if li_nags:
            li = []
            st = set()
            for x in li_nags:
                x = str(x)
                if x in st:
                    continue
                st.add(x)
                if x in dicNG:
                    li.append(dicNG[x])
            li_nags = li

        iniPZ = None
        finPZ = None
        if self.si_figurines_pgn and pgn:
            if pgn[0] in "QBKRN":
                iniPZ = pgn[0] if is_white else pgn[0].lower()
                pgn = pgn[1:]
            elif pgn[-1] in "QBRN":
                finPZ = pgn[-1] if is_white else pgn[-1].lower()
                pgn = pgn[:-1]

        if info and not finPZ:
            pgn += info
            info = None

        rect = option.rect
        width = rect.width()
        height = rect.height()
        x0 = rect.x()
        y0 = rect.y()
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(
                rect, QtGui.QColor(Code.configuration.pgn_selbackground())
            )  # sino no se ve en CDE-Motif-Windows
        elif self.siFondo:
            fondo = index.model().getFondo(index)
            if fondo:
                painter.fillRect(rect, fondo)

        if agrisar:
            painter.setOpacity(0.18)

        if indicadorInicial:
            painter.save()
            painter.translate(x0, y0)
            painter.drawPixmap(0, 0, dicPM[indicadorInicial])
            painter.restore()

        documentPGN = QtGui.QTextDocument()
        documentPGN.setDefaultFont(option.font)
        if color:
            pgn = '<font color="%s"><b>%s</b></font>' % (color, pgn)
        documentPGN.setHtml(pgn)
        wPGN = documentPGN.idealWidth()
        hPGN = documentPGN.size().height()
        hx = hPGN * 80 / 100
        wpz = int(hx * 0.8)

        if info:
            documentINFO = QtGui.QTextDocument()
            documentINFO.setDefaultFont(option.font)
            if color:
                info = '<font color="%s"><b>%s</b></font>' % (color, info)
            documentINFO.setHtml(info)
            wINFO = documentINFO.idealWidth()

        ancho = wPGN
        if iniPZ:
            ancho += wpz
        if finPZ:
            ancho += wpz
        if info:
            ancho += wINFO
        if li_nags:
            ancho += wpz * len(li_nags)

        x = x0 + (width - ancho) / 2
        if self.siAlineacion:
            alineacion = index.model().getAlineacion(index)
            if alineacion == "i":
                x = x0 + 3
            elif alineacion == "d":
                x = x0 + (width - ancho - 3)

        y = y0 + (height - hPGN * 0.9) / 2

        if iniPZ:
            painter.save()
            painter.translate(x, y)
            pm = dicPZ[iniPZ]
            pmRect = QtCore.QRectF(0, 0, hx, hx)
            pm.render(painter, pmRect)
            painter.restore()
            x += wpz

        painter.save()
        painter.translate(x, y)
        documentPGN.drawContents(painter)
        painter.restore()
        x += wPGN

        if finPZ:
            painter.save()
            painter.translate(x - 0.3 * wpz, y)
            pm = dicPZ[finPZ]
            pmRect = QtCore.QRectF(0, 0, hx, hx)
            pm.render(painter, pmRect)
            painter.restore()
            x += wpz

        if info:
            painter.save()
            painter.translate(x, y)
            documentINFO.drawContents(painter)
            painter.restore()
            x += wINFO

        if li_nags:
            for rndr in li_nags:
                painter.save()
                painter.translate(x - 0.2 * wpz, y)
                pmRect = QtCore.QRectF(0, 0, hx, hx)
                rndr.render(painter, pmRect)
                painter.restore()
                x += wpz

        if agrisar:
            painter.setOpacity(1.0)

        if self.siLineas:
            if not is_white:
                pen = QtGui.QPen()
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(x0, y0 + height - 1, x0 + width, y0 + height - 1)

            if siLine:
                pen = QtGui.QPen()
                pen.setWidth(1)
                painter.setPen(pen)
                painter.drawLine(x0 + width - 2, y0, x0 + width - 2, y0 + height)
