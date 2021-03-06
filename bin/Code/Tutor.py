import os

import FasterCode

from Code.Analysis import Analysis
from Code.Base import Game
from Code.QT import WindowTutor
from Code.QT import QTUtil2
from Code import Util


class Tutor:
    def __init__(self, manager, move, from_sq, to_sq, siEntrenando):
        self.manager = manager

        self.difpts = manager.configuration.x_tutor_difpoints
        self.difporc = manager.configuration.x_tutor_difporc

        self.game = manager.game

        self.main_window = manager.main_window
        self.managerTutor = manager.xtutor
        self.last_position = self.game.last_position
        self.move = move
        self.from_sq = from_sq
        self.to_sq = to_sq
        self.mrmTutor = manager.mrmTutor
        self.rm_rival = manager.rm_rival
        self.is_white = manager.human_side
        self.siEntrenando = siEntrenando
        self.list_rm = None  # necesario

        self.x_save_csv = manager.configuration.x_save_csv

        self.is_moving_time = False

    def elegir(self, siPuntos, liApPosibles=None):

        self.rmUsuario, posUsuario = self.mrmTutor.buscaRM(self.move.movimiento())
        if self.rmUsuario is None:
            # Elegimos si la opcion del tutor es mejor que la del usuario
            # Ponemos un mensaje mientras piensa
            me = QTUtil2.mensEspera.start(self.main_window, _("Analyzing the move...."), physical_pos="ad")

            fen = self.move.position.fen()
            mrmUsuario = self.managerTutor.analiza(fen)
            if len(mrmUsuario.li_rm) == 0:
                self.rmUsuario = self.mrmTutor.li_rm[0].copia()
                self.rmUsuario.from_sq = self.move.from_sq
                self.rmUsuario.to_sq = self.move.to_sq
                self.rmUsuario.promotion = self.move.promotion
                self.rmUsuario.mate = 0
                self.rmUsuario.puntos = 0
            else:
                self.rmUsuario = mrmUsuario.li_rm[0]
                self.rmUsuario.cambiaColor(self.move.position)

            me.final()

        # Estadisticas
        if self.x_save_csv:
            self.guardaEstadisticas()

        # Comparamos la puntuacion del usuario con la del tutor
        if not self.mrmTutor.mejorRMQue(self.rmUsuario, self.difpts, self.difporc):
            return False

        # Creamos la lista de movimientos analizados por el tutor
        self.list_rm = self.do_lirm(posUsuario)  # rm,name

        # Creamos la ventana

        siRival = self.rm_rival and " " in self.rm_rival.getPV()

        self.liApPosibles = liApPosibles
        in_the_opening = not (liApPosibles is None)
        if in_the_opening:
            siRival = False

        self.w = w = WindowTutor.WindowTutor(self.manager, self, siRival, in_the_opening, self.is_white, siPuntos)

        self.cambiadoRM(0)

        self.gameUsuario = Game.Game(self.move.position)
        self.gameUsuario.add_move(self.move)
        self.gameUsuario.read_pv(self.rmUsuario.getPV())
        self.posUsuario = 0
        self.maxUsuario = len(self.gameUsuario.li_moves)
        self.boardUsuario.set_position(self.move.position)
        w.ponPuntuacionUsuario(self.rmUsuario.texto())

        if siRival:
            self.rm_rival.cambiaColor()
            pvBloque = self.rm_rival.getPV()
            n = pvBloque.find(" ")
            if n > 0:
                pvBloque = pvBloque[n + 1 :].strip()
            else:
                pvBloque = ""

            if pvBloque:
                self.gameRival = Game.Game(self.last_position)
                self.gameRival.read_pv(pvBloque)
                self.posRival = 0
                self.maxRival = len(self.gameRival.li_moves) - 1
                if self.maxRival >= 0:
                    self.boardRival.set_position(self.gameRival.li_moves[0].position)
                    self.play_rival(True)
                    w.ponPuntuacionRival(self.rm_rival.texto())

        self.moving_tutor(True)
        self.moving_user(True)

        if w.exec_():
            if w.siElegidaOpening:
                from_sq = self.gameOpenings.move(0).from_sq
                to_sq = self.gameOpenings.move(0).to_sq
                if from_sq == self.from_sq and to_sq == self.to_sq:
                    return False
                self.from_sq = from_sq
                self.to_sq = to_sq
                self.promotion = ""
            elif w.respLibro:
                self.from_sq, self.to_sq, self.promotion = w.respLibro
            else:
                rm = self.list_rm[self.pos_rm][0]
                self.from_sq = rm.from_sq
                self.to_sq = rm.to_sq
                self.promotion = rm.promotion
            return True
        return False

    def ponVariations(self, move, numJugada):
        if self.list_rm:
            rm, name = self.list_rm[0]
            game = Game.Game(self.move.position_before)
            game.read_pv(rm.getPV())

            jgvar = game.move(0)
            jgvar.comment = rm.texto()

            move.add_variation(game)

            txt = self.gameUsuario.pgnBaseRAW(numJugada)
            puntos = self.rmUsuario.texto()
            vusu = "%s : %s" % (puntos, txt)
            move.comment = vusu.replace("\n", "")

    def do_lirm(self, posUsuario):
        li = []
        pb = self.move.position_before

        for n, rm in enumerate(self.mrmTutor.li_rm):
            if n != posUsuario:
                pv1 = rm.getPV().split(" ")[0]
                from_sq = pv1[:2]
                to_sq = pv1[2:4]
                promotion = pv1[4] if len(pv1) == 5 else ""
                name = pb.pgn_translated(from_sq, to_sq, promotion)
                name += " " + rm.abrTexto()

                li.append((rm, name))
        return li

    def cambiadoRM(self, pos):
        self.pos_rm = pos
        rm = self.list_rm[pos][0]
        self.game_tutor = Game.Game(self.last_position)
        self.game_tutor.read_pv(rm.getPV())

        self.w.ponPuntuacionTutor(rm.texto())

        self.pos_tutor = 0
        self.max_tutor = len(self.game_tutor)
        self.moving_tutor(True)

    def mueve(self, quien, que):

        funcion = eval("self.moving_" + quien)

        if que == "Adelante":
            funcion(nSaltar=1)
        elif que == "Atras":
            funcion(nSaltar=-1)
        elif que == "Inicio":
            funcion(is_base=True)
        elif que == "Final":
            funcion(siFinal=True)
        elif que == "Libre":
            self.analiza(quien)
        elif que == "Tiempo":
            tb = eval("self.w.tb" + quien)
            posMax = eval("self.max" + quien)
            self.move_timed(funcion, tb, posMax)

    def move_timed(self, funcion, tb, posMax):
        if self.is_moving_time:
            self.is_moving_time = False
            self.time_others_tb(True)
            self.w.stop_clock()
            return

        def otrosTB(siHabilitar):
            for accion in tb.li_acciones:
                if not accion.key.endswith("MoverTiempo"):
                    accion.setEnabled(siHabilitar)

        self.time_function = funcion
        self.time_pos_max = posMax
        self.time_pos = -1
        self.time_others_tb = otrosTB
        self.is_moving_time = True
        otrosTB(False)
        funcion(is_base=True)
        self.w.start_clock(self.moving_time_1)

    def moving_time_1(self):
        self.time_pos += 1
        if self.time_pos == self.time_pos_max:
            self.is_moving_time = False
            self.time_others_tb(True)
            self.w.stop_clock()
            return
        if self.time_pos == 0:
            self.time_function(siInicio=True)
        else:
            self.time_function(nSaltar=1)

    def moving_user(self, siInicio=False, nSaltar=0, siFinal=False, is_base=False):
        if nSaltar:
            pos = self.posUsuario + nSaltar
            if 0 <= pos < self.maxUsuario:
                self.posUsuario = pos
            else:
                return
        elif siInicio:
            self.posUsuario = 0
        elif is_base:
            self.posUsuario = -1
        else:
            self.posUsuario = self.maxUsuario - 1

        move = self.gameUsuario.move(self.posUsuario if self.posUsuario > -1 else 0)
        if is_base:
            self.boardUsuario.set_position(move.position_before)
        else:
            self.boardUsuario.set_position(move.position)
            self.boardUsuario.put_arrow_sc(move.from_sq, move.to_sq)

    def moving_tutor(self, siInicio=False, nSaltar=0, siFinal=False, is_base=False):
        if nSaltar:
            pos = self.pos_tutor + nSaltar
            if 0 <= pos < self.max_tutor:
                self.pos_tutor = pos
            else:
                return
        elif siInicio:
            self.pos_tutor = 0
        elif is_base:
            self.pos_tutor = -1
        else:
            self.pos_tutor = self.max_tutor - 1

        move = self.game_tutor.move(self.pos_tutor if self.pos_tutor > -1 else 0)
        if is_base:
            self.boardTutor.set_position(move.position_before)
        else:
            self.boardTutor.set_position(move.position)
            self.boardTutor.put_arrow_sc(move.from_sq, move.to_sq)

    def play_rival(self, siInicio=False, nSaltar=0, siFinal=False, is_base=False):
        if nSaltar:
            pos = self.posRival + nSaltar
            if 0 <= pos < self.maxRival:
                self.posRival = pos
            else:
                return
        elif siInicio:
            self.posRival = 0
        elif is_base:
            self.posRival = -1
        else:
            self.posRival = self.maxRival - 1

        move = self.gameRival.move(self.posRival if self.posRival > -1 else 0)
        if is_base:
            self.boardRival.set_position(move.position_before)
        else:
            self.boardRival.set_position(move.position)
            self.boardRival.put_arrow_sc(move.from_sq, move.to_sq)

    def mueveOpening(self, siInicio=False, nSaltar=0, siFinal=False, is_base=False):
        if nSaltar:
            pos = self.posOpening + nSaltar
            if 0 <= pos < self.maxOpening:
                self.posOpening = pos
            else:
                return
        elif siInicio:
            self.posOpening = 0
        elif is_base:
            self.posOpening = -1
        else:
            self.posOpening = self.maxOpening - 1

        move = self.gameOpenings.move(self.posOpening if self.posOpening > -1 else 0)
        if is_base:
            self.boardOpenings.set_position(move.position_before)
        else:
            self.boardOpenings.set_position(move.position)
            self.boardOpenings.put_arrow_sc(move.from_sq, move.to_sq)

    def ponBoardsGUI(self, boardTutor, boardUsuario, boardRival, boardOpenings):
        self.boardTutor = boardTutor
        self.boardTutor.exePulsadoNum = self.exePulsadoNumTutor
        self.boardUsuario = boardUsuario
        self.boardUsuario.exePulsadoNum = self.exePulsadoNumUsuario
        self.boardRival = boardRival
        self.boardOpenings = boardOpenings

    def cambiarOpening(self, number):
        self.gameOpenings = Game.Game(self.last_position)
        self.gameOpenings.read_pv(self.liApPosibles[number].a1h8)
        self.boardOpenings.set_position(self.gameOpenings.move(0).position)
        self.maxOpening = len(self.gameOpenings)
        self.mueveOpening(siInicio=True)

    def opcionesOpenings(self):
        return [(ap.trNombre, num) for num, ap in enumerate(self.liApPosibles)]

    def analiza(self, quien):
        if quien == "Tutor":
            rmTutor = self.list_rm[self.pos_rm][0]
            move = self.game_tutor.move(self.pos_tutor)
            pts = rmTutor.texto()
        else:
            move = self.gameUsuario.move(self.posUsuario)
            pts = self.rmUsuario.texto()

        Analysis.AnalisisVariations(self.w, self.manager.xtutor, move, self.is_white, pts)

    def exePulsadoNumTutor(self, siActivar, number):
        if number in [1, 8]:
            if siActivar:
                # Que move esta en el board
                move = self.game_tutor.move(self.pos_tutor if self.pos_tutor > -1 else 0)
                if self.pos_tutor == -1:
                    fen = move.position_before.fen()
                else:
                    fen = move.position.fen()
                is_white = " w " in fen
                if is_white:
                    siMB = number == 1
                else:
                    siMB = number == 8
                self.boardTutor.remove_arrows()
                if self.boardTutor.flechaSC:
                    self.boardTutor.flechaSC.hide()
                li = FasterCode.get_captures(fen, siMB)
                for m in li:
                    d = m.from_sq()
                    h = m.to_sq()
                    self.boardTutor.creaFlechaMov(d, h, "c")
            else:
                self.boardTutor.remove_arrows()
                if self.boardTutor.flechaSC:
                    self.boardTutor.flechaSC.show()

    def exePulsadoNumUsuario(self, siActivar, number):
        if number in [1, 8]:
            if siActivar:
                # Que move esta en el board
                move = self.gameUsuario.move(self.posUsuario if self.posUsuario > -1 else 0)
                if self.posUsuario == -1:
                    fen = move.position_before.fen()
                else:
                    fen = move.position.fen()
                is_white = " w " in fen
                if is_white:
                    siMB = number == 1
                else:
                    siMB = number == 8
                self.boardUsuario.remove_arrows()
                if self.boardUsuario.flechaSC:
                    self.boardUsuario.flechaSC.hide()
                li = FasterCode.get_captures(fen, siMB)
                for m in li:
                    d = m.from_sq()
                    h = m.to_sq()
                    self.boardUsuario.creaFlechaMov(d, h, "c")
            else:
                self.boardUsuario.remove_arrows()
                if self.boardUsuario.flechaSC:
                    self.boardUsuario.flechaSC.show()

    def guardaEstadisticas(self):
        date = str(Util.today())
        li = date.split(" ")
        fecha = li[0]
        hora = li[1].split(".")[0]
        fen = self.move.position.fen()
        rmTutor = self.mrmTutor.li_rm[0]
        suggested_move = rmTutor.from_sq + rmTutor.to_sq + rmTutor.promotion
        suggested_move_puntos = rmTutor.puntos
        suggested_move_mate = rmTutor.mate
        player_move = self.rmUsuario.from_sq + self.rmUsuario.to_sq + self.rmUsuario.promotion
        player_move_puntos = self.rmUsuario.puntos
        player_move_mate = self.rmUsuario.mate
        tutor = self.managerTutor.name.replace('"', "").replace(";", "")
        tutor_tiempo = self.managerTutor.motorTiempoJugada

        try:
            if not os.path.isfile(self.x_save_csv):
                f = open(self.x_save_csv, "wt", encoding="utf-8", errors="ignore")
                ntutor = _("Tutor").replace('"', "").replace(";", "")
                player = _("Player").replace('"', "").replace(";", "")
                puntos = _("points")
                mate = _("Mate").lower()
                txt = '"%s";"%s";"FEN";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (
                    _("Date"),
                    _("Time"),
                    ntutor,
                    ntutor + "-" + puntos,
                    ntutor + "-" + mate,
                    player,
                    player + "-" + puntos,
                    player + "-" + mate,
                    ntutor + "-" + _("Engine"),
                    _("Time engine MS"),
                )
                f.write(txt)
            else:
                f = open(self.x_save_csv, "at", encoding="utf-8", errors="ignore")

            f.write(
                '%s;%s;"%s";"%s";%d;%d;"%s";%d;%d;"%s";%d\n'
                % (
                    fecha,
                    hora,
                    fen,
                    suggested_move,
                    suggested_move_puntos,
                    suggested_move_mate,
                    player_move,
                    player_move_puntos,
                    player_move_mate,
                    tutor,
                    tutor_tiempo,
                )
            )
            f.close()
        except:
            pass
