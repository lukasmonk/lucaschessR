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
    return PM(15278,16063)


def Certabo():
    return QtGui.QIcon(pmCertabo())


def pmNovag():
    return PM(16063,16807)


def Novag():
    return QtGui.QIcon(pmNovag())


def pmFindAllMoves():
    return PM(16807,18403)


def FindAllMoves():
    return QtGui.QIcon(pmFindAllMoves())


def pmResizeBoard():
    return PM(16807,18403)


def ResizeBoard():
    return QtGui.QIcon(pmResizeBoard())


def pmMensEspera():
    return PM(18403,22151)


def MensEspera():
    return QtGui.QIcon(pmMensEspera())


def pmUtilidades():
    return PM(22151,28580)


def Utilidades():
    return QtGui.QIcon(pmUtilidades())


def pmTerminar():
    return PM(28580,30330)


def Terminar():
    return QtGui.QIcon(pmTerminar())


def pmNuevaPartida():
    return PM(30330,32078)


def NuevaPartida():
    return QtGui.QIcon(pmNuevaPartida())


def pmOpciones():
    return PM(32078,33806)


def Opciones():
    return QtGui.QIcon(pmOpciones())


def pmEntrenamiento():
    return PM(7617,9646)


def Entrenamiento():
    return QtGui.QIcon(pmEntrenamiento())


def pmAplazar():
    return PM(33806,36873)


def Aplazar():
    return QtGui.QIcon(pmAplazar())


def pmAplazamientos():
    return PM(36873,40189)


def Aplazamientos():
    return QtGui.QIcon(pmAplazamientos())


def pmCapturas():
    return PM(40189,42230)


def Capturas():
    return QtGui.QIcon(pmCapturas())


def pmReiniciar():
    return PM(42230,44524)


def Reiniciar():
    return QtGui.QIcon(pmReiniciar())


def pmMotores():
    return PM(44524,50423)


def Motores():
    return QtGui.QIcon(pmMotores())


def pmImportarGM():
    return PM(50423,53023)


def ImportarGM():
    return QtGui.QIcon(pmImportarGM())


def pmAbandonar():
    return PM(53023,57023)


def Abandonar():
    return QtGui.QIcon(pmAbandonar())


def pmEmpezar():
    return PM(57023,59059)


def Empezar():
    return QtGui.QIcon(pmEmpezar())


def pmOtros():
    return PM(59059,63529)


def Otros():
    return QtGui.QIcon(pmOtros())


def pmAnalizar():
    return PM(63529,65066)


def Analizar():
    return QtGui.QIcon(pmAnalizar())


def pmMainMenu():
    return PM(65066,69376)


def MainMenu():
    return QtGui.QIcon(pmMainMenu())


def pmFinPartida():
    return PM(69376,72324)


def FinPartida():
    return QtGui.QIcon(pmFinPartida())


def pmGrabar():
    return PM(72324,73787)


def Grabar():
    return QtGui.QIcon(pmGrabar())


def pmGrabarComo():
    return PM(73787,75839)


def GrabarComo():
    return QtGui.QIcon(pmGrabarComo())


def pmRecuperar():
    return PM(75839,78597)


def Recuperar():
    return QtGui.QIcon(pmRecuperar())


def pmInformacion():
    return PM(78597,80556)


def Informacion():
    return QtGui.QIcon(pmInformacion())


def pmNuevo():
    return PM(80556,81310)


def Nuevo():
    return QtGui.QIcon(pmNuevo())


def pmCopiar():
    return PM(81310,82491)


def Copiar():
    return QtGui.QIcon(pmCopiar())


def pmModificar():
    return PM(82491,86888)


def Modificar():
    return QtGui.QIcon(pmModificar())


def pmBorrar():
    return PM(86888,91879)


def Borrar():
    return QtGui.QIcon(pmBorrar())


def pmMarcar():
    return PM(91879,96808)


def Marcar():
    return QtGui.QIcon(pmMarcar())


def pmPegar():
    return PM(96808,99119)


def Pegar():
    return QtGui.QIcon(pmPegar())


def pmFichero():
    return PM(99119,103804)


def Fichero():
    return QtGui.QIcon(pmFichero())


def pmNuestroFichero():
    return PM(103804,106851)


def NuestroFichero():
    return QtGui.QIcon(pmNuestroFichero())


def pmFicheroRepite():
    return PM(106851,108347)


def FicheroRepite():
    return QtGui.QIcon(pmFicheroRepite())


def pmInformacionPGN():
    return PM(108347,109365)


def InformacionPGN():
    return QtGui.QIcon(pmInformacionPGN())


def pmVer():
    return PM(109365,110819)


def Ver():
    return QtGui.QIcon(pmVer())


def pmInicio():
    return PM(110819,112833)


def Inicio():
    return QtGui.QIcon(pmInicio())


def pmFinal():
    return PM(112833,114827)


def Final():
    return QtGui.QIcon(pmFinal())


def pmFiltrar():
    return PM(114827,121317)


def Filtrar():
    return QtGui.QIcon(pmFiltrar())


def pmArriba():
    return PM(121317,123470)


def Arriba():
    return QtGui.QIcon(pmArriba())


def pmAbajo():
    return PM(123470,125578)


def Abajo():
    return QtGui.QIcon(pmAbajo())


def pmEstadisticas():
    return PM(125578,127717)


def Estadisticas():
    return QtGui.QIcon(pmEstadisticas())


def pmCheck():
    return PM(127717,130941)


def Check():
    return QtGui.QIcon(pmCheck())


def pmTablas():
    return PM(130941,132564)


def Tablas():
    return QtGui.QIcon(pmTablas())


def pmAtras():
    return PM(132564,134083)


def Atras():
    return QtGui.QIcon(pmAtras())


def pmBuscar():
    return PM(134083,136068)


def Buscar():
    return QtGui.QIcon(pmBuscar())


def pmLibros():
    return PM(136068,138196)


def Libros():
    return QtGui.QIcon(pmLibros())


def pmAceptar():
    return PM(138196,141543)


def Aceptar():
    return QtGui.QIcon(pmAceptar())


def pmCancelar():
    return PM(141543,143526)


def Cancelar():
    return QtGui.QIcon(pmCancelar())


def pmDefecto():
    return PM(143526,146845)


def Defecto():
    return QtGui.QIcon(pmDefecto())


def pmInsertar():
    return PM(146845,149241)


def Insertar():
    return QtGui.QIcon(pmInsertar())


def pmJugar():
    return PM(149241,151450)


def Jugar():
    return QtGui.QIcon(pmJugar())


def pmConfigurar():
    return PM(151450,154534)


def Configurar():
    return QtGui.QIcon(pmConfigurar())


def pmS_Aceptar():
    return PM(138196,141543)


def S_Aceptar():
    return QtGui.QIcon(pmS_Aceptar())


def pmS_Cancelar():
    return PM(141543,143526)


def S_Cancelar():
    return QtGui.QIcon(pmS_Cancelar())


def pmS_Microfono():
    return PM(154534,159975)


def S_Microfono():
    return QtGui.QIcon(pmS_Microfono())


def pmS_LeerWav():
    return PM(50423,53023)


def S_LeerWav():
    return QtGui.QIcon(pmS_LeerWav())


def pmS_Play():
    return PM(159975,165313)


def S_Play():
    return QtGui.QIcon(pmS_Play())


def pmS_StopPlay():
    return PM(165313,165923)


def S_StopPlay():
    return QtGui.QIcon(pmS_StopPlay())


def pmS_StopMicrofono():
    return PM(165313,165923)


def S_StopMicrofono():
    return QtGui.QIcon(pmS_StopMicrofono())


def pmS_Record():
    return PM(165923,169156)


def S_Record():
    return QtGui.QIcon(pmS_Record())


def pmS_Limpiar():
    return PM(86888,91879)


def S_Limpiar():
    return QtGui.QIcon(pmS_Limpiar())


def pmHistorial():
    return PM(169156,170419)


def Historial():
    return QtGui.QIcon(pmHistorial())


def pmPegar16():
    return PM(170419,171413)


def Pegar16():
    return QtGui.QIcon(pmPegar16())


def pmRivalesMP():
    return PM(171413,174095)


def RivalesMP():
    return QtGui.QIcon(pmRivalesMP())


def pmCamara():
    return PM(174095,175617)


def Camara():
    return QtGui.QIcon(pmCamara())


def pmUsuarios():
    return PM(175617,176857)


def Usuarios():
    return QtGui.QIcon(pmUsuarios())


def pmResistencia():
    return PM(176857,179919)


def Resistencia():
    return QtGui.QIcon(pmResistencia())


def pmCebra():
    return PM(179919,182372)


def Cebra():
    return QtGui.QIcon(pmCebra())


def pmGafas():
    return PM(182372,183530)


def Gafas():
    return QtGui.QIcon(pmGafas())


def pmPuente():
    return PM(183530,184166)


def Puente():
    return QtGui.QIcon(pmPuente())


def pmWeb():
    return PM(184166,185348)


def Web():
    return QtGui.QIcon(pmWeb())


def pmMail():
    return PM(185348,186308)


def Mail():
    return QtGui.QIcon(pmMail())


def pmAyuda():
    return PM(186308,187489)


def Ayuda():
    return QtGui.QIcon(pmAyuda())


def pmFAQ():
    return PM(187489,188810)


def FAQ():
    return QtGui.QIcon(pmFAQ())


def pmActualiza():
    return PM(188810,189676)


def Actualiza():
    return QtGui.QIcon(pmActualiza())


def pmRefresh():
    return PM(189676,192068)


def Refresh():
    return QtGui.QIcon(pmRefresh())


def pmJuegaSolo():
    return PM(192068,193920)


def JuegaSolo():
    return QtGui.QIcon(pmJuegaSolo())


def pmPlayer():
    return PM(193920,195102)


def Player():
    return QtGui.QIcon(pmPlayer())


def pmJS_Rotacion():
    return PM(195102,197012)


def JS_Rotacion():
    return QtGui.QIcon(pmJS_Rotacion())


def pmElo():
    return PM(197012,198518)


def Elo():
    return QtGui.QIcon(pmElo())


def pmMate():
    return PM(198518,199079)


def Mate():
    return QtGui.QIcon(pmMate())


def pmEloTimed():
    return PM(199079,200563)


def EloTimed():
    return QtGui.QIcon(pmEloTimed())


def pmPGN():
    return PM(200563,202561)


def PGN():
    return QtGui.QIcon(pmPGN())


def pmPGN_Importar():
    return PM(202561,204151)


def PGN_Importar():
    return QtGui.QIcon(pmPGN_Importar())


def pmAyudaGR():
    return PM(204151,210029)


def AyudaGR():
    return QtGui.QIcon(pmAyudaGR())


def pmBotonAyuda():
    return PM(210029,212489)


def BotonAyuda():
    return QtGui.QIcon(pmBotonAyuda())


def pmColores():
    return PM(212489,213720)


def Colores():
    return QtGui.QIcon(pmColores())


def pmEditarColores():
    return PM(213720,216023)


def EditarColores():
    return QtGui.QIcon(pmEditarColores())


def pmGranMaestro():
    return PM(216023,216879)


def GranMaestro():
    return QtGui.QIcon(pmGranMaestro())


def pmFavoritos():
    return PM(216879,218645)


def Favoritos():
    return QtGui.QIcon(pmFavoritos())


def pmCarpeta():
    return PM(218645,219349)


def Carpeta():
    return QtGui.QIcon(pmCarpeta())


def pmDivision():
    return PM(219349,220014)


def Division():
    return QtGui.QIcon(pmDivision())


def pmDivisionF():
    return PM(220014,221128)


def DivisionF():
    return QtGui.QIcon(pmDivisionF())


def pmDelete():
    return PM(221128,222052)


def Delete():
    return QtGui.QIcon(pmDelete())


def pmModificarP():
    return PM(222052,223118)


def ModificarP():
    return QtGui.QIcon(pmModificarP())


def pmGrupo_Si():
    return PM(223118,223580)


def Grupo_Si():
    return QtGui.QIcon(pmGrupo_Si())


def pmGrupo_No():
    return PM(223580,223903)


def Grupo_No():
    return QtGui.QIcon(pmGrupo_No())


def pmMotor_Si():
    return PM(223903,224365)


def Motor_Si():
    return QtGui.QIcon(pmMotor_Si())


def pmMotor_No():
    return PM(221128,222052)


def Motor_No():
    return QtGui.QIcon(pmMotor_No())


def pmMotor_Actual():
    return PM(224365,225382)


def Motor_Actual():
    return QtGui.QIcon(pmMotor_Actual())


def pmMotor():
    return PM(225382,226009)


def Motor():
    return QtGui.QIcon(pmMotor())


def pmMoverInicio():
    return PM(226009,226307)


def MoverInicio():
    return QtGui.QIcon(pmMoverInicio())


def pmMoverFinal():
    return PM(226307,226608)


def MoverFinal():
    return QtGui.QIcon(pmMoverFinal())


def pmMoverAdelante():
    return PM(226608,226963)


def MoverAdelante():
    return QtGui.QIcon(pmMoverAdelante())


def pmMoverAtras():
    return PM(226963,227328)


def MoverAtras():
    return QtGui.QIcon(pmMoverAtras())


def pmMoverLibre():
    return PM(227328,227746)


def MoverLibre():
    return QtGui.QIcon(pmMoverLibre())


def pmMoverTiempo():
    return PM(227746,228325)


def MoverTiempo():
    return QtGui.QIcon(pmMoverTiempo())


def pmMoverMas():
    return PM(228325,229364)


def MoverMas():
    return QtGui.QIcon(pmMoverMas())


def pmMoverGrabar():
    return PM(229364,230220)


def MoverGrabar():
    return QtGui.QIcon(pmMoverGrabar())


def pmMoverGrabarTodos():
    return PM(230220,231264)


def MoverGrabarTodos():
    return QtGui.QIcon(pmMoverGrabarTodos())


def pmMoverJugar():
    return PM(231264,232095)


def MoverJugar():
    return QtGui.QIcon(pmMoverJugar())


def pmPelicula():
    return PM(232095,234229)


def Pelicula():
    return QtGui.QIcon(pmPelicula())


def pmPelicula_Pausa():
    return PM(234229,235988)


def Pelicula_Pausa():
    return QtGui.QIcon(pmPelicula_Pausa())


def pmPelicula_Seguir():
    return PM(235988,238077)


def Pelicula_Seguir():
    return QtGui.QIcon(pmPelicula_Seguir())


def pmPelicula_Rapido():
    return PM(238077,240136)


def Pelicula_Rapido():
    return QtGui.QIcon(pmPelicula_Rapido())


def pmPelicula_Lento():
    return PM(240136,242011)


def Pelicula_Lento():
    return QtGui.QIcon(pmPelicula_Lento())


def pmPelicula_Repetir():
    return PM(42230,44524)


def Pelicula_Repetir():
    return QtGui.QIcon(pmPelicula_Repetir())


def pmPelicula_PGN():
    return PM(242011,242919)


def Pelicula_PGN():
    return QtGui.QIcon(pmPelicula_PGN())


def pmMemoria():
    return PM(242919,244860)


def Memoria():
    return QtGui.QIcon(pmMemoria())


def pmEntrenar():
    return PM(244860,246399)


def Entrenar():
    return QtGui.QIcon(pmEntrenar())


def pmEnviar():
    return PM(244860,246399)


def Enviar():
    return QtGui.QIcon(pmEnviar())


def pmBoxRooms():
    return PM(246399,251202)


def BoxRooms():
    return QtGui.QIcon(pmBoxRooms())


def pmBoxRoom():
    return PM(251202,251664)


def BoxRoom():
    return QtGui.QIcon(pmBoxRoom())


def pmNewBoxRoom():
    return PM(251664,253172)


def NewBoxRoom():
    return QtGui.QIcon(pmNewBoxRoom())


def pmNuevoMas():
    return PM(251664,253172)


def NuevoMas():
    return QtGui.QIcon(pmNuevoMas())


def pmTemas():
    return PM(253172,255395)


def Temas():
    return QtGui.QIcon(pmTemas())


def pmTutorialesCrear():
    return PM(255395,261664)


def TutorialesCrear():
    return QtGui.QIcon(pmTutorialesCrear())


def pmMover():
    return PM(261664,262246)


def Mover():
    return QtGui.QIcon(pmMover())


def pmSeleccionar():
    return PM(262246,267950)


def Seleccionar():
    return QtGui.QIcon(pmSeleccionar())


def pmVista():
    return PM(267950,269874)


def Vista():
    return QtGui.QIcon(pmVista())


def pmInformacionPGNUno():
    return PM(269874,271252)


def InformacionPGNUno():
    return QtGui.QIcon(pmInformacionPGNUno())


def pmDailyTest():
    return PM(271252,273592)


def DailyTest():
    return QtGui.QIcon(pmDailyTest())


def pmJuegaPorMi():
    return PM(273592,275312)


def JuegaPorMi():
    return QtGui.QIcon(pmJuegaPorMi())


def pmArbol():
    return PM(275312,275946)


def Arbol():
    return QtGui.QIcon(pmArbol())


def pmGrabarFichero():
    return PM(72324,73787)


def GrabarFichero():
    return QtGui.QIcon(pmGrabarFichero())


def pmClipboard():
    return PM(275946,276724)


def Clipboard():
    return QtGui.QIcon(pmClipboard())


def pmFics():
    return PM(276724,277141)


def Fics():
    return QtGui.QIcon(pmFics())


def pmFide():
    return PM(9646,11623)


def Fide():
    return QtGui.QIcon(pmFide())


def pmFichPGN():
    return PM(30330,32078)


def FichPGN():
    return QtGui.QIcon(pmFichPGN())


def pmFlechas():
    return PM(277141,280493)


def Flechas():
    return QtGui.QIcon(pmFlechas())


def pmMarcos():
    return PM(280493,281940)


def Marcos():
    return QtGui.QIcon(pmMarcos())


def pmSVGs():
    return PM(281940,285509)


def SVGs():
    return QtGui.QIcon(pmSVGs())


def pmAmarillo():
    return PM(285509,286761)


def Amarillo():
    return QtGui.QIcon(pmAmarillo())


def pmNaranja():
    return PM(286761,287993)


def Naranja():
    return QtGui.QIcon(pmNaranja())


def pmVerde():
    return PM(287993,289269)


def Verde():
    return QtGui.QIcon(pmVerde())


def pmAzul():
    return PM(289269,290357)


def Azul():
    return QtGui.QIcon(pmAzul())


def pmMagenta():
    return PM(290357,291645)


def Magenta():
    return QtGui.QIcon(pmMagenta())


def pmRojo():
    return PM(291645,292864)


def Rojo():
    return QtGui.QIcon(pmRojo())


def pmGris():
    return PM(292864,293822)


def Gris():
    return QtGui.QIcon(pmGris())


def pmAmarillo32():
    return PM(293822,295802)


def Amarillo32():
    return QtGui.QIcon(pmAmarillo32())


def pmNaranja32():
    return PM(295802,297926)


def Naranja32():
    return QtGui.QIcon(pmNaranja32())


def pmVerde32():
    return PM(297926,300047)


def Verde32():
    return QtGui.QIcon(pmVerde32())


def pmAzul32():
    return PM(300047,302426)


def Azul32():
    return QtGui.QIcon(pmAzul32())


def pmMagenta32():
    return PM(302426,304877)


def Magenta32():
    return QtGui.QIcon(pmMagenta32())


def pmRojo32():
    return PM(304877,306692)


def Rojo32():
    return QtGui.QIcon(pmRojo32())


def pmGris32():
    return PM(306692,308606)


def Gris32():
    return QtGui.QIcon(pmGris32())


def pmPuntoBlanco():
    return PM(308606,308955)


def PuntoBlanco():
    return QtGui.QIcon(pmPuntoBlanco())


def pmPuntoAmarillo():
    return PM(223118,223580)


def PuntoAmarillo():
    return QtGui.QIcon(pmPuntoAmarillo())


def pmPuntoNaranja():
    return PM(308955,309417)


def PuntoNaranja():
    return QtGui.QIcon(pmPuntoNaranja())


def pmPuntoVerde():
    return PM(223903,224365)


def PuntoVerde():
    return QtGui.QIcon(pmPuntoVerde())


def pmPuntoAzul():
    return PM(251202,251664)


def PuntoAzul():
    return QtGui.QIcon(pmPuntoAzul())


def pmPuntoMagenta():
    return PM(309417,309916)


def PuntoMagenta():
    return QtGui.QIcon(pmPuntoMagenta())


def pmPuntoRojo():
    return PM(309916,310415)


def PuntoRojo():
    return QtGui.QIcon(pmPuntoRojo())


def pmPuntoNegro():
    return PM(223580,223903)


def PuntoNegro():
    return QtGui.QIcon(pmPuntoNegro())


def pmPuntoEstrella():
    return PM(310415,310842)


def PuntoEstrella():
    return QtGui.QIcon(pmPuntoEstrella())


def pmComentario():
    return PM(310842,311479)


def Comentario():
    return QtGui.QIcon(pmComentario())


def pmComentarioMas():
    return PM(311479,312418)


def ComentarioMas():
    return QtGui.QIcon(pmComentarioMas())


def pmComentarioEditar():
    return PM(229364,230220)


def ComentarioEditar():
    return QtGui.QIcon(pmComentarioEditar())


def pmOpeningComentario():
    return PM(312418,313414)


def OpeningComentario():
    return QtGui.QIcon(pmOpeningComentario())


def pmMas():
    return PM(313414,313923)


def Mas():
    return QtGui.QIcon(pmMas())


def pmMasR():
    return PM(313923,314411)


def MasR():
    return QtGui.QIcon(pmMasR())


def pmMasDoc():
    return PM(314411,315212)


def MasDoc():
    return QtGui.QIcon(pmMasDoc())


def pmPotencia():
    return PM(188810,189676)


def Potencia():
    return QtGui.QIcon(pmPotencia())


def pmBMT():
    return PM(315212,316090)


def BMT():
    return QtGui.QIcon(pmBMT())


def pmOjo():
    return PM(316090,317212)


def Ojo():
    return QtGui.QIcon(pmOjo())


def pmOcultar():
    return PM(316090,317212)


def Ocultar():
    return QtGui.QIcon(pmOcultar())


def pmMostrar():
    return PM(317212,318268)


def Mostrar():
    return QtGui.QIcon(pmMostrar())


def pmBlog():
    return PM(318268,318790)


def Blog():
    return QtGui.QIcon(pmBlog())


def pmVariations():
    return PM(318790,319697)


def Variations():
    return QtGui.QIcon(pmVariations())


def pmVariationsG():
    return PM(319697,322124)


def VariationsG():
    return QtGui.QIcon(pmVariationsG())


def pmCambiar():
    return PM(322124,323838)


def Cambiar():
    return QtGui.QIcon(pmCambiar())


def pmAnterior():
    return PM(323838,325892)


def Anterior():
    return QtGui.QIcon(pmAnterior())


def pmSiguiente():
    return PM(325892,327962)


def Siguiente():
    return QtGui.QIcon(pmSiguiente())


def pmSiguienteF():
    return PM(327962,330137)


def SiguienteF():
    return QtGui.QIcon(pmSiguienteF())


def pmAnteriorF():
    return PM(330137,332331)


def AnteriorF():
    return QtGui.QIcon(pmAnteriorF())


def pmX():
    return PM(332331,333613)


def X():
    return QtGui.QIcon(pmX())


def pmTools():
    return PM(333613,336214)


def Tools():
    return QtGui.QIcon(pmTools())


def pmTacticas():
    return PM(336214,338787)


def Tacticas():
    return QtGui.QIcon(pmTacticas())


def pmCancelarPeque():
    return PM(338787,339349)


def CancelarPeque():
    return QtGui.QIcon(pmCancelarPeque())


def pmAceptarPeque():
    return PM(224365,225382)


def AceptarPeque():
    return QtGui.QIcon(pmAceptarPeque())


def pmLibre():
    return PM(339349,341741)


def Libre():
    return QtGui.QIcon(pmLibre())


def pmEnBlanco():
    return PM(341741,342467)


def EnBlanco():
    return QtGui.QIcon(pmEnBlanco())


def pmDirector():
    return PM(342467,345441)


def Director():
    return QtGui.QIcon(pmDirector())


def pmTorneos():
    return PM(345441,347179)


def Torneos():
    return QtGui.QIcon(pmTorneos())


def pmOpenings():
    return PM(347179,348104)


def Openings():
    return QtGui.QIcon(pmOpenings())


def pmV_Blancas():
    return PM(348104,348384)


def V_Blancas():
    return QtGui.QIcon(pmV_Blancas())


def pmV_Blancas_Mas():
    return PM(348384,348664)


def V_Blancas_Mas():
    return QtGui.QIcon(pmV_Blancas_Mas())


def pmV_Blancas_Mas_Mas():
    return PM(348664,348936)


def V_Blancas_Mas_Mas():
    return QtGui.QIcon(pmV_Blancas_Mas_Mas())


def pmV_Negras():
    return PM(348936,349211)


def V_Negras():
    return QtGui.QIcon(pmV_Negras())


def pmV_Negras_Mas():
    return PM(349211,349486)


def V_Negras_Mas():
    return QtGui.QIcon(pmV_Negras_Mas())


def pmV_Negras_Mas_Mas():
    return PM(349486,349755)


def V_Negras_Mas_Mas():
    return QtGui.QIcon(pmV_Negras_Mas_Mas())


def pmV_Blancas_Igual_Negras():
    return PM(349755,350057)


def V_Blancas_Igual_Negras():
    return QtGui.QIcon(pmV_Blancas_Igual_Negras())


def pmMezclar():
    return PM(146845,149241)


def Mezclar():
    return QtGui.QIcon(pmMezclar())


def pmVoyager():
    return PM(350057,350900)


def Voyager():
    return QtGui.QIcon(pmVoyager())


def pmVoyager32():
    return PM(350900,352788)


def Voyager32():
    return QtGui.QIcon(pmVoyager32())


def pmReindexar():
    return PM(352788,354605)


def Reindexar():
    return QtGui.QIcon(pmReindexar())


def pmRename():
    return PM(354605,355589)


def Rename():
    return QtGui.QIcon(pmRename())


def pmAdd():
    return PM(355589,356542)


def Add():
    return QtGui.QIcon(pmAdd())


def pmMas22():
    return PM(356542,357206)


def Mas22():
    return QtGui.QIcon(pmMas22())


def pmMenos22():
    return PM(357206,357650)


def Menos22():
    return QtGui.QIcon(pmMenos22())


def pmTransposition():
    return PM(357650,358169)


def Transposition():
    return QtGui.QIcon(pmTransposition())


def pmRat():
    return PM(358169,363873)


def Rat():
    return QtGui.QIcon(pmRat())


def pmAlligator():
    return PM(363873,368865)


def Alligator():
    return QtGui.QIcon(pmAlligator())


def pmAnt():
    return PM(368865,375563)


def Ant():
    return QtGui.QIcon(pmAnt())


def pmBat():
    return PM(375563,378517)


def Bat():
    return QtGui.QIcon(pmBat())


def pmBear():
    return PM(378517,385796)


def Bear():
    return QtGui.QIcon(pmBear())


def pmBee():
    return PM(385796,390798)


def Bee():
    return QtGui.QIcon(pmBee())


def pmBird():
    return PM(390798,396857)


def Bird():
    return QtGui.QIcon(pmBird())


def pmBull():
    return PM(396857,403826)


def Bull():
    return QtGui.QIcon(pmBull())


def pmBulldog():
    return PM(403826,410717)


def Bulldog():
    return QtGui.QIcon(pmBulldog())


def pmButterfly():
    return PM(410717,418091)


def Butterfly():
    return QtGui.QIcon(pmButterfly())


def pmCat():
    return PM(418091,424363)


def Cat():
    return QtGui.QIcon(pmCat())


def pmChicken():
    return PM(424363,430174)


def Chicken():
    return QtGui.QIcon(pmChicken())


def pmCow():
    return PM(430174,436917)


def Cow():
    return QtGui.QIcon(pmCow())


def pmCrab():
    return PM(436917,442506)


def Crab():
    return QtGui.QIcon(pmCrab())


def pmCrocodile():
    return PM(442506,448647)


def Crocodile():
    return QtGui.QIcon(pmCrocodile())


def pmDeer():
    return PM(448647,454954)


def Deer():
    return QtGui.QIcon(pmDeer())


def pmDog():
    return PM(454954,461557)


def Dog():
    return QtGui.QIcon(pmDog())


def pmDonkey():
    return PM(461557,467204)


def Donkey():
    return QtGui.QIcon(pmDonkey())


def pmDuck():
    return PM(467204,473747)


def Duck():
    return QtGui.QIcon(pmDuck())


def pmEagle():
    return PM(473747,478565)


def Eagle():
    return QtGui.QIcon(pmEagle())


def pmElephant():
    return PM(478565,485046)


def Elephant():
    return QtGui.QIcon(pmElephant())


def pmFish():
    return PM(485046,491887)


def Fish():
    return QtGui.QIcon(pmFish())


def pmFox():
    return PM(491887,498670)


def Fox():
    return QtGui.QIcon(pmFox())


def pmFrog():
    return PM(498670,505086)


def Frog():
    return QtGui.QIcon(pmFrog())


def pmGiraffe():
    return PM(505086,512264)


def Giraffe():
    return QtGui.QIcon(pmGiraffe())


def pmGorilla():
    return PM(512264,518803)


def Gorilla():
    return QtGui.QIcon(pmGorilla())


def pmHippo():
    return PM(518803,525924)


def Hippo():
    return QtGui.QIcon(pmHippo())


def pmHorse():
    return PM(525924,532471)


def Horse():
    return QtGui.QIcon(pmHorse())


def pmInsect():
    return PM(532471,538406)


def Insect():
    return QtGui.QIcon(pmInsect())


def pmLion():
    return PM(538406,547316)


def Lion():
    return QtGui.QIcon(pmLion())


def pmMonkey():
    return PM(547316,554995)


def Monkey():
    return QtGui.QIcon(pmMonkey())


def pmMoose():
    return PM(554995,561619)


def Moose():
    return QtGui.QIcon(pmMoose())


def pmMouse():
    return PM(358169,363873)


def Mouse():
    return QtGui.QIcon(pmMouse())


def pmOwl():
    return PM(561619,568325)


def Owl():
    return QtGui.QIcon(pmOwl())


def pmPanda():
    return PM(568325,572359)


def Panda():
    return QtGui.QIcon(pmPanda())


def pmPenguin():
    return PM(572359,577908)


def Penguin():
    return QtGui.QIcon(pmPenguin())


def pmPig():
    return PM(577908,585948)


def Pig():
    return QtGui.QIcon(pmPig())


def pmRabbit():
    return PM(585948,593249)


def Rabbit():
    return QtGui.QIcon(pmRabbit())


def pmRhino():
    return PM(593249,599636)


def Rhino():
    return QtGui.QIcon(pmRhino())


def pmRooster():
    return PM(599636,604899)


def Rooster():
    return QtGui.QIcon(pmRooster())


def pmShark():
    return PM(604899,610669)


def Shark():
    return QtGui.QIcon(pmShark())


def pmSheep():
    return PM(610669,614500)


def Sheep():
    return QtGui.QIcon(pmSheep())


def pmSnake():
    return PM(614500,620525)


def Snake():
    return QtGui.QIcon(pmSnake())


def pmTiger():
    return PM(620525,628562)


def Tiger():
    return QtGui.QIcon(pmTiger())


def pmTurkey():
    return PM(628562,635976)


def Turkey():
    return QtGui.QIcon(pmTurkey())


def pmTurtle():
    return PM(635976,642697)


def Turtle():
    return QtGui.QIcon(pmTurtle())


def pmWolf():
    return PM(642697,645792)


def Wolf():
    return QtGui.QIcon(pmWolf())


def pmSteven():
    return PM(645792,652944)


def Steven():
    return QtGui.QIcon(pmSteven())


def pmWheel():
    return PM(652944,661009)


def Wheel():
    return QtGui.QIcon(pmWheel())


def pmWheelchair():
    return PM(661009,669813)


def Wheelchair():
    return QtGui.QIcon(pmWheelchair())


def pmTouringMotorcycle():
    return PM(669813,676125)


def TouringMotorcycle():
    return QtGui.QIcon(pmTouringMotorcycle())


def pmContainer():
    return PM(676125,681460)


def Container():
    return QtGui.QIcon(pmContainer())


def pmBoatEquipment():
    return PM(681460,686983)


def BoatEquipment():
    return QtGui.QIcon(pmBoatEquipment())


def pmCar():
    return PM(686983,691629)


def Car():
    return QtGui.QIcon(pmCar())


def pmLorry():
    return PM(691629,697665)


def Lorry():
    return QtGui.QIcon(pmLorry())


def pmCarTrailer():
    return PM(697665,701762)


def CarTrailer():
    return QtGui.QIcon(pmCarTrailer())


def pmTowTruck():
    return PM(701762,706520)


def TowTruck():
    return QtGui.QIcon(pmTowTruck())


def pmQuadBike():
    return PM(706520,712489)


def QuadBike():
    return QtGui.QIcon(pmQuadBike())


def pmRecoveryTruck():
    return PM(712489,717486)


def RecoveryTruck():
    return QtGui.QIcon(pmRecoveryTruck())


def pmContainerLoader():
    return PM(717486,722628)


def ContainerLoader():
    return QtGui.QIcon(pmContainerLoader())


def pmPoliceCar():
    return PM(722628,727460)


def PoliceCar():
    return QtGui.QIcon(pmPoliceCar())


def pmExecutiveCar():
    return PM(727460,732138)


def ExecutiveCar():
    return QtGui.QIcon(pmExecutiveCar())


def pmTruck():
    return PM(732138,737601)


def Truck():
    return QtGui.QIcon(pmTruck())


def pmExcavator():
    return PM(737601,742492)


def Excavator():
    return QtGui.QIcon(pmExcavator())


def pmCabriolet():
    return PM(742492,747330)


def Cabriolet():
    return QtGui.QIcon(pmCabriolet())


def pmMixerTruck():
    return PM(747330,753640)


def MixerTruck():
    return QtGui.QIcon(pmMixerTruck())


def pmForkliftTruckLoaded():
    return PM(753640,759788)


def ForkliftTruckLoaded():
    return QtGui.QIcon(pmForkliftTruckLoaded())


def pmAmbulance():
    return PM(759788,765838)


def Ambulance():
    return QtGui.QIcon(pmAmbulance())


def pmDieselLocomotiveBoxcar():
    return PM(765838,769844)


def DieselLocomotiveBoxcar():
    return QtGui.QIcon(pmDieselLocomotiveBoxcar())


def pmTractorUnit():
    return PM(769844,775311)


def TractorUnit():
    return QtGui.QIcon(pmTractorUnit())


def pmFireTruck():
    return PM(775311,781650)


def FireTruck():
    return QtGui.QIcon(pmFireTruck())


def pmCargoShip():
    return PM(781650,785991)


def CargoShip():
    return QtGui.QIcon(pmCargoShip())


def pmSubwayTrain():
    return PM(785991,790881)


def SubwayTrain():
    return QtGui.QIcon(pmSubwayTrain())


def pmTruckMountedCrane():
    return PM(790881,796622)


def TruckMountedCrane():
    return QtGui.QIcon(pmTruckMountedCrane())


def pmAirAmbulance():
    return PM(796622,801735)


def AirAmbulance():
    return QtGui.QIcon(pmAirAmbulance())


def pmAirplane():
    return PM(801735,806623)


def Airplane():
    return QtGui.QIcon(pmAirplane())


def pmCaracol():
    return PM(806623,808439)


def Caracol():
    return QtGui.QIcon(pmCaracol())


def pmUno():
    return PM(808439,810901)


def Uno():
    return QtGui.QIcon(pmUno())


def pmMotoresExternos():
    return PM(810901,812803)


def MotoresExternos():
    return QtGui.QIcon(pmMotoresExternos())


def pmDatabase():
    return PM(812803,814119)


def Database():
    return QtGui.QIcon(pmDatabase())


def pmDatabaseMas():
    return PM(814119,815578)


def DatabaseMas():
    return QtGui.QIcon(pmDatabaseMas())


def pmDatabaseImport():
    return PM(815578,816214)


def DatabaseImport():
    return QtGui.QIcon(pmDatabaseImport())


def pmDatabaseExport():
    return PM(816214,816859)


def DatabaseExport():
    return QtGui.QIcon(pmDatabaseExport())


def pmDatabaseDelete():
    return PM(816859,817982)


def DatabaseDelete():
    return QtGui.QIcon(pmDatabaseDelete())


def pmDatabaseMaintenance():
    return PM(817982,819478)


def DatabaseMaintenance():
    return QtGui.QIcon(pmDatabaseMaintenance())


def pmAtacante():
    return PM(819478,820083)


def Atacante():
    return QtGui.QIcon(pmAtacante())


def pmAtacada():
    return PM(820083,820649)


def Atacada():
    return QtGui.QIcon(pmAtacada())


def pmGoToNext():
    return PM(820649,821061)


def GoToNext():
    return QtGui.QIcon(pmGoToNext())


def pmBlancas():
    return PM(821061,821412)


def Blancas():
    return QtGui.QIcon(pmBlancas())


def pmNegras():
    return PM(821412,821658)


def Negras():
    return QtGui.QIcon(pmNegras())


def pmFolderChange():
    return PM(75839,78597)


def FolderChange():
    return QtGui.QIcon(pmFolderChange())


def pmMarkers():
    return PM(821658,823353)


def Markers():
    return QtGui.QIcon(pmMarkers())


def pmTop():
    return PM(823353,823937)


def Top():
    return QtGui.QIcon(pmTop())


def pmBottom():
    return PM(823937,824526)


def Bottom():
    return QtGui.QIcon(pmBottom())


def pmSTS():
    return PM(824526,826717)


def STS():
    return QtGui.QIcon(pmSTS())


def pmRun():
    return PM(826717,828441)


def Run():
    return QtGui.QIcon(pmRun())


def pmRun2():
    return PM(828441,829961)


def Run2():
    return QtGui.QIcon(pmRun2())


def pmWorldMap():
    return PM(829961,832702)


def WorldMap():
    return QtGui.QIcon(pmWorldMap())


def pmAfrica():
    return PM(832702,835188)


def Africa():
    return QtGui.QIcon(pmAfrica())


def pmMaps():
    return PM(835188,836132)


def Maps():
    return QtGui.QIcon(pmMaps())


def pmSol():
    return PM(836132,837058)


def Sol():
    return QtGui.QIcon(pmSol())


def pmSolNubes():
    return PM(837058,837921)


def SolNubes():
    return QtGui.QIcon(pmSolNubes())


def pmSolNubesLluvia():
    return PM(837921,838881)


def SolNubesLluvia():
    return QtGui.QIcon(pmSolNubesLluvia())


def pmLluvia():
    return PM(838881,839720)


def Lluvia():
    return QtGui.QIcon(pmLluvia())


def pmInvierno():
    return PM(839720,841296)


def Invierno():
    return QtGui.QIcon(pmInvierno())


def pmFixedElo():
    return PM(169156,170419)


def FixedElo():
    return QtGui.QIcon(pmFixedElo())


def pmSoundTool():
    return PM(841296,843755)


def SoundTool():
    return QtGui.QIcon(pmSoundTool())


def pmTrain():
    return PM(843755,845125)


def Train():
    return QtGui.QIcon(pmTrain())


def pmPlay():
    return PM(235988,238077)


def Play():
    return QtGui.QIcon(pmPlay())


def pmMeasure():
    return PM(130941,132564)


def Measure():
    return QtGui.QIcon(pmMeasure())


def pmPlayGame():
    return PM(845125,849483)


def PlayGame():
    return QtGui.QIcon(pmPlayGame())


def pmScanner():
    return PM(849483,849824)


def Scanner():
    return QtGui.QIcon(pmScanner())


def pmMenos():
    return PM(849824,850349)


def Menos():
    return QtGui.QIcon(pmMenos())


def pmSchool():
    return PM(850349,851711)


def School():
    return QtGui.QIcon(pmSchool())


def pmLaw():
    return PM(851711,852327)


def Law():
    return QtGui.QIcon(pmLaw())


def pmLearnGame():
    return PM(852327,852760)


def LearnGame():
    return QtGui.QIcon(pmLearnGame())


def pmLonghaul():
    return PM(852760,853686)


def Longhaul():
    return QtGui.QIcon(pmLonghaul())


def pmTrekking():
    return PM(853686,854380)


def Trekking():
    return QtGui.QIcon(pmTrekking())


def pmPassword():
    return PM(854380,854833)


def Password():
    return QtGui.QIcon(pmPassword())


def pmSQL_RAW():
    return PM(845125,849483)


def SQL_RAW():
    return QtGui.QIcon(pmSQL_RAW())


def pmSun():
    return PM(315212,316090)


def Sun():
    return QtGui.QIcon(pmSun())


def pmLight32():
    return PM(854833,856533)


def Light32():
    return QtGui.QIcon(pmLight32())


def pmTOL():
    return PM(856533,857242)


def TOL():
    return QtGui.QIcon(pmTOL())


def pmUned():
    return PM(857242,857662)


def Uned():
    return QtGui.QIcon(pmUned())


def pmUwe():
    return PM(857662,858631)


def Uwe():
    return QtGui.QIcon(pmUwe())


def pmThinking():
    return PM(858631,859420)


def Thinking():
    return QtGui.QIcon(pmThinking())


def pmWashingMachine():
    return PM(859420,860083)


def WashingMachine():
    return QtGui.QIcon(pmWashingMachine())


def pmTerminal():
    return PM(860083,863627)


def Terminal():
    return QtGui.QIcon(pmTerminal())


def pmManualSave():
    return PM(863627,864210)


def ManualSave():
    return QtGui.QIcon(pmManualSave())


def pmSettings():
    return PM(864210,864648)


def Settings():
    return QtGui.QIcon(pmSettings())


def pmStrength():
    return PM(864648,865319)


def Strength():
    return QtGui.QIcon(pmStrength())


def pmSingular():
    return PM(865319,866174)


def Singular():
    return QtGui.QIcon(pmSingular())


def pmScript():
    return PM(866174,866743)


def Script():
    return QtGui.QIcon(pmScript())


def pmTexto():
    return PM(866743,869588)


def Texto():
    return QtGui.QIcon(pmTexto())


def pmLampara():
    return PM(869588,870297)


def Lampara():
    return QtGui.QIcon(pmLampara())


def pmFile():
    return PM(870297,872597)


def File():
    return QtGui.QIcon(pmFile())


def pmCalculo():
    return PM(872597,873523)


def Calculo():
    return QtGui.QIcon(pmCalculo())


def pmOpeningLines():
    return PM(873523,874201)


def OpeningLines():
    return QtGui.QIcon(pmOpeningLines())


def pmStudy():
    return PM(874201,875114)


def Study():
    return QtGui.QIcon(pmStudy())


def pmLichess():
    return PM(875114,876002)


def Lichess():
    return QtGui.QIcon(pmLichess())


def pmMiniatura():
    return PM(876002,876929)


def Miniatura():
    return QtGui.QIcon(pmMiniatura())


def pmLocomotora():
    return PM(876929,877710)


def Locomotora():
    return QtGui.QIcon(pmLocomotora())


def pmTrainSequential():
    return PM(877710,878851)


def TrainSequential():
    return QtGui.QIcon(pmTrainSequential())


def pmTrainStatic():
    return PM(878851,879811)


def TrainStatic():
    return QtGui.QIcon(pmTrainStatic())


def pmTrainPositions():
    return PM(879811,880792)


def TrainPositions():
    return QtGui.QIcon(pmTrainPositions())


def pmTrainEngines():
    return PM(880792,882226)


def TrainEngines():
    return QtGui.QIcon(pmTrainEngines())


def pmError():
    return PM(53023,57023)


def Error():
    return QtGui.QIcon(pmError())


def pmAtajos():
    return PM(882226,883405)


def Atajos():
    return QtGui.QIcon(pmAtajos())


def pmTOLline():
    return PM(883405,884509)


def TOLline():
    return QtGui.QIcon(pmTOLline())


def pmTOLchange():
    return PM(884509,886731)


def TOLchange():
    return QtGui.QIcon(pmTOLchange())


def pmPack():
    return PM(886731,887904)


def Pack():
    return QtGui.QIcon(pmPack())


def pmHome():
    return PM(184166,185348)


def Home():
    return QtGui.QIcon(pmHome())


def pmImport8():
    return PM(887904,888662)


def Import8():
    return QtGui.QIcon(pmImport8())


def pmExport8():
    return PM(888662,889287)


def Export8():
    return QtGui.QIcon(pmExport8())


def pmTablas8():
    return PM(889287,890079)


def Tablas8():
    return QtGui.QIcon(pmTablas8())


def pmBlancas8():
    return PM(890079,891109)


def Blancas8():
    return QtGui.QIcon(pmBlancas8())


def pmNegras8():
    return PM(891109,891948)


def Negras8():
    return QtGui.QIcon(pmNegras8())


def pmBook():
    return PM(891948,892522)


def Book():
    return QtGui.QIcon(pmBook())


def pmWrite():
    return PM(892522,893727)


def Write():
    return QtGui.QIcon(pmWrite())


def pmAlt():
    return PM(893727,894169)


def Alt():
    return QtGui.QIcon(pmAlt())


def pmShift():
    return PM(894169,894509)


def Shift():
    return QtGui.QIcon(pmShift())


def pmRightMouse():
    return PM(894509,895309)


def RightMouse():
    return QtGui.QIcon(pmRightMouse())


def pmControl():
    return PM(895309,895834)


def Control():
    return QtGui.QIcon(pmControl())


def pmFinales():
    return PM(895834,896921)


def Finales():
    return QtGui.QIcon(pmFinales())


def pmEditColumns():
    return PM(896921,897653)


def EditColumns():
    return QtGui.QIcon(pmEditColumns())


def pmResizeAll():
    return PM(897653,898163)


def ResizeAll():
    return QtGui.QIcon(pmResizeAll())


def pmChecked():
    return PM(898163,898669)


def Checked():
    return QtGui.QIcon(pmChecked())


def pmUnchecked():
    return PM(898669,898917)


def Unchecked():
    return QtGui.QIcon(pmUnchecked())


def pmBuscarC():
    return PM(898917,899361)


def BuscarC():
    return QtGui.QIcon(pmBuscarC())


def pmPeonBlanco():
    return PM(899361,901542)


def PeonBlanco():
    return QtGui.QIcon(pmPeonBlanco())


def pmPeonNegro():
    return PM(901542,903066)


def PeonNegro():
    return QtGui.QIcon(pmPeonNegro())


def pmReciclar():
    return PM(903066,903790)


def Reciclar():
    return QtGui.QIcon(pmReciclar())


def pmLanzamiento():
    return PM(903790,904503)


def Lanzamiento():
    return QtGui.QIcon(pmLanzamiento())


def pmEndGame():
    return PM(904503,904917)


def EndGame():
    return QtGui.QIcon(pmEndGame())


def pmPause():
    return PM(904917,905786)


def Pause():
    return QtGui.QIcon(pmPause())


def pmContinue():
    return PM(905786,906990)


def Continue():
    return QtGui.QIcon(pmContinue())


def pmClose():
    return PM(906990,907689)


def Close():
    return QtGui.QIcon(pmClose())


def pmStop():
    return PM(907689,908722)


def Stop():
    return QtGui.QIcon(pmStop())


def pmFactoryPolyglot():
    return PM(908722,909542)


def FactoryPolyglot():
    return QtGui.QIcon(pmFactoryPolyglot())


def pmTags():
    return PM(909542,910365)


def Tags():
    return QtGui.QIcon(pmTags())


def pmAppearance():
    return PM(910365,911092)


def Appearance():
    return QtGui.QIcon(pmAppearance())


def pmFill():
    return PM(911092,912130)


def Fill():
    return QtGui.QIcon(pmFill())


def pmSupport():
    return PM(912130,912862)


def Support():
    return QtGui.QIcon(pmSupport())


def pmOrder():
    return PM(912862,913660)


def Order():
    return QtGui.QIcon(pmOrder())


def pmPlay1():
    return PM(913660,914955)


def Play1():
    return QtGui.QIcon(pmPlay1())


def pmRemove1():
    return PM(914955,916082)


def Remove1():
    return QtGui.QIcon(pmRemove1())


def pmNew1():
    return PM(916082,916404)


def New1():
    return QtGui.QIcon(pmNew1())


def pmMensError():
    return PM(916404,918468)


def MensError():
    return QtGui.QIcon(pmMensError())


def pmMensInfo():
    return PM(918468,921023)


def MensInfo():
    return QtGui.QIcon(pmMensInfo())


def pmJump():
    return PM(921023,921698)


def Jump():
    return QtGui.QIcon(pmJump())


def pmCaptures():
    return PM(921698,922879)


def Captures():
    return QtGui.QIcon(pmCaptures())


def pmRepeat():
    return PM(922879,923538)


def Repeat():
    return QtGui.QIcon(pmRepeat())


def pmCount():
    return PM(923538,924214)


def Count():
    return QtGui.QIcon(pmCount())


def pmMate15():
    return PM(924214,925285)


def Mate15():
    return QtGui.QIcon(pmMate15())


def pmCoordinates():
    return PM(925285,926438)


def Coordinates():
    return QtGui.QIcon(pmCoordinates())


def pmKnight():
    return PM(926438,927681)


def Knight():
    return QtGui.QIcon(pmKnight())


def pmCorrecto():
    return PM(927681,928707)


def Correcto():
    return QtGui.QIcon(pmCorrecto())


def pmBlocks():
    return PM(928707,929044)


def Blocks():
    return QtGui.QIcon(pmBlocks())


def pmWest():
    return PM(929044,930150)


def West():
    return QtGui.QIcon(pmWest())


def pmOpening():
    return PM(930150,930408)


def Opening():
    return QtGui.QIcon(pmOpening())


def pmVariation():
    return PM(227328,227746)


def Variation():
    return QtGui.QIcon(pmVariation())


def pmComment():
    return PM(930408,930771)


def Comment():
    return QtGui.QIcon(pmComment())


def pmVariationComment():
    return PM(930771,931115)


def VariationComment():
    return QtGui.QIcon(pmVariationComment())


def pmOpeningVariation():
    return PM(931115,931579)


def OpeningVariation():
    return QtGui.QIcon(pmOpeningVariation())


def pmOpeningComment():
    return PM(931579,931912)


def OpeningComment():
    return QtGui.QIcon(pmOpeningComment())


def pmOpeningVariationComment():
    return PM(931115,931579)


def OpeningVariationComment():
    return QtGui.QIcon(pmOpeningVariationComment())


def pmDeleteRow():
    return PM(931912,932343)


def DeleteRow():
    return QtGui.QIcon(pmDeleteRow())


def pmDeleteColumn():
    return PM(932343,932786)


def DeleteColumn():
    return QtGui.QIcon(pmDeleteColumn())


def pmEditVariation():
    return PM(932786,933141)


def EditVariation():
    return QtGui.QIcon(pmEditVariation())


def pmKibitzer():
    return PM(933141,933740)


def Kibitzer():
    return QtGui.QIcon(pmKibitzer())


def pmKibitzer_Pause():
    return PM(933740,933912)


def Kibitzer_Pause():
    return QtGui.QIcon(pmKibitzer_Pause())


def pmKibitzer_Options():
    return PM(933912,934814)


def Kibitzer_Options():
    return QtGui.QIcon(pmKibitzer_Options())


def pmKibitzer_Voyager():
    return PM(350057,350900)


def Kibitzer_Voyager():
    return QtGui.QIcon(pmKibitzer_Voyager())


def pmKibitzer_Close():
    return PM(934814,935371)


def Kibitzer_Close():
    return QtGui.QIcon(pmKibitzer_Close())


def pmKibitzer_Down():
    return PM(935371,935760)


def Kibitzer_Down():
    return QtGui.QIcon(pmKibitzer_Down())


def pmKibitzer_Up():
    return PM(935760,936155)


def Kibitzer_Up():
    return QtGui.QIcon(pmKibitzer_Up())


def pmKibitzer_Back():
    return PM(936155,936588)


def Kibitzer_Back():
    return QtGui.QIcon(pmKibitzer_Back())


def pmKibitzer_Clipboard():
    return PM(936588,936974)


def Kibitzer_Clipboard():
    return QtGui.QIcon(pmKibitzer_Clipboard())


def pmKibitzer_Play():
    return PM(936974,937495)


def Kibitzer_Play():
    return QtGui.QIcon(pmKibitzer_Play())


def pmKibitzer_Side():
    return PM(937495,938248)


def Kibitzer_Side():
    return QtGui.QIcon(pmKibitzer_Side())


def pmKibitzer_Board():
    return PM(938248,938686)


def Kibitzer_Board():
    return QtGui.QIcon(pmKibitzer_Board())


def pmBoard():
    return PM(938686,939155)


def Board():
    return QtGui.QIcon(pmBoard())


def pmTraining_Games():
    return PM(939155,940847)


def Training_Games():
    return QtGui.QIcon(pmTraining_Games())


def pmTraining_Basic():
    return PM(940847,942220)


def Training_Basic():
    return QtGui.QIcon(pmTraining_Basic())


def pmTraining_Tactics():
    return PM(942220,943001)


def Training_Tactics():
    return QtGui.QIcon(pmTraining_Tactics())


def pmTraining_Endings():
    return PM(943001,943935)


def Training_Endings():
    return QtGui.QIcon(pmTraining_Endings())


def pmBridge():
    return PM(943935,944953)


def Bridge():
    return QtGui.QIcon(pmBridge())


def pmMaia():
    return PM(944953,945737)


def Maia():
    return QtGui.QIcon(pmMaia())


def pmBinBook():
    return PM(945737,946486)


def BinBook():
    return QtGui.QIcon(pmBinBook())


def pmConnected():
    return PM(946486,948104)


def Connected():
    return QtGui.QIcon(pmConnected())


def pmThemes():
    return PM(948104,948673)


def Themes():
    return QtGui.QIcon(pmThemes())


def pmReset():
    return PM(948673,950292)


def Reset():
    return QtGui.QIcon(pmReset())


def pmInstall():
    return PM(950292,952421)


def Install():
    return QtGui.QIcon(pmInstall())


def pmUninstall():
    return PM(952421,954447)


def Uninstall():
    return QtGui.QIcon(pmUninstall())


def pmLive():
    return PM(954447,957930)


def Live():
    return QtGui.QIcon(pmLive())


def pmLauncher():
    return PM(957930,962605)


def Launcher():
    return QtGui.QIcon(pmLauncher())


def pmLogInactive():
    return PM(962605,963136)


def LogInactive():
    return QtGui.QIcon(pmLogInactive())


def pmLogActive():
    return PM(963136,963700)


def LogActive():
    return QtGui.QIcon(pmLogActive())


def pmFolderAnil():
    return PM(963700,964064)


def FolderAnil():
    return QtGui.QIcon(pmFolderAnil())


def pmFolderBlack():
    return PM(964064,964401)


def FolderBlack():
    return QtGui.QIcon(pmFolderBlack())


def pmFolderBlue():
    return PM(964401,964775)


def FolderBlue():
    return QtGui.QIcon(pmFolderBlue())


def pmFolderGreen():
    return PM(964775,965147)


def FolderGreen():
    return QtGui.QIcon(pmFolderGreen())


def pmFolderMagenta():
    return PM(965147,965520)


def FolderMagenta():
    return QtGui.QIcon(pmFolderMagenta())


def pmFolderRed():
    return PM(965520,965884)


def FolderRed():
    return QtGui.QIcon(pmFolderRed())


def pmThis():
    return PM(965884,966338)


def This():
    return QtGui.QIcon(pmThis())


def pmAll():
    return PM(966338,966841)


def All():
    return QtGui.QIcon(pmAll())


def pmPrevious():
    return PM(966841,967300)


def Previous():
    return QtGui.QIcon(pmPrevious())


def pmLine():
    return PM(967300,967487)


def Line():
    return QtGui.QIcon(pmLine())


def pmEmpty():
    return PM(967487,967572)


def Empty():
    return QtGui.QIcon(pmEmpty())


def pmMore():
    return PM(967572,967861)


def More():
    return QtGui.QIcon(pmMore())


def pmSelectLogo():
    return PM(967861,968467)


def SelectLogo():
    return QtGui.QIcon(pmSelectLogo())


def pmSelect():
    return PM(968467,969121)


def Select():
    return QtGui.QIcon(pmSelect())


def pmSelectClose():
    return PM(969121,969893)


def SelectClose():
    return QtGui.QIcon(pmSelectClose())


def pmSelectHome():
    return PM(969893,970675)


def SelectHome():
    return QtGui.QIcon(pmSelectHome())


def pmSelectHistory():
    return PM(970675,971227)


def SelectHistory():
    return QtGui.QIcon(pmSelectHistory())


def pmSelectExplorer():
    return PM(971227,971960)


def SelectExplorer():
    return QtGui.QIcon(pmSelectExplorer())


def pmSelectFolderCreate():
    return PM(971960,972879)


def SelectFolderCreate():
    return QtGui.QIcon(pmSelectFolderCreate())


def pmSelectFolderRemove():
    return PM(972879,973906)


def SelectFolderRemove():
    return QtGui.QIcon(pmSelectFolderRemove())


def pmSelectReload():
    return PM(973906,975560)


def SelectReload():
    return QtGui.QIcon(pmSelectReload())


def pmSelectAccept():
    return PM(975560,976361)


def SelectAccept():
    return QtGui.QIcon(pmSelectAccept())


def pmWiki():
    return PM(976361,977478)


def Wiki():
    return QtGui.QIcon(pmWiki())


def pmCircle():
    return PM(977478,978938)


def Circle():
    return QtGui.QIcon(pmCircle())


def pmSortAZ():
    return PM(978938,979702)


def SortAZ():
    return QtGui.QIcon(pmSortAZ())


def pmReference():
    return PM(979702,980813)


def Reference():
    return QtGui.QIcon(pmReference())


def pmLanguageNew():
    return PM(980813,981540)


def LanguageNew():
    return QtGui.QIcon(pmLanguageNew())


def pmODT():
    return PM(981540,982655)


def ODT():
    return QtGui.QIcon(pmODT())


