import Code
from Code.SQL import UtilSQL
from Code.Kibitzers import WindowKibitzers
from Code import XRun
from Code.Base.Constantes import *


class Manager:
    def __init__(self, procesador):
        self.procesador = procesador
        self.main_window = procesador.main_window
        self.configuration = procesador.configuration
        self.li_activos = []

    def close(self):
        for ipc_kibitzer in self.li_activos:
            ipc_kibitzer.terminar()

    def edit(self):
        w = WindowKibitzers.WKibitzers(self.main_window, self)
        w.exec_()

    def some_working(self):
        for n, ipc_kibitzer in enumerate(self.li_activos):
            if ipc_kibitzer.working():
                return True
        return False

    def stop(self):
        for ipc_kibitzer in self.li_activos:
            ipc_kibitzer.stop()

    def put_game(self, game, only_last=False):
        if self.li_activos:
            if only_last:
                self.li_activos[-1].put_game(game)
            else:
                li_closed = []
                for n, ipc_kibitzer in enumerate(self.li_activos):
                    if ipc_kibitzer.working():
                        ipc_kibitzer.put_game(game)
                    else:
                        li_closed.append(n)
                if li_closed:
                    li_closed.sort(reverse=True)
                    for x in li_closed:
                        kibitzer = self.li_activos[x]
                        kibitzer.close()
                        del self.li_activos[x]

    def run_new(self, nkibitzer):
        ipc_kibitzer = IPCKibitzer(nkibitzer)
        self.li_activos.append(ipc_kibitzer)


class Orden:
    def __init__(self):
        self.key = ""
        self.dv = {}

    def ponVar(self, name, valor):
        self.dv[name] = valor

    def bloqueEnvio(self):
        self.dv["__CLAVE__"] = self.key
        return self.dv


class IPCKibitzer:
    def __init__(self, numkibitzer):
        configuration = Code.configuration

        fdb = configuration.ficheroTemporal("db")

        self.ipc = UtilSQL.IPC(fdb, True)

        orden = Orden()
        orden.key = KIBRUN_CONFIGURATION
        orden.dv["USER"] = configuration.user
        orden.dv["NUMKIBITZER"] = numkibitzer

        self.escribe(orden)

        self.popen = XRun.run_lucas("-kibitzer", fdb)

    def escribe(self, orden):
        self.ipc.push(orden.bloqueEnvio())

    def working(self):
        if self.popen is None:
            return False
        return self.popen.poll() is None

    def put_game(self, game):
        orden = Orden()
        orden.key = KIBRUN_GAME
        orden.dv["GAME"] = game.save()
        self.escribe(orden)

    def stop(self):
        orden = Orden()
        orden.key = KIBRUN_STOP
        self.escribe(orden)

    def terminar(self):
        try:
            orden = Orden()
            orden.key = KIBRUN_CLOSE
            self.escribe(orden)
            self.ipc.close()
            self.close()
        except:
            pass

    def close(self):
        if self.popen:
            try:
                self.popen.terminate()
                self.popen = None
            except:
                pass
