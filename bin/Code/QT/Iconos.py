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


def pmPartidaOriginal():
    return PM(9646,11623)


def PartidaOriginal():
    return QtGui.QIcon(pmPartidaOriginal())


def pmDGT():
    return PM(11623,12617)


def DGT():
    return QtGui.QIcon(pmDGT())


def pmDGTB():
    return PM(12617,14041)


def DGTB():
    return QtGui.QIcon(pmDGTB())


def pmMillenium():
    return PM(14041,15278)


def Millenium():
    return QtGui.QIcon(pmMillenium())


def pmCertabo():
    return PM(15278,15991)


def Certabo():
    return QtGui.QIcon(pmCertabo())


def pmNovag():
    return PM(15991,16735)


def Novag():
    return QtGui.QIcon(pmNovag())


def pmFindAllMoves():
    return PM(16735,18331)


def FindAllMoves():
    return QtGui.QIcon(pmFindAllMoves())


def pmResizeBoard():
    return PM(16735,18331)


def ResizeBoard():
    return QtGui.QIcon(pmResizeBoard())


def pmMensEspera():
    return PM(18331,22079)


def MensEspera():
    return QtGui.QIcon(pmMensEspera())


def pmUtilidades():
    return PM(22079,28508)


def Utilidades():
    return QtGui.QIcon(pmUtilidades())


def pmTerminar():
    return PM(28508,30258)


def Terminar():
    return QtGui.QIcon(pmTerminar())


def pmNuevaPartida():
    return PM(30258,32006)


def NuevaPartida():
    return QtGui.QIcon(pmNuevaPartida())


def pmOpciones():
    return PM(32006,33734)


def Opciones():
    return QtGui.QIcon(pmOpciones())


def pmEntrenamiento():
    return PM(7617,9646)


def Entrenamiento():
    return QtGui.QIcon(pmEntrenamiento())


def pmAplazar():
    return PM(33734,36801)


def Aplazar():
    return QtGui.QIcon(pmAplazar())


def pmAplazamientos():
    return PM(36801,40117)


def Aplazamientos():
    return QtGui.QIcon(pmAplazamientos())


def pmCapturas():
    return PM(40117,42158)


def Capturas():
    return QtGui.QIcon(pmCapturas())


def pmReiniciar():
    return PM(42158,44452)


def Reiniciar():
    return QtGui.QIcon(pmReiniciar())


def pmMotores():
    return PM(44452,50351)


def Motores():
    return QtGui.QIcon(pmMotores())


def pmImportarGM():
    return PM(50351,52951)


def ImportarGM():
    return QtGui.QIcon(pmImportarGM())


def pmAbandonar():
    return PM(52951,56951)


def Abandonar():
    return QtGui.QIcon(pmAbandonar())


def pmEmpezar():
    return PM(56951,58987)


def Empezar():
    return QtGui.QIcon(pmEmpezar())


def pmOtros():
    return PM(58987,63457)


def Otros():
    return QtGui.QIcon(pmOtros())


def pmAnalizar():
    return PM(63457,64994)


def Analizar():
    return QtGui.QIcon(pmAnalizar())


def pmMainMenu():
    return PM(64994,69304)


def MainMenu():
    return QtGui.QIcon(pmMainMenu())


def pmFinPartida():
    return PM(69304,72252)


def FinPartida():
    return QtGui.QIcon(pmFinPartida())


def pmGrabar():
    return PM(72252,73715)


def Grabar():
    return QtGui.QIcon(pmGrabar())


def pmGrabarComo():
    return PM(73715,75767)


def GrabarComo():
    return QtGui.QIcon(pmGrabarComo())


def pmRecuperar():
    return PM(75767,78525)


def Recuperar():
    return QtGui.QIcon(pmRecuperar())


def pmInformacion():
    return PM(78525,80484)


def Informacion():
    return QtGui.QIcon(pmInformacion())


def pmNuevo():
    return PM(80484,81238)


def Nuevo():
    return QtGui.QIcon(pmNuevo())


def pmCopiar():
    return PM(81238,82419)


def Copiar():
    return QtGui.QIcon(pmCopiar())


def pmModificar():
    return PM(82419,86816)


def Modificar():
    return QtGui.QIcon(pmModificar())


def pmBorrar():
    return PM(86816,91807)


def Borrar():
    return QtGui.QIcon(pmBorrar())


def pmMarcar():
    return PM(91807,96736)


def Marcar():
    return QtGui.QIcon(pmMarcar())


def pmPegar():
    return PM(96736,99047)


def Pegar():
    return QtGui.QIcon(pmPegar())


def pmFichero():
    return PM(99047,103732)


def Fichero():
    return QtGui.QIcon(pmFichero())


def pmNuestroFichero():
    return PM(103732,106779)


def NuestroFichero():
    return QtGui.QIcon(pmNuestroFichero())


def pmFicheroRepite():
    return PM(106779,108275)


def FicheroRepite():
    return QtGui.QIcon(pmFicheroRepite())


def pmInformacionPGN():
    return PM(108275,109293)


def InformacionPGN():
    return QtGui.QIcon(pmInformacionPGN())


def pmVer():
    return PM(109293,110747)


def Ver():
    return QtGui.QIcon(pmVer())


def pmInicio():
    return PM(110747,112761)


def Inicio():
    return QtGui.QIcon(pmInicio())


def pmFinal():
    return PM(112761,114755)


def Final():
    return QtGui.QIcon(pmFinal())


def pmFiltrar():
    return PM(114755,121245)


def Filtrar():
    return QtGui.QIcon(pmFiltrar())


def pmArriba():
    return PM(121245,123398)


def Arriba():
    return QtGui.QIcon(pmArriba())


def pmAbajo():
    return PM(123398,125506)


def Abajo():
    return QtGui.QIcon(pmAbajo())


def pmEstadisticas():
    return PM(125506,127645)


def Estadisticas():
    return QtGui.QIcon(pmEstadisticas())


def pmCheck():
    return PM(127645,130869)


def Check():
    return QtGui.QIcon(pmCheck())


def pmTablas():
    return PM(130869,132492)


def Tablas():
    return QtGui.QIcon(pmTablas())


def pmAtras():
    return PM(132492,134011)


def Atras():
    return QtGui.QIcon(pmAtras())


def pmBuscar():
    return PM(134011,135996)


def Buscar():
    return QtGui.QIcon(pmBuscar())


def pmLibros():
    return PM(135996,138124)


def Libros():
    return QtGui.QIcon(pmLibros())


def pmAceptar():
    return PM(138124,141471)


def Aceptar():
    return QtGui.QIcon(pmAceptar())


def pmCancelar():
    return PM(141471,143454)


def Cancelar():
    return QtGui.QIcon(pmCancelar())


def pmDefecto():
    return PM(143454,146773)


def Defecto():
    return QtGui.QIcon(pmDefecto())


def pmInsertar():
    return PM(146773,149169)


def Insertar():
    return QtGui.QIcon(pmInsertar())


def pmJugar():
    return PM(149169,151378)


def Jugar():
    return QtGui.QIcon(pmJugar())


def pmConfigurar():
    return PM(151378,154462)


def Configurar():
    return QtGui.QIcon(pmConfigurar())


def pmS_Aceptar():
    return PM(138124,141471)


def S_Aceptar():
    return QtGui.QIcon(pmS_Aceptar())


def pmS_Cancelar():
    return PM(141471,143454)


def S_Cancelar():
    return QtGui.QIcon(pmS_Cancelar())


def pmS_Microfono():
    return PM(154462,159903)


def S_Microfono():
    return QtGui.QIcon(pmS_Microfono())


def pmS_LeerWav():
    return PM(50351,52951)


def S_LeerWav():
    return QtGui.QIcon(pmS_LeerWav())


def pmS_Play():
    return PM(159903,165241)


def S_Play():
    return QtGui.QIcon(pmS_Play())


def pmS_StopPlay():
    return PM(165241,165851)


def S_StopPlay():
    return QtGui.QIcon(pmS_StopPlay())


def pmS_StopMicrofono():
    return PM(165241,165851)


def S_StopMicrofono():
    return QtGui.QIcon(pmS_StopMicrofono())


def pmS_Record():
    return PM(165851,169084)


def S_Record():
    return QtGui.QIcon(pmS_Record())


def pmS_Limpiar():
    return PM(86816,91807)


def S_Limpiar():
    return QtGui.QIcon(pmS_Limpiar())


def pmHistorial():
    return PM(169084,170347)


def Historial():
    return QtGui.QIcon(pmHistorial())


def pmPegar16():
    return PM(170347,171341)


def Pegar16():
    return QtGui.QIcon(pmPegar16())


def pmRivalesMP():
    return PM(171341,174023)


def RivalesMP():
    return QtGui.QIcon(pmRivalesMP())


def pmCamara():
    return PM(174023,175545)


def Camara():
    return QtGui.QIcon(pmCamara())


def pmUsuarios():
    return PM(175545,176785)


def Usuarios():
    return QtGui.QIcon(pmUsuarios())


def pmResistencia():
    return PM(176785,179847)


def Resistencia():
    return QtGui.QIcon(pmResistencia())


def pmCebra():
    return PM(179847,182300)


def Cebra():
    return QtGui.QIcon(pmCebra())


def pmGafas():
    return PM(182300,183458)


def Gafas():
    return QtGui.QIcon(pmGafas())


def pmPuente():
    return PM(183458,184094)


def Puente():
    return QtGui.QIcon(pmPuente())


def pmWeb():
    return PM(184094,185276)


def Web():
    return QtGui.QIcon(pmWeb())


def pmMail():
    return PM(185276,186236)


def Mail():
    return QtGui.QIcon(pmMail())


def pmAyuda():
    return PM(186236,187417)


def Ayuda():
    return QtGui.QIcon(pmAyuda())


def pmFAQ():
    return PM(187417,188738)


def FAQ():
    return QtGui.QIcon(pmFAQ())


def pmActualiza():
    return PM(188738,189604)


def Actualiza():
    return QtGui.QIcon(pmActualiza())


def pmRefresh():
    return PM(189604,191996)


def Refresh():
    return QtGui.QIcon(pmRefresh())


def pmJuegaSolo():
    return PM(191996,193848)


def JuegaSolo():
    return QtGui.QIcon(pmJuegaSolo())


def pmPlayer():
    return PM(193848,195030)


def Player():
    return QtGui.QIcon(pmPlayer())


def pmJS_Rotacion():
    return PM(195030,196940)


def JS_Rotacion():
    return QtGui.QIcon(pmJS_Rotacion())


def pmElo():
    return PM(196940,198446)


def Elo():
    return QtGui.QIcon(pmElo())


def pmMate():
    return PM(198446,199007)


def Mate():
    return QtGui.QIcon(pmMate())


def pmEloTimed():
    return PM(199007,200491)


def EloTimed():
    return QtGui.QIcon(pmEloTimed())


def pmPGN():
    return PM(200491,202489)


def PGN():
    return QtGui.QIcon(pmPGN())


def pmPGN_Importar():
    return PM(202489,204079)


def PGN_Importar():
    return QtGui.QIcon(pmPGN_Importar())


def pmAyudaGR():
    return PM(204079,209957)


def AyudaGR():
    return QtGui.QIcon(pmAyudaGR())


def pmBotonAyuda():
    return PM(209957,212417)


def BotonAyuda():
    return QtGui.QIcon(pmBotonAyuda())


def pmColores():
    return PM(212417,213648)


def Colores():
    return QtGui.QIcon(pmColores())


def pmEditarColores():
    return PM(213648,215951)


def EditarColores():
    return QtGui.QIcon(pmEditarColores())


def pmGranMaestro():
    return PM(215951,216807)


def GranMaestro():
    return QtGui.QIcon(pmGranMaestro())


def pmFavoritos():
    return PM(216807,218573)


def Favoritos():
    return QtGui.QIcon(pmFavoritos())


def pmCarpeta():
    return PM(218573,219277)


def Carpeta():
    return QtGui.QIcon(pmCarpeta())


def pmDivision():
    return PM(219277,219942)


def Division():
    return QtGui.QIcon(pmDivision())


def pmDivisionF():
    return PM(219942,221056)


def DivisionF():
    return QtGui.QIcon(pmDivisionF())


def pmDelete():
    return PM(221056,221980)


def Delete():
    return QtGui.QIcon(pmDelete())


def pmModificarP():
    return PM(221980,223046)


def ModificarP():
    return QtGui.QIcon(pmModificarP())


def pmGrupo_Si():
    return PM(223046,223508)


def Grupo_Si():
    return QtGui.QIcon(pmGrupo_Si())


def pmGrupo_No():
    return PM(223508,223831)


def Grupo_No():
    return QtGui.QIcon(pmGrupo_No())


def pmMotor_Si():
    return PM(223831,224293)


def Motor_Si():
    return QtGui.QIcon(pmMotor_Si())


def pmMotor_No():
    return PM(221056,221980)


def Motor_No():
    return QtGui.QIcon(pmMotor_No())


def pmMotor_Actual():
    return PM(224293,225310)


def Motor_Actual():
    return QtGui.QIcon(pmMotor_Actual())


def pmMotor():
    return PM(225310,225937)


def Motor():
    return QtGui.QIcon(pmMotor())


def pmMoverInicio():
    return PM(225937,226235)


def MoverInicio():
    return QtGui.QIcon(pmMoverInicio())


def pmMoverFinal():
    return PM(226235,226536)


def MoverFinal():
    return QtGui.QIcon(pmMoverFinal())


def pmMoverAdelante():
    return PM(226536,226891)


def MoverAdelante():
    return QtGui.QIcon(pmMoverAdelante())


def pmMoverAtras():
    return PM(226891,227256)


def MoverAtras():
    return QtGui.QIcon(pmMoverAtras())


def pmMoverLibre():
    return PM(227256,227674)


def MoverLibre():
    return QtGui.QIcon(pmMoverLibre())


def pmMoverTiempo():
    return PM(227674,228253)


def MoverTiempo():
    return QtGui.QIcon(pmMoverTiempo())


def pmMoverMas():
    return PM(228253,229292)


def MoverMas():
    return QtGui.QIcon(pmMoverMas())


def pmMoverGrabar():
    return PM(229292,230148)


def MoverGrabar():
    return QtGui.QIcon(pmMoverGrabar())


def pmMoverGrabarTodos():
    return PM(230148,231192)


def MoverGrabarTodos():
    return QtGui.QIcon(pmMoverGrabarTodos())


def pmMoverJugar():
    return PM(231192,232023)


def MoverJugar():
    return QtGui.QIcon(pmMoverJugar())


def pmPelicula():
    return PM(232023,234157)


def Pelicula():
    return QtGui.QIcon(pmPelicula())


def pmPelicula_Pausa():
    return PM(234157,235916)


def Pelicula_Pausa():
    return QtGui.QIcon(pmPelicula_Pausa())


def pmPelicula_Seguir():
    return PM(235916,238005)


def Pelicula_Seguir():
    return QtGui.QIcon(pmPelicula_Seguir())


def pmPelicula_Rapido():
    return PM(238005,240064)


def Pelicula_Rapido():
    return QtGui.QIcon(pmPelicula_Rapido())


def pmPelicula_Lento():
    return PM(240064,241939)


def Pelicula_Lento():
    return QtGui.QIcon(pmPelicula_Lento())


def pmPelicula_Repetir():
    return PM(42158,44452)


def Pelicula_Repetir():
    return QtGui.QIcon(pmPelicula_Repetir())


def pmPelicula_PGN():
    return PM(241939,242847)


def Pelicula_PGN():
    return QtGui.QIcon(pmPelicula_PGN())


def pmMemoria():
    return PM(242847,244788)


def Memoria():
    return QtGui.QIcon(pmMemoria())


def pmEntrenar():
    return PM(244788,246327)


def Entrenar():
    return QtGui.QIcon(pmEntrenar())


def pmEnviar():
    return PM(244788,246327)


def Enviar():
    return QtGui.QIcon(pmEnviar())


def pmBoxRooms():
    return PM(246327,251130)


def BoxRooms():
    return QtGui.QIcon(pmBoxRooms())


def pmBoxRoom():
    return PM(251130,251592)


def BoxRoom():
    return QtGui.QIcon(pmBoxRoom())


def pmNewBoxRoom():
    return PM(251592,253100)


def NewBoxRoom():
    return QtGui.QIcon(pmNewBoxRoom())


def pmNuevoMas():
    return PM(251592,253100)


def NuevoMas():
    return QtGui.QIcon(pmNuevoMas())


def pmTemas():
    return PM(253100,255323)


def Temas():
    return QtGui.QIcon(pmTemas())


def pmTutorialesCrear():
    return PM(255323,261592)


def TutorialesCrear():
    return QtGui.QIcon(pmTutorialesCrear())


def pmMover():
    return PM(261592,262174)


def Mover():
    return QtGui.QIcon(pmMover())


def pmSeleccionar():
    return PM(262174,267878)


def Seleccionar():
    return QtGui.QIcon(pmSeleccionar())


def pmVista():
    return PM(267878,269802)


def Vista():
    return QtGui.QIcon(pmVista())


def pmInformacionPGNUno():
    return PM(269802,271180)


def InformacionPGNUno():
    return QtGui.QIcon(pmInformacionPGNUno())


def pmDailyTest():
    return PM(271180,273520)


def DailyTest():
    return QtGui.QIcon(pmDailyTest())


def pmJuegaPorMi():
    return PM(273520,275240)


def JuegaPorMi():
    return QtGui.QIcon(pmJuegaPorMi())


def pmArbol():
    return PM(275240,275874)


def Arbol():
    return QtGui.QIcon(pmArbol())


def pmGrabarFichero():
    return PM(72252,73715)


def GrabarFichero():
    return QtGui.QIcon(pmGrabarFichero())


def pmClipboard():
    return PM(275874,276652)


def Clipboard():
    return QtGui.QIcon(pmClipboard())


def pmFics():
    return PM(276652,277069)


def Fics():
    return QtGui.QIcon(pmFics())


def pmFide():
    return PM(9646,11623)


def Fide():
    return QtGui.QIcon(pmFide())


def pmFichPGN():
    return PM(30258,32006)


def FichPGN():
    return QtGui.QIcon(pmFichPGN())


def pmFlechas():
    return PM(277069,280421)


def Flechas():
    return QtGui.QIcon(pmFlechas())


def pmMarcos():
    return PM(280421,281868)


def Marcos():
    return QtGui.QIcon(pmMarcos())


def pmSVGs():
    return PM(281868,285437)


def SVGs():
    return QtGui.QIcon(pmSVGs())


def pmAmarillo():
    return PM(285437,286689)


def Amarillo():
    return QtGui.QIcon(pmAmarillo())


def pmNaranja():
    return PM(286689,287921)


def Naranja():
    return QtGui.QIcon(pmNaranja())


def pmVerde():
    return PM(287921,289197)


def Verde():
    return QtGui.QIcon(pmVerde())


def pmAzul():
    return PM(289197,290285)


def Azul():
    return QtGui.QIcon(pmAzul())


def pmMagenta():
    return PM(290285,291573)


def Magenta():
    return QtGui.QIcon(pmMagenta())


def pmRojo():
    return PM(291573,292792)


def Rojo():
    return QtGui.QIcon(pmRojo())


def pmGris():
    return PM(292792,293750)


def Gris():
    return QtGui.QIcon(pmGris())


def pmAmarillo32():
    return PM(293750,295730)


def Amarillo32():
    return QtGui.QIcon(pmAmarillo32())


def pmNaranja32():
    return PM(295730,297854)


def Naranja32():
    return QtGui.QIcon(pmNaranja32())


def pmVerde32():
    return PM(297854,299975)


def Verde32():
    return QtGui.QIcon(pmVerde32())


def pmAzul32():
    return PM(299975,302354)


def Azul32():
    return QtGui.QIcon(pmAzul32())


def pmMagenta32():
    return PM(302354,304805)


def Magenta32():
    return QtGui.QIcon(pmMagenta32())


def pmRojo32():
    return PM(304805,306620)


def Rojo32():
    return QtGui.QIcon(pmRojo32())


def pmGris32():
    return PM(306620,308534)


def Gris32():
    return QtGui.QIcon(pmGris32())


def pmPuntoBlanco():
    return PM(308534,308883)


def PuntoBlanco():
    return QtGui.QIcon(pmPuntoBlanco())


def pmPuntoAmarillo():
    return PM(223046,223508)


def PuntoAmarillo():
    return QtGui.QIcon(pmPuntoAmarillo())


def pmPuntoNaranja():
    return PM(308883,309345)


def PuntoNaranja():
    return QtGui.QIcon(pmPuntoNaranja())


def pmPuntoVerde():
    return PM(223831,224293)


def PuntoVerde():
    return QtGui.QIcon(pmPuntoVerde())


def pmPuntoAzul():
    return PM(251130,251592)


def PuntoAzul():
    return QtGui.QIcon(pmPuntoAzul())


def pmPuntoMagenta():
    return PM(309345,309844)


def PuntoMagenta():
    return QtGui.QIcon(pmPuntoMagenta())


def pmPuntoRojo():
    return PM(309844,310343)


def PuntoRojo():
    return QtGui.QIcon(pmPuntoRojo())


def pmPuntoNegro():
    return PM(223508,223831)


def PuntoNegro():
    return QtGui.QIcon(pmPuntoNegro())


def pmPuntoEstrella():
    return PM(310343,310770)


def PuntoEstrella():
    return QtGui.QIcon(pmPuntoEstrella())


def pmComentario():
    return PM(310770,311407)


def Comentario():
    return QtGui.QIcon(pmComentario())


def pmComentarioMas():
    return PM(311407,312346)


def ComentarioMas():
    return QtGui.QIcon(pmComentarioMas())


def pmComentarioEditar():
    return PM(229292,230148)


def ComentarioEditar():
    return QtGui.QIcon(pmComentarioEditar())


def pmOpeningComentario():
    return PM(312346,313342)


def OpeningComentario():
    return QtGui.QIcon(pmOpeningComentario())


def pmMas():
    return PM(313342,313851)


def Mas():
    return QtGui.QIcon(pmMas())


def pmMasR():
    return PM(313851,314339)


def MasR():
    return QtGui.QIcon(pmMasR())


def pmMasDoc():
    return PM(314339,315140)


def MasDoc():
    return QtGui.QIcon(pmMasDoc())


def pmPotencia():
    return PM(188738,189604)


def Potencia():
    return QtGui.QIcon(pmPotencia())


def pmBMT():
    return PM(315140,316018)


def BMT():
    return QtGui.QIcon(pmBMT())


def pmOjo():
    return PM(316018,317140)


def Ojo():
    return QtGui.QIcon(pmOjo())


def pmOcultar():
    return PM(316018,317140)


def Ocultar():
    return QtGui.QIcon(pmOcultar())


def pmMostrar():
    return PM(317140,318196)


def Mostrar():
    return QtGui.QIcon(pmMostrar())


def pmBlog():
    return PM(318196,318718)


def Blog():
    return QtGui.QIcon(pmBlog())


def pmVariations():
    return PM(318718,319625)


def Variations():
    return QtGui.QIcon(pmVariations())


def pmVariationsG():
    return PM(319625,322052)


def VariationsG():
    return QtGui.QIcon(pmVariationsG())


def pmCambiar():
    return PM(322052,323766)


def Cambiar():
    return QtGui.QIcon(pmCambiar())


def pmAnterior():
    return PM(323766,325820)


def Anterior():
    return QtGui.QIcon(pmAnterior())


def pmSiguiente():
    return PM(325820,327890)


def Siguiente():
    return QtGui.QIcon(pmSiguiente())


def pmSiguienteF():
    return PM(327890,330065)


def SiguienteF():
    return QtGui.QIcon(pmSiguienteF())


def pmAnteriorF():
    return PM(330065,332259)


def AnteriorF():
    return QtGui.QIcon(pmAnteriorF())


def pmX():
    return PM(332259,333541)


def X():
    return QtGui.QIcon(pmX())


def pmTools():
    return PM(333541,336142)


def Tools():
    return QtGui.QIcon(pmTools())


def pmTacticas():
    return PM(336142,338715)


def Tacticas():
    return QtGui.QIcon(pmTacticas())


def pmCancelarPeque():
    return PM(338715,339277)


def CancelarPeque():
    return QtGui.QIcon(pmCancelarPeque())


def pmAceptarPeque():
    return PM(224293,225310)


def AceptarPeque():
    return QtGui.QIcon(pmAceptarPeque())


def pmLibre():
    return PM(339277,341669)


def Libre():
    return QtGui.QIcon(pmLibre())


def pmEnBlanco():
    return PM(341669,342395)


def EnBlanco():
    return QtGui.QIcon(pmEnBlanco())


def pmDirector():
    return PM(342395,345369)


def Director():
    return QtGui.QIcon(pmDirector())


def pmTorneos():
    return PM(345369,347107)


def Torneos():
    return QtGui.QIcon(pmTorneos())


def pmOpenings():
    return PM(347107,348032)


def Openings():
    return QtGui.QIcon(pmOpenings())


def pmV_Blancas():
    return PM(348032,348312)


def V_Blancas():
    return QtGui.QIcon(pmV_Blancas())


def pmV_Blancas_Mas():
    return PM(348312,348592)


def V_Blancas_Mas():
    return QtGui.QIcon(pmV_Blancas_Mas())


def pmV_Blancas_Mas_Mas():
    return PM(348592,348864)


def V_Blancas_Mas_Mas():
    return QtGui.QIcon(pmV_Blancas_Mas_Mas())


def pmV_Negras():
    return PM(348864,349139)


def V_Negras():
    return QtGui.QIcon(pmV_Negras())


def pmV_Negras_Mas():
    return PM(349139,349414)


def V_Negras_Mas():
    return QtGui.QIcon(pmV_Negras_Mas())


def pmV_Negras_Mas_Mas():
    return PM(349414,349683)


def V_Negras_Mas_Mas():
    return QtGui.QIcon(pmV_Negras_Mas_Mas())


def pmV_Blancas_Igual_Negras():
    return PM(349683,349985)


def V_Blancas_Igual_Negras():
    return QtGui.QIcon(pmV_Blancas_Igual_Negras())


def pmMezclar():
    return PM(146773,149169)


def Mezclar():
    return QtGui.QIcon(pmMezclar())


def pmVoyager():
    return PM(349985,350828)


def Voyager():
    return QtGui.QIcon(pmVoyager())


def pmVoyager32():
    return PM(350828,352716)


def Voyager32():
    return QtGui.QIcon(pmVoyager32())


def pmReindexar():
    return PM(352716,354533)


def Reindexar():
    return QtGui.QIcon(pmReindexar())


def pmRename():
    return PM(354533,355517)


def Rename():
    return QtGui.QIcon(pmRename())


def pmAdd():
    return PM(355517,356470)


def Add():
    return QtGui.QIcon(pmAdd())


def pmMas22():
    return PM(356470,357134)


def Mas22():
    return QtGui.QIcon(pmMas22())


def pmMenos22():
    return PM(357134,357578)


def Menos22():
    return QtGui.QIcon(pmMenos22())


def pmTransposition():
    return PM(357578,358097)


def Transposition():
    return QtGui.QIcon(pmTransposition())


def pmRat():
    return PM(358097,363801)


def Rat():
    return QtGui.QIcon(pmRat())


def pmAlligator():
    return PM(363801,368793)


def Alligator():
    return QtGui.QIcon(pmAlligator())


def pmAnt():
    return PM(368793,375491)


def Ant():
    return QtGui.QIcon(pmAnt())


def pmBat():
    return PM(375491,378445)


def Bat():
    return QtGui.QIcon(pmBat())


def pmBear():
    return PM(378445,385724)


def Bear():
    return QtGui.QIcon(pmBear())


def pmBee():
    return PM(385724,390726)


def Bee():
    return QtGui.QIcon(pmBee())


def pmBird():
    return PM(390726,396785)


def Bird():
    return QtGui.QIcon(pmBird())


def pmBull():
    return PM(396785,403754)


def Bull():
    return QtGui.QIcon(pmBull())


def pmBulldog():
    return PM(403754,410645)


def Bulldog():
    return QtGui.QIcon(pmBulldog())


def pmButterfly():
    return PM(410645,418019)


def Butterfly():
    return QtGui.QIcon(pmButterfly())


def pmCat():
    return PM(418019,424291)


def Cat():
    return QtGui.QIcon(pmCat())


def pmChicken():
    return PM(424291,430102)


def Chicken():
    return QtGui.QIcon(pmChicken())


def pmCow():
    return PM(430102,436845)


def Cow():
    return QtGui.QIcon(pmCow())


def pmCrab():
    return PM(436845,442434)


def Crab():
    return QtGui.QIcon(pmCrab())


def pmCrocodile():
    return PM(442434,448575)


def Crocodile():
    return QtGui.QIcon(pmCrocodile())


def pmDeer():
    return PM(448575,454882)


def Deer():
    return QtGui.QIcon(pmDeer())


def pmDog():
    return PM(454882,461485)


def Dog():
    return QtGui.QIcon(pmDog())


def pmDonkey():
    return PM(461485,467132)


def Donkey():
    return QtGui.QIcon(pmDonkey())


def pmDuck():
    return PM(467132,473675)


def Duck():
    return QtGui.QIcon(pmDuck())


def pmEagle():
    return PM(473675,478493)


def Eagle():
    return QtGui.QIcon(pmEagle())


def pmElephant():
    return PM(478493,484974)


def Elephant():
    return QtGui.QIcon(pmElephant())


def pmFish():
    return PM(484974,491815)


def Fish():
    return QtGui.QIcon(pmFish())


def pmFox():
    return PM(491815,498598)


def Fox():
    return QtGui.QIcon(pmFox())


def pmFrog():
    return PM(498598,505014)


def Frog():
    return QtGui.QIcon(pmFrog())


def pmGiraffe():
    return PM(505014,512192)


def Giraffe():
    return QtGui.QIcon(pmGiraffe())


def pmGorilla():
    return PM(512192,518731)


def Gorilla():
    return QtGui.QIcon(pmGorilla())


def pmHippo():
    return PM(518731,525852)


def Hippo():
    return QtGui.QIcon(pmHippo())


def pmHorse():
    return PM(525852,532399)


def Horse():
    return QtGui.QIcon(pmHorse())


def pmInsect():
    return PM(532399,538334)


def Insect():
    return QtGui.QIcon(pmInsect())


def pmLion():
    return PM(538334,547244)


def Lion():
    return QtGui.QIcon(pmLion())


def pmMonkey():
    return PM(547244,554923)


def Monkey():
    return QtGui.QIcon(pmMonkey())


def pmMoose():
    return PM(554923,561547)


def Moose():
    return QtGui.QIcon(pmMoose())


def pmMouse():
    return PM(358097,363801)


def Mouse():
    return QtGui.QIcon(pmMouse())


def pmOwl():
    return PM(561547,568253)


def Owl():
    return QtGui.QIcon(pmOwl())


def pmPanda():
    return PM(568253,572287)


def Panda():
    return QtGui.QIcon(pmPanda())


def pmPenguin():
    return PM(572287,577836)


def Penguin():
    return QtGui.QIcon(pmPenguin())


def pmPig():
    return PM(577836,585876)


def Pig():
    return QtGui.QIcon(pmPig())


def pmRabbit():
    return PM(585876,593177)


def Rabbit():
    return QtGui.QIcon(pmRabbit())


def pmRhino():
    return PM(593177,599564)


def Rhino():
    return QtGui.QIcon(pmRhino())


def pmRooster():
    return PM(599564,604827)


def Rooster():
    return QtGui.QIcon(pmRooster())


def pmShark():
    return PM(604827,610597)


def Shark():
    return QtGui.QIcon(pmShark())


def pmSheep():
    return PM(610597,614428)


def Sheep():
    return QtGui.QIcon(pmSheep())


def pmSnake():
    return PM(614428,620453)


def Snake():
    return QtGui.QIcon(pmSnake())


def pmTiger():
    return PM(620453,628490)


def Tiger():
    return QtGui.QIcon(pmTiger())


def pmTurkey():
    return PM(628490,635904)


def Turkey():
    return QtGui.QIcon(pmTurkey())


def pmTurtle():
    return PM(635904,642625)


def Turtle():
    return QtGui.QIcon(pmTurtle())


def pmWolf():
    return PM(642625,645720)


def Wolf():
    return QtGui.QIcon(pmWolf())


def pmSteven():
    return PM(645720,652872)


def Steven():
    return QtGui.QIcon(pmSteven())


def pmWheel():
    return PM(652872,660937)


def Wheel():
    return QtGui.QIcon(pmWheel())


def pmWheelchair():
    return PM(660937,669741)


def Wheelchair():
    return QtGui.QIcon(pmWheelchair())


def pmTouringMotorcycle():
    return PM(669741,676053)


def TouringMotorcycle():
    return QtGui.QIcon(pmTouringMotorcycle())


def pmContainer():
    return PM(676053,681388)


def Container():
    return QtGui.QIcon(pmContainer())


def pmBoatEquipment():
    return PM(681388,686911)


def BoatEquipment():
    return QtGui.QIcon(pmBoatEquipment())


def pmCar():
    return PM(686911,691557)


def Car():
    return QtGui.QIcon(pmCar())


def pmLorry():
    return PM(691557,697593)


def Lorry():
    return QtGui.QIcon(pmLorry())


def pmCarTrailer():
    return PM(697593,701690)


def CarTrailer():
    return QtGui.QIcon(pmCarTrailer())


def pmTowTruck():
    return PM(701690,706448)


def TowTruck():
    return QtGui.QIcon(pmTowTruck())


def pmQuadBike():
    return PM(706448,712417)


def QuadBike():
    return QtGui.QIcon(pmQuadBike())


def pmRecoveryTruck():
    return PM(712417,717414)


def RecoveryTruck():
    return QtGui.QIcon(pmRecoveryTruck())


def pmContainerLoader():
    return PM(717414,722556)


def ContainerLoader():
    return QtGui.QIcon(pmContainerLoader())


def pmPoliceCar():
    return PM(722556,727388)


def PoliceCar():
    return QtGui.QIcon(pmPoliceCar())


def pmExecutiveCar():
    return PM(727388,732066)


def ExecutiveCar():
    return QtGui.QIcon(pmExecutiveCar())


def pmTruck():
    return PM(732066,737529)


def Truck():
    return QtGui.QIcon(pmTruck())


def pmExcavator():
    return PM(737529,742420)


def Excavator():
    return QtGui.QIcon(pmExcavator())


def pmCabriolet():
    return PM(742420,747258)


def Cabriolet():
    return QtGui.QIcon(pmCabriolet())


def pmMixerTruck():
    return PM(747258,753568)


def MixerTruck():
    return QtGui.QIcon(pmMixerTruck())


def pmForkliftTruckLoaded():
    return PM(753568,759716)


def ForkliftTruckLoaded():
    return QtGui.QIcon(pmForkliftTruckLoaded())


def pmAmbulance():
    return PM(759716,765766)


def Ambulance():
    return QtGui.QIcon(pmAmbulance())


def pmDieselLocomotiveBoxcar():
    return PM(765766,769772)


def DieselLocomotiveBoxcar():
    return QtGui.QIcon(pmDieselLocomotiveBoxcar())


def pmTractorUnit():
    return PM(769772,775239)


def TractorUnit():
    return QtGui.QIcon(pmTractorUnit())


def pmFireTruck():
    return PM(775239,781578)


def FireTruck():
    return QtGui.QIcon(pmFireTruck())


def pmCargoShip():
    return PM(781578,785919)


def CargoShip():
    return QtGui.QIcon(pmCargoShip())


def pmSubwayTrain():
    return PM(785919,790809)


def SubwayTrain():
    return QtGui.QIcon(pmSubwayTrain())


def pmTruckMountedCrane():
    return PM(790809,796550)


def TruckMountedCrane():
    return QtGui.QIcon(pmTruckMountedCrane())


def pmAirAmbulance():
    return PM(796550,801663)


def AirAmbulance():
    return QtGui.QIcon(pmAirAmbulance())


def pmAirplane():
    return PM(801663,806551)


def Airplane():
    return QtGui.QIcon(pmAirplane())


def pmCaracol():
    return PM(806551,808367)


def Caracol():
    return QtGui.QIcon(pmCaracol())


def pmUno():
    return PM(808367,810829)


def Uno():
    return QtGui.QIcon(pmUno())


def pmMotoresExternos():
    return PM(810829,812731)


def MotoresExternos():
    return QtGui.QIcon(pmMotoresExternos())


def pmDatabase():
    return PM(812731,814047)


def Database():
    return QtGui.QIcon(pmDatabase())


def pmDatabaseMas():
    return PM(814047,815506)


def DatabaseMas():
    return QtGui.QIcon(pmDatabaseMas())


def pmDatabaseImport():
    return PM(815506,816142)


def DatabaseImport():
    return QtGui.QIcon(pmDatabaseImport())


def pmDatabaseExport():
    return PM(816142,816787)


def DatabaseExport():
    return QtGui.QIcon(pmDatabaseExport())


def pmDatabaseDelete():
    return PM(816787,817910)


def DatabaseDelete():
    return QtGui.QIcon(pmDatabaseDelete())


def pmDatabaseMaintenance():
    return PM(817910,819406)


def DatabaseMaintenance():
    return QtGui.QIcon(pmDatabaseMaintenance())


def pmAtacante():
    return PM(819406,820011)


def Atacante():
    return QtGui.QIcon(pmAtacante())


def pmAtacada():
    return PM(820011,820577)


def Atacada():
    return QtGui.QIcon(pmAtacada())


def pmGoToNext():
    return PM(820577,820989)


def GoToNext():
    return QtGui.QIcon(pmGoToNext())


def pmBlancas():
    return PM(820989,821340)


def Blancas():
    return QtGui.QIcon(pmBlancas())


def pmNegras():
    return PM(821340,821586)


def Negras():
    return QtGui.QIcon(pmNegras())


def pmFolderChange():
    return PM(75767,78525)


def FolderChange():
    return QtGui.QIcon(pmFolderChange())


def pmMarkers():
    return PM(821586,823281)


def Markers():
    return QtGui.QIcon(pmMarkers())


def pmTop():
    return PM(823281,823865)


def Top():
    return QtGui.QIcon(pmTop())


def pmBottom():
    return PM(823865,824454)


def Bottom():
    return QtGui.QIcon(pmBottom())


def pmSTS():
    return PM(824454,826645)


def STS():
    return QtGui.QIcon(pmSTS())


def pmRun():
    return PM(826645,828369)


def Run():
    return QtGui.QIcon(pmRun())


def pmRun2():
    return PM(828369,829889)


def Run2():
    return QtGui.QIcon(pmRun2())


def pmWorldMap():
    return PM(829889,832630)


def WorldMap():
    return QtGui.QIcon(pmWorldMap())


def pmAfrica():
    return PM(832630,835116)


def Africa():
    return QtGui.QIcon(pmAfrica())


def pmMaps():
    return PM(835116,836060)


def Maps():
    return QtGui.QIcon(pmMaps())


def pmSol():
    return PM(836060,836986)


def Sol():
    return QtGui.QIcon(pmSol())


def pmSolNubes():
    return PM(836986,837849)


def SolNubes():
    return QtGui.QIcon(pmSolNubes())


def pmSolNubesLluvia():
    return PM(837849,838809)


def SolNubesLluvia():
    return QtGui.QIcon(pmSolNubesLluvia())


def pmLluvia():
    return PM(838809,839648)


def Lluvia():
    return QtGui.QIcon(pmLluvia())


def pmInvierno():
    return PM(839648,841224)


def Invierno():
    return QtGui.QIcon(pmInvierno())


def pmFixedElo():
    return PM(169084,170347)


def FixedElo():
    return QtGui.QIcon(pmFixedElo())


def pmSoundTool():
    return PM(841224,843683)


def SoundTool():
    return QtGui.QIcon(pmSoundTool())


def pmTrain():
    return PM(843683,845053)


def Train():
    return QtGui.QIcon(pmTrain())


def pmPlay():
    return PM(235916,238005)


def Play():
    return QtGui.QIcon(pmPlay())


def pmMeasure():
    return PM(130869,132492)


def Measure():
    return QtGui.QIcon(pmMeasure())


def pmPlayGame():
    return PM(845053,849411)


def PlayGame():
    return QtGui.QIcon(pmPlayGame())


def pmScanner():
    return PM(849411,849752)


def Scanner():
    return QtGui.QIcon(pmScanner())


def pmMenos():
    return PM(849752,850277)


def Menos():
    return QtGui.QIcon(pmMenos())


def pmSchool():
    return PM(850277,851639)


def School():
    return QtGui.QIcon(pmSchool())


def pmLaw():
    return PM(851639,852255)


def Law():
    return QtGui.QIcon(pmLaw())


def pmLearnGame():
    return PM(852255,852688)


def LearnGame():
    return QtGui.QIcon(pmLearnGame())


def pmLonghaul():
    return PM(852688,853614)


def Longhaul():
    return QtGui.QIcon(pmLonghaul())


def pmTrekking():
    return PM(853614,854308)


def Trekking():
    return QtGui.QIcon(pmTrekking())


def pmPassword():
    return PM(854308,854761)


def Password():
    return QtGui.QIcon(pmPassword())


def pmSQL_RAW():
    return PM(845053,849411)


def SQL_RAW():
    return QtGui.QIcon(pmSQL_RAW())


def pmSun():
    return PM(315140,316018)


def Sun():
    return QtGui.QIcon(pmSun())


def pmLight32():
    return PM(854761,856461)


def Light32():
    return QtGui.QIcon(pmLight32())


def pmTOL():
    return PM(856461,857170)


def TOL():
    return QtGui.QIcon(pmTOL())


def pmUned():
    return PM(857170,857590)


def Uned():
    return QtGui.QIcon(pmUned())


def pmUwe():
    return PM(857590,858559)


def Uwe():
    return QtGui.QIcon(pmUwe())


def pmThinking():
    return PM(858559,859348)


def Thinking():
    return QtGui.QIcon(pmThinking())


def pmWashingMachine():
    return PM(859348,860011)


def WashingMachine():
    return QtGui.QIcon(pmWashingMachine())


def pmTerminal():
    return PM(860011,863555)


def Terminal():
    return QtGui.QIcon(pmTerminal())


def pmManualSave():
    return PM(863555,864138)


def ManualSave():
    return QtGui.QIcon(pmManualSave())


def pmSettings():
    return PM(864138,864576)


def Settings():
    return QtGui.QIcon(pmSettings())


def pmStrength():
    return PM(864576,865247)


def Strength():
    return QtGui.QIcon(pmStrength())


def pmSingular():
    return PM(865247,866102)


def Singular():
    return QtGui.QIcon(pmSingular())


def pmScript():
    return PM(866102,866671)


def Script():
    return QtGui.QIcon(pmScript())


def pmTexto():
    return PM(866671,869516)


def Texto():
    return QtGui.QIcon(pmTexto())


def pmLampara():
    return PM(869516,870225)


def Lampara():
    return QtGui.QIcon(pmLampara())


def pmFile():
    return PM(870225,872525)


def File():
    return QtGui.QIcon(pmFile())


def pmCalculo():
    return PM(872525,873451)


def Calculo():
    return QtGui.QIcon(pmCalculo())


def pmOpeningLines():
    return PM(873451,874129)


def OpeningLines():
    return QtGui.QIcon(pmOpeningLines())


def pmStudy():
    return PM(874129,875042)


def Study():
    return QtGui.QIcon(pmStudy())


def pmLichess():
    return PM(875042,875930)


def Lichess():
    return QtGui.QIcon(pmLichess())


def pmMiniatura():
    return PM(875930,876857)


def Miniatura():
    return QtGui.QIcon(pmMiniatura())


def pmLocomotora():
    return PM(876857,877638)


def Locomotora():
    return QtGui.QIcon(pmLocomotora())


def pmTrainSequential():
    return PM(877638,878779)


def TrainSequential():
    return QtGui.QIcon(pmTrainSequential())


def pmTrainStatic():
    return PM(878779,879739)


def TrainStatic():
    return QtGui.QIcon(pmTrainStatic())


def pmTrainPositions():
    return PM(879739,880720)


def TrainPositions():
    return QtGui.QIcon(pmTrainPositions())


def pmTrainEngines():
    return PM(880720,882154)


def TrainEngines():
    return QtGui.QIcon(pmTrainEngines())


def pmError():
    return PM(52951,56951)


def Error():
    return QtGui.QIcon(pmError())


def pmAtajos():
    return PM(882154,883333)


def Atajos():
    return QtGui.QIcon(pmAtajos())


def pmTOLline():
    return PM(883333,884437)


def TOLline():
    return QtGui.QIcon(pmTOLline())


def pmTOLchange():
    return PM(884437,886659)


def TOLchange():
    return QtGui.QIcon(pmTOLchange())


def pmPack():
    return PM(886659,887832)


def Pack():
    return QtGui.QIcon(pmPack())


def pmHome():
    return PM(184094,185276)


def Home():
    return QtGui.QIcon(pmHome())


def pmImport8():
    return PM(887832,888590)


def Import8():
    return QtGui.QIcon(pmImport8())


def pmExport8():
    return PM(888590,889215)


def Export8():
    return QtGui.QIcon(pmExport8())


def pmTablas8():
    return PM(889215,890007)


def Tablas8():
    return QtGui.QIcon(pmTablas8())


def pmBlancas8():
    return PM(890007,891037)


def Blancas8():
    return QtGui.QIcon(pmBlancas8())


def pmNegras8():
    return PM(891037,891876)


def Negras8():
    return QtGui.QIcon(pmNegras8())


def pmBook():
    return PM(891876,892450)


def Book():
    return QtGui.QIcon(pmBook())


def pmWrite():
    return PM(892450,893655)


def Write():
    return QtGui.QIcon(pmWrite())


def pmAlt():
    return PM(893655,894097)


def Alt():
    return QtGui.QIcon(pmAlt())


def pmShift():
    return PM(894097,894437)


def Shift():
    return QtGui.QIcon(pmShift())


def pmRightMouse():
    return PM(894437,895237)


def RightMouse():
    return QtGui.QIcon(pmRightMouse())


def pmControl():
    return PM(895237,895762)


def Control():
    return QtGui.QIcon(pmControl())


def pmFinales():
    return PM(895762,896849)


def Finales():
    return QtGui.QIcon(pmFinales())


def pmEditColumns():
    return PM(896849,897581)


def EditColumns():
    return QtGui.QIcon(pmEditColumns())


def pmResizeAll():
    return PM(897581,898091)


def ResizeAll():
    return QtGui.QIcon(pmResizeAll())


def pmChecked():
    return PM(898091,898597)


def Checked():
    return QtGui.QIcon(pmChecked())


def pmUnchecked():
    return PM(898597,898845)


def Unchecked():
    return QtGui.QIcon(pmUnchecked())


def pmBuscarC():
    return PM(898845,899289)


def BuscarC():
    return QtGui.QIcon(pmBuscarC())


def pmPeonBlanco():
    return PM(899289,901470)


def PeonBlanco():
    return QtGui.QIcon(pmPeonBlanco())


def pmPeonNegro():
    return PM(901470,902994)


def PeonNegro():
    return QtGui.QIcon(pmPeonNegro())


def pmReciclar():
    return PM(902994,903718)


def Reciclar():
    return QtGui.QIcon(pmReciclar())


def pmLanzamiento():
    return PM(903718,904431)


def Lanzamiento():
    return QtGui.QIcon(pmLanzamiento())


def pmEndGame():
    return PM(904431,904845)


def EndGame():
    return QtGui.QIcon(pmEndGame())


def pmPause():
    return PM(904845,905714)


def Pause():
    return QtGui.QIcon(pmPause())


def pmContinue():
    return PM(905714,906918)


def Continue():
    return QtGui.QIcon(pmContinue())


def pmClose():
    return PM(906918,907617)


def Close():
    return QtGui.QIcon(pmClose())


def pmStop():
    return PM(907617,908650)


def Stop():
    return QtGui.QIcon(pmStop())


def pmFactoryPolyglot():
    return PM(908650,909470)


def FactoryPolyglot():
    return QtGui.QIcon(pmFactoryPolyglot())


def pmTags():
    return PM(909470,910293)


def Tags():
    return QtGui.QIcon(pmTags())


def pmAppearance():
    return PM(910293,911020)


def Appearance():
    return QtGui.QIcon(pmAppearance())


def pmFill():
    return PM(911020,912058)


def Fill():
    return QtGui.QIcon(pmFill())


def pmSupport():
    return PM(912058,912790)


def Support():
    return QtGui.QIcon(pmSupport())


def pmOrder():
    return PM(912790,913588)


def Order():
    return QtGui.QIcon(pmOrder())


def pmPlay1():
    return PM(913588,914883)


def Play1():
    return QtGui.QIcon(pmPlay1())


def pmRemove1():
    return PM(914883,916010)


def Remove1():
    return QtGui.QIcon(pmRemove1())


def pmNew1():
    return PM(916010,916332)


def New1():
    return QtGui.QIcon(pmNew1())


def pmMensError():
    return PM(916332,918396)


def MensError():
    return QtGui.QIcon(pmMensError())


def pmMensInfo():
    return PM(918396,920951)


def MensInfo():
    return QtGui.QIcon(pmMensInfo())


def pmJump():
    return PM(920951,921626)


def Jump():
    return QtGui.QIcon(pmJump())


def pmCaptures():
    return PM(921626,922807)


def Captures():
    return QtGui.QIcon(pmCaptures())


def pmRepeat():
    return PM(922807,923466)


def Repeat():
    return QtGui.QIcon(pmRepeat())


def pmCount():
    return PM(923466,924142)


def Count():
    return QtGui.QIcon(pmCount())


def pmMate15():
    return PM(924142,925213)


def Mate15():
    return QtGui.QIcon(pmMate15())


def pmCoordinates():
    return PM(925213,926366)


def Coordinates():
    return QtGui.QIcon(pmCoordinates())


def pmKnight():
    return PM(926366,927609)


def Knight():
    return QtGui.QIcon(pmKnight())


def pmCorrecto():
    return PM(927609,928635)


def Correcto():
    return QtGui.QIcon(pmCorrecto())


def pmBlocks():
    return PM(928635,928972)


def Blocks():
    return QtGui.QIcon(pmBlocks())


def pmWest():
    return PM(928972,930078)


def West():
    return QtGui.QIcon(pmWest())


def pmOpening():
    return PM(930078,930336)


def Opening():
    return QtGui.QIcon(pmOpening())


def pmVariation():
    return PM(227256,227674)


def Variation():
    return QtGui.QIcon(pmVariation())


def pmComment():
    return PM(930336,930699)


def Comment():
    return QtGui.QIcon(pmComment())


def pmVariationComment():
    return PM(930699,931043)


def VariationComment():
    return QtGui.QIcon(pmVariationComment())


def pmOpeningVariation():
    return PM(931043,931507)


def OpeningVariation():
    return QtGui.QIcon(pmOpeningVariation())


def pmOpeningComment():
    return PM(931507,931840)


def OpeningComment():
    return QtGui.QIcon(pmOpeningComment())


def pmOpeningVariationComment():
    return PM(931043,931507)


def OpeningVariationComment():
    return QtGui.QIcon(pmOpeningVariationComment())


def pmDeleteRow():
    return PM(931840,932271)


def DeleteRow():
    return QtGui.QIcon(pmDeleteRow())


def pmDeleteColumn():
    return PM(932271,932714)


def DeleteColumn():
    return QtGui.QIcon(pmDeleteColumn())


def pmEditVariation():
    return PM(932714,933069)


def EditVariation():
    return QtGui.QIcon(pmEditVariation())


def pmKibitzer():
    return PM(933069,933668)


def Kibitzer():
    return QtGui.QIcon(pmKibitzer())


def pmKibitzer_Pause():
    return PM(933668,933840)


def Kibitzer_Pause():
    return QtGui.QIcon(pmKibitzer_Pause())


def pmKibitzer_Options():
    return PM(933840,934742)


def Kibitzer_Options():
    return QtGui.QIcon(pmKibitzer_Options())


def pmKibitzer_Voyager():
    return PM(349985,350828)


def Kibitzer_Voyager():
    return QtGui.QIcon(pmKibitzer_Voyager())


def pmKibitzer_Close():
    return PM(934742,935299)


def Kibitzer_Close():
    return QtGui.QIcon(pmKibitzer_Close())


def pmKibitzer_Down():
    return PM(935299,935688)


def Kibitzer_Down():
    return QtGui.QIcon(pmKibitzer_Down())


def pmKibitzer_Up():
    return PM(935688,936083)


def Kibitzer_Up():
    return QtGui.QIcon(pmKibitzer_Up())


def pmKibitzer_Back():
    return PM(936083,936516)


def Kibitzer_Back():
    return QtGui.QIcon(pmKibitzer_Back())


def pmKibitzer_Clipboard():
    return PM(936516,936902)


def Kibitzer_Clipboard():
    return QtGui.QIcon(pmKibitzer_Clipboard())


def pmKibitzer_Play():
    return PM(936902,937423)


def Kibitzer_Play():
    return QtGui.QIcon(pmKibitzer_Play())


def pmKibitzer_Side():
    return PM(937423,938176)


def Kibitzer_Side():
    return QtGui.QIcon(pmKibitzer_Side())


def pmKibitzer_Board():
    return PM(938176,938614)


def Kibitzer_Board():
    return QtGui.QIcon(pmKibitzer_Board())


def pmBoard():
    return PM(938614,939083)


def Board():
    return QtGui.QIcon(pmBoard())


def pmTraining_Games():
    return PM(939083,940775)


def Training_Games():
    return QtGui.QIcon(pmTraining_Games())


def pmTraining_Basic():
    return PM(940775,942148)


def Training_Basic():
    return QtGui.QIcon(pmTraining_Basic())


def pmTraining_Tactics():
    return PM(942148,942929)


def Training_Tactics():
    return QtGui.QIcon(pmTraining_Tactics())


def pmTraining_Endings():
    return PM(942929,943863)


def Training_Endings():
    return QtGui.QIcon(pmTraining_Endings())


def pmBridge():
    return PM(943863,944881)


def Bridge():
    return QtGui.QIcon(pmBridge())


def pmMaia():
    return PM(944881,945665)


def Maia():
    return QtGui.QIcon(pmMaia())


def pmBinBook():
    return PM(945665,946414)


def BinBook():
    return QtGui.QIcon(pmBinBook())


def pmConnected():
    return PM(946414,948032)


def Connected():
    return QtGui.QIcon(pmConnected())


def pmThemes():
    return PM(948032,948601)


def Themes():
    return QtGui.QIcon(pmThemes())


def pmReset():
    return PM(948601,950220)


def Reset():
    return QtGui.QIcon(pmReset())


def pmInstall():
    return PM(950220,952349)


def Install():
    return QtGui.QIcon(pmInstall())


def pmUninstall():
    return PM(952349,954375)


def Uninstall():
    return QtGui.QIcon(pmUninstall())


def pmLive():
    return PM(954375,957858)


def Live():
    return QtGui.QIcon(pmLive())


def pmLauncher():
    return PM(957858,962533)


def Launcher():
    return QtGui.QIcon(pmLauncher())


def pmLogInactive():
    return PM(962533,963064)


def LogInactive():
    return QtGui.QIcon(pmLogInactive())


def pmLogActive():
    return PM(963064,963628)


def LogActive():
    return QtGui.QIcon(pmLogActive())


def pmFolderAnil():
    return PM(963628,963992)


def FolderAnil():
    return QtGui.QIcon(pmFolderAnil())


def pmFolderBlack():
    return PM(963992,964329)


def FolderBlack():
    return QtGui.QIcon(pmFolderBlack())


def pmFolderBlue():
    return PM(964329,964703)


def FolderBlue():
    return QtGui.QIcon(pmFolderBlue())


def pmFolderGreen():
    return PM(964703,965075)


def FolderGreen():
    return QtGui.QIcon(pmFolderGreen())


def pmFolderMagenta():
    return PM(965075,965448)


def FolderMagenta():
    return QtGui.QIcon(pmFolderMagenta())


def pmFolderRed():
    return PM(965448,965812)


def FolderRed():
    return QtGui.QIcon(pmFolderRed())


def pmThis():
    return PM(965812,966266)


def This():
    return QtGui.QIcon(pmThis())


def pmAll():
    return PM(966266,966769)


def All():
    return QtGui.QIcon(pmAll())


def pmPrevious():
    return PM(966769,967228)


def Previous():
    return QtGui.QIcon(pmPrevious())


def pmLine():
    return PM(967228,967415)


def Line():
    return QtGui.QIcon(pmLine())


def pmEmpty():
    return PM(967415,967500)


def Empty():
    return QtGui.QIcon(pmEmpty())


def pmMore():
    return PM(967500,967789)


def More():
    return QtGui.QIcon(pmMore())


def pmSelectLogo():
    return PM(967789,968395)


def SelectLogo():
    return QtGui.QIcon(pmSelectLogo())


def pmSelect():
    return PM(968395,969049)


def Select():
    return QtGui.QIcon(pmSelect())


def pmSelectClose():
    return PM(969049,969821)


def SelectClose():
    return QtGui.QIcon(pmSelectClose())


def pmSelectHome():
    return PM(969821,970603)


def SelectHome():
    return QtGui.QIcon(pmSelectHome())


def pmSelectHistory():
    return PM(970603,971155)


def SelectHistory():
    return QtGui.QIcon(pmSelectHistory())


def pmSelectExplorer():
    return PM(971155,971888)


def SelectExplorer():
    return QtGui.QIcon(pmSelectExplorer())


def pmSelectFolderCreate():
    return PM(971888,972807)


def SelectFolderCreate():
    return QtGui.QIcon(pmSelectFolderCreate())


def pmSelectFolderRemove():
    return PM(972807,973834)


def SelectFolderRemove():
    return QtGui.QIcon(pmSelectFolderRemove())


def pmSelectReload():
    return PM(973834,975488)


def SelectReload():
    return QtGui.QIcon(pmSelectReload())


def pmSelectAccept():
    return PM(975488,976289)


def SelectAccept():
    return QtGui.QIcon(pmSelectAccept())


def pmWiki():
    return PM(976289,977406)


def Wiki():
    return QtGui.QIcon(pmWiki())


def pmCircle():
    return PM(977406,978866)


def Circle():
    return QtGui.QIcon(pmCircle())


