"""
El grid es un TableView de QT.

Realiza llamadas a rutinas de la ventana donde esta ante determinados eventos, o en determinadas situaciones,
siempre que la rutina se haya definido en la ventana:

    - grid_doble_clickCabecera : ante un doble click en la head, normalmente se usa para la reordenacion de la tabla por la column pulsada.
    - grid_tecla_pulsada : al pulsarse una tecla, llama a esta rutina, para que pueda usarse por ejemplo en busquedas.
    - grid_tecla_control : al pulsarse una tecla de control, llama a esta rutina, para que pueda usarse por ejemplo en busquedas.
    - grid_doble_click : en el caso de un doble click en un registro, se hace la llamad a esta rutina
    - grid_right_button : si se ha pulsado el boton derecho del raton.
    - grid_setvalue : si hay un campo editable, la llamada se produce cuando se ha cambiado el valor tras la edicion.

    - grid_color_texto : si esta definida se la llama al mostrar el texto de un campo, para determinar el color del mismo.
    - grid_color_fondo : si esta definida se la llama al mostrar el texto de un campo, para determinar el color del fondo del mismo.

"""

from PySide2 import QtCore, QtGui, QtWidgets

from Code.QT import QTUtil
import Code


class ControlGrid(QtCore.QAbstractTableModel):
    """
    Modelo de datos asociado al grid, y que realiza xtodo el trabajo asignado por QT.
    """

    def __init__(self, grid, w_parent, oColumnasR):
        """
        @param tableView:
        @param oColumnasR: ListaColumnas con la configuration de todas las columnas visualizables.
        """
        QtCore.QAbstractTableModel.__init__(self, w_parent)
        self.grid = grid
        self.w_parent = w_parent
        self.siOrden = False
        self.hh = grid.horizontalHeader()
        self.siColorTexto = hasattr(self.w_parent, "grid_color_texto")
        self.siColorFondo = hasattr(self.w_parent, "grid_color_fondo")
        self.siAlineacion = hasattr(self.w_parent, "grid_alineacion")
        self.font = grid.font()
        self.siBold = hasattr(self.w_parent, "grid_bold")
        if self.siBold:
            self.bfont = QtGui.QFont(self.font)
            self.bfont.setWeight(75)

        self.oColumnasR = oColumnasR

    def rowCount(self, parent):
        """
        Llamada interna, solicitando el number de registros.
        """
        self.num_rows = self.w_parent.grid_num_datos(self.grid)
        return self.num_rows

    def refresh(self):
        """
        Si hay un cambio del number de registros, la llamada a esta rutina actualiza la visualizacion.
        """
        # self.emit(QtCore.SIGNAL("layoutAboutToBeChanged()"))
        self.layoutAboutToBeChanged.emit()
        ant_ndatos = self.num_rows
        nue_ndatos = self.w_parent.grid_num_datos(self.grid)
        if ant_ndatos != nue_ndatos:
            if ant_ndatos < nue_ndatos:
                self.insertRows(ant_ndatos, nue_ndatos - ant_ndatos)
            else:
                self.removeRows(nue_ndatos, ant_ndatos - nue_ndatos)
            self.num_rows = nue_ndatos

        ant_ncols = self.numCols
        nue_ncols = self.oColumnasR.numColumnas()
        if ant_ncols != nue_ncols:
            if ant_ncols < nue_ncols:
                self.insertColumns(0, nue_ncols - ant_ncols)
            else:
                self.removeColumns(nue_ncols, ant_ncols - nue_ncols)

        self.layoutChanged.emit()

    def columnCount(self, parent):
        """
        Llamada interna, solicitando el number de columnas.
        """
        self.numCols = self.oColumnasR.numColumnas()
        return self.numCols

    def data(self, index, role):
        """
        Llamada interna, solicitando informacion que ha de tener/contener el campo actual.
        """
        if not index.isValid():
            return None

        column = self.oColumnasR.column(index.column())

        if role == QtCore.Qt.TextAlignmentRole:
            if self.siAlineacion:
                resp = self.w_parent.grid_alineacion(self.grid, index.row(), column)
                if resp:
                    return column.QTalineacion(resp)
            return column.qtAlineacion
        elif role == QtCore.Qt.BackgroundRole:
            if self.siColorFondo:
                resp = self.w_parent.grid_color_fondo(self.grid, index.row(), column)
                if resp:
                    return resp
            return column.qtColorFondo
        elif role == QtCore.Qt.TextColorRole:
            if self.siColorTexto:
                resp = self.w_parent.grid_color_texto(self.grid, index.row(), column)
                if resp:
                    return resp
            return column.qtColorTexto
        elif self.siBold and role == QtCore.Qt.FontRole:
            if self.w_parent.grid_bold(self.grid, index.row(), column):
                return self.bfont
            return None

        if role == QtCore.Qt.DisplayRole:
            return self.w_parent.grid_dato(self.grid, index.row(), column)

        return None

    def getAlineacion(self, index):
        column = self.oColumnasR.column(index.column())
        return self.w_parent.grid_alineacion(self.grid, index.row(), column)

    def getFondo(self, index):
        column = self.oColumnasR.column(index.column())
        return self.w_parent.grid_color_fondo(self.grid, index.row(), column)

    def flags(self, index):
        """
        Llamada interna, solicitando mas informacion sobre las carcateristicas del campo actual.
        """
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        flag = QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable
        column = self.oColumnasR.column(index.column())
        if column.siEditable:
            flag |= QtCore.Qt.ItemIsEditable

        if column.siChecked:
            flag |= QtCore.Qt.ItemIsUserCheckable
        return flag

    def setData(self, index, valor, role=QtCore.Qt.EditRole):
        """
        Tras producirse la edicion de un campo en un registro se llama a esta rutina para cambiar el valor en el origen de los datos.
        Se lanza grid_setvalue en la ventana propietaria.
        """
        if not index.isValid():
            return None
        if role == QtCore.Qt.EditRole or role == QtCore.Qt.CheckStateRole:
            column = self.oColumnasR.column(index.column())
            nfila = index.row()
            self.w_parent.grid_setvalue(self.grid, nfila, column, valor)
            index2 = self.createIndex(nfila, 1)
            # self.emit(QtCore.SIGNAL('dataChanged(const QModelIndex &,const QModelIndex &)'), index2, index2)
            self.dataChanged.emit(index2, index2)

        return True

    def headerData(self, col, orientation, role):
        """
        Llamada interna, para determinar el texto de las cabeceras de las columnas.
        """
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            column = self.oColumnasR.column(col)
            return column.head
        # elif orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
        #     return str(col+1)
        return None


class Cabecera(QtWidgets.QHeaderView):
    """
    Se crea esta clase para poder implementar el doble click en la head.
    """

    def __init__(self, tvParent, siCabeceraMovible):
        QtWidgets.QHeaderView.__init__(self, QtCore.Qt.Horizontal)
        self.setSectionsMovable(siCabeceraMovible)
        self.setSectionsClickable(True)
        self.tvParent = tvParent

    def mouseDoubleClickEvent(self, event):
        numColumna = self.logicalIndexAt(event.x(), event.y())
        self.tvParent.dobleClickCabecera(numColumna)
        return QtWidgets.QHeaderView.mouseDoubleClickEvent(self, event)

    def mouseReleaseEvent(self, event):
        QtWidgets.QHeaderView.mouseReleaseEvent(self, event)
        numColumna = self.logicalIndexAt(event.x(), event.y())
        self.tvParent.mouseCabecera(numColumna)


class CabeceraHeight(Cabecera):
    def __init__(self, tvParent, siCabeceraMovible, height):
        Cabecera.__init__(self, tvParent, siCabeceraMovible)
        self.height = height

    def sizeHint(self):
        baseSize = Cabecera.sizeHint(self)
        baseSize.setHeight(self.height)
        return baseSize


class Grid(QtWidgets.QTableView):
    """
    Implementa un TableView, en base a la configuration de una lista de columnas.
    """

    def __init__(
        self,
        w_parent,
        o_columns,
        dicVideo=None,
        altoFila=24,
        siSelecFilas=False,
        siSeleccionMultiple=False,
        siLineas=True,
        siEditable=False,
        siCabeceraMovible=True,
        xid=None,
        background="",
        siCabeceraVisible=True,
        altoCabecera=None,
    ):
        """
        @param w_parent: ventana propietaria
        @param o_columns: configuration de las columnas.
        @param altoFila: altura de todas las filas.
        """

        assert w_parent is not None

        self.starting = True

        QtWidgets.QTableView.__init__(self)

        configuration = Code.configuration

        p = self.palette()
        p.setBrush(
            QtGui.QPalette.Active,
            QtGui.QPalette.Highlight,
            QtGui.QBrush(QtGui.QColor(configuration.pgn_selbackground())),
        )
        self.setPalette(p)

        self.w_parent = w_parent
        self.id = xid

        self.siCabeceraMovible = siCabeceraMovible

        self.o_columns = o_columns
        if dicVideo:
            self.restore_video(dicVideo)
        self.oColumnasR = self.o_columns.columnasMostrables(self)  # Necesario tras recuperar video

        self.cg = ControlGrid(self, w_parent, self.oColumnasR)

        self.setModel(self.cg)
        self.setShowGrid(siLineas)
        self.setWordWrap(False)
        self.setTextElideMode(QtCore.Qt.ElideNone)

        if background == "":
            self.setStyleSheet("QTableView {background: %s;}" % QTUtil.backgroundGUI())
        elif background is not None:
            self.setStyleSheet("QTableView {background: %s;}" % background)

        if configuration.x_pgn_headerbackground:
            self.setStyleSheet("QHeaderView::section { background-color:%s }" % configuration.pgn_headerbackground())

        self.coloresAlternados()

        if altoCabecera:
            hh = CabeceraHeight(self, siCabeceraMovible, altoCabecera)
        else:
            hh = Cabecera(self, siCabeceraMovible)
        self.setHorizontalHeader(hh)
        if not siCabeceraVisible:
            hh.setVisible(False)

        self.ponAltoFila(altoFila)

        self.seleccionaFilas(siSelecFilas, siSeleccionMultiple)

        self.set_widthsColumnas()  # es necesario llamarlo from_sq aqui

        self.siEditable = siEditable
        self.starting = False

        self.right_button_without_rows = False

    def set_right_button_without_rows(self, ok):
        self.right_button_without_rows = ok

    def buscaCabecera(self, key):
        return self.o_columns.buscaColumna(key)

    def coloresAlternados(self):
        self.setAlternatingRowColors(True)

    def seleccionaFilas(self, siSelecFilas, siSeleccionMultiple):
        sel = QtWidgets.QAbstractItemView.SelectRows if siSelecFilas else QtWidgets.QAbstractItemView.SelectItems
        if siSeleccionMultiple:
            selMode = QtWidgets.QAbstractItemView.ExtendedSelection
        else:
            selMode = QtWidgets.QAbstractItemView.SingleSelection
        self.setSelectionMode(selMode)
        self.setSelectionBehavior(sel)

    def releerColumnas(self):
        """
        Cuando se cambia la configuration de las columnas, se vuelven a releer y se indican al control de datos.
        """
        self.oColumnasR = self.o_columns.columnasMostrables(self)
        self.cg.oColumnasR = self.oColumnasR
        self.cg.refresh()
        self.set_widthsColumnas()

    def set_widthsColumnas(self):
        for numCol, column in enumerate(self.oColumnasR.li_columns):
            self.setColumnWidth(numCol, column.ancho)
            if column.edicion and column.must_show:
                self.setItemDelegateForColumn(numCol, column.edicion)

    def keyPressEvent(self, event):
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        cada tecla pulsada, llamando a la rutina correspondiente si existe (grid_tecla_pulsada/grid_tecla_control)
        """
        k = event.key()
        m = int(event.modifiers())
        is_shift = (m & QtCore.Qt.ShiftModifier) > 0
        is_control = (m & QtCore.Qt.ControlModifier) > 0
        is_alt = (m & QtCore.Qt.AltModifier) > 0
        if hasattr(self.w_parent, "grid_tecla_pulsada"):
            if not (is_control or is_alt) and k < 256:
                self.w_parent.grid_tecla_pulsada(self, event.text())
        if hasattr(self.w_parent, "grid_tecla_control"):
            self.w_parent.grid_tecla_control(self, k, is_shift, is_control, is_alt)
            event.ignore()
            return

        QtWidgets.QTableView.keyPressEvent(self, event)

    def selectionChanged(self, uno, dos):
        if self.starting:
            return
        if hasattr(self.w_parent, "grid_cambiado_registro"):
            fil, column = self.current_position()
            self.w_parent.grid_cambiado_registro(self, fil, column)
        self.refresh()

    def wheelEvent(self, event):
        if hasattr(self.w_parent, "grid_wheel_event"):
            self.w_parent.grid_wheel_event(self, event.angleDelta().y() > 0)
        else:
            QtWidgets.QTableView.wheelEvent(self, event)

    def mouseDoubleClickEvent(self, event):
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        cada doble click, llamando a la rutina correspondiente si existe (grid_doble_click)
        con el number de row y el objeto column como argumentos
        """
        if self.siEditable:
            QtWidgets.QTableView.mouseDoubleClickEvent(self, event)
        if hasattr(self.w_parent, "grid_doble_click") and event.button() == 1:
            fil, column = self.current_position()
            self.w_parent.grid_doble_click(self, fil, column)

    def mousePressEvent(self, event):
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        cada pulsacion del boton derecho, llamando a la rutina correspondiente si existe (grid_right_button)
        """
        QtWidgets.QTableView.mousePressEvent(self, event)
        button = event.button()
        fil, col = self.current_position()
        if button == QtCore.Qt.RightButton:
            if hasattr(self.w_parent, "grid_right_button"):
                if fil < 0 and not self.right_button_without_rows:
                    return

                class Vacia:
                    pass

                modif = Vacia()
                m = int(event.modifiers())
                modif.is_shift = (m & QtCore.Qt.ShiftModifier) > 0
                modif.is_control = (m & QtCore.Qt.ControlModifier) > 0
                modif.is_alt = (m & QtCore.Qt.AltModifier) > 0
                self.w_parent.grid_right_button(self, fil, col, modif)
        elif button == QtCore.Qt.LeftButton:
            if fil < 0:
                return
            if col.siChecked:
                value = self.w_parent.grid_dato(self, fil, col)
                self.w_parent.grid_setvalue(self, fil, col, not value)
                self.refresh()
            elif hasattr(self.w_parent, "grid_left_button"):
                self.w_parent.grid_left_button(self, fil, col)

    def dobleClickCabecera(self, numColumna):
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        los doble clicks sobre la head , normalmente para cambiar el orden de la column,
        llamando a la rutina correspondiente si existe (grid_doble_clickCabecera) y con el
        argumento del objeto column
        """
        if hasattr(self.w_parent, "grid_doble_clickCabecera"):
            self.w_parent.grid_doble_clickCabecera(self, self.oColumnasR.column(numColumna))

    def mouseCabecera(self, numColumna):
        """
        Se gestiona este evento, ante la posibilidad de que la ventana quiera controlar,
        los doble clicks sobre la head , normalmente para cambiar el orden de la column,
        llamando a la rutina correspondiente si existe (grid_doble_clickCabecera) y con el
        argumento del objeto column
        """
        if hasattr(self.w_parent, "grid_pulsada_cabecera"):
            self.w_parent.grid_pulsada_cabecera(self, self.oColumnasR.column(numColumna))

    def save_video(self, dic):
        """
        Guarda en el diccionario de video la configuration actual de todas las columnas

        @param dic: diccionario de video donde se guarda la configuration de las columnas
        """
        liClaves = []
        for n, column in enumerate(self.oColumnasR.li_columns):
            column.ancho = self.columnWidth(n)
            column.position = self.columnViewportPosition(n)
            column.guardarConf(dic, self)
            liClaves.append(column.key)

        # Las que no se muestran
        for column in self.o_columns.li_columns:
            if not (column.key in liClaves):
                column.guardarConf(dic, self)

    def restore_video(self, dic):
        for column in self.o_columns.li_columns:
            column.recuperarConf(dic, self)

        if self.siCabeceraMovible:
            self.o_columns.li_columns.sort(key=lambda xcol: xcol.position)

    def columnas(self):
        for n, column in enumerate(self.oColumnasR.li_columns):
            column.ancho = self.columnWidth(n)
            column.position = self.columnViewportPosition(n)
        if self.siCabeceraMovible:
            self.o_columns.li_columns.sort(key=lambda xcol: xcol.position)
        return self.o_columns

    def anchoColumnas(self):
        """
        Calcula el ancho que corresponde a todas las columnas mostradas.
        """
        ancho = 0
        for n, column in enumerate(self.oColumnasR.li_columns):
            ancho += column.ancho
        return ancho

    def fixMinWidth(self):
        nAncho = self.anchoColumnas() + 24
        self.setMinimumWidth(nAncho)
        return nAncho

    def recno(self):
        """
        Devuelve la row actual.
        """
        n = self.currentIndex().row()
        nX = self.cg.num_rows - 1
        return n if n <= nX else nX

    def reccount(self):
        return self.cg.num_rows

    def recnosSeleccionados(self):
        li = []
        for x in self.selectionModel().selectedIndexes():
            li.append(x.row())

        return list(set(li))

    def goto(self, row, col):
        """
        Se situa en una position determinada.
        """
        elem = self.cg.createIndex(row, col)
        self.setCurrentIndex(elem)
        self.scrollTo(elem)

    def gotop(self):
        """
        Se situa al principio del grid.
        """
        if self.cg.num_rows > 0:
            self.goto(0, 0)

    def gobottom(self, col=0):
        """
        Se situa en el ultimo registro del frid.
        """
        if self.cg.num_rows > 0:
            self.goto(self.cg.num_rows - 1, col)

    def refresh(self):
        """
        Hace un refresco de la visualizacion del grid, ante algun cambio en el contenido.
        """
        self.cg.refresh()

    def current_position(self):
        """
        Devuelve la position actual.

        @return: tupla con ( num row, objeto column )
        """
        column = self.oColumnasR.column(self.currentIndex().column())
        return self.recno(), column

    def posActualN(self):
        """
        Devuelve la position actual.

        @return: tupla con ( num row, num  column )
        """
        return self.recno(), self.currentIndex().column()

    def tipoLetra(self, name="", puntos=8, peso=50, is_italic=False, is_underlined=False, is_striked=False, txt=None):
        font = QtGui.QFont()
        if txt is None:
            cursiva = 1 if is_italic else 0
            subrayado = 1 if is_underlined else 0
            tachado = 1 if is_striked else 0
            if not name:
                name = font.defaultFamily()
            txt = "%s,%d,-1,5,%d,%d,%d,%d,0,0" % (name, puntos, peso, cursiva, subrayado, tachado)
        font.fromString(txt)
        self.ponFuente(font)

    def ponFuente(self, font):
        self.setFont(font)
        hh = self.horizontalHeader()
        hh.setFont(font)

    def ponAltoFila(self, altoFila):
        vh = self.verticalHeader()
        vh.setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        vh.setDefaultSectionSize(altoFila)
        vh.setVisible(False)
