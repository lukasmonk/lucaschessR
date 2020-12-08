from PySide2 import QtCore

from Code import DGT

from Code.QT import FormLayout
from Code.QT import QTUtil2
from Code.QT import Iconos
from Code import Util
from Code.Base.Constantes import *


def opciones(parent, configuration):
    form = FormLayout.FormLayout(parent, _("Configuration"), Iconos.Opciones(), anchoMinimo=640)

    # Datos generales ##############################################################################################
    form.separador()

    form.edit(_("Player's name"), configuration.x_player)
    form.separador()
    # form.combobox(_("Window style"), configuration.estilos(), configuration.x_style)
    # form.separador()

    li_traducciones = configuration.list_translations()
    tr_actual = configuration.translator()
    li = []
    for k, trad, porc, author in li_traducciones:
        label = "%s" % trad
        if int(porc) < 90:
            label += " (%s%%)" % porc
        li.append((label, k))
    form.combobox(_("Language"), li, tr_actual)
    form.separador()

    li = [
        (_("Play against an engine"), MENU_PLAY_ANY_ENGINE),
        (_("Opponents for young players"), MENU_PLAY_YOUNG_PLAYERS),
        (_("Both"), MENU_PLAY_BOTH),
    ]
    form.combobox(_("Menu Play"), li, configuration.x_menu_play)
    form.separador()

    form.checkbox(_("Check for updates at startup"), configuration.x_check_for_update)

    form.add_tab(_("General"))

    # Sonidos ########################################################################################################
    form.separador()
    form.checkbox(_("Beep after opponent's move"), configuration.x_sound_beep)
    form.separador()
    form.apart(_("Sound on in"))
    form.checkbox(_("Results"), configuration.x_sound_results)
    form.checkbox(_("Rival moves"), configuration.x_sound_move)
    form.separador()
    form.checkbox(_("Activate sounds with our moves") + ":", configuration.x_sound_our)

    form.add_tab(_("Sounds"))

    # Tutor ##########################################################################################################
    form.separador()
    form.combobox(_("Engine"), configuration.listaCambioTutor(), configuration.tutor.key)
    form.float(_("Duration of tutor analysis (secs)"), float(configuration.x_tutor_mstime / 1000.0))
    form.spinbox(_("Depth"), 0, 40, 100, configuration.x_tutor_depth)

    form.spinbox(_("Number of moves evaluated by engine(MultiPV)"), 0, 512, 100, configuration.x_tutor_multipv)
    form.separador()
    form.checkbox(_("Tutor enabled"), configuration.x_default_tutor_active)

    li_pos_tutor = [
        (_("Horizontal"), POS_TUTOR_HORIZONTAL),
        (_("Horizontal") + " 2+1", POS_TUTOR_HORIZONTAL_2_1),
        (_("Horizontal") + " 1+2", POS_TUTOR_HORIZONTAL_1_2),
        (_("Vertical"), POS_TUTOR_VERTICAL),
    ]
    form.combobox(_("Tutor boards position"), li_pos_tutor, configuration.x_tutor_view)
    form.separador()
    form.separador()
    form.apart(_("Sensitivity"))
    form.spinbox(_("Minimum difference in centipawns"), 0, 1000, 70, configuration.x_tutor_difpoints)
    form.spinbox(_("Minimum difference in %"), 0, 1000, 70, configuration.x_tutor_difporc)

    form.add_tab(_("Tutor"))

    # Engines #####################################################################################################
    form.separador()
    form.checkbox(_("Work in the background, when possible"), not configuration.x_engine_notbackground)
    form.separador()
    form.checkbox("%s -> %s:" % (_("Save engines log"), "UserData/EngineLogs"), configuration.x_log_engines)
    form.separador()
    form.folder(_("Gaviota Tablebases"), configuration.x_carpeta_gaviota, configuration.carpeta_gaviota_defecto())
    form.separador()

    form.add_tab(_("Engines"))

    # Boards #########################################################################################################
    form.separador()
    form.checkbox(_("Visual effects"), configuration.x_show_effects)

    drap = {1: 100, 2: 150, 3: 200, 4: 250, 5: 300, 6: 350, 7: 400, 8: 450, 9: 500}
    drap_v = {}
    for x in drap:
        drap_v[drap[x]] = x
    form.dial(
        "%s (%s=1)" % (_("Speed"), _("Default")),
        1,
        len(drap),
        drap_v.get(configuration.x_pieces_speed, 100),
        siporc=False,
    )
    form.separador()

    li_mouse_sh = [
        (_("Type fixed: you must always indicate origin and destination"), False),
        (_("Type predictive: program tries to guess your intention"), True),
    ]
    form.combobox(_("Mouse shortcuts"), li_mouse_sh, configuration.x_mouse_shortcuts)
    form.checkbox(_("Show candidates"), configuration.x_show_candidates)
    form.checkbox(_("Always promote to queen\nALT key allows to change"), configuration.x_autopromotion_q)
    form.checkbox(_("Show cursor when engine is thinking"), configuration.x_cursor_thinking)
    form.separador()
    form.checkbox(_("Enable captured material window by default"), configuration.x_captures_activate)
    # liMat = [
    #     (_("Difference material"), "D"),
    #     (_("Captured material at beginning"), "C"),
    #     (_("Material advantage"), "M"),
    # ]
    # form.combobox(_("Show material"), liMat, configuration.x_capture_option)
    form.separador()
    form.checkbox(_("Enable information panel by default"), configuration.x_info_activate)
    form.separador()

    x = " - %s Graham O'Neill (https://goneill.co.nz)" % _("developed by")
    li_db = [(_("None"), ""),
             (_("DGT"), "DGT"),
             (_("Novag UCB") + x, "Novag UCB"),
             (_("Millennium") + x, "Millennium"),
             (_("Certabo") + x, "Certabo"),
             ]
    form.combobox(_("Digital board"), li_db, configuration.x_digital_board)

    form.separador()
    form.checkbox(_("Show configuration icon"), configuration.x_opacity_tool_board > 6)
    li_pos = [(_("Bottom"), "B"), (_("Top"), "T")]
    form.combobox(_("Configuration icon position"), li_pos, configuration.x_position_tool_board)
    form.separador()
    form.checkbox(_("Show icon when position has graphic information"), configuration.x_director_icon)
    form.separador()
    form.checkbox(_("Live graphics with the right mouse button"), configuration.x_direct_graphics)

    form.add_tab(_("Boards"))

    # Aspect ########################################################################################################
    form.checkbox(_("By default"), False)
    form.separador()
    form.font(_("Font"), configuration.x_font_family)

    form.apart(_("Menus"))
    form.spinbox(_("Font size"), 5, 64, 60, configuration.x_menu_points)
    form.checkbox(_("Bold"), configuration.x_menu_bold)

    form.separador()
    form.apart(_("Toolbars"))
    form.spinbox(_("Font size"), 5, 64, 60, configuration.x_tb_fontpoints)
    form.checkbox(_("Bold"), configuration.x_tb_bold)
    li = (
        (_("Only display the icon"), QtCore.Qt.ToolButtonIconOnly),
        (_("Only display the text"), QtCore.Qt.ToolButtonTextOnly),
        (_("The text appears beside the icon"), QtCore.Qt.ToolButtonTextBesideIcon),
        (_("The text appears under the icon"), QtCore.Qt.ToolButtonTextUnderIcon),
    )
    form.combobox(_("Icons"), li, configuration.tipoIconos())

    form.separador()
    form.apart(_("PGN table"))
    form.spinbox(_("Width"), 283, 1000, 70, configuration.x_pgn_width)
    form.spinbox(_("Height of each row"), 18, 99, 70, configuration.x_pgn_rowheight)
    form.spinbox(_("Font size"), 10, 99, 70, configuration.x_pgn_fontpoints)
    form.checkbox(_("PGN always in English"), configuration.x_pgn_english)
    form.checkbox(_("PGN with figurines"), configuration.x_pgn_withfigurines)
    form.separador()

    form.spinbox(_("Font size of information labels"), 8, 30, 70, configuration.x_sizefont_infolabels)

    form.add_tab(_("Appearance"))

    # Perfomance ####################################################################################################
    perf = configuration.perfomance

    def d(num):
        return " (%s %d)" % (_("default"), num)

    form.separador()
    form.apart(_("Bad moves: lost points to consider a move as bad"))
    form.spinbox(_("Bad move") + d(90), 20, 1000, 60, perf.bad_lostp)
    form.spinbox(_("Very bad move") + d(200), 50, 1000, 60, perf.very_bad_lostp)
    form.separador()
    form.spinbox(_("Degree of effect of bad moves on the game elo") + d(2), 0, 5, 40, perf.bad_factor)
    form.separador()
    form.apart(_("Good moves: minimum depth required by the engine to discover the move"))
    form.spinbox(_("Good move") + d(3), 2, 20, 40, perf.good_depth)
    form.spinbox(_("Very good move") + d(6), 3, 20, 40, perf.very_good_depth)

    form.add_tab(_("Performance"))

    # Salvado automatico #############################################################################################
    form.separador()
    form.file(_("Autosave to a PGN file"), "pgn", True, configuration.x_save_pgn)
    form.checkbox(_("Won games"), configuration.x_save_won)
    form.checkbox(_("Lost/Drawn games"), configuration.x_save_lost)
    form.checkbox(_("Unfinished games"), configuration.x_save_unfinished)
    form.separador()
    form.checkbox(_("Save as variation tutor's suggestion"), configuration.x_save_tutor_variations)
    form.separador()
    form.file(_("Autosave to a CSV file moves played"), "csv", True, configuration.x_save_csv)

    form.add_tab(_("Autosave"))

    # Modo no competitivo ############################################################################################
    form.separador()
    form.spinbox(_("Lucas-Elo"), 0, 3200, 70, configuration.x_elo)
    form.separador()
    form.spinbox(_("Tourney-Elo"), 0, 3200, 70, configuration.x_michelo)
    form.separador()
    form.spinbox(_("Fics-Elo"), 0, 3200, 70, configuration.x_fics)
    form.separador()
    form.spinbox(_("Fide-Elo"), 0, 3200, 70, configuration.x_fide)
    form.separador()
    form.spinbox(_("Lichess-Elo"), 0, 3200, 70, configuration.x_lichess)

    form.add_tab(_("Change elos"))

    resultado = form.run()

    if resultado:
        accion, resp = resultado

        li_gen, li_son, li_tt, li_eng, li_b, li_asp, li_pr, li_sa, li_nc = resp

        (
            configuration.x_player,
            # configuration.x_style,
            translator,
            configuration.x_menu_play,
            configuration.x_check_for_update,
        ) = li_gen

        configuration.set_translator(translator)

        por_defecto = li_asp[0]
        if por_defecto:
            li_asp = "", 11, False, 11, False, QtCore.Qt.ToolButtonTextUnderIcon, 283, 22, 10, False, True, 10
        else:
            del li_asp[0]
        (
            configuration.x_font_family,
            configuration.x_menu_points,
            configuration.x_menu_bold,
            configuration.x_tb_fontpoints,
            configuration.x_tb_bold,
            qt_iconstb,
            configuration.x_pgn_width,
            configuration.x_pgn_rowheight,
            configuration.x_pgn_fontpoints,
            configuration.x_pgn_english,
            configuration.x_pgn_withfigurines,
            configuration.x_sizefont_infolabels,
        ) = li_asp
        if configuration.x_font_family == "System":
            configuration.x_font_family = ""

        configuration.set_tipoIconos(qt_iconstb)

        (
            configuration.x_sound_beep,
            configuration.x_sound_results,
            configuration.x_sound_move,
            configuration.x_sound_our,
        ) = li_son

        (
            configuration.x_tutor_clave,
            tiempoTutor,
            configuration.x_tutor_depth,
            configuration.x_tutor_multipv,
            configuration.x_default_tutor_active,
            configuration.x_tutor_view,
            configuration.x_tutor_difpoints,
            configuration.x_tutor_difporc,
        ) = li_tt
        configuration.x_tutor_mstime = int(tiempoTutor * 1000)

        (
            configuration.x_elo,
            configuration.x_michelo,
            configuration.x_fics,
            configuration.x_fide,
            configuration.x_lichess,
        ) = li_nc

        (workinbackground, configuration.x_log_engines, configuration.x_carpeta_gaviota) = li_eng
        configuration.x_engine_notbackground = not workinbackground

        (
            configuration.x_show_effects,
            rapidezMovPiezas,
            configuration.x_mouse_shortcuts,
            configuration.x_show_candidates,
            configuration.x_autopromotion_q,
            configuration.x_cursor_thinking,
            configuration.x_captures_activate,
            configuration.x_info_activate,
            dboard,
            toolIcon,
            configuration.x_position_tool_board,
            configuration.x_director_icon,
            configuration.x_direct_graphics,
        ) = li_b
        configuration.x_opacity_tool_board = 10 if toolIcon else 1
        configuration.x_pieces_speed = drap[rapidezMovPiezas]
        if configuration.x_digital_board != dboard:
            if dboard:
                if QTUtil2.pregunta(parent, "%s<br><br>%s %s" % (
                    _("Are you sure %s is the correct driver ?") % dboard,
                    _("WARNING: selecting the wrong driver might cause damage to your board."),
                    _("Proceed at your own risk.")
                    )
                ):
                    DGT.ponON()
                else:
                    dboard = ""
            configuration.x_digital_board = dboard

        perf.bad_lostp, perf.very_bad_lostp, perf.bad_factor, perf.good_depth, perf.very_good_depth = li_pr
        perf.very_bad_factor = perf.bad_factor * 4

        (
            configuration.x_save_pgn,
            configuration.x_save_won,
            configuration.x_save_lost,
            configuration.x_save_unfinished,
            configuration.x_save_tutor_variations,
            configuration.x_save_csv,
        ) = li_sa
        configuration.x_save_csv = Util.relative_path(configuration.x_save_csv)

        return True
    else:
        return False


def options_first_time(parent, configuration):
    form = FormLayout.FormLayout(parent, _("Player"), Iconos.Usuarios(), anchoMinimo=460)
    form.separador()
    form.edit(_("Player's name"), configuration.x_player)
    result = form.run()
    if result:
        accion, resp = result
        player = resp[0].strip()
        if not player:
            player = _("Player")
        configuration.x_player = player
        return True
    else:
        return False
