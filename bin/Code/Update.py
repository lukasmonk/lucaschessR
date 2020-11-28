import shutil
import urllib
import zipfile

from Code.QT import QTUtil2
from Code import Util

WEBUPDATES = "https://lucaschess.pythonanywhere.com/static/updates11/updates.txt"


def update_file(titulo, urlfichero, tam):
    shutil.rmtree("actual", ignore_errors=True)
    Util.create_folder("actual")

    # Se trae el file
    global progreso, is_beginning
    progreso = QTUtil2.BarraProgreso(None, titulo, _("Updating..."), 100).mostrar()
    is_beginning = True

    def hook(bloques, tambloque, tamfichero):
        global progreso, is_beginning
        if is_beginning:
            total = tamfichero / tambloque
            if tambloque * total < tamfichero:
                total += 1
            progreso.ponTotal(total)
            is_beginning = False
        progreso.inc()

    local_file = urlfichero.split("/")[-1]
    local_file = "actual/%s" % local_file
    urllib.urlretrieve(urlfichero, local_file, hook)

    is_canceled = progreso.is_canceled()
    progreso.cerrar()

    if is_canceled:
        return False

    # Comprobamos que se haya traido bien el file
    if tam != Util.filesize(local_file):
        return False

    # Se descomprime
    zp = zipfile.ZipFile(local_file, "r")
    zp.extractall("actual")

    # Se ejecuta act.py
    exec(open("actual/act.py").read())

    return True


def update(current_version, main_window):
    num_act = 0
    mens_error = None

    try:
        f = urllib.urlopen(WEBUPDATES)
        for x in f:
            act = x.strip()
            if not act.startswith("#"):  # Comentarios
                li = act.split(" ")
                # version urlfichero tama_o
                if len(li) == 3 and li[2].isdigit():
                    version, urlfichero, tam = li
                    current_major = current_version.split(".")[0]
                    version_major = version.split(".")[0]
                    if current_major == version_major:
                        if current_version < version:
                            if update_file(_X(_("version %1"), version), urlfichero, int(tam)):
                                current_version = version
                            else:
                                mens_error = _X(_("An error has occurred during the upgrade to version %1"), version)
                                break
                            num_act += 1

        f.close()
    except:
        mens_error = _("Encountered a network problem, cannot access the Internet")

    if mens_error:
        QTUtil2.message_error(main_window, mens_error)
        return False

    if num_act == 0:
        QTUtil2.message_bold(main_window, _("There are no pending updates"))
        return False

    return True


def test_update(current_version, procesador):
    nresp = 0
    try:
        f = urllib.urlopen(WEBUPDATES)
        for x in f:
            act = x.strip()
            if not act.startswith("#"):  # Comentarios
                li = act.split(" ")
                # version urlfichero tama_o
                if len(li) == 3 and li[2].isdigit():
                    version, urlfichero, tam = li
                    current_major = current_version.split(".")[0]
                    version_major = version.split(".")[0]
                    if current_major == version_major:
                        if current_version < version:
                            nresp = QTUtil2.preguntaCancelar123(
                                procesador.main_window,
                                _("Update"),
                                _("Version %s is ready to update") % version,
                                _("Update now"),
                                _("Do not do anything"),
                                _("Don't ask again"),
                            )
                            break
        f.close()
    except:
        pass

    if nresp == 1:
        procesador.actualiza()
    elif nresp == 3:
        procesador.configuration.x_check_for_update = False
        procesador.configuration.graba()
