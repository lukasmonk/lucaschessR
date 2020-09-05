import os

import FasterCode

import Code
from Code.Engines import Priorities, EngineResponse, EngineRunDirect, EngineRun
from Code.Base.Constantes import ADJUST_SELECTED_BY_PLAYER


class ListEngineManagers:
    def __init__(self):
        self.lista = []

    def append(self, engine_manager):
        self.lista.append(engine_manager)

    def listaActivos(self):
        return [engine_manager for engine_manager in self.lista if engine_manager.activo]

    def close_all(self):
        for engine_manager in self.lista:
            engine_manager.terminar()


class EngineManager:
    def __init__(self, procesador, confMotor, direct=False):
        self.procesador = procesador

        self.engine = None
        self.confMotor = confMotor
        self.name = confMotor.name
        self.key = confMotor.key
        self.nMultiPV = 0

        self.priority = Priorities.priorities.normal

        self.dispatching = None

        self.activo = True  # No es suficiente con engine == None para saber si esta activo y se puede logear

        self.ficheroLog = None

        self.direct = direct
        Code.list_engine_managers.append(self)
        if Code.configuration.x_log_engines:
            self.log_open()

    def set_direct(self):
        self.direct = True

    def opciones(self, tiempoJugada, profundidad, siMultiPV):
        self.motorTiempoJugada = tiempoJugada
        self.motorProfundidad = profundidad
        self.nMultiPV = self.confMotor.multiPV if siMultiPV else 0

        self.siInfinito = self.key == "tarrasch"

        if self.key in ("daydreamer", "cinnamon") and profundidad and profundidad == 1:
            self.motorProfundidad = 2

    def log_open(self):
        carpeta = os.path.join(Code.configuration.carpeta, "EngineLogs")
        if not os.path.isdir(carpeta):
            os.mkdir(carpeta)
        plantlog = "%s_%%05d" % os.path.join(carpeta, self.name)
        pos = 1
        nomlog = plantlog % pos

        while os.path.isfile(nomlog):
            pos += 1
            nomlog = plantlog % pos
        self.ficheroLog = nomlog
        if self.engine:
            self.engine.log_open(nomlog)

    def log_close(self):
        self.ficheroLog = None
        if self.engine:
            self.engine.log_close()

    def cambiaOpciones(self, tiempoJugada, profundidad):
        self.motorTiempoJugada = tiempoJugada
        self.motorProfundidad = profundidad

    def setPriority(self, priority):
        self.priority = priority if priority else Priorities.priorities.normal

    def maximizaMultiPV(self):
        self.nMultiPV = 9999

    def ponGuiDispatch(self, rutina, whoDispatch=None):
        if self.engine:
            self.engine.ponGuiDispatch(rutina, whoDispatch)
        else:
            self.dispatching = rutina, whoDispatch

    def actMultiPV(self, xMultiPV):
        self.confMotor.actMultiPV(xMultiPV)
        self.testEngine()
        self.engine.ponMultiPV(self.confMotor.multiPV)

    def anulaMultiPV(self):
        self.nMultiPV = 0

    def setMultiPV(self, nMultiPV):
        self.nMultiPV = nMultiPV

    def remove_gui_dispatch(self):
        if self.engine:
            self.engine.gui_dispatch = None

    def testEngine(self, nMultiPV=0):
        if self.engine:
            return
        if self.nMultiPV:
            self.nMultiPV = min(self.nMultiPV, self.confMotor.maxMultiPV)

        exe = self.confMotor.ejecutable()
        args = self.confMotor.argumentos()
        liUCI = self.confMotor.liUCI
        if self.direct:
            self.engine = EngineRunDirect.DirectEngine(
                self.name, exe, liUCI, self.nMultiPV, priority=self.priority, args=args
            )
        else:
            # self.engine = RunEngine.RunEngine(self.name, exe, liUCI, self.nMultiPV, priority=self.priority, args=args)
            self.engine = EngineRun.RunEngine(self.name, exe, liUCI, self.nMultiPV, priority=self.priority, args=args)

        if self.confMotor.siDebug:
            self.engine.siDebug = True
            self.engine.nomDebug = self.confMotor.nomDebug
        if self.dispatching:
            rutina, whoDispatch = self.dispatching
            self.engine.ponGuiDispatch(rutina, whoDispatch)
        if self.ficheroLog:
            self.engine.log_open(self.ficheroLog)

    def juegaSegundos(self, segundos):
        self.testEngine()
        game = self.procesador.manager.game
        if self.siInfinito:  # problema tarrasch
            mrm = self.engine.bestmove_infinite(game, segundos * 1000)
        else:
            mrm = self.engine.bestmove_game(game, segundos * 1000, None)
        return mrm.mejorMov() if mrm else None

    def juega(self, nAjustado=0):
        return self.juegaPartida(self.procesador.manager.game, nAjustado)

    def juegaPartida(self, game, nAjustado=0):
        self.testEngine()

        if self.siInfinito:  # problema tarrasch
            if self.motorProfundidad:
                mrm = self.engine.bestmove_infinite_depth(game, self.motorProfundidad)
            else:
                mrm = self.engine.bestmove_infinite(game, self.motorTiempoJugada)

        else:
            mrm = self.engine.bestmove_game(game, self.motorTiempoJugada, self.motorProfundidad)

        if nAjustado:
            mrm.game = game
            if nAjustado >= 1000:
                mrm.liPersonalidades = self.procesador.configuration.liPersonalidades
                mrm.fenBase = game.last_position.fen()
            return mrm.mejorMovAjustado(nAjustado) if nAjustado != ADJUST_SELECTED_BY_PLAYER else mrm
        else:
            return mrm.mejorMov()

    def juegaTiempo(self, tiempoBlancas, tiempoNegras, tiempoJugada, nAjustado=0):
        self.testEngine()
        if self.motorTiempoJugada or self.motorProfundidad:
            return self.juega(nAjustado)
        tiempoBlancas = int(tiempoBlancas * 1000)
        tiempoNegras = int(tiempoNegras * 1000)
        tiempoJugada = int(tiempoJugada * 1000)
        game = self.procesador.manager.game
        mrm = self.engine.bestmove_time(game, tiempoBlancas, tiempoNegras, tiempoJugada)
        if mrm is None:
            return None

        if nAjustado:
            mrm.game = game
            if nAjustado >= 1000:
                mrm.liPersonalidades = self.procesador.configuration.liPersonalidades
                mrm.fenBase = game.last_position.fen()
            return mrm.mejorMovAjustado(nAjustado) if nAjustado != ADJUST_SELECTED_BY_PLAYER else mrm
        else:
            return mrm.mejorMov()

    def juegaTiempoTorneo(self, game, tiempoBlancas, tiempoNegras, tiempoJugada):
        self.testEngine()
        if self.engine.pondering:
            self.engine.stop_ponder()
        if self.motorTiempoJugada or self.motorProfundidad:
            mrm = self.engine.bestmove_game(game, self.motorTiempoJugada, self.motorProfundidad)
        else:
            tiempoBlancas = int(tiempoBlancas * 1000)
            tiempoNegras = int(tiempoNegras * 1000)
            tiempoJugada = int(tiempoJugada * 1000)
            mrm = self.engine.bestmove_time(game, tiempoBlancas, tiempoNegras, tiempoJugada)
        if self.engine and self.engine.ponder:  # test si self.engine, ya que puede haber terminado en el ponder
            self.engine.run_ponder(game, mrm)
        return mrm

    def analiza(self, fen):
        self.testEngine()
        return self.engine.bestmove_fen(fen, self.motorTiempoJugada, self.motorProfundidad)

    def valora(self, position, from_sq, to_sq, promotion):
        self.testEngine()

        posicionNueva = position.copia()
        posicionNueva.mover(from_sq, to_sq, promotion)

        fen = posicionNueva.fen()
        if FasterCode.fen_ended(fen):
            rm = EngineResponse.EngineResponse("", position.is_white)
            rm.sinInicializar = False
            self.sinMovimientos = True
            self.pv = from_sq + to_sq + promotion
            self.from_sq = from_sq
            self.to_sq = to_sq
            self.promotion = promotion
            return rm

        mrm = self.engine.bestmove_fen(fen, self.motorTiempoJugada, self.motorProfundidad)
        rm = mrm.mejorMov()
        rm.cambiaColor(position)
        mv = from_sq + to_sq + (promotion if promotion else "")
        rm.pv = mv + " " + rm.pv
        rm.from_sq = from_sq
        rm.to_sq = to_sq
        rm.promotion = promotion if promotion else ""
        rm.is_white = position.is_white
        return rm

    def control(self, fen, profundidad):
        self.testEngine()
        return self.engine.bestmove_fen(fen, 0, profundidad)

    def terminar(self):
        if self.engine:
            self.engine.close()
            self.engine = None
            self.activo = False

    def analyse_move(self, move, vtime, depth=0, brDepth=5, brPuntos=50):
        self.testEngine()

        mrm = self.engine.bestmove_fen(move.position_before.fen(), vtime, depth, is_savelines=True)
        mv = move.movimiento()
        if not mv:
            return mrm, 0
        rm, n = mrm.buscaRM(move.movimiento())
        if rm:
            if n == 0:
                mrm.miraBrilliancies(brDepth, brPuntos)
            return mrm, n

        # No esta considerado, obliga a hacer el analysis de nuevo from_sq position
        if move.is_mate or move.is_draw:
            rm = EngineResponse.EngineResponse(self.name, move.position_before.is_white)
            rm.from_sq = mv[:2]
            rm.to_sq = mv[2:4]
            rm.promotion = mv[4] if len(mv) == 5 else ""
            rm.pv = mv
        else:
            position = move.position

            mrm1 = self.engine.bestmove_fen(position.fen(), vtime, depth)
            if mrm1 and mrm1.li_rm:
                rm = mrm1.li_rm[0]
                rm.cambiaColor(position)
                rm.pv = mv + " " + rm.pv
            else:
                rm = EngineResponse.EngineResponse(self.name, mrm1.is_white)
                rm.pv = mv
            rm.from_sq = mv[:2]
            rm.to_sq = mv[2:4]
            rm.promotion = mv[4] if len(mv) == 5 else ""
            rm.is_white = move.position_before.is_white
        pos = mrm.agregaRM(rm)

        return mrm, pos

    def analizaJugadaPartida(
        self,
        game,
        njg,
        vtime,
        depth=0,
        brDepth=5,
        brPuntos=50,
        stability=False,
        st_centipawns=0,
        st_depths=0,
        st_timelimit=0,
    ):
        self.testEngine()

        if stability:
            mrm = self.engine.analysis_stable(game, njg, vtime, depth, True, st_centipawns, st_depths, st_timelimit)
        else:
            mrm = self.engine.bestmove_game_jg(game, njg, vtime, depth, is_savelines=True)

        move = game.move(njg)
        mv = move.movimiento()
        if not mv:
            return mrm, 0
        rm, n = mrm.buscaRM(mv)
        if rm:
            if n == 0:
                mrm.miraBrilliancies(brDepth, brPuntos)
            return mrm, n

        # No esta considerado, obliga a hacer el analysis de nuevo from_sq position
        if game.is_finished():
            rm = EngineResponse.EngineResponse(self.name, move.position_before.is_white)
            rm.from_sq = mv[:2]
            rm.to_sq = mv[2:4]
            rm.promotion = mv[4] if len(mv) == 5 else ""
            rm.pv = mv
        else:
            position = move.position

            mrm1 = self.engine.bestmove_fen(position.fen(), vtime, depth)
            if mrm1 and mrm1.li_rm:
                rm = mrm1.li_rm[0]
                rm.cambiaColor(position)
                rm.pv = mv + " " + rm.pv
            else:
                rm = EngineResponse.EngineResponse(self.name, mrm1.is_white)
                rm.pv = mv
            rm.from_sq = mv[:2]
            rm.to_sq = mv[2:4]
            rm.promotion = mv[4] if len(mv) == 5 else ""
            rm.is_white = move.position_before.is_white
        pos = mrm.agregaRM(rm)

        return mrm, pos

    def analizaVariation(self, move, vtime, is_white):
        self.testEngine()

        mrm = self.engine.bestmove_fen(move.position.fen(), vtime, None)
        if mrm.li_rm:
            rm = mrm.li_rm[0]
            # if is_white != move.position.is_white:
            #     if rm.mate:
            #         rm.mate += +1 if rm.mate > 0 else -1
        else:
            rm = EngineResponse.EngineResponse("", is_white)
        return rm

    def ac_inicio(self, game):
        self.testEngine()
        self.engine.ac_inicio(game)

    def ac_minimo(self, minTiempo, lockAC):
        self.testEngine()
        return self.engine.ac_minimo(minTiempo, lockAC)

    def ac_minimoTD(self, minTiempo, minDepth, lockAC):
        self.testEngine()
        return self.engine.ac_minimoTD(minTiempo, minDepth, lockAC)

    def ac_estado(self):
        self.testEngine()
        return self.engine.ac_estado()

    def ac_final(self, minTiempo):
        self.testEngine()
        return self.engine.ac_final(minTiempo)

    def set_option(self, name, value):
        self.testEngine()
        self.engine.set_option(name, value)

    def miraListaPV(self, fen, siUna):  #
        """Servicio para Opening lines-importar polyglot-generador de movimientos-emula un book polyglot"""
        mrm = self.analiza(fen)
        lipv = [rm.movimiento() for rm in mrm.li_rm]
        return lipv[0] if siUna else lipv

    def busca_mate(self, game, mate):
        self.testEngine()
        return self.engine.busca_mate(game, mate)

    def stop(self):
        self.engine.put_line("stop")

    def current_rm(self):
        if not self.engine:
            return None
        mrm = self.engine.mrm
        if mrm is None:
            return None
        mrm.ordena()
        return mrm.mejorMov()

    def play_time(self, routine_return, tiempoBlancas, tiempoNegras, tiempoJugada, nAjustado=0):
        self.testEngine()
        game = self.procesador.manager.game

        def play_return(mrm):
            self.engine.gui_dispatch = None
            if mrm is None:
                resp = None
            elif nAjustado:
                mrm.ordena()
                mrm.game = game
                if nAjustado >= 1000:
                    mrm.liPersonalidades = self.procesador.configuration.liPersonalidades
                    mrm.fenBase = game.last_position.fen()
                resp = mrm.mejorMovAjustado(nAjustado) if nAjustado != ADJUST_SELECTED_BY_PLAYER else mrm
            else:
                resp = mrm.mejorMov()
            routine_return(resp)

        # mrm = self.engine.bestmove_game(game, 0, 5)
        # play_return(mrm)
        # return
        if self.motorTiempoJugada or self.motorProfundidad:
            if self.siInfinito:  # problema tarrasch
                if self.motorProfundidad:
                    mrm = self.engine.bestmove_infinite_depth(game, self.motorProfundidad)
                else:
                    mrm = self.engine.bestmove_infinite(game, self.motorTiempoJugada)
                play_return(mrm)
            else:
                self.engine.play_bestmove_game(play_return, game, self.motorTiempoJugada, self.motorProfundidad)

        else:
            tiempoBlancas = int(tiempoBlancas * 1000)
            tiempoNegras = int(tiempoNegras * 1000)
            tiempoJugada = int(tiempoJugada * 1000)
            self.engine.play_bestmove_time(play_return, game, tiempoBlancas, tiempoNegras, tiempoJugada)
