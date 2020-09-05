from Code import ManagerVariations


def edit_variation(procesador, game, titulo=None, with_engine_active=False, is_competitive=False, is_white_bottom=None):
    window = procesador.main_window
    xtutor = procesador.XTutor()
    procesador_variations = procesador.clonVariations(window, xtutor, is_competitive=is_competitive)

    manager_variations = ManagerVariations.ManagerVariations(procesador_variations)
    manager_variations.inicio(game, is_white_bottom, with_engine_active, is_competitive)
    procesador_variations.manager = manager_variations

    if titulo is None:
        titulo = game.pgnBaseRAW()

    procesador_variations.main_window.muestraVariations(titulo)

    return manager_variations.valor()


def edit_variation_moves(procesador, window, is_white_bottom, fen, linea_pgn, titulo=None):
    procesador_variations = procesador.clonVariations(window)

    manager_variations = ManagerVariations.ManagerVariations(procesador_variations)
    manager_variations.inicio(fen, linea_pgn, False, is_white_bottom)
    procesador_variations.manager = manager_variations

    if titulo is None:
        titulo = linea_pgn
    procesador_variations.main_window.muestraVariations(titulo)

    return manager_variations.valor()  # pgn y a1h8, el a1h8 nos servira para edit las aperturas
