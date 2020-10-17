import sys
import os

lucas_chess = None  # asignado en Translate

folder_OS = os.path.realpath(os.path.join("OS", sys.platform))

folder_engines = os.path.join(folder_OS, "Engines")
sys.path.insert(0, folder_OS)
sys.path.insert(0, os.path.realpath(os.curdir))

folder_resources = os.path.realpath("../Resources")
folder_root = os.path.realpath("..")


def path_resource(*lista):
    p = folder_resources
    for x in lista:
        p = os.path.join(p, x)
    return os.path.realpath(p)


current_dir = os.path.realpath(os.path.dirname(sys.argv[0]))
if current_dir:
    os.chdir(current_dir)

sys.path.append(os.path.join(current_dir, "Code"))

isLinux = sys.platform == "linux"
isWindows = not isLinux
if isLinux:
    startfile = os.system
else:
    startfile = os.startfile

dgt = None
dgtDispatch = None

configuration = None
procesador = None

todasPiezas = None

tbook = path_resource("Openings", "GMopenings.bin")
tbookPTZ = path_resource("Openings", "fics15.bin")
tbookI = path_resource("Openings", "irina.bin")
xtutor = None

list_engine_managers = None

mate_en_dos = 175522

runSound = None

VERSION = "R0.33"
DEBUG = False
DEBUG_ENGINE = False

if DEBUG:
    import builtins


    def prlk(*x):
        import sys

        lx = len(x)-1

        for n, l in enumerate(x):
            sys.stdout.write(str(l))
            if n < lx:
                sys.stdout.write(" ")


    def stack(si_previo=False):
        import traceback

        if si_previo:
            prlk("-" * 80 + "\n")
            prlk(traceback.format_stack())
            prlk("\n" + "-" * 80 + "\n")
        for line in traceback.format_stack()[:-1]:
            prlk(line.strip() + "\n")


    builtins.__dict__["stack"] = stack
    builtins.__dict__["prlk"] = prlk

    prlk("Modo debug\n")

    import time

    def xpr(name, line):
        t = time.time()
        if name:
            li = name.split(" ")
            name = li[0]

        prlk("%0.02f %s %s" % (t - tdbg[0], name, line))
        tdbg[0] = t
        return True


    if DEBUG_ENGINE:
        tdbg = [time.time()]
        xpr("", "Modo debug engine")

    builtins.__dict__["xpr"] = xpr
