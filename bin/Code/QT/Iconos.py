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


def pmVoyager32():
    return PM(346710,348598)


def Voyager32():
    return QtGui.QIcon(pmVoyager32())


def pmReindexar():
    return PM(348598,350415)


def Reindexar():
    return QtGui.QIcon(pmReindexar())


def pmRename():
    return PM(350415,351399)


def Rename():
    return QtGui.QIcon(pmRename())


def pmAdd():
    return PM(351399,352352)


def Add():
    return QtGui.QIcon(pmAdd())


def pmMas22():
    return PM(352352,353016)


def Mas22():
    return QtGui.QIcon(pmMas22())


def pmMenos22():
    return PM(353016,353460)


def Menos22():
    return QtGui.QIcon(pmMenos22())


def pmTransposition():
    return PM(353460,353979)


def Transposition():
    return QtGui.QIcon(pmTransposition())


def pmRat():
    return PM(353979,359683)


def Rat():
    return QtGui.QIcon(pmRat())


def pmAlligator():
    return PM(359683,364675)


def Alligator():
    return QtGui.QIcon(pmAlligator())


def pmAnt():
    return PM(364675,371373)


def Ant():
    return QtGui.QIcon(pmAnt())


def pmBat():
    return PM(371373,374327)


def Bat():
    return QtGui.QIcon(pmBat())


def pmBear():
    return PM(374327,381606)


def Bear():
    return QtGui.QIcon(pmBear())


def pmBee():
    return PM(381606,386608)


def Bee():
    return QtGui.QIcon(pmBee())


def pmBird():
    return PM(386608,392667)


def Bird():
    return QtGui.QIcon(pmBird())


def pmBull():
    return PM(392667,399636)


def Bull():
    return QtGui.QIcon(pmBull())


def pmBulldog():
    return PM(399636,406527)


def Bulldog():
    return QtGui.QIcon(pmBulldog())


def pmButterfly():
    return PM(406527,413901)


def Butterfly():
    return QtGui.QIcon(pmButterfly())


def pmCat():
    return PM(413901,420173)


def Cat():
    return QtGui.QIcon(pmCat())


def pmChicken():
    return PM(420173,425984)


def Chicken():
    return QtGui.QIcon(pmChicken())


def pmCow():
    return PM(425984,432727)


def Cow():
    return QtGui.QIcon(pmCow())


def pmCrab():
    return PM(432727,438316)


def Crab():
    return QtGui.QIcon(pmCrab())


def pmCrocodile():
    return PM(438316,444457)


def Crocodile():
    return QtGui.QIcon(pmCrocodile())


def pmDeer():
    return PM(444457,450764)


def Deer():
    return QtGui.QIcon(pmDeer())


def pmDog():
    return PM(450764,457367)


def Dog():
    return QtGui.QIcon(pmDog())


def pmDonkey():
    return PM(457367,463014)


def Donkey():
    return QtGui.QIcon(pmDonkey())


def pmDuck():
    return PM(463014,469557)


def Duck():
    return QtGui.QIcon(pmDuck())


def pmEagle():
    return PM(469557,474375)


def Eagle():
    return QtGui.QIcon(pmEagle())


def pmElephant():
    return PM(474375,480856)


def Elephant():
    return QtGui.QIcon(pmElephant())


def pmFish():
    return PM(480856,487697)


def Fish():
    return QtGui.QIcon(pmFish())


def pmFox():
    return PM(487697,494480)


def Fox():
    return QtGui.QIcon(pmFox())


def pmFrog():
    return PM(494480,500896)


def Frog():
    return QtGui.QIcon(pmFrog())


def pmGiraffe():
    return PM(500896,508074)


def Giraffe():
    return QtGui.QIcon(pmGiraffe())


def pmGorilla():
    return PM(508074,514613)


def Gorilla():
    return QtGui.QIcon(pmGorilla())


def pmHippo():
    return PM(514613,521734)


def Hippo():
    return QtGui.QIcon(pmHippo())


def pmHorse():
    return PM(521734,528281)


def Horse():
    return QtGui.QIcon(pmHorse())


def pmInsect():
    return PM(528281,534216)


def Insect():
    return QtGui.QIcon(pmInsect())


def pmLion():
    return PM(534216,543126)


def Lion():
    return QtGui.QIcon(pmLion())


def pmMonkey():
    return PM(543126,550805)


def Monkey():
    return QtGui.QIcon(pmMonkey())


def pmMoose():
    return PM(550805,557429)


def Moose():
    return QtGui.QIcon(pmMoose())


def pmMouse():
    return PM(353979,359683)


def Mouse():
    return QtGui.QIcon(pmMouse())


def pmOwl():
    return PM(557429,564135)


def Owl():
    return QtGui.QIcon(pmOwl())


def pmPanda():
    return PM(564135,568169)


def Panda():
    return QtGui.QIcon(pmPanda())


def pmPenguin():
    return PM(568169,573718)


def Penguin():
    return QtGui.QIcon(pmPenguin())


def pmPig():
    return PM(573718,581758)


def Pig():
    return QtGui.QIcon(pmPig())


def pmRabbit():
    return PM(581758,589059)


def Rabbit():
    return QtGui.QIcon(pmRabbit())


def pmRhino():
    return PM(589059,595446)


def Rhino():
    return QtGui.QIcon(pmRhino())


def pmRooster():
    return PM(595446,600709)


def Rooster():
    return QtGui.QIcon(pmRooster())


def pmShark():
    return PM(600709,606479)


def Shark():
    return QtGui.QIcon(pmShark())


def pmSheep():
    return PM(606479,610310)


def Sheep():
    return QtGui.QIcon(pmSheep())


def pmSnake():
    return PM(610310,616335)


def Snake():
    return QtGui.QIcon(pmSnake())


def pmTiger():
    return PM(616335,624372)


def Tiger():
    return QtGui.QIcon(pmTiger())


def pmTurkey():
    return PM(624372,631786)


def Turkey():
    return QtGui.QIcon(pmTurkey())


def pmTurtle():
    return PM(631786,638507)


def Turtle():
    return QtGui.QIcon(pmTurtle())


def pmWolf():
    return PM(638507,641602)


def Wolf():
    return QtGui.QIcon(pmWolf())


def pmSteven():
    return PM(641602,648754)


def Steven():
    return QtGui.QIcon(pmSteven())


def pmWheel():
    return PM(648754,656819)


def Wheel():
    return QtGui.QIcon(pmWheel())


def pmWheelchair():
    return PM(656819,665623)


def Wheelchair():
    return QtGui.QIcon(pmWheelchair())


def pmTouringMotorcycle():
    return PM(665623,671935)


def TouringMotorcycle():
    return QtGui.QIcon(pmTouringMotorcycle())


def pmContainer():
    return PM(671935,677270)


def Container():
    return QtGui.QIcon(pmContainer())


def pmBoatEquipment():
    return PM(677270,682793)


def BoatEquipment():
    return QtGui.QIcon(pmBoatEquipment())


def pmCar():
    return PM(682793,687439)


def Car():
    return QtGui.QIcon(pmCar())


def pmLorry():
    return PM(687439,693475)


def Lorry():
    return QtGui.QIcon(pmLorry())


def pmCarTrailer():
    return PM(693475,697572)


def CarTrailer():
    return QtGui.QIcon(pmCarTrailer())


def pmTowTruck():
    return PM(697572,702330)


def TowTruck():
    return QtGui.QIcon(pmTowTruck())


def pmQuadBike():
    return PM(702330,708299)


def QuadBike():
    return QtGui.QIcon(pmQuadBike())


def pmRecoveryTruck():
    return PM(708299,713296)


def RecoveryTruck():
    return QtGui.QIcon(pmRecoveryTruck())


def pmContainerLoader():
    return PM(713296,718438)


def ContainerLoader():
    return QtGui.QIcon(pmContainerLoader())


def pmPoliceCar():
    return PM(718438,723270)


def PoliceCar():
    return QtGui.QIcon(pmPoliceCar())


def pmExecutiveCar():
    return PM(723270,727948)


def ExecutiveCar():
    return QtGui.QIcon(pmExecutiveCar())


def pmTruck():
    return PM(727948,733411)


def Truck():
    return QtGui.QIcon(pmTruck())


def pmExcavator():
    return PM(733411,738302)


def Excavator():
    return QtGui.QIcon(pmExcavator())


def pmCabriolet():
    return PM(738302,743140)


def Cabriolet():
    return QtGui.QIcon(pmCabriolet())


def pmMixerTruck():
    return PM(743140,749450)


def MixerTruck():
    return QtGui.QIcon(pmMixerTruck())


def pmForkliftTruckLoaded():
    return PM(749450,755598)


def ForkliftTruckLoaded():
    return QtGui.QIcon(pmForkliftTruckLoaded())


def pmAmbulance():
    return PM(755598,761648)


def Ambulance():
    return QtGui.QIcon(pmAmbulance())


def pmDieselLocomotiveBoxcar():
    return PM(761648,765654)


def DieselLocomotiveBoxcar():
    return QtGui.QIcon(pmDieselLocomotiveBoxcar())


def pmTractorUnit():
    return PM(765654,771121)


def TractorUnit():
    return QtGui.QIcon(pmTractorUnit())


def pmFireTruck():
    return PM(771121,777460)


def FireTruck():
    return QtGui.QIcon(pmFireTruck())


def pmCargoShip():
    return PM(777460,781801)


def CargoShip():
    return QtGui.QIcon(pmCargoShip())


def pmSubwayTrain():
    return PM(781801,786691)


def SubwayTrain():
    return QtGui.QIcon(pmSubwayTrain())


def pmTruckMountedCrane():
    return PM(786691,792432)


def TruckMountedCrane():
    return QtGui.QIcon(pmTruckMountedCrane())


def pmAirAmbulance():
    return PM(792432,797545)


def AirAmbulance():
    return QtGui.QIcon(pmAirAmbulance())


def pmAirplane():
    return PM(797545,802433)


def Airplane():
    return QtGui.QIcon(pmAirplane())


def pmCaracol():
    return PM(802433,804249)


def Caracol():
    return QtGui.QIcon(pmCaracol())


def pmUno():
    return PM(804249,806711)


def Uno():
    return QtGui.QIcon(pmUno())


def pmMotoresExternos():
    return PM(806711,808613)


def MotoresExternos():
    return QtGui.QIcon(pmMotoresExternos())


def pmDatabase():
    return PM(808613,809929)


def Database():
    return QtGui.QIcon(pmDatabase())


def pmDatabaseMas():
    return PM(809929,811388)


def DatabaseMas():
    return QtGui.QIcon(pmDatabaseMas())


def pmDatabaseImport():
    return PM(811388,812024)


def DatabaseImport():
    return QtGui.QIcon(pmDatabaseImport())


def pmDatabaseExport():
    return PM(812024,812669)


def DatabaseExport():
    return QtGui.QIcon(pmDatabaseExport())


def pmDatabaseDelete():
    return PM(812669,813792)


def DatabaseDelete():
    return QtGui.QIcon(pmDatabaseDelete())


def pmDatabaseMaintenance():
    return PM(813792,815288)


def DatabaseMaintenance():
    return QtGui.QIcon(pmDatabaseMaintenance())


def pmAtacante():
    return PM(815288,815893)


def Atacante():
    return QtGui.QIcon(pmAtacante())


def pmAtacada():
    return PM(815893,816459)


def Atacada():
    return QtGui.QIcon(pmAtacada())


def pmGoToNext():
    return PM(816459,816871)


def GoToNext():
    return QtGui.QIcon(pmGoToNext())


def pmBlancas():
    return PM(816871,817222)


def Blancas():
    return QtGui.QIcon(pmBlancas())


def pmNegras():
    return PM(817222,817468)


def Negras():
    return QtGui.QIcon(pmNegras())


def pmFolderChange():
    return PM(71649,74407)


def FolderChange():
    return QtGui.QIcon(pmFolderChange())


def pmMarkers():
    return PM(817468,819163)


def Markers():
    return QtGui.QIcon(pmMarkers())


def pmTop():
    return PM(819163,819747)


def Top():
    return QtGui.QIcon(pmTop())


def pmBottom():
    return PM(819747,820336)


def Bottom():
    return QtGui.QIcon(pmBottom())


def pmSTS():
    return PM(820336,822527)


def STS():
    return QtGui.QIcon(pmSTS())


def pmRun():
    return PM(822527,824251)


def Run():
    return QtGui.QIcon(pmRun())


def pmRun2():
    return PM(824251,825771)


def Run2():
    return QtGui.QIcon(pmRun2())


def pmWorldMap():
    return PM(825771,828512)


def WorldMap():
    return QtGui.QIcon(pmWorldMap())


def pmAfrica():
    return PM(828512,830998)


def Africa():
    return QtGui.QIcon(pmAfrica())


def pmMaps():
    return PM(830998,831942)


def Maps():
    return QtGui.QIcon(pmMaps())


def pmSol():
    return PM(831942,832868)


def Sol():
    return QtGui.QIcon(pmSol())


def pmSolNubes():
    return PM(832868,833731)


def SolNubes():
    return QtGui.QIcon(pmSolNubes())


def pmSolNubesLluvia():
    return PM(833731,834691)


def SolNubesLluvia():
    return QtGui.QIcon(pmSolNubesLluvia())


def pmLluvia():
    return PM(834691,835530)


def Lluvia():
    return QtGui.QIcon(pmLluvia())


def pmInvierno():
    return PM(835530,837106)


def Invierno():
    return QtGui.QIcon(pmInvierno())


def pmFixedElo():
    return PM(164966,166229)


def FixedElo():
    return QtGui.QIcon(pmFixedElo())


def pmSoundTool():
    return PM(837106,839565)


def SoundTool():
    return QtGui.QIcon(pmSoundTool())


def pmTrain():
    return PM(839565,840935)


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
    return PM(840935,845293)


def PlayGame():
    return QtGui.QIcon(pmPlayGame())


def pmScanner():
    return PM(845293,845634)


def Scanner():
    return QtGui.QIcon(pmScanner())


def pmMenos():
    return PM(845634,846159)


def Menos():
    return QtGui.QIcon(pmMenos())


def pmSchool():
    return PM(846159,847521)


def School():
    return QtGui.QIcon(pmSchool())


def pmLaw():
    return PM(847521,848137)


def Law():
    return QtGui.QIcon(pmLaw())


def pmLearnGame():
    return PM(848137,848570)


def LearnGame():
    return QtGui.QIcon(pmLearnGame())


def pmLonghaul():
    return PM(848570,849496)


def Longhaul():
    return QtGui.QIcon(pmLonghaul())


def pmTrekking():
    return PM(849496,850190)


def Trekking():
    return QtGui.QIcon(pmTrekking())


def pmPassword():
    return PM(850190,850643)


def Password():
    return QtGui.QIcon(pmPassword())


def pmSQL_RAW():
    return PM(840935,845293)


def SQL_RAW():
    return QtGui.QIcon(pmSQL_RAW())


def pmSun():
    return PM(311022,311900)


def Sun():
    return QtGui.QIcon(pmSun())


def pmLight32():
    return PM(850643,852343)


def Light32():
    return QtGui.QIcon(pmLight32())


def pmTOL():
    return PM(852343,853052)


def TOL():
    return QtGui.QIcon(pmTOL())


def pmUned():
    return PM(853052,853472)


def Uned():
    return QtGui.QIcon(pmUned())


def pmUwe():
    return PM(853472,854441)


def Uwe():
    return QtGui.QIcon(pmUwe())


def pmThinking():
    return PM(854441,855230)


def Thinking():
    return QtGui.QIcon(pmThinking())


def pmWashingMachine():
    return PM(855230,855893)


def WashingMachine():
    return QtGui.QIcon(pmWashingMachine())


def pmTerminal():
    return PM(855893,859437)


def Terminal():
    return QtGui.QIcon(pmTerminal())


def pmManualSave():
    return PM(859437,860020)


def ManualSave():
    return QtGui.QIcon(pmManualSave())


def pmSettings():
    return PM(860020,860458)


def Settings():
    return QtGui.QIcon(pmSettings())


def pmStrength():
    return PM(860458,861129)


def Strength():
    return QtGui.QIcon(pmStrength())


def pmSingular():
    return PM(861129,861984)


def Singular():
    return QtGui.QIcon(pmSingular())


def pmScript():
    return PM(861984,862553)


def Script():
    return QtGui.QIcon(pmScript())


def pmTexto():
    return PM(862553,865398)


def Texto():
    return QtGui.QIcon(pmTexto())


def pmLampara():
    return PM(865398,866107)


def Lampara():
    return QtGui.QIcon(pmLampara())


def pmFile():
    return PM(866107,868407)


def File():
    return QtGui.QIcon(pmFile())


def pmCalculo():
    return PM(868407,869333)


def Calculo():
    return QtGui.QIcon(pmCalculo())


def pmOpeningLines():
    return PM(869333,870011)


def OpeningLines():
    return QtGui.QIcon(pmOpeningLines())


def pmStudy():
    return PM(870011,870924)


def Study():
    return QtGui.QIcon(pmStudy())


def pmLichess():
    return PM(870924,871814)


def Lichess():
    return QtGui.QIcon(pmLichess())


def pmMiniatura():
    return PM(871814,872741)


def Miniatura():
    return QtGui.QIcon(pmMiniatura())


def pmLocomotora():
    return PM(872741,873522)


def Locomotora():
    return QtGui.QIcon(pmLocomotora())


def pmTrainSequential():
    return PM(873522,874663)


def TrainSequential():
    return QtGui.QIcon(pmTrainSequential())


def pmTrainStatic():
    return PM(874663,875623)


def TrainStatic():
    return QtGui.QIcon(pmTrainStatic())


def pmTrainPositions():
    return PM(875623,876604)


def TrainPositions():
    return QtGui.QIcon(pmTrainPositions())


def pmTrainEngines():
    return PM(876604,878038)


def TrainEngines():
    return QtGui.QIcon(pmTrainEngines())


def pmError():
    return PM(48833,52833)


def Error():
    return QtGui.QIcon(pmError())


def pmAtajos():
    return PM(878038,879217)


def Atajos():
    return QtGui.QIcon(pmAtajos())


def pmTOLline():
    return PM(879217,880321)


def TOLline():
    return QtGui.QIcon(pmTOLline())


def pmTOLchange():
    return PM(880321,882543)


def TOLchange():
    return QtGui.QIcon(pmTOLchange())


def pmPack():
    return PM(882543,883716)


def Pack():
    return QtGui.QIcon(pmPack())


def pmHome():
    return PM(179976,181158)


def Home():
    return QtGui.QIcon(pmHome())


def pmImport8():
    return PM(883716,884474)


def Import8():
    return QtGui.QIcon(pmImport8())


def pmExport8():
    return PM(884474,885099)


def Export8():
    return QtGui.QIcon(pmExport8())


def pmTablas8():
    return PM(885099,885891)


def Tablas8():
    return QtGui.QIcon(pmTablas8())


def pmBlancas8():
    return PM(885891,886921)


def Blancas8():
    return QtGui.QIcon(pmBlancas8())


def pmNegras8():
    return PM(886921,887760)


def Negras8():
    return QtGui.QIcon(pmNegras8())


def pmBook():
    return PM(887760,888334)


def Book():
    return QtGui.QIcon(pmBook())


def pmWrite():
    return PM(888334,889539)


def Write():
    return QtGui.QIcon(pmWrite())


def pmAlt():
    return PM(889539,889981)


def Alt():
    return QtGui.QIcon(pmAlt())


def pmShift():
    return PM(889981,890321)


def Shift():
    return QtGui.QIcon(pmShift())


def pmRightMouse():
    return PM(890321,891121)


def RightMouse():
    return QtGui.QIcon(pmRightMouse())


def pmControl():
    return PM(891121,891646)


def Control():
    return QtGui.QIcon(pmControl())


def pmFinales():
    return PM(891646,892733)


def Finales():
    return QtGui.QIcon(pmFinales())


def pmEditColumns():
    return PM(892733,893465)


def EditColumns():
    return QtGui.QIcon(pmEditColumns())


def pmResizeAll():
    return PM(893465,893975)


def ResizeAll():
    return QtGui.QIcon(pmResizeAll())


def pmChecked():
    return PM(893975,894481)


def Checked():
    return QtGui.QIcon(pmChecked())


def pmUnchecked():
    return PM(894481,894729)


def Unchecked():
    return QtGui.QIcon(pmUnchecked())


def pmBuscarC():
    return PM(894729,895173)


def BuscarC():
    return QtGui.QIcon(pmBuscarC())


def pmPeonBlanco():
    return PM(895173,897354)


def PeonBlanco():
    return QtGui.QIcon(pmPeonBlanco())


def pmPeonNegro():
    return PM(897354,898878)


def PeonNegro():
    return QtGui.QIcon(pmPeonNegro())


def pmReciclar():
    return PM(898878,899602)


def Reciclar():
    return QtGui.QIcon(pmReciclar())


def pmLanzamiento():
    return PM(899602,900315)


def Lanzamiento():
    return QtGui.QIcon(pmLanzamiento())


def pmEndGame():
    return PM(900315,900729)


def EndGame():
    return QtGui.QIcon(pmEndGame())


def pmPause():
    return PM(900729,901598)


def Pause():
    return QtGui.QIcon(pmPause())


def pmContinue():
    return PM(901598,902802)


def Continue():
    return QtGui.QIcon(pmContinue())


def pmClose():
    return PM(902802,903501)


def Close():
    return QtGui.QIcon(pmClose())


def pmStop():
    return PM(903501,904534)


def Stop():
    return QtGui.QIcon(pmStop())


def pmFactoryPolyglot():
    return PM(904534,905354)


def FactoryPolyglot():
    return QtGui.QIcon(pmFactoryPolyglot())


def pmTags():
    return PM(905354,906177)


def Tags():
    return QtGui.QIcon(pmTags())


def pmAppearance():
    return PM(906177,906904)


def Appearance():
    return QtGui.QIcon(pmAppearance())


def pmFill():
    return PM(906904,907942)


def Fill():
    return QtGui.QIcon(pmFill())


def pmSupport():
    return PM(907942,908674)


def Support():
    return QtGui.QIcon(pmSupport())


def pmOrder():
    return PM(908674,909472)


def Order():
    return QtGui.QIcon(pmOrder())


def pmPlay1():
    return PM(909472,910767)


def Play1():
    return QtGui.QIcon(pmPlay1())


def pmRemove1():
    return PM(910767,911894)


def Remove1():
    return QtGui.QIcon(pmRemove1())


def pmNew1():
    return PM(911894,912216)


def New1():
    return QtGui.QIcon(pmNew1())


def pmMensError():
    return PM(912216,914280)


def MensError():
    return QtGui.QIcon(pmMensError())


def pmMensInfo():
    return PM(914280,916835)


def MensInfo():
    return QtGui.QIcon(pmMensInfo())


def pmJump():
    return PM(916835,917510)


def Jump():
    return QtGui.QIcon(pmJump())


def pmCaptures():
    return PM(917510,918691)


def Captures():
    return QtGui.QIcon(pmCaptures())


def pmRepeat():
    return PM(918691,919350)


def Repeat():
    return QtGui.QIcon(pmRepeat())


def pmCount():
    return PM(919350,920026)


def Count():
    return QtGui.QIcon(pmCount())


def pmMate15():
    return PM(920026,921097)


def Mate15():
    return QtGui.QIcon(pmMate15())


def pmCoordinates():
    return PM(921097,922250)


def Coordinates():
    return QtGui.QIcon(pmCoordinates())


def pmKnight():
    return PM(922250,923493)


def Knight():
    return QtGui.QIcon(pmKnight())


def pmCorrecto():
    return PM(923493,924519)


def Correcto():
    return QtGui.QIcon(pmCorrecto())


def pmBlocks():
    return PM(924519,924856)


def Blocks():
    return QtGui.QIcon(pmBlocks())


def pmWest():
    return PM(924856,925962)


def West():
    return QtGui.QIcon(pmWest())


def pmOpening():
    return PM(925962,926220)


def Opening():
    return QtGui.QIcon(pmOpening())


def pmVariation():
    return PM(223138,223556)


def Variation():
    return QtGui.QIcon(pmVariation())


def pmComment():
    return PM(926220,926583)


def Comment():
    return QtGui.QIcon(pmComment())


def pmVariationComment():
    return PM(926583,926927)


def VariationComment():
    return QtGui.QIcon(pmVariationComment())


def pmOpeningVariation():
    return PM(926927,927391)


def OpeningVariation():
    return QtGui.QIcon(pmOpeningVariation())


def pmOpeningComment():
    return PM(927391,927724)


def OpeningComment():
    return QtGui.QIcon(pmOpeningComment())


def pmOpeningVariationComment():
    return PM(926927,927391)


def OpeningVariationComment():
    return QtGui.QIcon(pmOpeningVariationComment())


def pmDeleteRow():
    return PM(927724,928155)


def DeleteRow():
    return QtGui.QIcon(pmDeleteRow())


def pmDeleteColumn():
    return PM(928155,928598)


def DeleteColumn():
    return QtGui.QIcon(pmDeleteColumn())


def pmEditVariation():
    return PM(928598,928953)


def EditVariation():
    return QtGui.QIcon(pmEditVariation())


def pmKibitzer():
    return PM(928953,929552)


def Kibitzer():
    return QtGui.QIcon(pmKibitzer())


def pmKibitzer_Pause():
    return PM(929552,929724)


def Kibitzer_Pause():
    return QtGui.QIcon(pmKibitzer_Pause())


def pmKibitzer_Options():
    return PM(929724,930626)


def Kibitzer_Options():
    return QtGui.QIcon(pmKibitzer_Options())


def pmKibitzer_Voyager():
    return PM(345867,346710)


def Kibitzer_Voyager():
    return QtGui.QIcon(pmKibitzer_Voyager())


def pmKibitzer_Close():
    return PM(930626,931183)


def Kibitzer_Close():
    return QtGui.QIcon(pmKibitzer_Close())


def pmKibitzer_Down():
    return PM(931183,931572)


def Kibitzer_Down():
    return QtGui.QIcon(pmKibitzer_Down())


def pmKibitzer_Up():
    return PM(931572,931967)


def Kibitzer_Up():
    return QtGui.QIcon(pmKibitzer_Up())


def pmKibitzer_Back():
    return PM(931967,932400)


def Kibitzer_Back():
    return QtGui.QIcon(pmKibitzer_Back())


def pmKibitzer_Clipboard():
    return PM(932400,932786)


def Kibitzer_Clipboard():
    return QtGui.QIcon(pmKibitzer_Clipboard())


def pmKibitzer_Play():
    return PM(932786,933307)


def Kibitzer_Play():
    return QtGui.QIcon(pmKibitzer_Play())


def pmKibitzer_Side():
    return PM(933307,934060)


def Kibitzer_Side():
    return QtGui.QIcon(pmKibitzer_Side())


def pmKibitzer_Board():
    return PM(934060,934498)


def Kibitzer_Board():
    return QtGui.QIcon(pmKibitzer_Board())


def pmBoard():
    return PM(934498,934967)


def Board():
    return QtGui.QIcon(pmBoard())


def pmTraining_Games():
    return PM(934967,936659)


def Training_Games():
    return QtGui.QIcon(pmTraining_Games())


def pmTraining_Basic():
    return PM(936659,938032)


def Training_Basic():
    return QtGui.QIcon(pmTraining_Basic())


def pmTraining_Tactics():
    return PM(938032,938813)


def Training_Tactics():
    return QtGui.QIcon(pmTraining_Tactics())


def pmTraining_Endings():
    return PM(938813,939747)


def Training_Endings():
    return QtGui.QIcon(pmTraining_Endings())


def pmBridge():
    return PM(939747,940765)


def Bridge():
    return QtGui.QIcon(pmBridge())


def pmMaia():
    return PM(940765,941549)


def Maia():
    return QtGui.QIcon(pmMaia())


def pmBinBook():
    return PM(941549,942298)


def BinBook():
    return QtGui.QIcon(pmBinBook())


def pmConnected():
    return PM(942298,943916)


def Connected():
    return QtGui.QIcon(pmConnected())


