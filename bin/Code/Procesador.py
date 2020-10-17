import os
import random
import sys
import webbrowser

import Code
from Code import Util
from Code import Routes
from Code import Update
from Code.Engines import EngineManager, WEngines
from Code.PlayAgainstEngine import ManagerPlayAgainstEngine, PlayAgainstEngine
from Code.Base.Constantes import *
from Code import Albums
from Code import CPU
from Code.Config import Configuration, WindowConfig

# Added by GON
from Code import DGT
# ------------

from Code.Base import Position
from Code import Trainings
from Code import ManagerAlbum
from Code.GM import ManagerGM
from Code import ManagerElo
from Code import ManagerEntPos
from Code import ManagerEverest
from Code import ManagerFideFics
from Code import ManagerMateMap
from Code import ManagerMicElo
from Code import ManagerCompeticion
from Code import ManagerOpeningLines
from Code import ManagerPerson
from Code import ManagerRoutes
from Code import ManagerSingularM
from Code import ManagerSolo
from Code import ManagerPartida
from Code import Presentacion
from Code import ManagerWashing
from Code import ManagerPlayGame
from Code import ManagerAnotar
from Code import Adjourns
from Code.QT import WCompetitionWithTutor, BasicMenus
from Code.QT import Iconos
from Code.QT import About
from Code.MainWindow import MainWindow
from Code.QT import WindowAlbumes
from Code.QT import WindowAnotar
from Code.Openings import WindowOpenings, WindowOpeningLine, WindowOpeningLines, OpeningLines, OpeningsStd
from Code.QT import WindowBMT
from Code.QT import WindowColores
from Code.QT import WindowEverest
from Code.QT import WindowRoutes
from Code.QT import WindowSTS
from Code.Sound import WindowSonido
from Code.QT import WindowSingularM
from Code.QT import WindowUsuarios
from Code.QT import WindowWashing
from Code.QT import WindowWorkMap
from Code.QT import WindowPlayGame
from Code.QT import Piezas
from Code.QT import QTUtil
from Code.QT import QTUtil2
from Code.QT import QTVarios
from Code.Databases import WindowDatabase, WDB_Games, DBgames
from Code.QT import WindowManualSave
from Code.Kibitzers import KibitzersManager
from Code.Tournaments import WTournaments
from Code.Polyglots import WFactory
from Code.Polyglots import WPolyglot
from Code.Endings import WEndingsGTB


class Procesador:
    user = None
    li_opciones_inicio = None
    configuration = None
    manager = None
    version = None

    def __init__(self):
        if Code.list_engine_managers is None:
            Code.list_engine_managers = EngineManager.ListEngineManagers()

        self.web = "https://lucaschess.pythonanywhere.com"
        self.blog = "https://lucaschess.blogspot.com"
        self.github = "https://github.com/lukasmonk/lucaschessR"

    def start_with_user(self, user):
        self.user = user

        self.li_opciones_inicio = [
            TB_QUIT,
            TB_PLAY,
            TB_TRAIN,
            TB_COMPETE,
            TB_TOOLS,
            TB_OPTIONS,
            TB_INFORMATION,
        ]  # Lo incluimos aqui porque sino no lo lee, en caso de aplazada

        self.configuration = Configuration.Configuration(user)
        self.configuration.start()
        Code.configuration = self.configuration
        Code.procesador = self
        OpeningsStd.reset()

        # Tras crear configuración miramos si hay adjourns
        self.test_opcion_adjourns()

        Code.todasPiezas = Piezas.TodasPiezas()

        self.manager = None

        self.siPrimeraVez = True
        self.siPresentacion = False  # si esta funcionando la presentacion

        self.posicionInicial = Position.Position()
        self.posicionInicial.set_pos_initial()

        self.xrival = None
        self.xtutor = None  # creaTutor lo usa asi que hay que definirlo antes
        self.xanalyzer = None   # cuando se juega ManagerEntMaq y el tutor danzando a toda maquina,
                                # se necesita otro diferente
        self.replay = None
        self.replayBeep = None

    def test_opcion_adjourns(self):
        must_adjourn = len(Adjourns.Adjourns()) > 0
        if TB_ADJOURNS in self.li_opciones_inicio:
            if not must_adjourn:
                pos = self.li_opciones_inicio.index(TB_ADJOURNS)
                del self.li_opciones_inicio[pos]
        else:
            if must_adjourn:
                self.li_opciones_inicio.insert(1, TB_ADJOURNS)

    def set_version(self, version):
        self.version = version

    def iniciar_gui(self):
        if len(sys.argv) > 1:
            comando = sys.argv[1]
            if comando.lower().endswith(".pgn"):
                self.main_window = None
                self.read_pgn(comando)
                return

        self.main_window = MainWindow.MainWindow(self)
        self.main_window.set_manager_active(self)  # antes que muestra
        self.main_window.muestra()
        self.kibitzers_manager = KibitzersManager.Manager(self)

        self.board = self.main_window.board

        self.entrenamientos = Trainings.Entrenamientos(self)

        if self.configuration.x_check_for_update:
            Update.test_update(self.version, self)

        if len(sys.argv) > 1:
            comando = sys.argv[1]
            comandoL = comando.lower()
            if comandoL.endswith(".pgn"):
                aplazamiento = {}
                aplazamiento["TIPOJUEGO"] = GT_AGAINST_PGN
                aplazamiento["ISWHITE"] = True  # Compatibilidad
                self.juegaAplazada(aplazamiento)
                return
            elif comandoL.endswith(".lcsb"):
                aplazamiento = {}
                aplazamiento["TIPOJUEGO"] = GT_ALONE
                aplazamiento["ISWHITE"] = True  # Compatibilidad
                self.juegaAplazada(aplazamiento)
                return
            elif comandoL.endswith(".lcdb"):
                self.externDatabase(comando)
                return
            elif comandoL.endswith(".bmt"):
                self.inicio()
                self.externBMT(comando)
                return
            elif comando == "-play":
                fich_tmp = sys.argv[2]
                self.juegaExterno(fich_tmp)
                return

        else:
            self.inicio()

    def reset(self):
        self.main_window.activaCapturas(False)
        self.main_window.activaInformacionPGN(False)
        if self.manager:
            self.manager.finManager()
            self.manager = None
        self.main_window.set_manager_active(self)  # Necesario, no borrar
        self.board.side_indicator_sc.setVisible(False)
        self.board.blindfoldQuitar()
        self.test_opcion_adjourns()
        self.main_window.pon_toolbar(self.li_opciones_inicio, atajos=True)
        self.main_window.activaJuego(False, False)
        self.board.exePulsadoNum = None
        self.board.set_position(self.posicionInicial)
        self.board.borraMovibles()
        self.board.remove_arrows()
        self.main_window.ajustaTam()
        self.main_window.ponTitulo()
        self.pararMotores()

        self.main_window.current_height = self.main_window.height()

    def inicio(self):
        Code.runSound.close()
        if self.manager:
            del self.manager
            self.manager = None
        self.configuration.limpiaTemporal()
        self.reset()
        if self.configuration.siPrimeraVez:
            self.cambiaconfigurationPrimeraVez()
            self.configuration.siPrimeraVez = False
            self.main_window.ponTitulo()
        if self.siPrimeraVez:
            self.siPrimeraVez = False
            self.cpu = CPU.CPU(self.main_window)
            self.presentacion()
        self.kibitzers_manager.stop()

    def presentacion(self, siEmpezar=True):
        self.siPresentacion = siEmpezar
        if not siEmpezar:
            self.cpu.stop()
            self.board.ponerPiezasAbajo(True)
            self.board.activaMenuVisual(True)
            self.board.set_position(self.posicionInicial)
            self.board.setToolTip("")
            self.board.bloqueaRotacion(False)

        else:
            self.board.bloqueaRotacion(True)
            self.board.setToolTip("")
            self.board.activaMenuVisual(True)
            Presentacion.ManagerChallenge101(self)

    def juegaAplazada(self, aplazamiento):
        self.cpu = CPU.CPU(self.main_window)

        tipoJuego = aplazamiento["TIPOJUEGO"]
        is_white = aplazamiento["ISWHITE"]

        if tipoJuego == GT_COMPETITION_WITH_TUTOR:
            categoria = self.configuration.rival.categorias.segun_clave(aplazamiento["CATEGORIA"])
            nivel = aplazamiento["LEVEL"]
            puntos = aplazamiento["PUNTOS"]
            self.manager = ManagerCompeticion.ManagerCompeticion(self)
            self.manager.inicio(categoria, nivel, is_white, puntos, aplazamiento)
        elif tipoJuego == GT_AGAINST_ENGINE:
            if aplazamiento["MODO"] == "Basic":
                self.entrenaMaquina(aplazamiento)
            else:
                self.playPersonAplazada(aplazamiento)
        elif tipoJuego == GT_ELO:
            self.manager = ManagerElo.ManagerElo(self)
            self.manager.inicio(aplazamiento)
        elif tipoJuego == GT_MICELO:
            self.manager = ManagerMicElo.ManagerMicElo(self)
            self.manager.inicio(None, 0, 0, aplazamiento)
        elif tipoJuego == GT_ALBUM:
            self.manager = ManagerAlbum.ManagerAlbum(self)
            self.manager.inicio(None, None, aplazamiento)
        elif tipoJuego == GT_AGAINST_PGN:
            self.read_pgn(sys.argv[1])
        elif tipoJuego in (GT_FICS, GT_FIDE, GT_LICHESS):
            self.manager = ManagerFideFics.ManagerFideFics(self)
            self.manager.selecciona(tipoJuego)
            self.manager.inicio(aplazamiento["IDGAME"], aplazamiento=aplazamiento)

    def XTutor(self):
        if self.xtutor is None or not self.xtutor.activo:
            self.creaXTutor()
        return self.xtutor

    def creaXTutor(self):
        xtutor = EngineManager.EngineManager(self, self.configuration.tutor)
        xtutor.name += "(%s)" % _("tutor")
        xtutor.opciones(self.configuration.x_tutor_mstime, self.configuration.x_tutor_depth, True)
        if self.configuration.x_tutor_multipv == 0:
            xtutor.maximizaMultiPV()
        else:
            xtutor.setMultiPV(self.configuration.x_tutor_multipv)

        self.xtutor = xtutor

    def cambiaXTutor(self):
        if self.xtutor:
            self.xtutor.terminar()
        self.creaXTutor()
        self.cambiaXAnalyzer()

    def XAnalyzer(self):
        if self.xanalyzer is None or not self.xanalyzer.activo:
            self.creaXAnalyzer()
        return self.xanalyzer

    def creaXAnalyzer(self):
        xanalyzer = EngineManager.EngineManager(self, self.configuration.tutor)
        xanalyzer.name += "(%s)" % _("analyzer")
        xanalyzer.opciones(self.configuration.x_tutor_mstime, self.configuration.x_tutor_depth, True)
        if self.configuration.x_tutor_multipv == 0:
            xanalyzer.maximizaMultiPV()
        else:
            xanalyzer.setMultiPV(self.configuration.x_tutor_multipv)

        self.xanalyzer = xanalyzer
        Code.xanalyzer = xanalyzer

    def cambiaXAnalyzer(self):
        if self.xanalyzer:
            self.xanalyzer.terminar()
        self.creaXAnalyzer()

    def creaManagerMotor(self, confMotor, vtime, nivel, siMultiPV=False, priority=None):
        xmanager = EngineManager.EngineManager(self, confMotor)
        xmanager.opciones(vtime, nivel, siMultiPV)
        xmanager.setPriority(priority)
        return xmanager

    def pararMotores(self):
        Code.list_engine_managers.close_all()

    # Added by GON
    def desactivarDGT(self):
        if Code.dgt:
            DGT.desactivar()
    # ------------        

    def cambiaRival(self, nuevo):
        """
        Llamado from_sq DatosNueva, cuando elegimos otro engine para jugar.
        """
        self.configuration.rival = self.configuration.buscaRival(nuevo)
        self.configuration.graba()

    def menuplay(self):
        resp = BasicMenus.menuplay(self)
        if resp:
            self.menuPlay_run(resp)

    def menuPlay_run(self, resp):
        tipo, rival = resp
        if tipo == "free":
            self.libre()

        elif tipo == "person":
            self.playPerson(rival)

        elif tipo == "animales":
            self.albumAnimales(rival)

        elif tipo == "vehicles":
            self.albumVehicles(rival)

    def playPersonAplazada(self, aplazamiento):
        self.manager = ManagerPerson.ManagerPerson(self)
        self.manager.inicio(None, aplazamiento=aplazamiento)

    def playPerson(self, rival):
        uno = QTVarios.blancasNegrasTiempo(self.main_window)
        if not uno:
            return
        is_white, siTiempo, minutos, segundos, fastmoves = uno
        if is_white is None:
            return

        dic = {}
        dic["ISWHITE"] = is_white
        dic["RIVAL"] = rival

        dic["SITIEMPO"] = siTiempo and minutos > 0
        dic["MINUTOS"] = minutos
        dic["SEGUNDOS"] = segundos

        dic["FASTMOVES"] = fastmoves

        self.manager = ManagerPerson.ManagerPerson(self)
        self.manager.inicio(dic)

    def reabrirAlbum(self, album):
        tipo, name = album.claveDB.split("_")
        if tipo == "animales":
            self.albumAnimales(name)
        elif tipo == "vehicles":
            self.albumVehicles(name)

    def albumAnimales(self, animal):
        albumes = Albums.AlbumesAnimales()
        album = albumes.get_album(animal)
        album.test_finished()
        cromo, siRebuild = WindowAlbumes.eligeCromo(self.main_window, self, album)
        if cromo is None:
            if siRebuild:
                albumes.reset(animal)
                self.albumAnimales(animal)
            return

        self.manager = ManagerAlbum.ManagerAlbum(self)
        self.manager.inicio(album, cromo)

    def albumVehicles(self, character):
        albumes = Albums.AlbumesVehicles()
        album = albumes.get_album(character)
        album.test_finished()
        cromo, siRebuild = WindowAlbumes.eligeCromo(self.main_window, self, album)
        if cromo is None:
            if siRebuild:
                albumes.reset(character)
                self.albumVehicles(character)
            return

        self.manager = ManagerAlbum.ManagerAlbum(self)
        self.manager.inicio(album, cromo)

    def menucompete(self):
        resp = BasicMenus.menucompete(self)
        if resp:
            self.menucompete_run(resp)

    def menucompete_run(self, resp):
        tipo, rival = resp
        if tipo == "competition":
            self.competicion()

        elif tipo == "lucaselo":
            self.lucaselo()

        elif tipo == "micelo":
            self.micelo()

        elif tipo == "fics":
            self.ficselo(rival)

        elif tipo == "fide":
            self.fideelo(rival)

        elif tipo == "lichess":
            self.lichesselo(rival)

        elif tipo == "challenge101":
            Presentacion.ManagerChallenge101(self)

        elif tipo == "strenght101":
            self.strenght101()

    def strenght101(self):
        w = WindowSingularM.WSingularM(self.main_window, self.configuration)
        if w.exec_():
            self.manager = ManagerSingularM.ManagerSingularM(self)
            self.manager.inicio(w.sm)

    def lucaselo(self):
        self.manager = ManagerElo.ManagerElo(self)
        resp = WEngines.select_engine_elo(self.manager, self.configuration.eloActivo())
        if resp:
            self.manager.inicio(resp)

    def micelo(self):
        self.manager = ManagerMicElo.ManagerMicElo(self)
        resp = WEngines.select_engine_micelo(self.manager, self.configuration.miceloActivo())
        if resp:
            respT = QTVarios.vtime(self.main_window, minMinutos=3, minSegundos=0, maxMinutos=999, maxSegundos=999)
            if respT:
                minutos, segundos = respT
                self.manager.inicio(resp, minutos, segundos)

    def ficselo(self, nivel):
        self.manager = ManagerFideFics.ManagerFideFics(self)
        self.manager.selecciona(GT_FICS)
        xid = self.manager.elige_juego(nivel)
        self.manager.inicio(xid)

    def fideelo(self, nivel):
        self.manager = ManagerFideFics.ManagerFideFics(self)
        self.manager.selecciona(GT_FIDE)
        xid = self.manager.elige_juego(nivel)
        self.manager.inicio(xid)

    def lichesselo(self, nivel):
        self.manager = ManagerFideFics.ManagerFideFics(self)
        self.manager.selecciona(GT_LICHESS)
        xid = self.manager.elige_juego(nivel)
        self.manager.inicio(xid)

    def run_action(self, key):
        if self.siPresentacion:
            self.presentacion(False)

        if key == TB_QUIT:
            if hasattr(self, "cpu"):
                self.cpu.stop()
            self.main_window.procesosFinales()
            self.main_window.accept()

        elif key == TB_PLAY:
            self.menuplay()

        elif key == TB_COMPETE:
            self.menucompete()

        elif key == TB_TRAIN:
            self.entrenamientos.lanza()

        elif key == TB_OPTIONS:
            self.opciones()

        elif key == TB_TOOLS:
            self.menu_tools()

        elif key == TB_INFORMATION:
            self.informacion()

        elif key == TB_ADJOURNS:
            self.adjourns()

    def adjourns(self):
        menu = QTVarios.LCMenu(self.main_window)
        li_adjourns = Adjourns.Adjourns().list_menu()
        for key, label, tp in li_adjourns:
            menu.opcion((True, key, tp), label, Iconos.PuntoMagenta())
            menu.addSeparator()
        menu.addSeparator()
        mr = menu.submenu(_("Remove"), Iconos.Borrar())
        for key, label, tp in li_adjourns:
            mr.opcion((False, key, tp), label, Iconos.Delete())

        resp = menu.lanza()
        if resp:
            si_run, key, tp = resp
            if si_run:
                dic = Adjourns.Adjourns().get(key)
                Adjourns.Adjourns().remove(key)
                if tp == GT_AGAINST_ENGINE:
                    self.manager = ManagerPlayAgainstEngine.ManagerPlayAgainstEngine(self)
                    self.manager.run_adjourn(dic)
                elif tp == GT_ALBUM:
                    self.manager = ManagerAlbum.ManagerAlbum(self)
                    self.manager.run_adjourn(dic)
                elif tp == GT_COMPETITION_WITH_TUTOR:
                    self.manager = ManagerCompeticion.ManagerCompeticion(self)
                    self.manager.run_adjourn(dic)
                elif tp == GT_ELO:
                    self.manager = ManagerElo.ManagerElo(self)
                    self.manager.run_adjourn(dic)
                elif tp == GT_AGAINST_GM:
                    self.manager = ManagerGM.ManagerGM(self)
                    self.manager.run_adjourn(dic)
                elif tp in (GT_FIDE, GT_FICS, GT_LICHESS):
                    self.manager = ManagerFideFics.ManagerFideFics(self)
                    self.manager.selecciona(tp)
                    self.manager.run_adjourn(dic)
                return

            else:
                Adjourns.Adjourns().remove(key)

            self.test_opcion_adjourns()
            self.main_window.pon_toolbar(self.li_opciones_inicio, atajos=True)

    def lanza_atajos(self):
        BasicMenus.atajos(self)

    def lanzaAtajosALT(self, key):
        BasicMenus.atajosALT(self, key)

    def opciones(self):
        menu = QTVarios.LCMenu(self.main_window)

        menu.opcion(self.cambiaconfiguration, _("Configuration"), Iconos.Opciones())
        menu.separador()

        menu1 = menu.submenu(_("Colors"), Iconos.Colores())
        menu1.opcion(self.editColoresBoard, _("Main board"), Iconos.EditarColores())
        menu1.separador()
        menu1.opcion(self.cambiaColores, _("General"), Iconos.Vista())
        menu.separador()

        menu.opcion(self.sonidos, _("Custom sounds"), Iconos.SoundTool())
        menu.separador()
        menu.opcion(self.setPassword, _("Set password"), Iconos.Password())

        if self.configuration.is_main:
            menu.separador()
            menu.opcion(self.usuarios, _("Usuarios"), Iconos.Usuarios())
            menu.separador()

            menu1 = menu.submenu(_("User data folder"), Iconos.Carpeta())
            menu1.opcion(self.folder_change, _("Change the folder"), Iconos.FolderChange())
            if not Configuration.is_default_folder():
                menu1.separador()
                menu1.opcion(self.folder_default, _("Set the default"), Iconos.Defecto())

        resp = menu.lanza()
        if resp:
            if isinstance(resp, tuple):
                resp[0](resp[1])
            else:
                resp()

    def cambiaconfiguration(self):
        if WindowConfig.opciones(self.main_window, self.configuration):
            self.configuration.graba()
            self.reiniciar()

    def editColoresBoard(self):
        w = WindowColores.WColores(self.board)
        w.exec_()

    def cambiaColores(self):
        if WindowColores.cambiaColores(self.main_window, self.configuration):
            self.reiniciar()

    def sonidos(self):
        w = WindowSonido.WSonidos(self)
        w.exec_()

    def folder_change(self):
        carpeta = QTUtil2.leeCarpeta(
            self.main_window,
            self.configuration.carpeta,
            _("Change the folder where all data is saved") + "\n" + _("Be careful please"),
        )
        if carpeta:
            if os.path.isdir(carpeta):
                self.configuration.changeActiveFolder(carpeta)
                self.reiniciar()

    def folder_default(self):
        self.configuration.changeActiveFolder(None)
        self.reiniciar()

    def reiniciar(self):
        self.main_window.accept()
        QTUtil.salirAplicacion(OUT_REINIT)

    def cambiaconfigurationPrimeraVez(self):
        if WindowConfig.options_first_time(self.main_window, self.configuration):
            self.configuration.graba()

    def motoresExternos(self):
        w = WEngines.WEngines(self.main_window, self.configuration)
        w.exec_()

    def aperturaspers(self):
        w = WindowOpenings.OpeningsPersonales(self)
        w.exec_()

    def usuarios(self):
        WindowUsuarios.editUsuarios(self)

    def setPassword(self):
        WindowUsuarios.setPassword(self)

    def trainingMap(self, mapa):
        resp = WindowWorkMap.train_map(self, mapa)
        if resp:
            self.manager = ManagerMateMap.ManagerMateMap(self)
            self.manager.inicio(resp)

    def menu_tools(self):
        resp = BasicMenus.menu_tools(self)
        if resp:
            self.menuTools_run(resp)

    def menuTools_run(self, resp):
        if resp == "pgn":
            self.visorPGN()

        elif resp == "miniatura":
            self.miniatura()

        elif resp == "polyglot":
            self.polyglot_factory()

        elif resp == "pgn_paste":
            self.pgn_paste()

        elif resp == "juega_solo":
            self.jugarSolo()

        elif resp == "torneos":
            self.torneos()
        elif resp == "motores":
            self.motoresExternos()
        elif resp == "sts":
            self.sts()
        elif resp == "kibitzers":
            self.kibitzers_manager.edit()

        elif resp == "manual_save":
            self.manual_save()

        elif resp.startswith("dbase_"):
            comando = resp[6:]
            accion = comando[0]  # R = read database,  N = create new, D = delete
            valor = comando[2:]
            self.database(accion, valor)

        elif resp == "aperturaspers":
            self.aperturaspers()
        elif resp == "openings":
            self.openings()

    def openings(self):
        dicline = WindowOpeningLines.openingLines(self)
        if dicline:
            if "TRAIN" in dicline:
                resp = "tr_%s" % dicline["TRAIN"]
            else:
                resp = WindowOpeningLine.study(self, dicline["file"])
            if resp is None:
                self.openings()
            else:
                pathFichero = os.path.join(self.configuration.folder_openings(), dicline["file"])
                if resp == "tr_sequential":
                    self.openingsTrainingSequential(pathFichero)
                elif resp == "tr_static":
                    self.openingsTrainingStatic(pathFichero)
                elif resp == "tr_positions":
                    self.openingsTrainingPositions(pathFichero)
                elif resp == "tr_engines":
                    self.openingsTrainingEngines(pathFichero)

    def openingsTrainingSequential(self, pathFichero):
        self.manager = ManagerOpeningLines.ManagerOpeningLines(self)
        self.manager.inicio(pathFichero, "sequential", 0)

    def openingsTrainingEngines(self, pathFichero):
        self.manager = ManagerOpeningLines.ManagerOpeningEngines(self)
        self.manager.inicio(pathFichero)

    def openingsTrainingStatic(self, pathFichero):
        dbop = OpeningLines.Opening(pathFichero)
        num_linea = WindowOpeningLines.selectLine(self, dbop)
        dbop.close()
        if num_linea is not None:
            self.manager = ManagerOpeningLines.ManagerOpeningLines(self)
            self.manager.inicio(pathFichero, "static", num_linea)
        else:
            self.openings()

    def openingsTrainingPositions(self, pathFichero):
        self.manager = ManagerOpeningLines.ManagerOpeningLinesPositions(self)
        self.manager.inicio(pathFichero)

    def externBMT(self, fichero):
        self.configuration.ficheroBMT = fichero
        WindowBMT.windowBMT(self)

    def anotar(self, game, siblancasabajo):
        self.manager = ManagerAnotar.ManagerAnotar(self)
        self.manager.inicio(game, siblancasabajo)

    def show_anotar(self):
        w = WindowAnotar.WAnotar(self)
        if w.exec_():
            pc, siblancasabajo = w.resultado
            if pc is None:
                pc = DBgames.get_random_game()
            self.anotar(pc, siblancasabajo)

    def externDatabase(self, fichero):
        self.configuration.ficheroDBgames = fichero
        self.database(fichero)
        self.run_action(TB_QUIT)

    def database(self, accion, dbpath, temporary=False):
        if accion == "M":
            if Code.isWindows:
                os.startfile(self.configuration.folder_databases())
            return

        if accion == "N":
            dbpath = WDB_Games.new_database(self.main_window, self.configuration)
            if dbpath is None:
                return
            accion = "R"

        if accion == "D":
            resp = QTVarios.select_db(self.main_window, self.configuration, True, False)
            if resp:
                if QTUtil2.pregunta(self.main_window, "%s\n%s" % (_("Do you want to remove ?"), resp)):
                    Util.remove_file(resp)
                    Util.remove_file(resp + ".st1")
            return

        if accion == "R":
            self.configuration.set_last_database(Util.relative_path(dbpath))
            w = WindowDatabase.WBDatabase(self.main_window, self, dbpath, temporary, False)
            if self.main_window:
                if w.exec_():
                    if w.reiniciar:
                        self.database("R", self.configuration.get_last_database())
            else:
                w.show()

    def manual_save(self):
        WindowManualSave.manual_save(self)

    def torneos(self):
        WTournaments.tournaments(self.main_window)

    def sts(self):
        WindowSTS.sts(self, self.main_window)

    def libre(self):
        dic = PlayAgainstEngine.play_against_engine(self, _("Play against an engine"))
        if dic:
            self.entrenaMaquina(dic)

    def entrenaMaquina(self, dic):
        self.manager = ManagerPlayAgainstEngine.ManagerPlayAgainstEngine(self)
        side = dic["SIDE"]
        if side == "R":
            side = "B" if random.randint(1, 2) == 1 else "N"
        dic["ISWHITE"] = side == "B"
        self.manager.inicio(dic)

    def read_pgn(self, fichero_pgn):
        fichero_pgn = os.path.abspath(fichero_pgn)
        cfecha_pgn = str(os.path.getmtime(fichero_pgn))
        cdir = self.configuration.folder_databases_pgn()

        file_db = os.path.join(cdir, os.path.basename(fichero_pgn)[:-4] + ".lcdb")

        if Util.exist_file(file_db):
            create = False
            db = DBgames.DBgames(file_db)
            cfecha_pgn_ant = db.recuperaConfig("PGN_DATE")
            fichero_pgn_ant = db.recuperaConfig("PGN_FILE")
            db.close()
            if cfecha_pgn != cfecha_pgn_ant or fichero_pgn_ant != fichero_pgn:
                create = True
                Util.remove_file(file_db)
        else:
            create = True

        if create:
            db = DBgames.DBgames(file_db)
            dlTmp = QTVarios.ImportarFicheroPGN(self.main_window)
            dlTmp.show()
            db.leerPGNs([fichero_pgn], dlTmp=dlTmp)
            db.guardaConfig("PGN_DATE", cfecha_pgn)
            db.guardaConfig("PGN_FILE", fichero_pgn)
            db.close()
            dlTmp.close()

        self.database("R", file_db, temporary=True)

    def visorPGN(self):
        path = QTVarios.select_pgn(self.main_window)
        if path:
            self.read_pgn(path)

    def select_1_pgn(self, wparent=None):
        wparent = self.main_window if wparent is None else wparent
        path = QTVarios.select_pgn(wparent)
        if path:
            fichero_pgn = os.path.abspath(path)
            cfecha_pgn = str(os.path.getmtime(fichero_pgn))
            cdir = self.configuration.folder_databases_pgn()

            file_db = os.path.join(cdir, os.path.basename(fichero_pgn)[:-4] + ".lcdb")

            if Util.exist_file(file_db):
                create = False
                db = DBgames.DBgames(file_db)
                cfecha_pgn_ant = db.recuperaConfig("PGN_DATE")
                fichero_pgn_ant = db.recuperaConfig("PGN_FILE")
                db.close()
                if cfecha_pgn != cfecha_pgn_ant or fichero_pgn_ant != fichero_pgn:
                    create = True
                    Util.remove_file(file_db)
            else:
                create = True

            if create:
                db = DBgames.DBgames(file_db)
                dlTmp = QTVarios.ImportarFicheroPGN(wparent)
                dlTmp.show()
                db.leerPGNs([fichero_pgn], dlTmp=dlTmp)
                db.guardaConfig("PGN_DATE", cfecha_pgn)
                db.guardaConfig("PGN_FILE", fichero_pgn)
                db.close()
                dlTmp.close()

            w = WindowDatabase.WBDatabase(self.main_window, self, file_db, True, True)
            if w.exec_():
                return w.game

        return None

    def pgn_paste(self):
        path = self.configuration.ficheroTemporal("lcdb")
        texto = QTUtil.traePortapapeles()
        if texto:
            with open(path, "wb") as q:
                q.write(texto)
            self.read_pgn(path)

    def miniatura(self):
        file_miniatures = Code.path_resource("IntFiles", "Miniatures.lcdb")
        db = DBgames.DBgames(file_miniatures)
        db.all_reccount()
        num_game = random.randint(0, db.reccount() - 1)
        game = db.leePartidaRecno(num_game)
        db.close()
        dic = {"GAME": game.save()}
        manager = ManagerSolo.ManagerSolo(self)
        manager.inicio(dic)

    def polyglot_factory(self):
        resp = WFactory.polyglots_factory(self)
        if resp:
            w = WPolyglot.WPolyglot(self.main_window, self.configuration, resp)
            w.exec_()
            self.polyglot_factory()

    def juegaExterno(self, fich_tmp):
        dic_sended = Util.restore_pickle(fich_tmp)
        fich = Util.relative_path(self.configuration.ficheroTemporal(".pkd"))

        dic = PlayAgainstEngine.play_position(self, _("Play a position"), dic_sended["ISWHITE"])
        if dic is None:
            self.run_action(TB_QUIT)
        else:
            side = dic["SIDE"]
            if side == "R":
                side = "B" if random.randint(1, 2) == 1 else "N"
            dic["ISWHITE"] = side == "B"
            self.manager = ManagerPlayAgainstEngine.ManagerPlayAgainstEngine(self)
            self.manager.play_position(dic, dic_sended["GAME"])

    def jugarSolo(self):
        self.manager = ManagerSolo.ManagerSolo(self)
        self.manager.inicio()

    def entrenaPos(self, position, nPosiciones, titentreno, liEntrenamientos, entreno, jump):
        # self.game_type = GT_POSITIONS
        # self.state = ST_PLAYING
        self.manager = ManagerEntPos.ManagerEntPos(self)
        self.manager.set_training(entreno)
        self.manager.inicio(position, nPosiciones, titentreno, liEntrenamientos, is_automatic_jump=jump)

    def playRoute(self, route):
        if route.state == Routes.BETWEEN:
            self.manager = ManagerRoutes.ManagerRoutesTactics(self)
            # self.state = ST_PLAYING
            # self.game_type = GT_POSITIONS
            self.manager.inicio(route)
        elif route.state == Routes.ENDING:
            self.manager = ManagerRoutes.ManagerRoutesEndings(self)
            # self.state = ST_PLAYING
            # self.game_type = GT_POSITIONS
            self.manager.inicio(route)
        elif route.state == Routes.PLAYING:
            self.manager = ManagerRoutes.ManagerRoutesPlay(self)
            # self.state = ST_PLAYING
            # self.game_type = GT_AGAINST_ENGINE
            self.manager.inicio(route)

    def showRoute(self):
        WindowRoutes.train_train(self)

    def playEverest(self, recno):
        self.manager = ManagerEverest.ManagerEverest(self)
        # self.state = ST_PLAYING
        # self.game_type = GT_AGAINST_ENGINE
        self.manager.inicio(recno)

    def showEverest(self, recno):
        if WindowEverest.show_expedition(self.main_window, self.configuration, recno):
            self.playEverest(recno)

    def play_game(self):
        w = WindowPlayGame.WPlayGameBase(self)
        if w.exec_():
            recno = w.recno
            if recno is not None:
                is_white = w.is_white
                self.manager = ManagerPlayGame.ManagerPlayGame(self)
                self.manager.inicio(recno, is_white)

    def play_game_show(self, recno):
        db = WindowPlayGame.DBPlayGame(self.configuration.file_play_game())
        w = WindowPlayGame.WPlay1(self.main_window, self.configuration, db, recno)
        if w.exec_():
            if w.recno is not None:
                is_white = w.is_white
                self.manager = ManagerPlayGame.ManagerPlayGame(self)
                self.manager.inicio(w.recno, is_white)
        db.close()

    def showTurnOnLigths(self, name):
        self.entrenamientos.turn_on_lights(name)

    def playWashing(self):
        ManagerWashing.managerWashing(self)

    def showWashing(self):
        if WindowWashing.windowWashing(self):
            self.playWashing()

    def informacion(self):
        resp = BasicMenus.menuInformacion(self)
        if resp:
            self.informacion_run(resp)

    def informacion_run(self, resp):
        if resp == "acercade":
            self.acercade()
        elif resp == "docs":
            webbrowser.open("%s/docs" % self.web)
        elif resp == "blog":
            webbrowser.open(self.blog)
        elif resp.startswith("http"):
            webbrowser.open(resp)
        elif resp == "web":
            webbrowser.open("%s/index?lang=%s" % (self.web, self.configuration.translator()))
        elif resp == "mail":
            webbrowser.open("mailto:lukasmonk@gmail.com")

        elif resp == "actualiza":
            self.actualiza()

    def adTitulo(self):
        return "<b>" + Code.lucas_chess + "</b><br>" + _X(_("version %1"), self.version)

    def adPie(self):
        return (
            "<hr><br><b>%s</b>" % _("Author")
            + ': <a href="mailto:lukasmonk@gmail.com">Lucas Monge</a> -'
            + ' <a href="%s">%s</a></a>' % (self.web, self.web)
            + '(%s <a href="http://www.gnu.org/copyleft/gpl.html"> GPL</a>).<br>' % _("License")
        )

    def acercade(self):
        w = About.WAbout(self)
        w.exec_()

    def actualiza(self):
        if Update.update(self.version, self.main_window):
            self.reiniciar()

    def unMomento(self, mensaje=None):
        return QTUtil2.mensEspera.inicio(
            self.main_window, mensaje if mensaje else _("One moment please..."), physical_pos="ad"
        )

    def num_rows(self):
        return 0

    def competicion(self):
        opciones = WCompetitionWithTutor.datos(self.main_window, self.configuration, self)
        if opciones:
            # self.game_type = GT_COMPETITION_WITH_TUTOR
            categorias, categoria, nivel, is_white, puntos = opciones

            self.manager = ManagerCompeticion.ManagerCompeticion(self)
            self.manager.inicio(categorias, categoria, nivel, is_white, puntos)

    def final_x(self):
        return True

    def finalX0(self):
        return True

    def clonVariations(self, window, xtutor=None, is_competitive=False):
        return ProcesadorVariations(
            window, xtutor, is_competitive=is_competitive, kibitzers_manager=self.kibitzers_manager
        )

    def managerPartida(self, window, game, si_completa, si_solo_consultar, boardFather):
        clonProcesador = ProcesadorVariations(
            window, self.xtutor, is_competitive=False, kibitzers_manager=self.kibitzers_manager
        )
        clonProcesador.manager = ManagerPartida.ManagerPartida(clonProcesador)
        clonProcesador.manager.inicio(game, si_completa, si_solo_consultar)

        board = clonProcesador.main_window.board
        if boardFather:
            board.dbVisual_setFichero(boardFather.dbVisual.fichero)
            board.dbVisual_setShowAllways(boardFather.dbVisual.showAllways)

        resp = clonProcesador.main_window.muestraVariations(clonProcesador.manager.tituloVentana())
        if boardFather:
            boardFather.dbVisual_setFichero(boardFather.dbVisual.fichero)
            boardFather.dbVisual_setShowAllways(boardFather.dbVisual.showAllways())

        if resp:
            return clonProcesador.manager.game
        else:
            return None

    def selectOneFNS(self, owner=None):
        if owner is None:
            owner = self.main_window
        return Trainings.selectOneFNS(owner, self)

    def gaviota_endings(self):
        WEndingsGTB.train_gtb(self)


class ProcesadorVariations(Procesador):
    def __init__(self, window, xtutor, is_competitive=False, kibitzers_manager=None):

        self.kibitzers_manager = kibitzers_manager
        self.is_competitive = is_competitive

        self.configuration = Code.configuration

        self.li_opciones_inicio = [
            TB_QUIT,
            TB_PLAY,
            TB_TRAIN,
            TB_COMPETE,
            TB_TOOLS,
            TB_OPTIONS,
            TB_INFORMATION,
        ]  # Lo incluimos aqui porque sino no lo lee, en caso de aplazada

        self.siPresentacion = False

        self.main_window = MainWindow.MainWindow(self, window)
        self.main_window.set_manager_active(self)

        self.board = self.main_window.board

        self.xtutor = xtutor
        self.xrival = None
        self.xanalyzer = None

        self.replayBeep = None

        self.posicionInicial = None

        self.cpu = CPU.CPU(self.main_window)
