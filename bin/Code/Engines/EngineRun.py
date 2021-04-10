import sys
import signal

import os
import time
import subprocess
import threading
import psutil
import random

from PySide2 import QtCore

import Code
from Code.Engines import Priorities
from Code.Engines import EngineResponse
from Code.Polyglots import Books
from Code import Util
from Code.QT import QTUtil2


class RunEngine:
    def __init__(self, name, exe, liOpcionesUCI=None, nMultiPV=0, priority=None, args=None):
        if Code.DEBUG_ENGINE:
            self.put_line = self.put_line_debug
            self.xstdout_thread = self.xstdout_thread_debug
        else:
            self.put_line = self.put_line_base
            self.xstdout_thread = self.xstdout_thread_base

        self.name = name

        self.ponder = False
        self.pondering = False

        self.is_white = True

        self.gui_dispatch = None
        self.ultDispatch = 0
        self.minDispatch = 1.0  # segundos
        self.whoDispatch = name
        self.uci_ok = False

        self.log = None

        self.uci_lines = []

        if not os.path.isfile(exe):
            QTUtil2.message_error(None, "%s:\n  %s" % (_("Engine not found"), exe))
            return

        self.pid = None
        self.exe = os.path.abspath(exe)
        self.direxe = os.path.dirname(exe)
        self.priority = priority
        self.working = True
        self.liBuffer = []
        self.starting = True
        self.args = ["./%s" % os.path.basename(self.exe)]
        if args:
            self.args.extend(args)

        self.direct_dispatch = None

        self.mrm = None

        self.start()

        self.lockAC = True

        self.orden_uci()

        txt_uci_analysismode = "UCI_AnalyseMode"
        uci_analysismode = False

        setoptions = False
        if liOpcionesUCI:
            for opcion, valor in liOpcionesUCI:
                if type(valor) == bool:
                    valor = str(valor).lower()
                self.set_option(opcion, valor)
                setoptions = True
                if opcion == txt_uci_analysismode:
                    uci_analysismode = True
                if opcion.lower() == "ponder":
                    self.ponder = valor == "true"

        self.nMultiPV = nMultiPV
        if nMultiPV:
            self.ponMultiPV(nMultiPV)
            if not uci_analysismode:
                for line in self.uci_lines:
                    if "UCI_AnalyseMode" in line:
                        self.set_option("UCI_AnalyseMode", "true")
                        setoptions = True
        if setoptions:
            self.put_line_base("isready")
            self.wait_mrm("readyok", 1000)

        self.ucinewgame()

    def cerrar(self):
        self.working = False

    def put_line_debug(self, line: str):
        if self.working:
            Code.xpr(self.name, "put>>> %s\n" % line)
            self.stdin_lock.acquire()
            line = line.encode()
            if self.log:
                self.log_write(">>> %s\n" % line)
            self.stdin.write(line + b"\n")
            self.stdin.flush()
            self.stdin_lock.release()

    def put_line_base(self, line: str):
        if self.working:
            self.stdin_lock.acquire()
            line = line.encode()
            if self.log:
                self.log_write(">>> %s\n" % line)
            self.stdin.write(line + b"\n")
            self.stdin.flush()
            self.stdin_lock.release()

    def get_lines(self):
        self.stdout_lock.acquire()
        li = self.liBuffer
        self.liBuffer = []
        self.stdout_lock.release()
        if self.log:
            for line in li:
                self.log_write(line)
        return li

    def hay_datos(self):
        return len(self.liBuffer) > 0

    def reset(self):
        self.stdout_lock.acquire()
        self.mrm = EngineResponse.MultiEngineResponse(self.name, self.is_white)
        self.stdout_lock.release()

    def xstdout_thread_base(self, stdout, lock):
        try:
            while self.working:
                line = stdout.readline().decode()
                if not line:
                    break
                lock.acquire()
                self.liBuffer.append(line)
                if self.direct_dispatch:
                    self.mrm.dispatch(line)
                lock.release()
                if self.direct_dispatch and "bestmove" in line:
                    self.direct_dispatch()
        except:
            pass
        finally:
            stdout.close()

    def xstdout_thread_debug(self, stdout, lock):
        try:
            while self.working:
                line = stdout.readline().decode()
                if not line:
                    break
                xpr(self.name, line)
                lock.acquire()
                self.liBuffer.append(line)
                if self.direct_dispatch:
                    self.mrm.dispatch(line)
                lock.release()
                if self.direct_dispatch and "bestmove" in line:
                    self.direct_dispatch()
        except:
            pass
        finally:
            stdout.close()

    def start_engine(self):
        if Code.is_windows:
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
        else:
            startupinfo = None
        curdir = os.path.abspath(os.curdir)  # problem with "." as curdir
        os.chdir(self.direxe)  # to fix problems with non ascii folders

        self.process = subprocess.Popen(
            self.args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, startupinfo=startupinfo
        )
        os.chdir(curdir)

        self.pid = self.process.pid
        if self.priority is not None:
            p = psutil.Process(self.pid)
            p.nice(Priorities.priorities.value(self.priority))

        self.stdin = self.process.stdin
        self.stdout = self.process.stdout

    def start(self):
        self.start_engine()

        self.stdout_lock = threading.Lock()
        stdout_thread = threading.Thread(target=self.xstdout_thread, args=(self.process.stdout, self.stdout_lock))
        stdout_thread.daemon = True
        stdout_thread.start()

        self.stdin_lock = threading.Lock()

        self.starting = False

    def close(self):
        self.working = False
        if self.log:
            self.log_close()
            self.log = None

        if self.pid:
            try:
                if self.process.poll() is None:
                    self.put_line("stop")
                    self.put_line("quit")
                    self.process.kill()
                    self.process.terminate()
            except:
                if Code.is_windows:
                    subprocess.call(['taskkill', '/F', '/T', '/PID', str(self.pid)])
                else:
                    os.kill(self.pid, signal.SIGTERM)
                sys.stderr.write("INFO X CLOSE: except - the engine %s won't close properly.\n" % self.exe)

            self.pid = None

    def log_open(self, file):
        self.log = open(file, "at", encoding="utf-8")
        self.log.write("%s %s\n\n" % (str(Util.today()), "-" * 70))

    def log_close(self):
        if self.log:
            self.log.close()
            self.log = None

    def log_write(self, line):
        self.log.write(line)

    def dispatch(self):
        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.ExcludeUserInputEvents)
        if self.gui_dispatch:
            tm = time.time()
            if tm - self.ultDispatch < self.minDispatch:
                return True
            self.ultDispatch = tm
            self.mrm.ordena()
            rm = self.mrm.mejorMov()
            rm.whoDispatch = self.whoDispatch
            if not self.gui_dispatch(rm):
                return False
        return True

    def wait_mrm(self, seektxt, msStop):
        iniTiempo = time.time()
        stop = False
        while True:
            if self.hay_datos():
                for line in self.get_lines():
                    self.mrm.dispatch(line)
                    if seektxt in line:
                        if not self.dispatch():
                            self.put_line("stop")
                        return True

            queda = msStop - int((time.time() - iniTiempo) * 1000)
            if queda <= 0:
                if stop:
                    return True
                self.put_line("stop")
                msStop += 2000
                stop = True
            if not self.hay_datos():
                if not self.dispatch():
                    self.put_line("stop")
                    return False
                time.sleep(0.001)

    def wait_list(self, txt, ms_stop):
        ini_tiempo = time.time()
        stop = False
        ok = False
        li = []
        while True:
            lt = self.get_lines()
            if lt:
                for line in lt:
                    if txt in line:
                        ok = True
                        break
                li.extend(lt)
                if ok:
                    return li, True

            queda = ms_stop - int((time.time() - ini_tiempo) * 1000)
            if queda <= 0:
                if stop:
                    return li, False
                self.put_line("stop")
                ms_stop += 2000
                stop = True
            if not self.hay_datos():
                time.sleep(0.001)

    def wait_txt(self, seektxt, msStop):
        ini_tiempo = time.time()
        while True:
            lt = self.get_lines()
            for line in lt:
                if seektxt in line:
                    return True

            queda = msStop - int((time.time() - ini_tiempo) * 1000)
            if queda <= 0:
                return False
            if not self.hay_datos():
                time.sleep(0.090)

    def work_ok(self, orden):
        self.reset()
        self.put_line(orden)
        self.put_line("isready")
        return self.wait_list("readyok", 1000)

    def work_bestmove(self, orden, msmax_time):
        self.reset()
        self.put_line(orden)
        self.wait_mrm("bestmove", msmax_time)

    def work_infinite(self, busca, msmax_time):
        self.reset()
        self.put_line("go infinite")
        self.wait_mrm(busca, msmax_time)

    def seek_bestmove(self, max_time, max_depth, is_savelines):
        env = "go"
        if max_depth:
            env += " depth %d" % max_depth
        elif max_time:
            env += " movetime %d" % max_time

        ms_time = 10000
        if max_time:
            ms_time = max_time + 3000
        elif max_depth:
            ms_time = int(max_depth * ms_time / 3.0)

        self.reset()
        if is_savelines:
            self.mrm.save_lines()
        self.mrm.setTimeDepth(max_time, max_depth)

        self.work_bestmove(env, ms_time)

        self.mrm.ordena()

        return self.mrm

    def seek_infinite(self, max_depth, max_time):
        if max_depth:
            busca = " depth %d " % (max_depth + 1,)

            max_time = max_depth * 2000
            if max_depth > 9:
                max_time += (max_depth - 9) * 20000
        else:
            busca = " @@ "  # que no busque nada
            max_depth = None

        self.reset()
        self.mrm.setTimeDepth(max_time, max_depth)

        self.work_infinite(busca, max_time)

        self.mrm.ordena()
        return self.mrm

    def seek_bestmove_time(self, time_white, time_black, inc_time_move):
        env = "go wtime %d btime %d" % (time_white, time_black)
        if inc_time_move:
            env += " winc %d" % inc_time_move
        max_time = time_white if self.is_white else time_black

        self.reset()
        self.mrm.setTimeDepth(max_time, None)

        self.work_bestmove(env, max_time)

        self.mrm.ordena()
        return self.mrm

    def set_game_position(self, game, njg=99999):
        pos_inicial = "startpos" if game.siFenInicial() else "fen %s" % game.first_position.fen()
        li = [move.movimiento().lower() for n, move in enumerate(game.li_moves) if n < njg]
        moves = " moves %s" % (" ".join(li)) if li else ""
        if not li:
            self.ucinewgame()
        self.work_ok("position %s%s" % (pos_inicial, moves))
        self.is_white = game.is_white() if njg > 9000 else game.move(njg).is_white()

    def set_fen_position(self, fen):
        self.ucinewgame()
        self.work_ok("position fen %s" % fen)
        self.is_white = "w" in fen

    def ucinewgame(self):
        self.work_ok("ucinewgame")

    def ac_inicio(self, game):
        self.lockAC = True
        self.set_game_position(game)
        self.reset()
        self.put_line("go infinite")
        self.lockAC = False

    def ac_inicio_limit(self, game, max_time, max_depth):
        self.lockAC = True
        self.best_move_done = False
        self.set_game_position(game)
        self.reset()
        env = "go"
        if max_depth:
            env += " depth %d" % max_depth
        elif max_time:
            env += " movetime %d" % max_time
        self.put_line(env)
        self.lockAC = False

    def ac_lee(self):
        if self.lockAC:
            return True
        nlines = 0
        for line in self.get_lines():
            if "bestmove" in line:
                self.best_move_done = True
            self.mrm.dispatch(line)
            nlines += 1
        return nlines

    def ac_estado(self):
        self.ac_lee()
        self.mrm.ordena()
        return self.mrm

    def ac_minimo(self, minimoTiempo, lockAC):
        self.ac_lee()
        self.mrm.ordena()
        rm = self.mrm.mejorMov()
        tm = rm.time  # problema cuando da por terminada la lectura y el rm.time siempre es el mismo
        bucle = 0
        while rm.time < minimoTiempo and tm < minimoTiempo:
            time.sleep(0.1)
            bucle += 1
            if bucle > 1 and self.ac_lee() == 0:
                break
            tm += 100
            rm = self.mrm.mejorMov()
        self.lockAC = lockAC
        return self.ac_estado()

    def ac_minimoTD(self, minTime, minDepth, lockAC):
        self.ac_lee()
        self.mrm.ordena()
        rm = self.mrm.mejorMov()
        while rm.time < minTime or rm.depth < minDepth:
            time.sleep(0.1)
            self.ac_lee()
            rm = self.mrm.mejorMov()
        self.lockAC = lockAC
        return self.ac_estado()

    def ac_final(self, minimo_ms_time):
        self.ac_minimo(minimo_ms_time, True)
        self.put_line("stop")
        time.sleep(0.1)
        return self.ac_estado()

    def ac_final_limit(self, minTime):
        if not self.best_move_done:
            self.ac_lee()
            self.mrm.ordena()
            rm = self.mrm.mejorMov()
            while rm.time < minTime and not self.best_move_done:
                time.sleep(0.1)
                self.ac_lee()
                rm = self.mrm.mejorMov()
        return self.ac_estado()

    def analysis_stable(self, game, njg, ktime, kdepth, is_savelines, st_centipawns, st_depths, st_timelimit):
        self.set_game_position(game, njg)
        self.reset()
        if is_savelines:
            self.mrm.save_lines()
        self.put_line("go infinite")

        def lee():
            for line in self.get_lines():
                self.mrm.dispatch(line)
            self.mrm.ordena()
            return self.mrm.mejorMov()

        ok_time = False if ktime else True
        ok_depth = False if kdepth else True
        while self.gui_dispatch(None):
            rm = lee()
            if not ok_time:
                ok_time = rm.time >= ktime
            if not ok_depth:
                ok_depth = rm.depth >= kdepth
            if ok_time and ok_depth:
                break
            time.sleep(0.1)

        if st_timelimit == 0:
            st_timelimit = 999999
        while not self.mrm.is_stable(st_centipawns, st_depths) and self.gui_dispatch(None) and st_timelimit > 0.0:
            time.sleep(0.1)
            st_timelimit -= 0.1
            lee()
        self.put_line("stop")
        return self.mrm

    def ponGuiDispatch(self, gui_dispatch, whoDispatch=None):
        self.gui_dispatch = gui_dispatch
        if whoDispatch is not None:
            self.whoDispatch = whoDispatch

    def ponMultiPV(self, nMultiPV):
        self.work_ok("setoption name MultiPV value %s" % nMultiPV)

    def orden_uci(self):
        self.reset()
        self.put_line("uci")
        li, self.uci_ok = self.wait_list("uciok", 10000)
        self.uci_lines = [x for x in li if x.startswith("id ") or x.startswith("option name")] if self.uci_ok else []

    def set_option(self, name, value):
        if value:
            self.put_line("setoption name %s value %s" % (name, value))
        else:
            self.put_line("setoption name %s" % name)

    def bestmove_game(self, game, max_time, max_depth):
        self.set_game_position(game)
        return self.seek_bestmove(max_time, max_depth, False)

    def bestmove_game_jg(self, game, njg, max_time, max_depth, is_savelines=False):
        self.set_game_position(game, njg)
        return self.seek_bestmove(max_time, max_depth, is_savelines)

    def bestmove_fen(self, fen, max_time, max_depth, is_savelines=False):
        self.set_fen_position(fen)
        return self.seek_bestmove(max_time, max_depth, is_savelines)

    def bestmove_infinite_depth(self, game, max_depth):
        self.set_game_position(game)
        mrm = self.seek_infinite(max_depth, None)
        self.put_line("stop")
        return mrm

    def bestmove_infinite(self, game, max_time):
        self.set_game_position(game)
        mrm = self.seek_infinite(None, max_time)
        self.put_line("stop")
        return mrm

    def bestmove_time(self, game, time_white, time_black, inc_time_move):
        self.set_game_position(game)
        return self.seek_bestmove_time(time_white, time_black, inc_time_move)

    def run_ponder(self, game, mrm):
        posInicial = "startpos" if game.siFenInicial() else "fen %s" % game.first_position.fen()
        li = [move.movimiento().lower() for move in game.li_moves]
        rm = mrm.rmBest()
        pv = rm.getPV()
        li1 = pv.split(" ")
        li.extend(li1[:2])
        moves = " moves %s" % (" ".join(li)) if li else ""
        if not li:
            self.ucinewgame()
        self.pondering = True
        self.work_ok("position %s%s" % (posInicial, moves))
        self.put_line("go ponder")

    def stop_ponder(self):
        self.work_ok("stop")
        self.pondering = False

    def busca_mate(self, game, mate):
        self.ac_inicio(game)
        tm = 10000
        li_r = []
        while tm > 0:
            tm -= 100
            time.sleep(0.1)
            mrm = self.ac_estado()
            li = mrm.bestmoves()
            if li:
                if 0 < li[0].mate <= mate:
                    li_r = li
                    break
        self.ac_final(-1)
        return li_r

    def play_with_return(self, play_return, game, line, max_time, max_depth):
        self.set_game_position(game)

        def dispatch():
            self.direct_dispatch = None
            self.mrm.ordena()
            play_return(self.mrm)

        self.reset()
        self.mrm.setTimeDepth(max_time, max_depth)

        self.direct_dispatch = dispatch
        self.working = True
        self.put_line(line)

    def play_bestmove_time(self, play_return, game, time_white, time_black, inc_time_move):
        env = "go wtime %d btime %d" % (time_white, time_black)
        if inc_time_move:
            env += " winc %d" % inc_time_move
        max_time = time_white if self.is_white else time_black
        self.play_with_return(play_return, game, env, max_time, None)

    def play_bestmove_game(self, play_return, game, max_time, max_depth):
        env = "go"
        if max_depth:
            env += " depth %d" % max_depth
        elif max_time:
            env += " movetime %d" % max_time
        self.play_with_return(play_return, game, env, max_time, max_depth)


class MaiaEngine(RunEngine):
    def __init__(self, name, exe, liOpcionesUCI=None, nMultiPV=0, priority=None, args=None):
        RunEngine.__init__(self, name, exe, liOpcionesUCI, nMultiPV, priority, args)
        self.stopping = False

        level = int(name[5:])
        book_name = "1100-1500.bin" if level <= 1500 else "1600-1900.bin"
        book_path = os.path.join(os.path.dirname(exe), book_name)
        self.book = Books.Book("P", book_name, book_path, True)
        self.book.polyglot()
        self.book_select = []
        mp = (level-1100)//10
        ap = 40 - 20*(level-1100)//800
        au = 100 - mp - ap
        self.book_select.extend(["mp"]*mp)
        self.book_select.extend(["ap"]*ap)
        self.book_select.extend(["au"]*au)
        # random.shuffle(self.book_select)

        # for lv in range(1100, 2000, 100):
        #     self.book_select = {}
        #     self.book_select["mp"] = (lv - 1100) // 10
        #     self.book_select["ap"] = 40 - 20 * (lv - 1100) // 800
        #     self.book_select["au"] = 100 - self.book_select["mp"] - self.book_select["ap"]
        #     prin t(lv, self.book_select)
        #
    def simulate_time(self, ms_time):
        tini = time.time()
        while not (self.stopping or (time.time()-tini)*1000 > ms_time):
            QtCore.QCoreApplication.processEvents()
            time.sleep(0.1)
        self.stopping = False

    def seek_bestmove(self, max_time, max_depth, is_savelines):
        tini = time.time()
        self.stopping = False
        env = "go nodes 1"
        ms_time = 10000
        if max_time:
            ms_time = max_time + 3000
        elif max_depth:
            ms_time = int(max_depth * ms_time / 3.0)

        self.reset()
        if is_savelines:
            self.mrm.save_lines()
        self.mrm.setTimeDepth(max_time, max_depth)

        self.work_bestmove(env, ms_time)
        if max_time:
            self.simulate_time(max_time-(time.time()-tini)*1000)

        self.mrm.ordena()

        return self.mrm

    def seek_bestmove_time(self, time_white, time_black, inc_time_move):
        tini = time.time()
        self.stopping = False
        env = "go nodes 1"
        max_time = time_white if self.is_white else time_black

        self.reset()
        self.mrm.setTimeDepth(max_time, None)

        self.work_bestmove(env, max_time)

        if time_white > 60000 and time_black > 60000:
            self.simulate_time(min(time_white/40, random.randint(1000, 15000))-(time.time()-tini)*1000)

        self.mrm.ordena()
        return self.mrm

    def play_bestmove_time(self, play_return, game, time_white, time_black, inc_time_move):
        self.stopping = False
        env = "go nodes 1"
        max_time = time_white if self.is_white else time_black
        if time_white > 60000 and time_black > 60000:
            time_simulate = min(time_white/40, random.randint(1000, 15000))
        else:
            time_simulate = 0
        self.play_with_return_maia(play_return, game, env, max_time, None, time_simulate)

    def play_bestmove_game(self, play_return, game, max_time, max_depth):
        self.stopping = False
        env = "go nodes 1"
        time_simulate = max_time
        self.play_with_return_maia(play_return, game, env, max_time, max_depth, time_simulate)

    def play_with_return_maia(self, play_return, game, line, max_time, max_depth, time_simulate):
        self.reset()
        if self.test_book(game):
            time_simulate /= 3
        else:
            self.mrm.setTimeDepth(max_time, max_depth)
            self.set_game_position(game)
            self.work_bestmove(line, 5000)
            self.mrm.ordena()
        self.simulate_time(time_simulate)
        play_return(self.mrm)

    def put_line_debug(self, line: str):
        if line == "stop":
            self.stopping = True
        RunEngine.put_line_debug(self, line)

    def put_line_base(self, line: str):
        if line == "stop":
            self.stopping = True
        RunEngine.put_line_base(self, line)

    def test_book(self, game):
        if len(game) < 30:
            pv = self.book.eligeJugadaTipo(game.last_position.fen(), random.choice(self.book_select))
            if pv:
                self.mrm.dispatch("bestmove %s" %pv)
                self.mrm.ordena()
                return True
        return False
