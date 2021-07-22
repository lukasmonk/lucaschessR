"""
Rutinas internas para la conexion con DGTEBDLL.dll
"""
import os
import ctypes

from Code import Util
import Code

DGT_ON = "DGT.ON"


def activarSegunON_OFF(dispatch):
    if siON():
        if Code.dgt is None:
            if activar():
                showDialog()
            else:
                ponOFF()
                return False
        Code.dgtDispatch = dispatch
    else:
        if Code.dgt:
            desactivar()
    return True


def siON():
    return Util.exist_file(DGT_ON)


def ponON():
    with open(DGT_ON, "wb") as f:
        f.write(b"act")


def ponOFF():
    Util.remove_file(DGT_ON)


def cambiarON_OFF():
    if siON():
        Util.remove_file(DGT_ON)
    else:
        ponON()


def envia(quien, dato):
    # log("[envia: %s] : %s [%s]"%(str(quien), str(dato), str(Code.dgtDispatch)))
    if Code.dgtDispatch:
        return Code.dgtDispatch(quien, dato)
    return 1


def set_position(game):
    if Code.dgt:
        if (Code.configuration.x_digital_board == "DGT") or (
            Code.configuration.x_digital_board == "Novag UCB" and Code.configuration.x_digital_board_version == 0
        ):
            writePosition(game.last_position.fenDGT())
        else:
            writePosition(game.last_position.fen())


def quitarDispatch():
    Code.dgtDispatch = None


def log(cad):
    import traceback

    with open("dgt.log", "at", encoding="utf-8", errors="ignore") as q:
        q.write("\n[%s] %s\n" % (Util.today(), cad))
        for line in traceback.format_stack():
            q.write("    %s\n" % line.strip())


# CALLBACKS


def registerStatusFunc(dato):
    envia("status", dato)
    return 1


def registerScanFunc(dato):
    envia("scan", _dgt2fen(dato))
    return 1


def registerWhiteMoveInputFunc(dato):
    return envia("whiteMove", _dgt2pv(dato))


def registerBlackMoveInputFunc(dato):
    return envia("blackMove", _dgt2pv(dato))


def registerWhiteTakeBackFunc():
    return envia("whiteTakeBack", True)


def registerBlackTakeBackFunc():
    return envia("blackTakeBack", True)


def activar():
    is_linux = Code.is_linux

    dgt = None
    if is_linux:
        functype = ctypes.CFUNCTYPE
        path = os.path.join(Code.folder_OS, "DigitalBoards")
        if Code.configuration.x_digital_board == "DGT-gon":
            path_so = os.path.join(path, "libdgt.so")
        elif Code.configuration.x_digital_board == "Certabo":
            path_so = os.path.join(path, "libcer.so")
        elif Code.configuration.x_digital_board == "CertaboBT":
            path_so = os.path.join(path, "libcerBT.so")
        elif Code.configuration.x_digital_board == "Millennium":
            path_so = os.path.join(path, "libmcl.so")
        elif Code.configuration.x_digital_board == "Citrine":
            path_so = os.path.join(path, "libcit.so")
        else:
            path_so = os.path.join(path, "libucb.so")
        if os.path.isfile(path_so):
            try:
                dgt = ctypes.CDLL(path_so)
            except:
                dgt = None
                from Code.QT import QTUtil2
                QTUtil2.message(None, """It is not possible to install the driver for the board, one way to solve the problem is to install the libraries:
 sudo apt install libqt5pas1
 or
 sudo dnf install qt5pas-devel""")

    else:
        functype = ctypes.WINFUNCTYPE
        for path in (
            os.path.join(Code.folder_OS, "DigitalBoards"),
            "",
            "C:/Program Files (x86)/DGT Projects/",
            "C:/Program Files (x86)/Common Files/DGT Projects/",
            "C:/Program Files/DGT Projects/",
            "C:/Program Files/Common Files/DGT Projects/",
        ):
            try:
                if Code.configuration.x_digital_board == "DGT":
                    path_dll = os.path.join(path, "DGTEBDLL.dll")
                elif Code.configuration.x_digital_board == "DGT-gon":
                    path_dll = os.path.join(path, "DGT_DLL.dll")
                elif Code.configuration.x_digital_board == "Certabo":
                    path_dll = os.path.join(path, "CER_DLL.dll")
                elif Code.configuration.x_digital_board == "Millennium":
                    path_dll = os.path.join(path, "MCL_DLL.dll")
                elif Code.configuration.x_digital_board == "Citrine":
                    path_dll = os.path.join(path, "CIT_DLL.dll")
                else:
                    path_dll = os.path.join(path, "UCB_DLL.dll")
                if os.path.isfile(path_dll):
                    dgt = ctypes.WinDLL(path_dll)
                    break
            except:
                pass
    if dgt is None:
        return False

    # log( "activar" )

    Code.dgt = dgt

    cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
    st = cmpfunc(registerStatusFunc)
    dgt._DGTDLL_RegisterStatusFunc.argtype = [st]
    dgt._DGTDLL_RegisterStatusFunc.restype = ctypes.c_int
    dgt._DGTDLL_RegisterStatusFunc(st)

    cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
    st = cmpfunc(registerScanFunc)
    dgt._DGTDLL_RegisterScanFunc.argtype = [st]
    dgt._DGTDLL_RegisterScanFunc.restype = ctypes.c_int
    dgt._DGTDLL_RegisterScanFunc(st)

    cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
    st = cmpfunc(registerWhiteMoveInputFunc)
    dgt._DGTDLL_RegisterWhiteMoveInputFunc.argtype = [st]
    dgt._DGTDLL_RegisterWhiteMoveInputFunc.restype = ctypes.c_int
    dgt._DGTDLL_RegisterWhiteMoveInputFunc(st)

    cmpfunc = functype(ctypes.c_int, ctypes.c_char_p)
    st = cmpfunc(registerBlackMoveInputFunc)
    dgt._DGTDLL_RegisterBlackMoveInputFunc.argtype = [st]
    dgt._DGTDLL_RegisterBlackMoveInputFunc.restype = ctypes.c_int
    dgt._DGTDLL_RegisterBlackMoveInputFunc(st)

    dgt._DGTDLL_WritePosition.argtype = [ctypes.c_char_p]
    dgt._DGTDLL_WritePosition.restype = ctypes.c_int

    dgt._DGTDLL_ShowDialog.argtype = [ctypes.c_int]
    dgt._DGTDLL_ShowDialog.restype = ctypes.c_int

    dgt._DGTDLL_HideDialog.argtype = [ctypes.c_int]
    dgt._DGTDLL_HideDialog.restype = ctypes.c_int

    dgt._DGTDLL_WriteDebug.argtype = [ctypes.c_bool]
    dgt._DGTDLL_WriteDebug.restype = ctypes.c_int

    dgt._DGTDLL_SetNRun.argtype = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
    dgt._DGTDLL_SetNRun.restype = ctypes.c_int

    # Added by GON
    if Code.configuration.x_digital_board != "DGT":
        dgt._DGTDLL_GetVersion.argtype = []
        dgt._DGTDLL_GetVersion.restype = ctypes.c_int
        Code.configuration.x_digital_board_version = dgt._DGTDLL_GetVersion()
        try:
            dgt._DGTDLL_AllowTakebacks.argtype = [ctypes.c_bool]
            dgt._DGTDLL_AllowTakebacks.restype = ctypes.c_int
            dgt._DGTDLL_AllowTakebacks(ctypes.c_bool(True))
            cmpfunc = functype(ctypes.c_int)
            st = cmpfunc(registerWhiteTakeBackFunc)
            dgt._DGTDLL_RegisterWhiteTakebackFunc.argtype = [st]
            dgt._DGTDLL_RegisterWhiteTakebackFunc.restype = ctypes.c_int
            dgt._DGTDLL_RegisterWhiteTakebackFunc(st)
            cmpfunc = functype(ctypes.c_int)
            st = cmpfunc(registerBlackTakeBackFunc)
            dgt._DGTDLL_RegisterBlackTakebackFunc.argtype = [st]
            dgt._DGTDLL_RegisterBlackTakebackFunc.restype = ctypes.c_int
            dgt._DGTDLL_RegisterBlackTakebackFunc(st)
        except:
            pass
    # ------------

    return True


def desactivar():
    if Code.dgt:
        # log( "desactivar" )
        hideDialog()
        del Code.dgt
        Code.dgt = None
        Code.dgtDispatch = None


# Funciones directas en la DGT


def showDialog():
    if Code.dgt:
        dgt = Code.dgt
        dgt._DGTDLL_ShowDialog(ctypes.c_int(1))


def hideDialog():
    if Code.dgt:
        dgt = Code.dgt
        dgt._DGTDLL_HideDialog(ctypes.c_int(1))


def writeDebug(activar):
    if Code.dgt:
        dgt = Code.dgt
        dgt._DGTDLL_WriteDebug(activar)


def writePosition(cposicion):
    if Code.dgt:
        # log( "Enviado a la DGT" + cposicion )
        dgt = Code.dgt
        dgt._DGTDLL_WritePosition(cposicion.encode())


def writeClocks(wclock, bclock):
    if Code.dgt:
        if (Code.configuration.x_digital_board == "DGT") or (Code.configuration.x_digital_board == "DGT-gon"):
            # log( "WriteClocks: W-%s B-%s"%(str(wclock), str(bclock)) )
            dgt = Code.dgt
            dgt._DGTDLL_SetNRun(wclock.encode(), bclock.encode(), 0)


# Utilidades para la trasferencia de datos


def _dgt2fen(datobyte):
    n = 0
    dato = datobyte.decode()
    ndato = len(dato)
    caja = [""] * 8
    ncaja = 0
    ntam = 0
    while True:
        if dato[n].isdigit():
            num = int(dato[n])
            if (n + 1 < ndato) and dato[n + 1].isdigit():
                num = num * 10 + int(dato[n + 1])
                n += 1
            while num:
                pte = 8 - ntam
                if num >= pte:
                    caja[ncaja] += str(pte)
                    ncaja += 1
                    ntam = 0
                    num -= pte
                else:
                    caja[ncaja] += str(num)
                    ntam += num
                    break

        else:
            caja[ncaja] += dato[n]
            ntam += 1
        if ntam == 8:
            ncaja += 1
            ntam = 0
        n += 1
        if n == ndato:
            break
    if ncaja != 8:
        caja[7] += str(8 - ntam)
    return "/".join(caja)


def _dgt2pv(datobyte):
    dato = datobyte.decode()
    # Coronacion
    if dato[0] in "Pp" and dato[3].lower() != "p":
        return dato[1:3] + dato[4:6] + dato[3].lower()

    return dato[1:3] + dato[4:6]


# Lo mismo, de otra forma


# def xdgt2fen(xdgt):
#     liD = xdgt.split(" ")
#     dgt = liD[0]
#
#     li = []
#     num = 0
#     for c in dgt:
#         if c.isdigit():
#             num = num * 10 + int(c)
#         else:
#             if num:
#                 li.append((1, num))
#                 num = 0
#             li.append((0, c))
#     if num:
#         li.append((1, num))
#     lir = []
#     act = ""
#     pte = 8
#     for tp, v in li:
#         if tp == 1:
#             while v >= pte:
#                 act += str(pte)
#                 lir.append(act)
#                 v -= pte
#                 act = ""
#                 pte = 8
#             if v:
#                 act += str(v)
#                 pte -= v
#         else:
#             act += v
#             pte -= 1
#         if pte == 0:
#             lir.append(act)
#             act = ""
#             pte = 8
#     if pte and len(lir) == 7:
#         act += str(pte)
#         lir.append(act)
#     liD[0] = "/".join(lir)
#     return " ".join(liD)


# def fen2xdgt(fen):
#     li = fen.split(" ")
#     x0 = li[0]
#     li0 = x0.replace("/", "")
#     resp = ""
#     num = 0
#     for c in li0:
#         if c.isdigit():
#             num += int(c)
#         else:
#             if num:
#                 resp += str(num)
#                 num = 0
#             resp += c
#     if num:
#         resp += str(num)
#     li[0] = resp
#     return " ".join(li)
