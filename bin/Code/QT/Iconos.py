from PySide2 import QtGui

import Code

f = open(Code.path_resource("IntFiles", "Iconos.bin"), "rb")
binIconos = f.read()
f.close()


def icono(name):
    return eval("%s()"%name)


def pixmap(name):
    return eval("pm%s()"%name)


def PM(desde, hasta):
    pm = QtGui.QPixmap()
    pm.loadFromData(binIconos[desde:hasta])
    return pm

def pmLM():
    return PM(0,1248)


def LM():
    return QtGui.QIcon(pmLM())


def pmAplicacion64():
    return PM(1248,6430)


def Aplicacion64():
    return QtGui.QIcon(pmAplicacion64())


def pmDatos():
    return PM(6430,7617)


def Datos():
    return QtGui.QIcon(pmDatos())


def pmTutor():
    return PM(7617,9646)


def Tutor():
    return QtGui.QIcon(pmTutor())


def pmBoard():
    return PM(6430,7617)


def Board():
    return QtGui.QIcon(pmBoard())


def pmPartidaOriginal():
    return PM(9646,11623)


def PartidaOriginal():
    return QtGui.QIcon(pmPartidaOriginal())


def pmDGT():
    return PM(11623,12617)


def DGT():
    return QtGui.QIcon(pmDGT())


def pmFindAllMoves():
    return PM(12617,14213)


def FindAllMoves():
    return QtGui.QIcon(pmFindAllMoves())


def pmResizeBoard():
    return PM(12617,14213)


def ResizeBoard():
    return QtGui.QIcon(pmResizeBoard())


def pmMensEspera():
    return PM(14213,17961)


def MensEspera():
    return QtGui.QIcon(pmMensEspera())


def pmUtilidades():
    return PM(17961,24390)


def Utilidades():
    return QtGui.QIcon(pmUtilidades())


def pmTerminar():
    return PM(24390,26140)


def Terminar():
    return QtGui.QIcon(pmTerminar())


def pmNuevaPartida():
    return PM(26140,27888)


def NuevaPartida():
    return QtGui.QIcon(pmNuevaPartida())


def pmOpciones():
    return PM(27888,29616)


def Opciones():
    return QtGui.QIcon(pmOpciones())


def pmEntrenamiento():
    return PM(7617,9646)


def Entrenamiento():
    return QtGui.QIcon(pmEntrenamiento())


def pmAplazar():
    return PM(29616,32683)


def Aplazar():
    return QtGui.QIcon(pmAplazar())


def pmAplazamientos():
    return PM(32683,35999)


def Aplazamientos():
    return QtGui.QIcon(pmAplazamientos())


def pmCapturas():
    return PM(35999,38040)


def Capturas():
    return QtGui.QIcon(pmCapturas())


def pmReiniciar():
    return PM(38040,40334)


def Reiniciar():
    return QtGui.QIcon(pmReiniciar())


def pmMotores():
    return PM(40334,46233)


def Motores():
    return QtGui.QIcon(pmMotores())


def pmImportarGM():
    return PM(46233,48833)


def ImportarGM():
    return QtGui.QIcon(pmImportarGM())


def pmAbandonar():
    return PM(48833,52833)


def Abandonar():
    return QtGui.QIcon(pmAbandonar())


def pmEmpezar():
    return PM(52833,54869)


def Empezar():
    return QtGui.QIcon(pmEmpezar())


def pmOtros():
    return PM(54869,59339)


def Otros():
    return QtGui.QIcon(pmOtros())


def pmAnalizar():
    return PM(59339,60876)


def Analizar():
    return QtGui.QIcon(pmAnalizar())


def pmMainMenu():
    return PM(60876,65186)


def MainMenu():
    return QtGui.QIcon(pmMainMenu())


def pmFinPartida():
    return PM(65186,68134)


def FinPartida():
    return QtGui.QIcon(pmFinPartida())


def pmGrabar():
    return PM(68134,69597)


def Grabar():
    return QtGui.QIcon(pmGrabar())


def pmGrabarComo():
    return PM(69597,71649)


def GrabarComo():
    return QtGui.QIcon(pmGrabarComo())


def pmRecuperar():
    return PM(71649,74407)


def Recuperar():
    return QtGui.QIcon(pmRecuperar())


def pmInformacion():
    return PM(74407,76366)


def Informacion():
    return QtGui.QIcon(pmInformacion())


def pmNuevo():
    return PM(76366,77120)


def Nuevo():
    return QtGui.QIcon(pmNuevo())


def pmCopiar():
    return PM(77120,78301)


def Copiar():
    return QtGui.QIcon(pmCopiar())


def pmModificar():
    return PM(78301,82698)


def Modificar():
    return QtGui.QIcon(pmModificar())


def pmBorrar():
    return PM(82698,87689)


def Borrar():
    return QtGui.QIcon(pmBorrar())


def pmMarcar():
    return PM(87689,92618)


def Marcar():
    return QtGui.QIcon(pmMarcar())


def pmPegar():
    return PM(92618,94929)


def Pegar():
    return QtGui.QIcon(pmPegar())


def pmFichero():
    return PM(94929,99614)


def Fichero():
    return QtGui.QIcon(pmFichero())


def pmNuestroFichero():
    return PM(99614,102661)


def NuestroFichero():
    return QtGui.QIcon(pmNuestroFichero())


def pmFicheroRepite():
    return PM(102661,104157)


def FicheroRepite():
    return QtGui.QIcon(pmFicheroRepite())


def pmInformacionPGN():
    return PM(104157,105175)


def InformacionPGN():
    return QtGui.QIcon(pmInformacionPGN())


def pmVer():
    return PM(105175,106629)


def Ver():
    return QtGui.QIcon(pmVer())


def pmInicio():
    return PM(106629,108643)


def Inicio():
    return QtGui.QIcon(pmInicio())


def pmFinal():
    return PM(108643,110637)


def Final():
    return QtGui.QIcon(pmFinal())


def pmFiltrar():
    return PM(110637,117127)


def Filtrar():
    return QtGui.QIcon(pmFiltrar())


def pmArriba():
    return PM(117127,119280)


def Arriba():
    return QtGui.QIcon(pmArriba())


def pmAbajo():
    return PM(119280,121388)


def Abajo():
    return QtGui.QIcon(pmAbajo())


def pmEstadisticas():
    return PM(121388,123527)


def Estadisticas():
    return QtGui.QIcon(pmEstadisticas())


def pmCheck():
    return PM(123527,126751)


def Check():
    return QtGui.QIcon(pmCheck())


def pmTablas():
    return PM(126751,128374)


def Tablas():
    return QtGui.QIcon(pmTablas())


def pmAtras():
    return PM(128374,129893)


def Atras():
    return QtGui.QIcon(pmAtras())


def pmBuscar():
    return PM(129893,131878)


def Buscar():
    return QtGui.QIcon(pmBuscar())


def pmLibros():
    return PM(131878,134006)


def Libros():
    return QtGui.QIcon(pmLibros())


def pmAceptar():
    return PM(134006,137353)


def Aceptar():
    return QtGui.QIcon(pmAceptar())


def pmCancelar():
    return PM(137353,139336)


def Cancelar():
    return QtGui.QIcon(pmCancelar())


def pmDefecto():
    return PM(139336,142655)


def Defecto():
    return QtGui.QIcon(pmDefecto())


def pmInsertar():
    return PM(142655,145051)


def Insertar():
    return QtGui.QIcon(pmInsertar())


def pmJugar():
    return PM(145051,147260)


def Jugar():
    return QtGui.QIcon(pmJugar())


def pmConfigurar():
    return PM(147260,150344)


def Configurar():
    return QtGui.QIcon(pmConfigurar())


def pmS_Aceptar():
    return PM(134006,137353)


def S_Aceptar():
    return QtGui.QIcon(pmS_Aceptar())


def pmS_Cancelar():
    return PM(137353,139336)


def S_Cancelar():
    return QtGui.QIcon(pmS_Cancelar())


def pmS_Microfono():
    return PM(150344,155785)


def S_Microfono():
    return QtGui.QIcon(pmS_Microfono())


def pmS_LeerWav():
    return PM(46233,48833)


def S_LeerWav():
    return QtGui.QIcon(pmS_LeerWav())


def pmS_Play():
    return PM(155785,161123)


def S_Play():
    return QtGui.QIcon(pmS_Play())


def pmS_StopPlay():
    return PM(161123,161733)


def S_StopPlay():
    return QtGui.QIcon(pmS_StopPlay())


def pmS_StopMicrofono():
    return PM(161123,161733)


def S_StopMicrofono():
    return QtGui.QIcon(pmS_StopMicrofono())


def pmS_Record():
    return PM(161733,164966)


def S_Record():
    return QtGui.QIcon(pmS_Record())


def pmS_Limpiar():
    return PM(82698,87689)


def S_Limpiar():
    return QtGui.QIcon(pmS_Limpiar())


def pmHistorial():
    return PM(164966,166229)


def Historial():
    return QtGui.QIcon(pmHistorial())


def pmPegar16():
    return PM(166229,167223)


def Pegar16():
    return QtGui.QIcon(pmPegar16())


def pmRivalesMP():
    return PM(167223,169905)


def RivalesMP():
    return QtGui.QIcon(pmRivalesMP())


def pmCamara():
    return PM(169905,171427)


def Camara():
    return QtGui.QIcon(pmCamara())


def pmUsuarios():
    return PM(171427,172667)


def Usuarios():
    return QtGui.QIcon(pmUsuarios())


def pmResistencia():
    return PM(172667,175729)


def Resistencia():
    return QtGui.QIcon(pmResistencia())


def pmCebra():
    return PM(175729,178182)


def Cebra():
    return QtGui.QIcon(pmCebra())


def pmGafas():
    return PM(178182,179340)


def Gafas():
    return QtGui.QIcon(pmGafas())


def pmPuente():
    return PM(179340,179976)


def Puente():
    return QtGui.QIcon(pmPuente())


def pmWeb():
    return PM(179976,181158)


def Web():
    return QtGui.QIcon(pmWeb())


def pmMail():
    return PM(181158,182118)


def Mail():
    return QtGui.QIcon(pmMail())


def pmAyuda():
    return PM(182118,183299)


def Ayuda():
    return QtGui.QIcon(pmAyuda())


def pmFAQ():
    return PM(183299,184620)


def FAQ():
    return QtGui.QIcon(pmFAQ())


def pmActualiza():
    return PM(184620,185486)


def Actualiza():
    return QtGui.QIcon(pmActualiza())


def pmRefresh():
    return PM(185486,187878)


def Refresh():
    return QtGui.QIcon(pmRefresh())


def pmJuegaSolo():
    return PM(187878,189730)


def JuegaSolo():
    return QtGui.QIcon(pmJuegaSolo())


def pmPlayer():
    return PM(189730,190912)


def Player():
    return QtGui.QIcon(pmPlayer())


def pmJS_Rotacion():
    return PM(190912,192822)


def JS_Rotacion():
    return QtGui.QIcon(pmJS_Rotacion())


def pmElo():
    return PM(192822,194328)


def Elo():
    return QtGui.QIcon(pmElo())


def pmMate():
    return PM(194328,194889)


def Mate():
    return QtGui.QIcon(pmMate())


def pmEloTimed():
    return PM(194889,196373)


def EloTimed():
    return QtGui.QIcon(pmEloTimed())


def pmPGN():
    return PM(196373,198371)


def PGN():
    return QtGui.QIcon(pmPGN())


def pmPGN_Importar():
    return PM(198371,199961)


def PGN_Importar():
    return QtGui.QIcon(pmPGN_Importar())


def pmAyudaGR():
    return PM(199961,205839)


def AyudaGR():
    return QtGui.QIcon(pmAyudaGR())


def pmBotonAyuda():
    return PM(205839,208299)


def BotonAyuda():
    return QtGui.QIcon(pmBotonAyuda())


def pmColores():
    return PM(208299,209530)


def Colores():
    return QtGui.QIcon(pmColores())


def pmEditarColores():
    return PM(209530,211833)


def EditarColores():
    return QtGui.QIcon(pmEditarColores())


def pmGranMaestro():
    return PM(211833,212689)


def GranMaestro():
    return QtGui.QIcon(pmGranMaestro())


def pmFavoritos():
    return PM(212689,214455)


def Favoritos():
    return QtGui.QIcon(pmFavoritos())


def pmCarpeta():
    return PM(214455,215159)


def Carpeta():
    return QtGui.QIcon(pmCarpeta())


def pmDivision():
    return PM(215159,215824)


def Division():
    return QtGui.QIcon(pmDivision())


def pmDivisionF():
    return PM(215824,216938)


def DivisionF():
    return QtGui.QIcon(pmDivisionF())


def pmKibitzer():
    return PM(216938,217477)


def Kibitzer():
    return QtGui.QIcon(pmKibitzer())


def pmKibitzer_Pausa():
    return PM(217477,218341)


def Kibitzer_Pausa():
    return QtGui.QIcon(pmKibitzer_Pausa())


def pmKibitzer_Continuar():
    return PM(218341,219172)


def Kibitzer_Continuar():
    return QtGui.QIcon(pmKibitzer_Continuar())


def pmKibitzer_Terminar():
    return PM(219172,220096)


def Kibitzer_Terminar():
    return QtGui.QIcon(pmKibitzer_Terminar())


def pmDelete():
    return PM(219172,220096)


def Delete():
    return QtGui.QIcon(pmDelete())


def pmModificarP():
    return PM(220096,221162)


def ModificarP():
    return QtGui.QIcon(pmModificarP())


def pmGrupo_Si():
    return PM(221162,221624)


def Grupo_Si():
    return QtGui.QIcon(pmGrupo_Si())


def pmGrupo_No():
    return PM(221624,221947)


def Grupo_No():
    return QtGui.QIcon(pmGrupo_No())


def pmMotor_Si():
    return PM(221947,222409)


def Motor_Si():
    return QtGui.QIcon(pmMotor_Si())


def pmMotor_No():
    return PM(219172,220096)


def Motor_No():
    return QtGui.QIcon(pmMotor_No())


def pmMotor_Actual():
    return PM(222409,223426)


def Motor_Actual():
    return QtGui.QIcon(pmMotor_Actual())


def pmMotor():
    return PM(223426,224053)


def Motor():
    return QtGui.QIcon(pmMotor())


def pmMoverInicio():
    return PM(224053,224351)


def MoverInicio():
    return QtGui.QIcon(pmMoverInicio())


def pmMoverFinal():
    return PM(224351,224652)


def MoverFinal():
    return QtGui.QIcon(pmMoverFinal())


def pmMoverAdelante():
    return PM(224652,225007)


def MoverAdelante():
    return QtGui.QIcon(pmMoverAdelante())


def pmMoverAtras():
    return PM(225007,225372)


def MoverAtras():
    return QtGui.QIcon(pmMoverAtras())


def pmMoverLibre():
    return PM(225372,225790)


def MoverLibre():
    return QtGui.QIcon(pmMoverLibre())


def pmMoverTiempo():
    return PM(225790,226369)


def MoverTiempo():
    return QtGui.QIcon(pmMoverTiempo())


def pmMoverMas():
    return PM(226369,227408)


def MoverMas():
    return QtGui.QIcon(pmMoverMas())


def pmMoverGrabar():
    return PM(227408,228264)


def MoverGrabar():
    return QtGui.QIcon(pmMoverGrabar())


def pmMoverGrabarTodos():
    return PM(228264,229308)


def MoverGrabarTodos():
    return QtGui.QIcon(pmMoverGrabarTodos())


def pmMoverJugar():
    return PM(218341,219172)


def MoverJugar():
    return QtGui.QIcon(pmMoverJugar())


def pmPelicula():
    return PM(229308,231442)


def Pelicula():
    return QtGui.QIcon(pmPelicula())


def pmPelicula_Pausa():
    return PM(231442,233201)


def Pelicula_Pausa():
    return QtGui.QIcon(pmPelicula_Pausa())


def pmPelicula_Seguir():
    return PM(233201,235290)


def Pelicula_Seguir():
    return QtGui.QIcon(pmPelicula_Seguir())


def pmPelicula_Rapido():
    return PM(235290,237349)


def Pelicula_Rapido():
    return QtGui.QIcon(pmPelicula_Rapido())


def pmPelicula_Lento():
    return PM(237349,239224)


def Pelicula_Lento():
    return QtGui.QIcon(pmPelicula_Lento())


def pmPelicula_Repetir():
    return PM(38040,40334)


def Pelicula_Repetir():
    return QtGui.QIcon(pmPelicula_Repetir())


def pmPelicula_PGN():
    return PM(239224,240132)


def Pelicula_PGN():
    return QtGui.QIcon(pmPelicula_PGN())


def pmMemoria():
    return PM(240132,242073)


def Memoria():
    return QtGui.QIcon(pmMemoria())


def pmEntrenar():
    return PM(242073,243612)


def Entrenar():
    return QtGui.QIcon(pmEntrenar())


def pmEnviar():
    return PM(242073,243612)


def Enviar():
    return QtGui.QIcon(pmEnviar())


def pmBoxRooms():
    return PM(243612,248415)


def BoxRooms():
    return QtGui.QIcon(pmBoxRooms())


def pmBoxRoom():
    return PM(248415,248877)


def BoxRoom():
    return QtGui.QIcon(pmBoxRoom())


def pmNewBoxRoom():
    return PM(248877,250385)


def NewBoxRoom():
    return QtGui.QIcon(pmNewBoxRoom())


def pmNuevoMas():
    return PM(248877,250385)


def NuevoMas():
    return QtGui.QIcon(pmNuevoMas())


def pmTemas():
    return PM(250385,252608)


def Temas():
    return QtGui.QIcon(pmTemas())


def pmTutorialesCrear():
    return PM(252608,258877)


def TutorialesCrear():
    return QtGui.QIcon(pmTutorialesCrear())


def pmMover():
    return PM(258877,259459)


def Mover():
    return QtGui.QIcon(pmMover())


def pmSeleccionar():
    return PM(259459,265163)


def Seleccionar():
    return QtGui.QIcon(pmSeleccionar())


def pmVista():
    return PM(265163,267087)


def Vista():
    return QtGui.QIcon(pmVista())


def pmInformacionPGNUno():
    return PM(267087,268465)


def InformacionPGNUno():
    return QtGui.QIcon(pmInformacionPGNUno())


def pmDailyTest():
    return PM(268465,270805)


def DailyTest():
    return QtGui.QIcon(pmDailyTest())


def pmJuegaPorMi():
    return PM(270805,272525)


def JuegaPorMi():
    return QtGui.QIcon(pmJuegaPorMi())


def pmArbol():
    return PM(272525,273159)


def Arbol():
    return QtGui.QIcon(pmArbol())


def pmGrabarFichero():
    return PM(68134,69597)


def GrabarFichero():
    return QtGui.QIcon(pmGrabarFichero())


def pmClipboard():
    return PM(273159,273937)


def Clipboard():
    return QtGui.QIcon(pmClipboard())


def pmFics():
    return PM(273937,274354)


def Fics():
    return QtGui.QIcon(pmFics())


def pmFide():
    return PM(9646,11623)


def Fide():
    return QtGui.QIcon(pmFide())


def pmFichPGN():
    return PM(26140,27888)


def FichPGN():
    return QtGui.QIcon(pmFichPGN())


def pmFlechas():
    return PM(274354,277706)


def Flechas():
    return QtGui.QIcon(pmFlechas())


def pmMarcos():
    return PM(277706,279153)


def Marcos():
    return QtGui.QIcon(pmMarcos())


def pmSVGs():
    return PM(279153,282722)


def SVGs():
    return QtGui.QIcon(pmSVGs())


def pmAmarillo():
    return PM(282722,283974)


def Amarillo():
    return QtGui.QIcon(pmAmarillo())


def pmNaranja():
    return PM(283974,285206)


def Naranja():
    return QtGui.QIcon(pmNaranja())


def pmVerde():
    return PM(285206,286482)


def Verde():
    return QtGui.QIcon(pmVerde())


def pmAzul():
    return PM(286482,287570)


def Azul():
    return QtGui.QIcon(pmAzul())


def pmMagenta():
    return PM(287570,288858)


def Magenta():
    return QtGui.QIcon(pmMagenta())


def pmRojo():
    return PM(288858,290077)


def Rojo():
    return QtGui.QIcon(pmRojo())


def pmGris():
    return PM(290077,291035)


def Gris():
    return QtGui.QIcon(pmGris())


def pmAmarillo32():
    return PM(291035,293015)


def Amarillo32():
    return QtGui.QIcon(pmAmarillo32())


def pmNaranja32():
    return PM(293015,295139)


def Naranja32():
    return QtGui.QIcon(pmNaranja32())


def pmVerde32():
    return PM(295139,297260)


def Verde32():
    return QtGui.QIcon(pmVerde32())


def pmAzul32():
    return PM(297260,299639)


def Azul32():
    return QtGui.QIcon(pmAzul32())


def pmMagenta32():
    return PM(299639,302090)


def Magenta32():
    return QtGui.QIcon(pmMagenta32())


def pmRojo32():
    return PM(302090,303905)


def Rojo32():
    return QtGui.QIcon(pmRojo32())


def pmGris32():
    return PM(303905,305819)


def Gris32():
    return QtGui.QIcon(pmGris32())


def pmPuntoBlanco():
    return PM(305819,306168)


def PuntoBlanco():
    return QtGui.QIcon(pmPuntoBlanco())


def pmPuntoAmarillo():
    return PM(221162,221624)


def PuntoAmarillo():
    return QtGui.QIcon(pmPuntoAmarillo())


def pmPuntoNaranja():
    return PM(306168,306630)


def PuntoNaranja():
    return QtGui.QIcon(pmPuntoNaranja())


def pmPuntoVerde():
    return PM(221947,222409)


def PuntoVerde():
    return QtGui.QIcon(pmPuntoVerde())


def pmPuntoAzul():
    return PM(248415,248877)


def PuntoAzul():
    return QtGui.QIcon(pmPuntoAzul())


def pmPuntoMagenta():
    return PM(306630,307129)


def PuntoMagenta():
    return QtGui.QIcon(pmPuntoMagenta())


def pmPuntoRojo():
    return PM(307129,307628)


def PuntoRojo():
    return QtGui.QIcon(pmPuntoRojo())


def pmPuntoNegro():
    return PM(221624,221947)


def PuntoNegro():
    return QtGui.QIcon(pmPuntoNegro())


def pmPuntoEstrella():
    return PM(307628,308055)


def PuntoEstrella():
    return QtGui.QIcon(pmPuntoEstrella())


def pmComentario():
    return PM(308055,308692)


def Comentario():
    return QtGui.QIcon(pmComentario())


def pmComentarioMas():
    return PM(308692,309631)


def ComentarioMas():
    return QtGui.QIcon(pmComentarioMas())


def pmComentarioEditar():
    return PM(227408,228264)


def ComentarioEditar():
    return QtGui.QIcon(pmComentarioEditar())


def pmOpeningComentario():
    return PM(309631,310627)


def OpeningComentario():
    return QtGui.QIcon(pmOpeningComentario())


def pmMas():
    return PM(310627,311136)


def Mas():
    return QtGui.QIcon(pmMas())


def pmMasR():
    return PM(311136,311624)


def MasR():
    return QtGui.QIcon(pmMasR())


def pmMasDoc():
    return PM(311624,312425)


def MasDoc():
    return QtGui.QIcon(pmMasDoc())


def pmPotencia():
    return PM(184620,185486)


def Potencia():
    return QtGui.QIcon(pmPotencia())


def pmBMT():
    return PM(312425,313303)


def BMT():
    return QtGui.QIcon(pmBMT())


def pmOjo():
    return PM(313303,314425)


def Ojo():
    return QtGui.QIcon(pmOjo())


def pmOcultar():
    return PM(313303,314425)


def Ocultar():
    return QtGui.QIcon(pmOcultar())


def pmMostrar():
    return PM(314425,315481)


def Mostrar():
    return QtGui.QIcon(pmMostrar())


def pmBlog():
    return PM(315481,316003)


def Blog():
    return QtGui.QIcon(pmBlog())


def pmVariations():
    return PM(316003,316910)


def Variations():
    return QtGui.QIcon(pmVariations())


def pmVariationsG():
    return PM(316910,319337)


def VariationsG():
    return QtGui.QIcon(pmVariationsG())


def pmCambiar():
    return PM(319337,321051)


def Cambiar():
    return QtGui.QIcon(pmCambiar())


def pmAnterior():
    return PM(321051,323105)


def Anterior():
    return QtGui.QIcon(pmAnterior())


def pmSiguiente():
    return PM(323105,325175)


def Siguiente():
    return QtGui.QIcon(pmSiguiente())


def pmSiguienteF():
    return PM(325175,327350)


def SiguienteF():
    return QtGui.QIcon(pmSiguienteF())


def pmAnteriorF():
    return PM(327350,329544)


def AnteriorF():
    return QtGui.QIcon(pmAnteriorF())


def pmX():
    return PM(329544,330826)


def X():
    return QtGui.QIcon(pmX())


def pmTools():
    return PM(330826,333427)


def Tools():
    return QtGui.QIcon(pmTools())


def pmTacticas():
    return PM(333427,336000)


def Tacticas():
    return QtGui.QIcon(pmTacticas())


def pmCancelarPeque():
    return PM(336000,336562)


def CancelarPeque():
    return QtGui.QIcon(pmCancelarPeque())


def pmAceptarPeque():
    return PM(222409,223426)


def AceptarPeque():
    return QtGui.QIcon(pmAceptarPeque())


def pmP_16c():
    return PM(336562,337086)


def P_16c():
    return QtGui.QIcon(pmP_16c())


def pmLibre():
    return PM(337086,339478)


def Libre():
    return QtGui.QIcon(pmLibre())


def pmEnBlanco():
    return PM(339478,340204)


def EnBlanco():
    return QtGui.QIcon(pmEnBlanco())


def pmDirector():
    return PM(340204,343178)


def Director():
    return QtGui.QIcon(pmDirector())


def pmTorneos():
    return PM(343178,344916)


def Torneos():
    return QtGui.QIcon(pmTorneos())


def pmOpenings():
    return PM(344916,345841)


def Openings():
    return QtGui.QIcon(pmOpenings())


def pmV_Blancas():
    return PM(345841,346121)


def V_Blancas():
    return QtGui.QIcon(pmV_Blancas())


def pmV_Blancas_Mas():
    return PM(346121,346401)


def V_Blancas_Mas():
    return QtGui.QIcon(pmV_Blancas_Mas())


def pmV_Blancas_Mas_Mas():
    return PM(346401,346673)


def V_Blancas_Mas_Mas():
    return QtGui.QIcon(pmV_Blancas_Mas_Mas())


def pmV_Negras():
    return PM(346673,346948)


def V_Negras():
    return QtGui.QIcon(pmV_Negras())


def pmV_Negras_Mas():
    return PM(346948,347223)


def V_Negras_Mas():
    return QtGui.QIcon(pmV_Negras_Mas())


def pmV_Negras_Mas_Mas():
    return PM(347223,347492)


def V_Negras_Mas_Mas():
    return QtGui.QIcon(pmV_Negras_Mas_Mas())


def pmV_Blancas_Igual_Negras():
    return PM(347492,347794)


def V_Blancas_Igual_Negras():
    return QtGui.QIcon(pmV_Blancas_Igual_Negras())


def pmMezclar():
    return PM(142655,145051)


def Mezclar():
    return QtGui.QIcon(pmMezclar())


def pmVoyager():
    return PM(347794,349756)


def Voyager():
    return QtGui.QIcon(pmVoyager())


def pmReindexar():
    return PM(349756,351573)


def Reindexar():
    return QtGui.QIcon(pmReindexar())


def pmRename():
    return PM(351573,352557)


def Rename():
    return QtGui.QIcon(pmRename())


def pmAdd():
    return PM(352557,353510)


def Add():
    return QtGui.QIcon(pmAdd())


def pmMas22():
    return PM(353510,354174)


def Mas22():
    return QtGui.QIcon(pmMas22())


def pmMenos22():
    return PM(354174,354618)


def Menos22():
    return QtGui.QIcon(pmMenos22())


def pmTransposition():
    return PM(354618,355137)


def Transposition():
    return QtGui.QIcon(pmTransposition())


def pmRat():
    return PM(355137,360841)


def Rat():
    return QtGui.QIcon(pmRat())


def pmAlligator():
    return PM(360841,365833)


def Alligator():
    return QtGui.QIcon(pmAlligator())


def pmAnt():
    return PM(365833,372531)


def Ant():
    return QtGui.QIcon(pmAnt())


def pmBat():
    return PM(372531,375485)


def Bat():
    return QtGui.QIcon(pmBat())


def pmBear():
    return PM(375485,382764)


def Bear():
    return QtGui.QIcon(pmBear())


def pmBee():
    return PM(382764,387766)


def Bee():
    return QtGui.QIcon(pmBee())


def pmBird():
    return PM(387766,393825)


def Bird():
    return QtGui.QIcon(pmBird())


def pmBull():
    return PM(393825,400794)


def Bull():
    return QtGui.QIcon(pmBull())


def pmBulldog():
    return PM(400794,407685)


def Bulldog():
    return QtGui.QIcon(pmBulldog())


def pmButterfly():
    return PM(407685,415059)


def Butterfly():
    return QtGui.QIcon(pmButterfly())


def pmCat():
    return PM(415059,421331)


def Cat():
    return QtGui.QIcon(pmCat())


def pmChicken():
    return PM(421331,427142)


def Chicken():
    return QtGui.QIcon(pmChicken())


def pmCow():
    return PM(427142,433885)


def Cow():
    return QtGui.QIcon(pmCow())


def pmCrab():
    return PM(433885,439474)


def Crab():
    return QtGui.QIcon(pmCrab())


def pmCrocodile():
    return PM(439474,445615)


def Crocodile():
    return QtGui.QIcon(pmCrocodile())


def pmDeer():
    return PM(445615,451922)


def Deer():
    return QtGui.QIcon(pmDeer())


def pmDog():
    return PM(451922,458525)


def Dog():
    return QtGui.QIcon(pmDog())


def pmDonkey():
    return PM(458525,464172)


def Donkey():
    return QtGui.QIcon(pmDonkey())


def pmDuck():
    return PM(464172,470715)


def Duck():
    return QtGui.QIcon(pmDuck())


def pmEagle():
    return PM(470715,475533)


def Eagle():
    return QtGui.QIcon(pmEagle())


def pmElephant():
    return PM(475533,482014)


def Elephant():
    return QtGui.QIcon(pmElephant())


def pmFish():
    return PM(482014,488855)


def Fish():
    return QtGui.QIcon(pmFish())


def pmFox():
    return PM(488855,495638)


def Fox():
    return QtGui.QIcon(pmFox())


def pmFrog():
    return PM(495638,502054)


def Frog():
    return QtGui.QIcon(pmFrog())


def pmGiraffe():
    return PM(502054,509232)


def Giraffe():
    return QtGui.QIcon(pmGiraffe())


def pmGorilla():
    return PM(509232,515771)


def Gorilla():
    return QtGui.QIcon(pmGorilla())


def pmHippo():
    return PM(515771,522892)


def Hippo():
    return QtGui.QIcon(pmHippo())


def pmHorse():
    return PM(522892,529439)


def Horse():
    return QtGui.QIcon(pmHorse())


def pmInsect():
    return PM(529439,535374)


def Insect():
    return QtGui.QIcon(pmInsect())


def pmLion():
    return PM(535374,544284)


def Lion():
    return QtGui.QIcon(pmLion())


def pmMonkey():
    return PM(544284,551963)


def Monkey():
    return QtGui.QIcon(pmMonkey())


def pmMoose():
    return PM(551963,558587)


def Moose():
    return QtGui.QIcon(pmMoose())


def pmMouse():
    return PM(355137,360841)


def Mouse():
    return QtGui.QIcon(pmMouse())


def pmOwl():
    return PM(558587,565293)


def Owl():
    return QtGui.QIcon(pmOwl())


def pmPanda():
    return PM(565293,569327)


def Panda():
    return QtGui.QIcon(pmPanda())


def pmPenguin():
    return PM(569327,574876)


def Penguin():
    return QtGui.QIcon(pmPenguin())


def pmPig():
    return PM(574876,582916)


def Pig():
    return QtGui.QIcon(pmPig())


def pmRabbit():
    return PM(582916,590217)


def Rabbit():
    return QtGui.QIcon(pmRabbit())


def pmRhino():
    return PM(590217,596604)


def Rhino():
    return QtGui.QIcon(pmRhino())


def pmRooster():
    return PM(596604,601867)


def Rooster():
    return QtGui.QIcon(pmRooster())


def pmShark():
    return PM(601867,607637)


def Shark():
    return QtGui.QIcon(pmShark())


def pmSheep():
    return PM(607637,611468)


def Sheep():
    return QtGui.QIcon(pmSheep())


def pmSnake():
    return PM(611468,617493)


def Snake():
    return QtGui.QIcon(pmSnake())


def pmTiger():
    return PM(617493,625530)


def Tiger():
    return QtGui.QIcon(pmTiger())


def pmTurkey():
    return PM(625530,632944)


def Turkey():
    return QtGui.QIcon(pmTurkey())


def pmTurtle():
    return PM(632944,639665)


def Turtle():
    return QtGui.QIcon(pmTurtle())


def pmWolf():
    return PM(639665,642760)


def Wolf():
    return QtGui.QIcon(pmWolf())


def pmSteven():
    return PM(642760,649912)


def Steven():
    return QtGui.QIcon(pmSteven())


def pmWheel():
    return PM(649912,657977)


def Wheel():
    return QtGui.QIcon(pmWheel())


def pmWheelchair():
    return PM(657977,666781)


def Wheelchair():
    return QtGui.QIcon(pmWheelchair())


def pmTouringMotorcycle():
    return PM(666781,673093)


def TouringMotorcycle():
    return QtGui.QIcon(pmTouringMotorcycle())


def pmContainer():
    return PM(673093,678428)


def Container():
    return QtGui.QIcon(pmContainer())


def pmBoatEquipment():
    return PM(678428,683951)


def BoatEquipment():
    return QtGui.QIcon(pmBoatEquipment())


def pmCar():
    return PM(683951,688597)


def Car():
    return QtGui.QIcon(pmCar())


def pmLorry():
    return PM(688597,694633)


def Lorry():
    return QtGui.QIcon(pmLorry())


def pmCarTrailer():
    return PM(694633,698730)


def CarTrailer():
    return QtGui.QIcon(pmCarTrailer())


def pmTowTruck():
    return PM(698730,703488)


def TowTruck():
    return QtGui.QIcon(pmTowTruck())


def pmQuadBike():
    return PM(703488,709457)


def QuadBike():
    return QtGui.QIcon(pmQuadBike())


def pmRecoveryTruck():
    return PM(709457,714454)


def RecoveryTruck():
    return QtGui.QIcon(pmRecoveryTruck())


def pmContainerLoader():
    return PM(714454,719596)


def ContainerLoader():
    return QtGui.QIcon(pmContainerLoader())


def pmPoliceCar():
    return PM(719596,724428)


def PoliceCar():
    return QtGui.QIcon(pmPoliceCar())


def pmExecutiveCar():
    return PM(724428,729106)


def ExecutiveCar():
    return QtGui.QIcon(pmExecutiveCar())


def pmTruck():
    return PM(729106,734569)


def Truck():
    return QtGui.QIcon(pmTruck())


def pmExcavator():
    return PM(734569,739460)


def Excavator():
    return QtGui.QIcon(pmExcavator())


def pmCabriolet():
    return PM(739460,744298)


def Cabriolet():
    return QtGui.QIcon(pmCabriolet())


def pmMixerTruck():
    return PM(744298,750608)


def MixerTruck():
    return QtGui.QIcon(pmMixerTruck())


def pmForkliftTruckLoaded():
    return PM(750608,756756)


def ForkliftTruckLoaded():
    return QtGui.QIcon(pmForkliftTruckLoaded())


def pmAmbulance():
    return PM(756756,762806)


def Ambulance():
    return QtGui.QIcon(pmAmbulance())


def pmDieselLocomotiveBoxcar():
    return PM(762806,766812)


def DieselLocomotiveBoxcar():
    return QtGui.QIcon(pmDieselLocomotiveBoxcar())


def pmTractorUnit():
    return PM(766812,772279)


def TractorUnit():
    return QtGui.QIcon(pmTractorUnit())


def pmFireTruck():
    return PM(772279,778618)


def FireTruck():
    return QtGui.QIcon(pmFireTruck())


def pmCargoShip():
    return PM(778618,782959)


def CargoShip():
    return QtGui.QIcon(pmCargoShip())


def pmSubwayTrain():
    return PM(782959,787849)


def SubwayTrain():
    return QtGui.QIcon(pmSubwayTrain())


def pmTruckMountedCrane():
    return PM(787849,793590)


def TruckMountedCrane():
    return QtGui.QIcon(pmTruckMountedCrane())


def pmAirAmbulance():
    return PM(793590,798703)


def AirAmbulance():
    return QtGui.QIcon(pmAirAmbulance())


def pmAirplane():
    return PM(798703,803591)


def Airplane():
    return QtGui.QIcon(pmAirplane())


def pmCaracol():
    return PM(803591,805407)


def Caracol():
    return QtGui.QIcon(pmCaracol())


def pmUno():
    return PM(805407,807869)


def Uno():
    return QtGui.QIcon(pmUno())


def pmMotoresExternos():
    return PM(807869,809771)


def MotoresExternos():
    return QtGui.QIcon(pmMotoresExternos())


def pmDatabase():
    return PM(809771,811087)


def Database():
    return QtGui.QIcon(pmDatabase())


def pmDatabaseMas():
    return PM(811087,812546)


def DatabaseMas():
    return QtGui.QIcon(pmDatabaseMas())


def pmDatabaseImport():
    return PM(812546,813182)


def DatabaseImport():
    return QtGui.QIcon(pmDatabaseImport())


def pmDatabaseExport():
    return PM(813182,813827)


def DatabaseExport():
    return QtGui.QIcon(pmDatabaseExport())


def pmDatabaseDelete():
    return PM(813827,814950)


def DatabaseDelete():
    return QtGui.QIcon(pmDatabaseDelete())


def pmDatabaseMaintenance():
    return PM(814950,816446)


def DatabaseMaintenance():
    return QtGui.QIcon(pmDatabaseMaintenance())


def pmAtacante():
    return PM(816446,817051)


def Atacante():
    return QtGui.QIcon(pmAtacante())


def pmAtacada():
    return PM(817051,817617)


def Atacada():
    return QtGui.QIcon(pmAtacada())


def pmGoToNext():
    return PM(817617,818029)


def GoToNext():
    return QtGui.QIcon(pmGoToNext())


def pmBlancas():
    return PM(818029,818380)


def Blancas():
    return QtGui.QIcon(pmBlancas())


def pmNegras():
    return PM(818380,818626)


def Negras():
    return QtGui.QIcon(pmNegras())


def pmFolderChange():
    return PM(71649,74407)


def FolderChange():
    return QtGui.QIcon(pmFolderChange())


def pmMarkers():
    return PM(818626,820321)


def Markers():
    return QtGui.QIcon(pmMarkers())


def pmTop():
    return PM(820321,820905)


def Top():
    return QtGui.QIcon(pmTop())


def pmBottom():
    return PM(820905,821494)


def Bottom():
    return QtGui.QIcon(pmBottom())


def pmSTS():
    return PM(821494,823685)


def STS():
    return QtGui.QIcon(pmSTS())


def pmRun():
    return PM(823685,825409)


def Run():
    return QtGui.QIcon(pmRun())


def pmRun2():
    return PM(825409,826929)


def Run2():
    return QtGui.QIcon(pmRun2())


def pmWorldMap():
    return PM(826929,829670)


def WorldMap():
    return QtGui.QIcon(pmWorldMap())


def pmAfrica():
    return PM(829670,832156)


def Africa():
    return QtGui.QIcon(pmAfrica())


def pmMaps():
    return PM(832156,833100)


def Maps():
    return QtGui.QIcon(pmMaps())


def pmSol():
    return PM(833100,834026)


def Sol():
    return QtGui.QIcon(pmSol())


def pmSolNubes():
    return PM(834026,834889)


def SolNubes():
    return QtGui.QIcon(pmSolNubes())


def pmSolNubesLluvia():
    return PM(834889,835849)


def SolNubesLluvia():
    return QtGui.QIcon(pmSolNubesLluvia())


def pmLluvia():
    return PM(835849,836688)


def Lluvia():
    return QtGui.QIcon(pmLluvia())


def pmInvierno():
    return PM(836688,838264)


def Invierno():
    return QtGui.QIcon(pmInvierno())


def pmFixedElo():
    return PM(164966,166229)


def FixedElo():
    return QtGui.QIcon(pmFixedElo())


def pmSoundTool():
    return PM(838264,840723)


def SoundTool():
    return QtGui.QIcon(pmSoundTool())


def pmVoyager1():
    return PM(840723,843173)


def Voyager1():
    return QtGui.QIcon(pmVoyager1())


def pmTrain():
    return PM(843173,844543)


def Train():
    return QtGui.QIcon(pmTrain())


def pmPlay():
    return PM(233201,235290)


def Play():
    return QtGui.QIcon(pmPlay())


def pmMeasure():
    return PM(126751,128374)


def Measure():
    return QtGui.QIcon(pmMeasure())


def pmPlayGame():
    return PM(844543,848901)


def PlayGame():
    return QtGui.QIcon(pmPlayGame())


def pmScanner():
    return PM(848901,849242)


def Scanner():
    return QtGui.QIcon(pmScanner())


def pmMenos():
    return PM(849242,849767)


def Menos():
    return QtGui.QIcon(pmMenos())


def pmSchool():
    return PM(849767,851129)


def School():
    return QtGui.QIcon(pmSchool())


def pmLaw():
    return PM(851129,851745)


def Law():
    return QtGui.QIcon(pmLaw())


def pmLearnGame():
    return PM(851745,852178)


def LearnGame():
    return QtGui.QIcon(pmLearnGame())


def pmLonghaul():
    return PM(852178,853104)


def Longhaul():
    return QtGui.QIcon(pmLonghaul())


def pmTrekking():
    return PM(853104,853798)


def Trekking():
    return QtGui.QIcon(pmTrekking())


def pmPassword():
    return PM(853798,854251)


def Password():
    return QtGui.QIcon(pmPassword())


def pmSQL_RAW():
    return PM(844543,848901)


def SQL_RAW():
    return QtGui.QIcon(pmSQL_RAW())


def pmSun():
    return PM(312425,313303)


def Sun():
    return QtGui.QIcon(pmSun())


def pmLight32():
    return PM(854251,855951)


def Light32():
    return QtGui.QIcon(pmLight32())


def pmTOL():
    return PM(855951,856660)


def TOL():
    return QtGui.QIcon(pmTOL())


def pmUned():
    return PM(856660,857080)


def Uned():
    return QtGui.QIcon(pmUned())


def pmUwe():
    return PM(857080,858049)


def Uwe():
    return QtGui.QIcon(pmUwe())


def pmThinking():
    return PM(858049,858838)


def Thinking():
    return QtGui.QIcon(pmThinking())


def pmWashingMachine():
    return PM(858838,859501)


def WashingMachine():
    return QtGui.QIcon(pmWashingMachine())


def pmTerminal():
    return PM(859501,863045)


def Terminal():
    return QtGui.QIcon(pmTerminal())


def pmManualSave():
    return PM(863045,863628)


def ManualSave():
    return QtGui.QIcon(pmManualSave())


def pmSettings():
    return PM(863628,864066)


def Settings():
    return QtGui.QIcon(pmSettings())


def pmStrength():
    return PM(864066,864737)


def Strength():
    return QtGui.QIcon(pmStrength())


def pmSingular():
    return PM(864737,865592)


def Singular():
    return QtGui.QIcon(pmSingular())


def pmScript():
    return PM(865592,866161)


def Script():
    return QtGui.QIcon(pmScript())


def pmTexto():
    return PM(866161,869006)


def Texto():
    return QtGui.QIcon(pmTexto())


def pmLampara():
    return PM(869006,869715)


def Lampara():
    return QtGui.QIcon(pmLampara())


def pmFile():
    return PM(869715,872015)


def File():
    return QtGui.QIcon(pmFile())


def pmCalculo():
    return PM(872015,872941)


def Calculo():
    return QtGui.QIcon(pmCalculo())


def pmOpeningLines():
    return PM(872941,873619)


def OpeningLines():
    return QtGui.QIcon(pmOpeningLines())


def pmStudy():
    return PM(873619,874532)


def Study():
    return QtGui.QIcon(pmStudy())


def pmLichess():
    return PM(874532,875422)


def Lichess():
    return QtGui.QIcon(pmLichess())


def pmMiniatura():
    return PM(875422,876349)


def Miniatura():
    return QtGui.QIcon(pmMiniatura())


def pmLocomotora():
    return PM(876349,877130)


def Locomotora():
    return QtGui.QIcon(pmLocomotora())


def pmTrainSequential():
    return PM(877130,878271)


def TrainSequential():
    return QtGui.QIcon(pmTrainSequential())


def pmTrainStatic():
    return PM(878271,879231)


def TrainStatic():
    return QtGui.QIcon(pmTrainStatic())


def pmTrainPositions():
    return PM(879231,880212)


def TrainPositions():
    return QtGui.QIcon(pmTrainPositions())


def pmTrainEngines():
    return PM(880212,881646)


def TrainEngines():
    return QtGui.QIcon(pmTrainEngines())


def pmError():
    return PM(48833,52833)


def Error():
    return QtGui.QIcon(pmError())


def pmAtajos():
    return PM(881646,882825)


def Atajos():
    return QtGui.QIcon(pmAtajos())


def pmTOLline():
    return PM(882825,883929)


def TOLline():
    return QtGui.QIcon(pmTOLline())


def pmTOLchange():
    return PM(883929,886151)


def TOLchange():
    return QtGui.QIcon(pmTOLchange())


def pmPack():
    return PM(886151,887324)


def Pack():
    return QtGui.QIcon(pmPack())


def pmHome():
    return PM(179976,181158)


def Home():
    return QtGui.QIcon(pmHome())


def pmImport8():
    return PM(887324,888082)


def Import8():
    return QtGui.QIcon(pmImport8())


def pmExport8():
    return PM(888082,888707)


def Export8():
    return QtGui.QIcon(pmExport8())


def pmTablas8():
    return PM(888707,889499)


def Tablas8():
    return QtGui.QIcon(pmTablas8())


def pmBlancas8():
    return PM(889499,890529)


def Blancas8():
    return QtGui.QIcon(pmBlancas8())


def pmNegras8():
    return PM(890529,891368)


def Negras8():
    return QtGui.QIcon(pmNegras8())


def pmBook():
    return PM(891368,891942)


def Book():
    return QtGui.QIcon(pmBook())


def pmWrite():
    return PM(891942,893147)


def Write():
    return QtGui.QIcon(pmWrite())


def pmAlt():
    return PM(893147,893589)


def Alt():
    return QtGui.QIcon(pmAlt())


def pmShift():
    return PM(893589,893929)


def Shift():
    return QtGui.QIcon(pmShift())


def pmRightMouse():
    return PM(893929,894729)


def RightMouse():
    return QtGui.QIcon(pmRightMouse())


def pmControl():
    return PM(894729,895254)


def Control():
    return QtGui.QIcon(pmControl())


def pmFinales():
    return PM(895254,896341)


def Finales():
    return QtGui.QIcon(pmFinales())


def pmEditColumns():
    return PM(896341,897073)


def EditColumns():
    return QtGui.QIcon(pmEditColumns())


def pmResizeAll():
    return PM(897073,897583)


def ResizeAll():
    return QtGui.QIcon(pmResizeAll())


def pmChecked():
    return PM(897583,898089)


def Checked():
    return QtGui.QIcon(pmChecked())


def pmUnchecked():
    return PM(898089,898337)


def Unchecked():
    return QtGui.QIcon(pmUnchecked())


def pmBuscarC():
    return PM(898337,898781)


def BuscarC():
    return QtGui.QIcon(pmBuscarC())


def pmPeonBlanco():
    return PM(898781,900962)


def PeonBlanco():
    return QtGui.QIcon(pmPeonBlanco())


def pmPeonNegro():
    return PM(900962,902486)


def PeonNegro():
    return QtGui.QIcon(pmPeonNegro())


def pmReciclar():
    return PM(902486,903210)


def Reciclar():
    return QtGui.QIcon(pmReciclar())


def pmLanzamiento():
    return PM(903210,903923)


def Lanzamiento():
    return QtGui.QIcon(pmLanzamiento())


def pmEndGame():
    return PM(903923,904337)


def EndGame():
    return QtGui.QIcon(pmEndGame())


def pmPause():
    return PM(904337,905206)


def Pause():
    return QtGui.QIcon(pmPause())


def pmContinue():
    return PM(905206,906410)


def Continue():
    return QtGui.QIcon(pmContinue())


def pmClose():
    return PM(906410,907109)


def Close():
    return QtGui.QIcon(pmClose())


def pmStop():
    return PM(907109,908142)


def Stop():
    return QtGui.QIcon(pmStop())


def pmFactoryPolyglot():
    return PM(908142,908962)


def FactoryPolyglot():
    return QtGui.QIcon(pmFactoryPolyglot())


def pmTags():
    return PM(908962,909785)


def Tags():
    return QtGui.QIcon(pmTags())


def pmAppearance():
    return PM(909785,910512)


def Appearance():
    return QtGui.QIcon(pmAppearance())


def pmFill():
    return PM(910512,911550)


def Fill():
    return QtGui.QIcon(pmFill())


def pmSupport():
    return PM(911550,912282)


def Support():
    return QtGui.QIcon(pmSupport())


def pmOrder():
    return PM(912282,913080)


def Order():
    return QtGui.QIcon(pmOrder())


def pmPlay1():
    return PM(913080,914375)


def Play1():
    return QtGui.QIcon(pmPlay1())


def pmRemove1():
    return PM(914375,915502)


def Remove1():
    return QtGui.QIcon(pmRemove1())


def pmNew1():
    return PM(915502,915824)


def New1():
    return QtGui.QIcon(pmNew1())


def pmMensError():
    return PM(915824,917888)


def MensError():
    return QtGui.QIcon(pmMensError())


def pmMensInfo():
    return PM(917888,920443)


def MensInfo():
    return QtGui.QIcon(pmMensInfo())


def pmJump():
    return PM(920443,921118)


def Jump():
    return QtGui.QIcon(pmJump())


def pmCaptures():
    return PM(921118,922299)


def Captures():
    return QtGui.QIcon(pmCaptures())


def pmRepeat():
    return PM(922299,922958)


def Repeat():
    return QtGui.QIcon(pmRepeat())


def pmCount():
    return PM(922958,923634)


def Count():
    return QtGui.QIcon(pmCount())


def pmMate15():
    return PM(923634,924705)


def Mate15():
    return QtGui.QIcon(pmMate15())


def pmCoordinates():
    return PM(924705,925858)


def Coordinates():
    return QtGui.QIcon(pmCoordinates())


def pmKnight():
    return PM(925858,927101)


def Knight():
    return QtGui.QIcon(pmKnight())


def pmCorrecto():
    return PM(927101,928127)


def Correcto():
    return QtGui.QIcon(pmCorrecto())


def pmBlocks():
    return PM(928127,928464)


def Blocks():
    return QtGui.QIcon(pmBlocks())


def pmWest():
    return PM(928464,929570)


def West():
    return QtGui.QIcon(pmWest())


def pmOpening():
    return PM(929570,929828)


def Opening():
    return QtGui.QIcon(pmOpening())


def pmVariation():
    return PM(225372,225790)


def Variation():
    return QtGui.QIcon(pmVariation())


def pmComment():
    return PM(929828,930191)


def Comment():
    return QtGui.QIcon(pmComment())


def pmVariationComment():
    return PM(930191,930535)


def VariationComment():
    return QtGui.QIcon(pmVariationComment())


def pmOpeningVariation():
    return PM(930535,930999)


def OpeningVariation():
    return QtGui.QIcon(pmOpeningVariation())


def pmOpeningComment():
    return PM(930999,931332)


def OpeningComment():
    return QtGui.QIcon(pmOpeningComment())


def pmOpeningVariationComment():
    return PM(930535,930999)


def OpeningVariationComment():
    return QtGui.QIcon(pmOpeningVariationComment())


