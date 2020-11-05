from PySide2 import QtGui

import Code

f = open(Code.path_resource("IntFiles", "Iconos.bin"), "rb")
binIconos = f.read()
f.close()


def icono(name):
    return eval("%s()"%name)


def pixmap(name):
    return eval("pm%s()"%name)


def PM(xfrom, xto):
    pm = QtGui.QPixmap()
    pm.loadFromData(binIconos[xfrom:xto])
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


def pmDelete():
    return PM(216938,217862)


def Delete():
    return QtGui.QIcon(pmDelete())


def pmModificarP():
    return PM(217862,218928)


def ModificarP():
    return QtGui.QIcon(pmModificarP())


def pmGrupo_Si():
    return PM(218928,219390)


def Grupo_Si():
    return QtGui.QIcon(pmGrupo_Si())


def pmGrupo_No():
    return PM(219390,219713)


def Grupo_No():
    return QtGui.QIcon(pmGrupo_No())


def pmMotor_Si():
    return PM(219713,220175)


def Motor_Si():
    return QtGui.QIcon(pmMotor_Si())


def pmMotor_No():
    return PM(216938,217862)


def Motor_No():
    return QtGui.QIcon(pmMotor_No())


def pmMotor_Actual():
    return PM(220175,221192)


def Motor_Actual():
    return QtGui.QIcon(pmMotor_Actual())


def pmMotor():
    return PM(221192,221819)


def Motor():
    return QtGui.QIcon(pmMotor())


def pmMoverInicio():
    return PM(221819,222117)


def MoverInicio():
    return QtGui.QIcon(pmMoverInicio())


def pmMoverFinal():
    return PM(222117,222418)


def MoverFinal():
    return QtGui.QIcon(pmMoverFinal())


def pmMoverAdelante():
    return PM(222418,222773)


def MoverAdelante():
    return QtGui.QIcon(pmMoverAdelante())


def pmMoverAtras():
    return PM(222773,223138)


def MoverAtras():
    return QtGui.QIcon(pmMoverAtras())


def pmMoverLibre():
    return PM(223138,223556)


def MoverLibre():
    return QtGui.QIcon(pmMoverLibre())


def pmMoverTiempo():
    return PM(223556,224135)


def MoverTiempo():
    return QtGui.QIcon(pmMoverTiempo())


def pmMoverMas():
    return PM(224135,225174)


def MoverMas():
    return QtGui.QIcon(pmMoverMas())


def pmMoverGrabar():
    return PM(225174,226030)


def MoverGrabar():
    return QtGui.QIcon(pmMoverGrabar())


def pmMoverGrabarTodos():
    return PM(226030,227074)


def MoverGrabarTodos():
    return QtGui.QIcon(pmMoverGrabarTodos())


def pmMoverJugar():
    return PM(227074,227905)


def MoverJugar():
    return QtGui.QIcon(pmMoverJugar())


def pmPelicula():
    return PM(227905,230039)


def Pelicula():
    return QtGui.QIcon(pmPelicula())


def pmPelicula_Pausa():
    return PM(230039,231798)


def Pelicula_Pausa():
    return QtGui.QIcon(pmPelicula_Pausa())


def pmPelicula_Seguir():
    return PM(231798,233887)


def Pelicula_Seguir():
    return QtGui.QIcon(pmPelicula_Seguir())


def pmPelicula_Rapido():
    return PM(233887,235946)


def Pelicula_Rapido():
    return QtGui.QIcon(pmPelicula_Rapido())


def pmPelicula_Lento():
    return PM(235946,237821)


def Pelicula_Lento():
    return QtGui.QIcon(pmPelicula_Lento())


def pmPelicula_Repetir():
    return PM(38040,40334)


def Pelicula_Repetir():
    return QtGui.QIcon(pmPelicula_Repetir())


def pmPelicula_PGN():
    return PM(237821,238729)


def Pelicula_PGN():
    return QtGui.QIcon(pmPelicula_PGN())


def pmMemoria():
    return PM(238729,240670)


def Memoria():
    return QtGui.QIcon(pmMemoria())


def pmEntrenar():
    return PM(240670,242209)


def Entrenar():
    return QtGui.QIcon(pmEntrenar())


def pmEnviar():
    return PM(240670,242209)


def Enviar():
    return QtGui.QIcon(pmEnviar())


def pmBoxRooms():
    return PM(242209,247012)


def BoxRooms():
    return QtGui.QIcon(pmBoxRooms())


def pmBoxRoom():
    return PM(247012,247474)


def BoxRoom():
    return QtGui.QIcon(pmBoxRoom())


def pmNewBoxRoom():
    return PM(247474,248982)


def NewBoxRoom():
    return QtGui.QIcon(pmNewBoxRoom())


def pmNuevoMas():
    return PM(247474,248982)


def NuevoMas():
    return QtGui.QIcon(pmNuevoMas())


def pmTemas():
    return PM(248982,251205)


def Temas():
    return QtGui.QIcon(pmTemas())


def pmTutorialesCrear():
    return PM(251205,257474)


def TutorialesCrear():
    return QtGui.QIcon(pmTutorialesCrear())


def pmMover():
    return PM(257474,258056)


def Mover():
    return QtGui.QIcon(pmMover())


def pmSeleccionar():
    return PM(258056,263760)


def Seleccionar():
    return QtGui.QIcon(pmSeleccionar())


def pmVista():
    return PM(263760,265684)


def Vista():
    return QtGui.QIcon(pmVista())


def pmInformacionPGNUno():
    return PM(265684,267062)


def InformacionPGNUno():
    return QtGui.QIcon(pmInformacionPGNUno())


def pmDailyTest():
    return PM(267062,269402)


def DailyTest():
    return QtGui.QIcon(pmDailyTest())


def pmJuegaPorMi():
    return PM(269402,271122)


def JuegaPorMi():
    return QtGui.QIcon(pmJuegaPorMi())


def pmArbol():
    return PM(271122,271756)


def Arbol():
    return QtGui.QIcon(pmArbol())


def pmGrabarFichero():
    return PM(68134,69597)


def GrabarFichero():
    return QtGui.QIcon(pmGrabarFichero())


def pmClipboard():
    return PM(271756,272534)


def Clipboard():
    return QtGui.QIcon(pmClipboard())


def pmFics():
    return PM(272534,272951)


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
    return PM(272951,276303)


def Flechas():
    return QtGui.QIcon(pmFlechas())


def pmMarcos():
    return PM(276303,277750)


def Marcos():
    return QtGui.QIcon(pmMarcos())


def pmSVGs():
    return PM(277750,281319)


def SVGs():
    return QtGui.QIcon(pmSVGs())


def pmAmarillo():
    return PM(281319,282571)


def Amarillo():
    return QtGui.QIcon(pmAmarillo())


def pmNaranja():
    return PM(282571,283803)


def Naranja():
    return QtGui.QIcon(pmNaranja())


def pmVerde():
    return PM(283803,285079)


def Verde():
    return QtGui.QIcon(pmVerde())


def pmAzul():
    return PM(285079,286167)


def Azul():
    return QtGui.QIcon(pmAzul())


def pmMagenta():
    return PM(286167,287455)


def Magenta():
    return QtGui.QIcon(pmMagenta())


def pmRojo():
    return PM(287455,288674)


def Rojo():
    return QtGui.QIcon(pmRojo())


def pmGris():
    return PM(288674,289632)


def Gris():
    return QtGui.QIcon(pmGris())


def pmAmarillo32():
    return PM(289632,291612)


def Amarillo32():
    return QtGui.QIcon(pmAmarillo32())


def pmNaranja32():
    return PM(291612,293736)


def Naranja32():
    return QtGui.QIcon(pmNaranja32())


def pmVerde32():
    return PM(293736,295857)


def Verde32():
    return QtGui.QIcon(pmVerde32())


def pmAzul32():
    return PM(295857,298236)


def Azul32():
    return QtGui.QIcon(pmAzul32())


def pmMagenta32():
    return PM(298236,300687)


def Magenta32():
    return QtGui.QIcon(pmMagenta32())


def pmRojo32():
    return PM(300687,302502)


def Rojo32():
    return QtGui.QIcon(pmRojo32())


def pmGris32():
    return PM(302502,304416)


def Gris32():
    return QtGui.QIcon(pmGris32())


def pmPuntoBlanco():
    return PM(304416,304765)


def PuntoBlanco():
    return QtGui.QIcon(pmPuntoBlanco())


def pmPuntoAmarillo():
    return PM(218928,219390)


def PuntoAmarillo():
    return QtGui.QIcon(pmPuntoAmarillo())


def pmPuntoNaranja():
    return PM(304765,305227)


def PuntoNaranja():
    return QtGui.QIcon(pmPuntoNaranja())


def pmPuntoVerde():
    return PM(219713,220175)


def PuntoVerde():
    return QtGui.QIcon(pmPuntoVerde())


def pmPuntoAzul():
    return PM(247012,247474)


def PuntoAzul():
    return QtGui.QIcon(pmPuntoAzul())


def pmPuntoMagenta():
    return PM(305227,305726)


def PuntoMagenta():
    return QtGui.QIcon(pmPuntoMagenta())


def pmPuntoRojo():
    return PM(305726,306225)


def PuntoRojo():
    return QtGui.QIcon(pmPuntoRojo())


def pmPuntoNegro():
    return PM(219390,219713)


def PuntoNegro():
    return QtGui.QIcon(pmPuntoNegro())


def pmPuntoEstrella():
    return PM(306225,306652)


def PuntoEstrella():
    return QtGui.QIcon(pmPuntoEstrella())


def pmComentario():
    return PM(306652,307289)


def Comentario():
    return QtGui.QIcon(pmComentario())


def pmComentarioMas():
    return PM(307289,308228)


def ComentarioMas():
    return QtGui.QIcon(pmComentarioMas())


def pmComentarioEditar():
    return PM(225174,226030)


def ComentarioEditar():
    return QtGui.QIcon(pmComentarioEditar())


def pmOpeningComentario():
    return PM(308228,309224)


def OpeningComentario():
    return QtGui.QIcon(pmOpeningComentario())


def pmMas():
    return PM(309224,309733)


def Mas():
    return QtGui.QIcon(pmMas())


def pmMasR():
    return PM(309733,310221)


def MasR():
    return QtGui.QIcon(pmMasR())


def pmMasDoc():
    return PM(310221,311022)


def MasDoc():
    return QtGui.QIcon(pmMasDoc())


def pmPotencia():
    return PM(184620,185486)


def Potencia():
    return QtGui.QIcon(pmPotencia())


def pmBMT():
    return PM(311022,311900)


def BMT():
    return QtGui.QIcon(pmBMT())


def pmOjo():
    return PM(311900,313022)


def Ojo():
    return QtGui.QIcon(pmOjo())


def pmOcultar():
    return PM(311900,313022)


def Ocultar():
    return QtGui.QIcon(pmOcultar())


def pmMostrar():
    return PM(313022,314078)


def Mostrar():
    return QtGui.QIcon(pmMostrar())


def pmBlog():
    return PM(314078,314600)


def Blog():
    return QtGui.QIcon(pmBlog())


def pmVariations():
    return PM(314600,315507)


def Variations():
    return QtGui.QIcon(pmVariations())


def pmVariationsG():
    return PM(315507,317934)


def VariationsG():
    return QtGui.QIcon(pmVariationsG())


def pmCambiar():
    return PM(317934,319648)


def Cambiar():
    return QtGui.QIcon(pmCambiar())


def pmAnterior():
    return PM(319648,321702)


def Anterior():
    return QtGui.QIcon(pmAnterior())


def pmSiguiente():
    return PM(321702,323772)


def Siguiente():
    return QtGui.QIcon(pmSiguiente())


def pmSiguienteF():
    return PM(323772,325947)


def SiguienteF():
    return QtGui.QIcon(pmSiguienteF())


def pmAnteriorF():
    return PM(325947,328141)


def AnteriorF():
    return QtGui.QIcon(pmAnteriorF())


def pmX():
    return PM(328141,329423)


def X():
    return QtGui.QIcon(pmX())


def pmTools():
    return PM(329423,332024)


def Tools():
    return QtGui.QIcon(pmTools())


def pmTacticas():
    return PM(332024,334597)


def Tacticas():
    return QtGui.QIcon(pmTacticas())


def pmCancelarPeque():
    return PM(334597,335159)


def CancelarPeque():
    return QtGui.QIcon(pmCancelarPeque())


def pmAceptarPeque():
    return PM(220175,221192)


def AceptarPeque():
    return QtGui.QIcon(pmAceptarPeque())


def pmLibre():
    return PM(335159,337551)


def Libre():
    return QtGui.QIcon(pmLibre())


def pmEnBlanco():
    return PM(337551,338277)


def EnBlanco():
    return QtGui.QIcon(pmEnBlanco())


def pmDirector():
    return PM(338277,341251)


def Director():
    return QtGui.QIcon(pmDirector())


def pmTorneos():
    return PM(341251,342989)


def Torneos():
    return QtGui.QIcon(pmTorneos())


def pmOpenings():
    return PM(342989,343914)


def Openings():
    return QtGui.QIcon(pmOpenings())


def pmV_Blancas():
    return PM(343914,344194)


def V_Blancas():
    return QtGui.QIcon(pmV_Blancas())


def pmV_Blancas_Mas():
    return PM(344194,344474)


def V_Blancas_Mas():
    return QtGui.QIcon(pmV_Blancas_Mas())


def pmV_Blancas_Mas_Mas():
    return PM(344474,344746)


def V_Blancas_Mas_Mas():
    return QtGui.QIcon(pmV_Blancas_Mas_Mas())


def pmV_Negras():
    return PM(344746,345021)


def V_Negras():
    return QtGui.QIcon(pmV_Negras())


def pmV_Negras_Mas():
    return PM(345021,345296)


def V_Negras_Mas():
    return QtGui.QIcon(pmV_Negras_Mas())


def pmV_Negras_Mas_Mas():
    return PM(345296,345565)


def V_Negras_Mas_Mas():
    return QtGui.QIcon(pmV_Negras_Mas_Mas())


def pmV_Blancas_Igual_Negras():
    return PM(345565,345867)


def V_Blancas_Igual_Negras():
    return QtGui.QIcon(pmV_Blancas_Igual_Negras())


def pmMezclar():
    return PM(142655,145051)


def Mezclar():
    return QtGui.QIcon(pmMezclar())


def pmVoyager():
    return PM(345867,346710)


def Voyager():
    return QtGui.QIcon(pmVoyager())


def pmReindexar():
    return PM(346710,348527)


def Reindexar():
    return QtGui.QIcon(pmReindexar())


def pmRename():
    return PM(348527,349511)


def Rename():
    return QtGui.QIcon(pmRename())


def pmAdd():
    return PM(349511,350464)


def Add():
    return QtGui.QIcon(pmAdd())


def pmMas22():
    return PM(350464,351128)


def Mas22():
    return QtGui.QIcon(pmMas22())


def pmMenos22():
    return PM(351128,351572)


def Menos22():
    return QtGui.QIcon(pmMenos22())


def pmTransposition():
    return PM(351572,352091)


def Transposition():
    return QtGui.QIcon(pmTransposition())


def pmRat():
    return PM(352091,357795)


def Rat():
    return QtGui.QIcon(pmRat())


def pmAlligator():
    return PM(357795,362787)


def Alligator():
    return QtGui.QIcon(pmAlligator())


def pmAnt():
    return PM(362787,369485)


def Ant():
    return QtGui.QIcon(pmAnt())


def pmBat():
    return PM(369485,372439)


def Bat():
    return QtGui.QIcon(pmBat())


def pmBear():
    return PM(372439,379718)


def Bear():
    return QtGui.QIcon(pmBear())


def pmBee():
    return PM(379718,384720)


def Bee():
    return QtGui.QIcon(pmBee())


def pmBird():
    return PM(384720,390779)


def Bird():
    return QtGui.QIcon(pmBird())


def pmBull():
    return PM(390779,397748)


def Bull():
    return QtGui.QIcon(pmBull())


def pmBulldog():
    return PM(397748,404639)


def Bulldog():
    return QtGui.QIcon(pmBulldog())


def pmButterfly():
    return PM(404639,412013)


def Butterfly():
    return QtGui.QIcon(pmButterfly())


def pmCat():
    return PM(412013,418285)


def Cat():
    return QtGui.QIcon(pmCat())


def pmChicken():
    return PM(418285,424096)


def Chicken():
    return QtGui.QIcon(pmChicken())


def pmCow():
    return PM(424096,430839)


def Cow():
    return QtGui.QIcon(pmCow())


def pmCrab():
    return PM(430839,436428)


def Crab():
    return QtGui.QIcon(pmCrab())


def pmCrocodile():
    return PM(436428,442569)


def Crocodile():
    return QtGui.QIcon(pmCrocodile())


def pmDeer():
    return PM(442569,448876)


def Deer():
    return QtGui.QIcon(pmDeer())


def pmDog():
    return PM(448876,455479)


def Dog():
    return QtGui.QIcon(pmDog())


def pmDonkey():
    return PM(455479,461126)


def Donkey():
    return QtGui.QIcon(pmDonkey())


def pmDuck():
    return PM(461126,467669)


def Duck():
    return QtGui.QIcon(pmDuck())


def pmEagle():
    return PM(467669,472487)


def Eagle():
    return QtGui.QIcon(pmEagle())


def pmElephant():
    return PM(472487,478968)


def Elephant():
    return QtGui.QIcon(pmElephant())


def pmFish():
    return PM(478968,485809)


def Fish():
    return QtGui.QIcon(pmFish())


def pmFox():
    return PM(485809,492592)


def Fox():
    return QtGui.QIcon(pmFox())


def pmFrog():
    return PM(492592,499008)


def Frog():
    return QtGui.QIcon(pmFrog())


def pmGiraffe():
    return PM(499008,506186)


def Giraffe():
    return QtGui.QIcon(pmGiraffe())


def pmGorilla():
    return PM(506186,512725)


def Gorilla():
    return QtGui.QIcon(pmGorilla())


def pmHippo():
    return PM(512725,519846)


def Hippo():
    return QtGui.QIcon(pmHippo())


def pmHorse():
    return PM(519846,526393)


def Horse():
    return QtGui.QIcon(pmHorse())


def pmInsect():
    return PM(526393,532328)


def Insect():
    return QtGui.QIcon(pmInsect())


def pmLion():
    return PM(532328,541238)


def Lion():
    return QtGui.QIcon(pmLion())


def pmMonkey():
    return PM(541238,548917)


def Monkey():
    return QtGui.QIcon(pmMonkey())


def pmMoose():
    return PM(548917,555541)


def Moose():
    return QtGui.QIcon(pmMoose())


def pmMouse():
    return PM(352091,357795)


def Mouse():
    return QtGui.QIcon(pmMouse())


def pmOwl():
    return PM(555541,562247)


def Owl():
    return QtGui.QIcon(pmOwl())


def pmPanda():
    return PM(562247,566281)


def Panda():
    return QtGui.QIcon(pmPanda())


def pmPenguin():
    return PM(566281,571830)


def Penguin():
    return QtGui.QIcon(pmPenguin())


def pmPig():
    return PM(571830,579870)


def Pig():
    return QtGui.QIcon(pmPig())


def pmRabbit():
    return PM(579870,587171)


def Rabbit():
    return QtGui.QIcon(pmRabbit())


def pmRhino():
    return PM(587171,593558)


def Rhino():
    return QtGui.QIcon(pmRhino())


def pmRooster():
    return PM(593558,598821)


def Rooster():
    return QtGui.QIcon(pmRooster())


def pmShark():
    return PM(598821,604591)


def Shark():
    return QtGui.QIcon(pmShark())


def pmSheep():
    return PM(604591,608422)


def Sheep():
    return QtGui.QIcon(pmSheep())


def pmSnake():
    return PM(608422,614447)


def Snake():
    return QtGui.QIcon(pmSnake())


def pmTiger():
    return PM(614447,622484)


def Tiger():
    return QtGui.QIcon(pmTiger())


def pmTurkey():
    return PM(622484,629898)


def Turkey():
    return QtGui.QIcon(pmTurkey())


def pmTurtle():
    return PM(629898,636619)


def Turtle():
    return QtGui.QIcon(pmTurtle())


def pmWolf():
    return PM(636619,639714)


def Wolf():
    return QtGui.QIcon(pmWolf())


def pmSteven():
    return PM(639714,646866)


def Steven():
    return QtGui.QIcon(pmSteven())


def pmWheel():
    return PM(646866,654931)


def Wheel():
    return QtGui.QIcon(pmWheel())


def pmWheelchair():
    return PM(654931,663735)


def Wheelchair():
    return QtGui.QIcon(pmWheelchair())


def pmTouringMotorcycle():
    return PM(663735,670047)


def TouringMotorcycle():
    return QtGui.QIcon(pmTouringMotorcycle())


def pmContainer():
    return PM(670047,675382)


def Container():
    return QtGui.QIcon(pmContainer())


def pmBoatEquipment():
    return PM(675382,680905)


def BoatEquipment():
    return QtGui.QIcon(pmBoatEquipment())


def pmCar():
    return PM(680905,685551)


def Car():
    return QtGui.QIcon(pmCar())


def pmLorry():
    return PM(685551,691587)


def Lorry():
    return QtGui.QIcon(pmLorry())


def pmCarTrailer():
    return PM(691587,695684)


def CarTrailer():
    return QtGui.QIcon(pmCarTrailer())


def pmTowTruck():
    return PM(695684,700442)


def TowTruck():
    return QtGui.QIcon(pmTowTruck())


def pmQuadBike():
    return PM(700442,706411)


def QuadBike():
    return QtGui.QIcon(pmQuadBike())


def pmRecoveryTruck():
    return PM(706411,711408)


def RecoveryTruck():
    return QtGui.QIcon(pmRecoveryTruck())


def pmContainerLoader():
    return PM(711408,716550)


def ContainerLoader():
    return QtGui.QIcon(pmContainerLoader())


def pmPoliceCar():
    return PM(716550,721382)


def PoliceCar():
    return QtGui.QIcon(pmPoliceCar())


def pmExecutiveCar():
    return PM(721382,726060)


def ExecutiveCar():
    return QtGui.QIcon(pmExecutiveCar())


def pmTruck():
    return PM(726060,731523)


def Truck():
    return QtGui.QIcon(pmTruck())


def pmExcavator():
    return PM(731523,736414)


def Excavator():
    return QtGui.QIcon(pmExcavator())


def pmCabriolet():
    return PM(736414,741252)


def Cabriolet():
    return QtGui.QIcon(pmCabriolet())


def pmMixerTruck():
    return PM(741252,747562)


def MixerTruck():
    return QtGui.QIcon(pmMixerTruck())


def pmForkliftTruckLoaded():
    return PM(747562,753710)


def ForkliftTruckLoaded():
    return QtGui.QIcon(pmForkliftTruckLoaded())


def pmAmbulance():
    return PM(753710,759760)


def Ambulance():
    return QtGui.QIcon(pmAmbulance())


def pmDieselLocomotiveBoxcar():
    return PM(759760,763766)


def DieselLocomotiveBoxcar():
    return QtGui.QIcon(pmDieselLocomotiveBoxcar())


def pmTractorUnit():
    return PM(763766,769233)


def TractorUnit():
    return QtGui.QIcon(pmTractorUnit())


def pmFireTruck():
    return PM(769233,775572)


def FireTruck():
    return QtGui.QIcon(pmFireTruck())


def pmCargoShip():
    return PM(775572,779913)


def CargoShip():
    return QtGui.QIcon(pmCargoShip())


def pmSubwayTrain():
    return PM(779913,784803)


def SubwayTrain():
    return QtGui.QIcon(pmSubwayTrain())


def pmTruckMountedCrane():
    return PM(784803,790544)


def TruckMountedCrane():
    return QtGui.QIcon(pmTruckMountedCrane())


def pmAirAmbulance():
    return PM(790544,795657)


def AirAmbulance():
    return QtGui.QIcon(pmAirAmbulance())


def pmAirplane():
    return PM(795657,800545)


def Airplane():
    return QtGui.QIcon(pmAirplane())


def pmCaracol():
    return PM(800545,802361)


def Caracol():
    return QtGui.QIcon(pmCaracol())


def pmUno():
    return PM(802361,804823)


def Uno():
    return QtGui.QIcon(pmUno())


def pmMotoresExternos():
    return PM(804823,806725)


def MotoresExternos():
    return QtGui.QIcon(pmMotoresExternos())


def pmDatabase():
    return PM(806725,808041)


def Database():
    return QtGui.QIcon(pmDatabase())


def pmDatabaseMas():
    return PM(808041,809500)


def DatabaseMas():
    return QtGui.QIcon(pmDatabaseMas())


def pmDatabaseImport():
    return PM(809500,810136)


def DatabaseImport():
    return QtGui.QIcon(pmDatabaseImport())


def pmDatabaseExport():
    return PM(810136,810781)


def DatabaseExport():
    return QtGui.QIcon(pmDatabaseExport())


def pmDatabaseDelete():
    return PM(810781,811904)


def DatabaseDelete():
    return QtGui.QIcon(pmDatabaseDelete())


def pmDatabaseMaintenance():
    return PM(811904,813400)


def DatabaseMaintenance():
    return QtGui.QIcon(pmDatabaseMaintenance())


def pmAtacante():
    return PM(813400,814005)


def Atacante():
    return QtGui.QIcon(pmAtacante())


def pmAtacada():
    return PM(814005,814571)


def Atacada():
    return QtGui.QIcon(pmAtacada())


def pmGoToNext():
    return PM(814571,814983)


def GoToNext():
    return QtGui.QIcon(pmGoToNext())


def pmBlancas():
    return PM(814983,815334)


def Blancas():
    return QtGui.QIcon(pmBlancas())


def pmNegras():
    return PM(815334,815580)


def Negras():
    return QtGui.QIcon(pmNegras())


def pmFolderChange():
    return PM(71649,74407)


def FolderChange():
    return QtGui.QIcon(pmFolderChange())


def pmMarkers():
    return PM(815580,817275)


def Markers():
    return QtGui.QIcon(pmMarkers())


def pmTop():
    return PM(817275,817859)


def Top():
    return QtGui.QIcon(pmTop())


def pmBottom():
    return PM(817859,818448)


def Bottom():
    return QtGui.QIcon(pmBottom())


def pmSTS():
    return PM(818448,820639)


def STS():
    return QtGui.QIcon(pmSTS())


def pmRun():
    return PM(820639,822363)


def Run():
    return QtGui.QIcon(pmRun())


def pmRun2():
    return PM(822363,823883)


def Run2():
    return QtGui.QIcon(pmRun2())


def pmWorldMap():
    return PM(823883,826624)


def WorldMap():
    return QtGui.QIcon(pmWorldMap())


def pmAfrica():
    return PM(826624,829110)


def Africa():
    return QtGui.QIcon(pmAfrica())


def pmMaps():
    return PM(829110,830054)


def Maps():
    return QtGui.QIcon(pmMaps())


def pmSol():
    return PM(830054,830980)


def Sol():
    return QtGui.QIcon(pmSol())


def pmSolNubes():
    return PM(830980,831843)


def SolNubes():
    return QtGui.QIcon(pmSolNubes())


def pmSolNubesLluvia():
    return PM(831843,832803)


def SolNubesLluvia():
    return QtGui.QIcon(pmSolNubesLluvia())


def pmLluvia():
    return PM(832803,833642)


def Lluvia():
    return QtGui.QIcon(pmLluvia())


def pmInvierno():
    return PM(833642,835218)


def Invierno():
    return QtGui.QIcon(pmInvierno())


def pmFixedElo():
    return PM(164966,166229)


def FixedElo():
    return QtGui.QIcon(pmFixedElo())


def pmSoundTool():
    return PM(835218,837677)


def SoundTool():
    return QtGui.QIcon(pmSoundTool())


def pmTrain():
    return PM(837677,839047)


def Train():
    return QtGui.QIcon(pmTrain())


def pmPlay():
    return PM(231798,233887)


def Play():
    return QtGui.QIcon(pmPlay())


def pmMeasure():
    return PM(126751,128374)


def Measure():
    return QtGui.QIcon(pmMeasure())


def pmPlayGame():
    return PM(839047,843405)


def PlayGame():
    return QtGui.QIcon(pmPlayGame())


def pmScanner():
    return PM(843405,843746)


def Scanner():
    return QtGui.QIcon(pmScanner())


def pmMenos():
    return PM(843746,844271)


def Menos():
    return QtGui.QIcon(pmMenos())


def pmSchool():
    return PM(844271,845633)


def School():
    return QtGui.QIcon(pmSchool())


def pmLaw():
    return PM(845633,846249)


def Law():
    return QtGui.QIcon(pmLaw())


def pmLearnGame():
    return PM(846249,846682)


def LearnGame():
    return QtGui.QIcon(pmLearnGame())


def pmLonghaul():
    return PM(846682,847608)


def Longhaul():
    return QtGui.QIcon(pmLonghaul())


def pmTrekking():
    return PM(847608,848302)


def Trekking():
    return QtGui.QIcon(pmTrekking())


def pmPassword():
    return PM(848302,848755)


def Password():
    return QtGui.QIcon(pmPassword())


def pmSQL_RAW():
    return PM(839047,843405)


def SQL_RAW():
    return QtGui.QIcon(pmSQL_RAW())


def pmSun():
    return PM(311022,311900)


def Sun():
    return QtGui.QIcon(pmSun())


def pmLight32():
    return PM(848755,850455)


def Light32():
    return QtGui.QIcon(pmLight32())


def pmTOL():
    return PM(850455,851164)


def TOL():
    return QtGui.QIcon(pmTOL())


def pmUned():
    return PM(851164,851584)


def Uned():
    return QtGui.QIcon(pmUned())


def pmUwe():
    return PM(851584,852553)


def Uwe():
    return QtGui.QIcon(pmUwe())


def pmThinking():
    return PM(852553,853342)


def Thinking():
    return QtGui.QIcon(pmThinking())


def pmWashingMachine():
    return PM(853342,854005)


def WashingMachine():
    return QtGui.QIcon(pmWashingMachine())


def pmTerminal():
    return PM(854005,857549)


def Terminal():
    return QtGui.QIcon(pmTerminal())


def pmManualSave():
    return PM(857549,858132)


def ManualSave():
    return QtGui.QIcon(pmManualSave())


def pmSettings():
    return PM(858132,858570)


def Settings():
    return QtGui.QIcon(pmSettings())


def pmStrength():
    return PM(858570,859241)


def Strength():
    return QtGui.QIcon(pmStrength())


def pmSingular():
    return PM(859241,860096)


def Singular():
    return QtGui.QIcon(pmSingular())


def pmScript():
    return PM(860096,860665)


def Script():
    return QtGui.QIcon(pmScript())


def pmTexto():
    return PM(860665,863510)


def Texto():
    return QtGui.QIcon(pmTexto())


def pmLampara():
    return PM(863510,864219)


def Lampara():
    return QtGui.QIcon(pmLampara())


def pmFile():
    return PM(864219,866519)


def File():
    return QtGui.QIcon(pmFile())


def pmCalculo():
    return PM(866519,867445)


def Calculo():
    return QtGui.QIcon(pmCalculo())


def pmOpeningLines():
    return PM(867445,868123)


def OpeningLines():
    return QtGui.QIcon(pmOpeningLines())


def pmStudy():
    return PM(868123,869036)


def Study():
    return QtGui.QIcon(pmStudy())


def pmLichess():
    return PM(869036,869926)


def Lichess():
    return QtGui.QIcon(pmLichess())


def pmMiniatura():
    return PM(869926,870853)


def Miniatura():
    return QtGui.QIcon(pmMiniatura())


def pmLocomotora():
    return PM(870853,871634)


def Locomotora():
    return QtGui.QIcon(pmLocomotora())


def pmTrainSequential():
    return PM(871634,872775)


def TrainSequential():
    return QtGui.QIcon(pmTrainSequential())


def pmTrainStatic():
    return PM(872775,873735)


def TrainStatic():
    return QtGui.QIcon(pmTrainStatic())


def pmTrainPositions():
    return PM(873735,874716)


def TrainPositions():
    return QtGui.QIcon(pmTrainPositions())


def pmTrainEngines():
    return PM(874716,876150)


def TrainEngines():
    return QtGui.QIcon(pmTrainEngines())


def pmError():
    return PM(48833,52833)


def Error():
    return QtGui.QIcon(pmError())


def pmAtajos():
    return PM(876150,877329)


def Atajos():
    return QtGui.QIcon(pmAtajos())


def pmTOLline():
    return PM(877329,878433)


def TOLline():
    return QtGui.QIcon(pmTOLline())


def pmTOLchange():
    return PM(878433,880655)


def TOLchange():
    return QtGui.QIcon(pmTOLchange())


def pmPack():
    return PM(880655,881828)


def Pack():
    return QtGui.QIcon(pmPack())


def pmHome():
    return PM(179976,181158)


def Home():
    return QtGui.QIcon(pmHome())


def pmImport8():
    return PM(881828,882586)


def Import8():
    return QtGui.QIcon(pmImport8())


def pmExport8():
    return PM(882586,883211)


def Export8():
    return QtGui.QIcon(pmExport8())


def pmTablas8():
    return PM(883211,884003)


def Tablas8():
    return QtGui.QIcon(pmTablas8())


def pmBlancas8():
    return PM(884003,885033)


def Blancas8():
    return QtGui.QIcon(pmBlancas8())


def pmNegras8():
    return PM(885033,885872)


def Negras8():
    return QtGui.QIcon(pmNegras8())


def pmBook():
    return PM(885872,886446)


def Book():
    return QtGui.QIcon(pmBook())


def pmWrite():
    return PM(886446,887651)


def Write():
    return QtGui.QIcon(pmWrite())


def pmAlt():
    return PM(887651,888093)


def Alt():
    return QtGui.QIcon(pmAlt())


def pmShift():
    return PM(888093,888433)


def Shift():
    return QtGui.QIcon(pmShift())


def pmRightMouse():
    return PM(888433,889233)


def RightMouse():
    return QtGui.QIcon(pmRightMouse())


def pmControl():
    return PM(889233,889758)


def Control():
    return QtGui.QIcon(pmControl())


def pmFinales():
    return PM(889758,890845)


def Finales():
    return QtGui.QIcon(pmFinales())


def pmEditColumns():
    return PM(890845,891577)


def EditColumns():
    return QtGui.QIcon(pmEditColumns())


def pmResizeAll():
    return PM(891577,892087)


def ResizeAll():
    return QtGui.QIcon(pmResizeAll())


def pmChecked():
    return PM(892087,892593)


def Checked():
    return QtGui.QIcon(pmChecked())


def pmUnchecked():
    return PM(892593,892841)


def Unchecked():
    return QtGui.QIcon(pmUnchecked())


def pmBuscarC():
    return PM(892841,893285)


def BuscarC():
    return QtGui.QIcon(pmBuscarC())


def pmPeonBlanco():
    return PM(893285,895466)


def PeonBlanco():
    return QtGui.QIcon(pmPeonBlanco())


def pmPeonNegro():
    return PM(895466,896990)


def PeonNegro():
    return QtGui.QIcon(pmPeonNegro())


def pmReciclar():
    return PM(896990,897714)


def Reciclar():
    return QtGui.QIcon(pmReciclar())


def pmLanzamiento():
    return PM(897714,898427)


def Lanzamiento():
    return QtGui.QIcon(pmLanzamiento())


def pmEndGame():
    return PM(898427,898841)


def EndGame():
    return QtGui.QIcon(pmEndGame())


def pmPause():
    return PM(898841,899710)


def Pause():
    return QtGui.QIcon(pmPause())


def pmContinue():
    return PM(899710,900914)


def Continue():
    return QtGui.QIcon(pmContinue())


def pmClose():
    return PM(900914,901613)


def Close():
    return QtGui.QIcon(pmClose())


def pmStop():
    return PM(901613,902646)


def Stop():
    return QtGui.QIcon(pmStop())


def pmFactoryPolyglot():
    return PM(902646,903466)


def FactoryPolyglot():
    return QtGui.QIcon(pmFactoryPolyglot())


def pmTags():
    return PM(903466,904289)


def Tags():
    return QtGui.QIcon(pmTags())


def pmAppearance():
    return PM(904289,905016)


def Appearance():
    return QtGui.QIcon(pmAppearance())


def pmFill():
    return PM(905016,906054)


def Fill():
    return QtGui.QIcon(pmFill())


def pmSupport():
    return PM(906054,906786)


def Support():
    return QtGui.QIcon(pmSupport())


def pmOrder():
    return PM(906786,907584)


def Order():
    return QtGui.QIcon(pmOrder())


def pmPlay1():
    return PM(907584,908879)


def Play1():
    return QtGui.QIcon(pmPlay1())


def pmRemove1():
    return PM(908879,910006)


def Remove1():
    return QtGui.QIcon(pmRemove1())


def pmNew1():
    return PM(910006,910328)


def New1():
    return QtGui.QIcon(pmNew1())


def pmMensError():
    return PM(910328,912392)


def MensError():
    return QtGui.QIcon(pmMensError())


def pmMensInfo():
    return PM(912392,914947)


def MensInfo():
    return QtGui.QIcon(pmMensInfo())


def pmJump():
    return PM(914947,915622)


def Jump():
    return QtGui.QIcon(pmJump())


def pmCaptures():
    return PM(915622,916803)


def Captures():
    return QtGui.QIcon(pmCaptures())


def pmRepeat():
    return PM(916803,917462)


def Repeat():
    return QtGui.QIcon(pmRepeat())


def pmCount():
    return PM(917462,918138)


def Count():
    return QtGui.QIcon(pmCount())


def pmMate15():
    return PM(918138,919209)


def Mate15():
    return QtGui.QIcon(pmMate15())


def pmCoordinates():
    return PM(919209,920362)


def Coordinates():
    return QtGui.QIcon(pmCoordinates())


def pmKnight():
    return PM(920362,921605)


def Knight():
    return QtGui.QIcon(pmKnight())


def pmCorrecto():
    return PM(921605,922631)


def Correcto():
    return QtGui.QIcon(pmCorrecto())


def pmBlocks():
    return PM(922631,922968)


def Blocks():
    return QtGui.QIcon(pmBlocks())


def pmWest():
    return PM(922968,924074)


def West():
    return QtGui.QIcon(pmWest())


def pmOpening():
    return PM(924074,924332)


def Opening():
    return QtGui.QIcon(pmOpening())


def pmVariation():
    return PM(223138,223556)


def Variation():
    return QtGui.QIcon(pmVariation())


def pmComment():
    return PM(924332,924695)


def Comment():
    return QtGui.QIcon(pmComment())


def pmVariationComment():
    return PM(924695,925039)


def VariationComment():
    return QtGui.QIcon(pmVariationComment())


def pmOpeningVariation():
    return PM(925039,925503)


def OpeningVariation():
    return QtGui.QIcon(pmOpeningVariation())


def pmOpeningComment():
    return PM(925503,925836)


def OpeningComment():
    return QtGui.QIcon(pmOpeningComment())


def pmOpeningVariationComment():
    return PM(925039,925503)


def OpeningVariationComment():
    return QtGui.QIcon(pmOpeningVariationComment())


def pmDeleteRow():
    return PM(925836,926267)


def DeleteRow():
    return QtGui.QIcon(pmDeleteRow())


def pmDeleteColumn():
    return PM(926267,926710)


def DeleteColumn():
    return QtGui.QIcon(pmDeleteColumn())


def pmEditVariation():
    return PM(926710,927065)


def EditVariation():
    return QtGui.QIcon(pmEditVariation())


def pmKibitzer():
    return PM(927065,927664)


def Kibitzer():
    return QtGui.QIcon(pmKibitzer())


def pmKibitzer_Pause():
    return PM(927664,927836)


def Kibitzer_Pause():
    return QtGui.QIcon(pmKibitzer_Pause())


def pmKibitzer_Options():
    return PM(927836,928738)


def Kibitzer_Options():
    return QtGui.QIcon(pmKibitzer_Options())


def pmKibitzer_Voyager():
    return PM(345867,346710)


def Kibitzer_Voyager():
    return QtGui.QIcon(pmKibitzer_Voyager())


def pmKibitzer_Close():
    return PM(928738,929295)


def Kibitzer_Close():
    return QtGui.QIcon(pmKibitzer_Close())


def pmKibitzer_Down():
    return PM(929295,929684)


def Kibitzer_Down():
    return QtGui.QIcon(pmKibitzer_Down())


def pmKibitzer_Up():
    return PM(929684,930079)


def Kibitzer_Up():
    return QtGui.QIcon(pmKibitzer_Up())


def pmKibitzer_Back():
    return PM(930079,930512)


def Kibitzer_Back():
    return QtGui.QIcon(pmKibitzer_Back())


def pmKibitzer_Clipboard():
    return PM(930512,930898)


def Kibitzer_Clipboard():
    return QtGui.QIcon(pmKibitzer_Clipboard())


def pmKibitzer_Play():
    return PM(930898,931419)


def Kibitzer_Play():
    return QtGui.QIcon(pmKibitzer_Play())


def pmKibitzer_Side():
    return PM(931419,932172)


def Kibitzer_Side():
    return QtGui.QIcon(pmKibitzer_Side())


def pmKibitzer_Board():
    return PM(932172,932610)


def Kibitzer_Board():
    return QtGui.QIcon(pmKibitzer_Board())


def pmBoard():
    return PM(932610,933079)


def Board():
    return QtGui.QIcon(pmBoard())


def pmTraining_Games():
    return PM(933079,934771)


def Training_Games():
    return QtGui.QIcon(pmTraining_Games())


def pmTraining_Basic():
    return PM(934771,936144)


def Training_Basic():
    return QtGui.QIcon(pmTraining_Basic())


def pmTraining_Tactics():
    return PM(936144,936925)


def Training_Tactics():
    return QtGui.QIcon(pmTraining_Tactics())


def pmTraining_Endings():
    return PM(936925,937859)


def Training_Endings():
    return QtGui.QIcon(pmTraining_Endings())


