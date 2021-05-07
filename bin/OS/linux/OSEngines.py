import os

import FasterCode

from Code.Engines import Engines


def read_engines(folder_engines):
    dic_engines = {}

    def mas(clave, autor, version, url, exe, elo):
        path_exe = os.path.join(folder_engines, clave, exe)
        engine = Engines.Engine(clave.lower(), autor, version, url, path_exe)
        engine.elo = elo
        engine.ordenUCI("Log", "false")
        engine.ordenUCI("Ponder", "false")
        engine.ordenUCI("Hash", "16")
        engine.ordenUCI("Threads", "1")
        dic_engines[clave.lower()] = engine
        return engine

    bmi2 = "-bmi2" if FasterCode.bmi2() else ""

    for level in range(1100, 2000, 100):
        cm = mas(
            "Maia-%d" % level,
            "Reid McIlroy-Young,Ashton Anderson,Siddhartha Sen,Jon Kleinberg,Russell Wang + LcZero team",
            "%d" % level,
            "https://maiachess.com/",
            "Lc0-0.27.0",
            level,
        )
        cm.ordenUCI("WeightsFile", "maia-%d.pb.gz" % level)
        cm.path_exe = os.path.join(folder_engines, "Maia", "Lc0-0.27.0")
        cm.name = "Maia-%d" % level
        cm.ordenUCI("Ponder", "false")
        cm.ordenUCI("Hash", "16")
        cm.ordenUCI("Threads", "1")

    cm = mas("Lc0", "The LCZero Authors", "0.27.0", "https://github.com/LeelaChessZero", "Lc0-0.27.0", 3332)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "32")
    cm.ordenUCI("Threads", "1")

    cm = mas("Stockfish", "Tord Romstad, Marco Costalba, Joona Kiiski", "13", "http://stockfishchess.org/", "Stockfish-13", 3551)
    cm.ordenUCI("Ponder", "true")
    cm.ordenUCI("Hash", "32")
    cm.ordenUCI("Threads", "1")
    cm.ponMultiPV(20, 500)

    cm = mas("Komodo", "Don Dailey, Larry Kaufman", f"12.1.1{bmi2}", "http://komodochess.com/", f"Komodo-12.1.1{bmi2}", 3240)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "32")
    cm.ordenUCI("Threads", "1")
    cm.ponMultiPV(20, 218)

    cm = mas("Amoeba", "Richard Delorme", "2.6", "https://github.com/abulmo/amoeba", "Amoeba-2.6", 2911)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Andscacs", "Daniel José Queraltó", "0.95", "http://www.andscacs.com/", "Andscacs-0.95", 3240)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Arasan", "Jon Dart", "22.2", "https://www.arasanchess.org/", "Arasan-22.2", 3259)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Asymptote", "Maximilian Lupke", "0.8", "https://github.com/malu/asymptote", "Asymptote-0.8", 2909)
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Beef", "Jonathan Tseng", "0.36", "https://github.com/jtseng20/Beef", "Beef-0.36", 3097)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Alouette", "Roland Chastain", "0.1.4", "https://github.com/rchastain/alouette", "Alouette-0.1.4", 689)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas(
        "Cassandre",
        "Jean-Francois Romang), Raphael Grundrich, Thomas Adolph, Chad Koch",
        "0.24",
        "https://sourceforge.net/projects/cassandre/",
        "Cassandre-0.24",
        1140,
    )
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("CeeChess", "Tom Reinitz", "1.3.2", "https://github.com/bctboi23/CeeChess", "CeeChess-1.3.2", 2268)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Cheng", "Martin Sedlák", "4.40", "http://www.vlasak.biz/cheng", "Cheng-4.40", 2750)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Cinnamon", "Giuseppe Cannella", "1.2b", "http://cinnamonchess.altervista.org/", "Cinnamon-1.2b", 1930)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Chessika", "Laurent Chea", "2.21", "https://gitlab.com/MrPingouin/chessika", "Chessika-2.21", 1441)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Clarabit", "Salvador Pallares Bejarano", "1.00", "http://sapabe.googlepages.com", "Clarabit-1.00", 2058)
    cm.ordenUCI("OwnBook", "false")
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Counter", "Vadim Chizhov", "3.7", "https://github.com/ChizhovVadim/CounterGo", "Counter-3.7", 2963)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Critter", "Richard Vida", "1.6a", "http://www.vlasak.biz/critter", "Critter-1.6a", 3091)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("CT800", "Rasmus Althoff", "1.42", "https://www.ct800.net/", "CT800-1.42", 2380)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Daydreamer", "Aaron Becker", "1.75 JA", "http://github.com/AaronBecker/daydreamer/downloads", "Daydreamer-1.75", 2670)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Delocto", "Moritz Terink", "0.61n", "https://github.com/moterink/Delocto", "Delocto-0.61n", 2625)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Discocheck", "Lucas Braesch", "5.2.1", "https://github.com/lucasart/", "Discocheck-5.2.1", 2700)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Dragontooth", "Dylan Hunn", "0.2", "https://github.com/dylhunn/dragontooth", "Dragontooth-0.2", 1225)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Drofa", "Alexander Litov", "2.2.0", "https://github.com/justNo4b/Drofa", "Drofa-2.2.0", 2642)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Ethereal", "Andrew Grant", "12.75", "https://github.com/AndyGrant/Ethereal", "Ethereal-12.75", 3392)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("FracTal", "Visan Alexandru", "1.0", "https://github.com/visanalexandru/FracTal-ChessEngine", "FracTal-1.0", 2010)
    cm.ordenUCI("Log", "false")
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Fruit", "Fabien Letouzey", "2.1", "http://www.fruitchess.com/", "Fruit-2.1", 2784)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Gaviota", "Miguel Ballicora", "0.84", "https://sites.google.com/site/gaviotachessengine/Home", "Gaviota-0.84", 2638)
    cm.ordenUCI("Log", "false")
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Glaurung", "Tord RomsTad", "2.2", "http://www.glaurungchess.com/", "Glaurung-2.2", 2765)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Godel", "Juan Manuel Vazquez", "7.0", "https://sites.google.com/site/godelchessengine", "Godel-7.0", 2979)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Goldfish", "Bendik Samseth", "1.13.0", "https://github.com/bsamseth/Goldfish", "Goldfish-1.13.0", 2050)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Greko", "Vladimir Medvedev", "2020.03", "http://greko.su/index_en.html", "GreKo-2020.03", 2480)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Gunborg", "Torbjorn Nilsson", "1.35", "https://github.com/torgnil/gunborg", "Gunborg-1.35", 2086)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Hactar", "Jost Triller", "0.9.05", "https://github.com/tsoj/hactar", "Hactar-0.9.0", 1421)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Igel", "Volodymyr Shcherbyna", "3.0.0", "https://github.com/vshcherbyna/igel/", "Igel-3.0.0", 3402)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Irina", "Lucas Monge", "0.15", "https://github.com/lukasmonk/irina", "Irina-0.15", 1200)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Jabba", "Richard Allbert", "1.0", "http://jabbachess.blogspot.com/", "Jabba-1.0", 2078)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("K2", "Sergey Meus", "0.99", "https://github.com/serg-meus/k2", "K2-0.99", 2704)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Laser", "Jeffrey An and Michael An", "1.7", "https://github.com/jeffreyan11/laser-chess-engine", "Laser-1.17", 3227)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Marvin", "Martin Danielsson", "5.0.0", "https://github.com/bmdanielsson/marvin-chess", "Marvin-5.0.0", 3112)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Monolith", "Jonas Mayr", "2.01", "https://github.com/cimarronOST/Monolith", "Monolith-2.01", 3003)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas(
        "Monochrome",
        "Dan Ravensloft, formerly Matthew Brades (England), Manik Charan (India), George Koskeridis, Robert Taylor",
        "",
        "https://github.com/cpirc/Monochrome",
        "Monochrome",
        1601,
    )
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Octochess", "Tim Kosse", "r5190", "http://octochess.org/", "Octochess-r5190", 2771)  # New build
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Pawny", "Mincho Georgiev", "1.2", "http://pawny.netii.net/", "Pawny-1.2", 2550)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Pigeon", "Stuart Riffle", "1.5.1", "https://github.com/StuartRiffle/pigeon", "Pigeon-1.5.1", 1836)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Pulse", "Phokham Nonava", "1.6.1", "https://github.com/fluxroot/pulse", "Pulse-1.6.1", 1615)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Quokka", "Matt Palmer", "2.1", "https://github.com/mattbruv/Quokka", "Quokka-2.1", 1448)  # New build
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Rocinante", "Antonio Torrecillas", "2.0", "http://sites.google.com/site/barajandotrebejos/", "Rocinante-2.0", 1800)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("RodentII", "Pawel Koziol", "0.9.64", "http://www.pkoziol.cal24.pl/rodent/rodent.htm", "RodentII-0.9.64", 2912)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Shallow-blue", "Rhys Rustad-Elliott", "2.0.0", "https://github.com/GunshipPenguin/shallow-blue", "Shallow-blue-2.0.0", 1712)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Simplex", "Antonio Torrecillas", "0.98", "http://sites.google.com/site/barajandotrebejos", "Simplex-0.9.8", 2396)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Sissa", "Christophe J. Mandin", "2.0", "http://devzero.fr/~mnc/SISSA/fr/index_fr.html", "Sissa-2.0", 1957)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("SpaceDog", "Eric Silverman", "0.97.7", "https://github.com/thorsilver/SpaceDog", "SpaceDog-0.97.7", 2231)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Stash", "Morgan Houppin", "29.0", "https://gitlab.com/mhouppin/stash-bot", "Stash-29.0", 3065)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Supernova", "Minkai Yang", "2.3", "https://github.com/MichaeltheCoder7/Supernova", "Supernova-2.3", 2646)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Teki", "Manik Charan", "2", "https://github.com/Mk-Chan/Teki", "Teki-2", 2439)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Texel", "Peter Österlund", "1.06", "http://web.comhem.se/petero2home/javachess/index.html#texel", "Texel-1.06", 2900)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Tucano", "Alcides Schulz", "9.00", "https://sites.google.com/site/tucanochess", "Tucano-9.00", 2940)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Tunguska", "Fernando Tenorio", "1.1", "https://github.com/fernandotenorio/Tunguska", "Tunguska-1.1", 2439)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Velvet", "Martin Honert", "1.2.0", "https://github.com/mhonert/velvet-chess", "Velvet-1.2.0", 2686)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Weiss", "Terje Kirstihagen", "1.2", "https://github.com/TerjeKir/weiss", "Weiss-1.2", 2982)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Wowl", "Eric Yip", "1.3.7", "https://github.com/eric-ycw/wowl", "Wowl-1.3.7", 1925)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("WyldChess", "Manik Charan", "1.51", "https://github.com/Mk-Chan/WyldChess", "WyldChess-1.51", 2682)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Zappa", "Anthony Cozzie", "1.1", "http://www.acoz.net/zappa/", "Zappa-1.1", 2614)
    cm.ordenUCI("Log", "false")
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    cm = mas("Zurichess", "Alexandru Mosoi", "1.7.4", "https://bitbucket.org/zurichess/zurichess/", "Zurichess-1.7.4", 2830)
    cm.ordenUCI("Ponder", "false")
    cm.ordenUCI("Hash", "16")
    cm.ordenUCI("Threads", "1")

    return dic_engines


def dict_engines_fixed_elo(folder_engines):
    d = read_engines(folder_engines)
    dic = {}
    for nm, xfrom, xto in (("stockfish", 1350, 2850),):
        for elo in range(xfrom, xto + 100, 100):
            cm = d[nm].clona()
            if elo not in dic:
                dic[elo] = []
            cm.ordenUCI("UCI_Elo", str(elo))
            cm.ordenUCI("UCI_LimitStrength", "true")
            cm.name += " (%d)" % elo
            cm.key += " (%d)" % elo
            dic[elo].append(cm)
    return dic
