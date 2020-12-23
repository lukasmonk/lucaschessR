import os
import datetime
import random
import inspect
import pickle
import zlib
import urllib.request
import collections
import glob
import hashlib
import shutil
import time
import psutil

import chardet.universaldetector


def md5_lc(x: str) -> int:
    return int.from_bytes(hashlib.md5(x.encode()).digest(), "big") & 0xFFFFFFFFFFFFFFF


class Log:
    def __init__(self, logname):
        self.logname = logname

    def write(self, buf):
        with open(self.logname, "at") as ferr:
            ferr.write(buf)

    def flush(self):
        pass  # To remove error 120 at exit


def remove_file(file: str) -> bool:
    try:
        os.remove(file)
    except:
        pass
    return not os.path.isfile(file)


def same_path(path1: str, path2: str) -> bool:
    return os.path.realpath(path1) == os.path.realpath(path2)


def create_folder(carpeta: str):
    try:
        os.mkdir(carpeta)
    except:
        pass


def filesize(file: str) -> int:
    return os.path.getsize(file) if os.path.isfile(file) else -1


def exist_file(file: str) -> bool:
    return filesize(file) >= 0


def exist_folder(folder: str) -> bool:
    return os.path.isdir(folder)


def file_copy(origin: str, destino: str) -> bool:
    if exist_file(origin):
        if remove_file(destino):
            shutil.copy2(origin, destino)
            return True
    return False


def file_next(folder: str, base: str, ext: str) -> str:
    n = 1
    path_ = os.path.join(folder, "%s%s.%s" % (base, "%d", ext))
    while exist_file(path_ % n):
        n += 1
    return path_ % n


def rename_file(origin: str, destination: str) -> bool:
    if not exist_file(origin):
        return False
    origin = os.path.abspath(origin)
    destination = os.path.abspath(destination)
    if origin == destination:
        return True
    if origin.lower() == destination.lower():
        os.rename(origin, destination)
        return True
    if remove_file(destination):
        shutil.move(origin, destination)
        return True
    return False


def temporary_file(pathTemp: str, ext: str) -> str:
    create_folder(pathTemp)
    while True:
        fich = os.path.join(pathTemp, "%d.%s" % (random.randint(1, 999999999), ext))
        if not exist_file(fich):
            return fich


def list_vars_values(obj):
    li = []
    for name, value in inspect.getmembers(obj):
        if not ("__" in name):
            if not inspect.ismethod(value):
                li.append((name, value))
    return li


def save_obj_pickle(obj):
    dic = {var: value for var, value in list_vars_values(obj)}
    return pickle.dumps(dic)


def restore_obj_pickle(obj, js_txt):
    dic = pickle.loads(js_txt)
    for k, v in dic.items():
        if hasattr(obj, k):
            setattr(obj, k, v)


def ini_dic(file: str) -> dict:
    dic = {}
    if os.path.isfile(file):
        with open(file, "rt", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if line:
                    n = line.find("=")
                    if n:
                        key = line[:n].strip()
                        value = line[n + 1 :].strip()
                        dic[key] = value
    return dic


def today():
    return datetime.datetime.now()


def new_id() -> int:
    d = datetime.datetime.now()
    r = random.randint
    t = (
        ((((r(1, d.year) * 12 + r(1, d.month)) * 31 + d.day) * 24 + d.hour) * 60 + d.minute) * 60 + d.second
    ) * 1000 + r(1, d.microsecond + 737) // 1000
    return t


def str_id() -> str:
    d = datetime.datetime.now()
    r = random.randint
    t = (
        ((((r(1, d.year) * 12 + r(1, d.month)) * 31 + d.day) * 24 + d.hour) * 60 + d.minute) * 60 + d.second
    ) * 1000 + r(1, d.microsecond + 737) // 1000
    return str(t)


def huella():
    m = hashlib.md5()
    s = str(random.random()) + str(today())
    m.update(s.encode("utf-8"))
    return m.hexdigest()


def save_pickle(fich: str, obj) -> bool:
    with open(fich, "wb") as q:
        q.write(pickle.dumps(obj))
    return True


def restore_pickle(fich: str):
    if exist_file(fich):
        with open(fich, "rb") as f:
            return pickle.loads(f.read())
    else:
        return None


def urlretrieve(url: str, fich: str) -> bool:
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
            if the_page:
                with open(fich, "wb") as q:
                    q.write(the_page)
                    return True
            return False
    except:
        return False


def var2zip(var):
    varp = pickle.dumps(var)
    return zlib.compress(varp, 5)


def zip2var(blob):
    if blob is None:
        return None
    try:
        varp = zlib.decompress(blob)
        return pickle.loads(varp)
    except:
        return None


class Record:
    pass


def var2txt(var):
    return pickle.dumps(var)


def txt2var(txt):
    return pickle.loads(txt)


def dtos(f):
    return "%04d%02d%02d" % (f.year, f.month, f.day)


def stod(txt):
    if txt and len(txt) == 8 and txt.isdigit():
        return datetime.date(int(txt[:4]), int(txt[4:6]), int(txt[6:]))
    return None


def dtosext(f):
    return "%04d%02d%02d%02d%02d%02d" % (f.year, f.month, f.day, f.hour, f.minute, f.second)


def dtostr_hm(f):
    return "%04d.%02d.%02d %02d:%02d" % (f.year, f.month, f.day, f.hour, f.minute)


def stodext(txt):
    if txt and len(txt) == 14 and txt.isdigit():
        return datetime.datetime(
            int(txt[:4]), int(txt[4:6]), int(txt[6:8]), int(txt[8:10]), int(txt[10:12]), int(txt[12:])
        )
    return None


def primera_mayuscula(txt):
    return txt[0].upper() + txt[1:].lower() if len(txt) > 0 else ""


def microsegundos_rnd():
    d = datetime.datetime.now()
    return random.randint(0, 1000) + 1000 * (
        d.microsecond + 1000000 * (d.second + 60 * (d.minute + 60 * (d.hour + 24 * d.toordinal())))
    )


def ini2dic(file):
    dic_base = collections.OrderedDict()

    if os.path.isfile(file):

        with open(file, "rt") as f:
            for linea in f:
                linea = linea.strip()
                if linea and not linea.startswith("#"):
                    if linea.startswith("["):
                        key = linea[1:-1]
                        dic = collections.OrderedDict()
                        dic_base[key] = dic
                    else:
                        n = linea.find("=")
                        if n > 0:
                            clave1 = linea[:n].strip()
                            valor = linea[n + 1 :].strip()
                            dic[clave1] = valor

    return dic_base


def dic2ini(file, dic):
    with open(file, "wt") as f:
        for k in dic:
            f.write("[%s]\n" % k)
            for key in dic[k]:
                f.write("%s=%s\n" % (key, dic[k][key]))


def ini_base2dic(file):
    dic = {}

    if os.path.isfile(file):

        with open(file, "rt", encoding="utf-8", errors="ignore") as f:
            for linea in f:
                linea = linea.strip()
                if linea.startswith("#"):
                    continue
                if linea:
                    n = linea.find("=")
                    if n:
                        key = linea[:n].strip()
                        valor = linea[n + 1 :].strip()
                        dic[key] = valor

    return dic


def secs2str(s):
    m = s / 60
    s = s % 60
    h = m / 60
    m = m % 60
    return "%02d:%02d:%02d" % (h, m, s)


class ListaNumerosImpresion:
    def __init__(self, txt):
        # Formas
        # 1. <num>            1, <num>, 0
        #   2. <num>-           2, <num>, 0
        #   3. <num>-<num>      3, <num>,<num>
        #   4. -<num>           4, <num>, 0
        self.lista = []
        if txt:
            txt = txt.replace("--", "-").replace(",,", ",").replace(" ", "")

            for bloque in txt.split(","):

                if bloque.startswith("-"):
                    num = bloque[1:]
                    if num.isdigit():
                        self.lista.append((4, int(num)))

                elif bloque.endswith("-"):
                    num = bloque[:-1]
                    if num.isdigit():
                        self.lista.append((2, int(num)))

                elif "-" in bloque:
                    li = bloque.split("-")
                    if len(li) == 2:
                        num1, num2 = li
                        if num1.isdigit() and num2.isdigit():
                            i1 = int(num1)
                            i2 = int(num2)
                            if i1 <= i2:
                                self.lista.append((3, i1, i2))

                elif bloque.isdigit():
                    self.lista.append((1, int(bloque)))

    def siEsta(self, pos):
        if not self.lista:
            return True

        for patron in self.lista:
            modo = patron[0]
            i1 = patron[1]
            if modo == 1:
                if pos == i1:
                    return True
            elif modo == 2:
                if pos >= i1:
                    return True
            elif modo == 3:
                i2 = patron[2]
                if i1 <= pos <= i2:
                    return True
            elif modo == 4:
                if pos <= i1:
                    return True

        return False

    def selected(self, lista):
        return [x for x in lista if self.siEsta(x)]


class SymbolDict:
    def __init__(self, dic=None):
        self._dic = {}
        self._keys = []
        if dic:
            for k, v in dic.items():
                self.__setitem__(k, v)

    def __contains__(self, key):
        return key.upper() in self._dic

    def __len__(self):
        return len(self._keys)

    def __getitem__(self, key):
        if type(key) == int:
            return self._keys[key]
        return self._dic[key.upper()]

    def __setitem__(self, key, valor):
        clu = key.upper()
        if not (clu in self._dic):
            self._keys.append(key)
        self._dic[clu] = valor

    def get(self, key, default=None):
        clu = key.upper()
        if not (clu in self._dic):
            return default
        return self.__getitem__(key)

    def items(self):
        for k in self._keys:
            yield k, self.__getitem__(k)

    def keys(self):
        return self._keys[:]

    def __str__(self):
        x = ""
        for t in self._keys:
            x += "[%s]=[%s]\n" % (t, str(self.__getitem__(t)))
        return x.strip()


class Rondo:
    def __init__(self, *lista):
        self.pos = -1
        self.lista = lista
        self.tope = len(self.lista)

    def shuffle(self):
        li = list(self.lista)
        random.shuffle(li)
        self.lista = li

    def otro(self):
        self.pos += 1
        if self.pos == self.tope:
            self.pos = 0
        return self.lista[self.pos]

    def reset(self):
        self.pos = -1


def valid_filename(name):
    name = name.strip()
    nom = []
    for x in name:
        if x in '\\:/|?*^%><(),;"' or ord(x) < 32:
            x = "_"
        nom.append(x)
    name = "".join(nom)
    li_invalid = [
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    ]
    if name.upper() in li_invalid:
        name = "__%s__" % name
    if "." in name:
        if name[: name.find(".")].upper() in li_invalid:
            name = "__%s__" % name
    return name


def asciiNomFichero(name):
    name = valid_filename(name)
    li = []
    for x in name:
        if not (31 < ord(x) < 127):
            li.append("_")
        else:
            li.append(x)
    name = "".join(li)
    while "__" in name:
        name = name.replace("__", "_")
    return name


def datefile(pathfile):
    try:
        mtime = os.path.getmtime(pathfile)
        return datetime.datetime.fromtimestamp(mtime)
    except:
        return None


class Timer:
    def __init__(self, tiempoPendiente):
        self.tiempoPendiente = tiempoPendiente
        self.marcaTiempo = None
        self.txt = ""
        self.marcaZeitnot = 0

    def texto(self, segs):
        if segs <= 0.0:
            segs = 0.0
        tp = int(segs)
        txt = "%02d:%02d" % (int(tp / 60), tp % 60)
        return txt

    def ponSegExtra(self, segs):
        self.tiempoPendiente += segs

    def dameSegundos(self):
        if self.marcaTiempo:
            tp = self.tiempoPendiente - (time.time() - self.marcaTiempo)
        else:
            tp = self.tiempoPendiente
        if tp <= 0.0:
            tp = 0
        return int(tp)

    def dameSegundos2(self):
        if self.marcaTiempo:
            tp2 = int(time.time() - self.marcaTiempo)
            tp = int(self.tiempoPendiente) - tp2
        else:
            tp = self.tiempoPendiente
            tp2 = 0
        if tp <= 0.0:
            tp = 0
        return int(tp), tp2

    def etiqueta(self):
        return self.texto(self.dameSegundos())

    def etiqueta2(self):
        tp, tp2 = self.dameSegundos2()
        return self.texto(tp), self.texto(tp2)

    def etiquetaDif(self):
        nvEti = self.etiqueta()
        if nvEti != self.txt:
            self.txt = nvEti
            return nvEti

        return None

    def etiquetaDif2(self):
        nvEti, nvEti2 = self.etiqueta2()
        if nvEti != self.txt:
            self.txt = nvEti
            return nvEti, nvEti2

        return None, None

    def etiquetaDGT(self):
        segs = self.dameSegundos()
        mins = segs / 60
        segs -= mins * 60
        hors = mins / 60
        mins -= hors * 60

        return "%d:%02d:%02d" % (hors, mins, segs)

    def siAgotado(self):
        if self.marcaTiempo:
            if (self.tiempoPendiente - (time.time() - self.marcaTiempo)) <= 0.0:
                return True
        else:
            return self.tiempoPendiente <= 0.0
        return False

    def isZeitnot(self):
        if self.marcaZeitnot:
            if self.marcaTiempo:
                t = self.tiempoPendiente - (time.time() - self.marcaTiempo)
            else:
                t = self.tiempoPendiente
            if t > 0:
                resp = t < self.marcaZeitnot
                if resp:
                    self.marcaZeitnot = None
                return resp
        return False

    def setZeitnot(self, segs):
        self.marcaZeitnot = segs

    def iniciaMarcador(self):
        self.marcaTiempo = time.time()

    def paraMarcador(self, tiempoJugada):
        if self.marcaTiempo:
            self.tiempoPendiente -= (time.time() - self.marcaTiempo) - tiempoJugada
            self.marcaTiempo = None

    def anulaMarcador(self):
        self.marcaTiempo = None

    def tiempoAplazamiento(self):
        self.paraMarcador(0.00)
        return self.tiempoPendiente

    def save(self):
        return (self.tiempoPendiente, self.marcaZeitnot)

    def restore(self, tvar):
        self.tiempoPendiente, self.marcaZeitnot = tvar
        self.marcaTiempo = None
        self.txt = ""


def fideELO(eloJugador, eloRival, resultado):
    if resultado == +1:
        resultado = 1.0
    elif resultado == 0:
        resultado = 0.5
    else:
        resultado = 0.0
    if eloJugador <= 1200:
        k = 40.0
    elif eloJugador <= 2100:
        k = 32.0
    elif eloRival < 2400:
        k = 24.0
    else:
        k = 16.0
    probabilidad = 1.0 / (1.0 + (10.0 ** ((eloRival - eloJugador) / 400.0)))
    return int(k * (resultado - probabilidad))


date_format = ["%Y.%m.%d"]


def localDate(date):
    return date.strftime(date_format[0])


def localDateT(date):
    return "%s %02d:%02d" % (date.strftime(date_format[0]), date.hour, date.minute)


def listfiles(*lista):
    f = lista[0]
    if len(lista) > 1:
        for x in lista[1:]:
            f = os.path.join(f, x)
    return glob.glob(f)


def listdir(txt):
    return os.scandir(txt)


class Timekeeper:
    def __init__(self):
        self._begin = None

    def start(self):
        self._begin = time.time()

    def stop(self):
        if self._begin:
            b = self._begin
            self._begin = None
            return time.time() - b
        else:
            return 0

    def stop_ms(self):
        if self._begin:
            b = self._begin
            self._begin = None
            return int(1000 * (time.time() - b))


class OpenCodec:
    def __init__(self, path, modo=None):
        with open(path, "rb") as f:
            u = chardet.universaldetector.UniversalDetector()
            u.feed(f.read(1024))
            u.close()
            encoding = u.result.get("encoding", "utf-8")
        if modo is None:
            modo = "rt"
        self.f = open(path, modo, encoding=encoding, errors="ignore")

    def __enter__(self):
        return self.f

    def __exit__(self, xtype, value, traceback):
        self.f.close()


def txt_encoding(txt):
    u = chardet.universaldetector.UniversalDetector()
    u.feed(txt)
    u.close()
    return u.result.get("encoding", "utf-8")


def bytes_str_codec(btxt):
    u = chardet.universaldetector.UniversalDetector()
    u.feed(btxt)
    u.close()
    codec = u.result.get("encoding", "utf-8")
    return btxt.decode(codec), codec


def file_encoding(fich, chunk=30000):
    with open(fich, "rb") as f:
        u = chardet.universaldetector.UniversalDetector()
        u.feed(f.read(chunk))
        u.close()
        codec = u.result.get("encoding", "latin-1")
        if codec == "ascii":
            codec = "latin-1"
        return codec


class Decode:
    def __init__(self, codec=None):
        self.codec = "utf-8" if codec is None else codec

    def read_file(self, file):
        self.codec = file_encoding(file)

    def decode(self, xbytes):
        try:
            resp = xbytes.decode(self.codec)
        except:
            u = chardet.universaldetector.UniversalDetector()
            u.feed(xbytes)
            u.close()
            codec = u.result.get("encoding", "latin-1")
            resp = xbytes.decode(codec, "ignore")
        return resp


def path_split(path):
    path = os.path.realpath(path)
    return path.split(os.sep)


def relative_path(*args):
    n_args = len(args)
    if n_args == 1:
        path = args[0]
    else:
        path = os.path.join(args[0], args[1])
        if n_args > 2:
            for x in range(2, n_args):
                path = os.path.join(path, args[x])
    try:
        path = os.path.abspath(path)
        rel = os.path.relpath(path)
        if not rel.startswith(".."):
            path = rel
    except ValueError:
        pass

    return path


def memory_python():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def unique_list(lista):
    st = set()
    li = []
    for x in lista:
        if x not in st:
            li.append(x)
            st.add(x)
    return li


def div_list(list, max_group):
    nlist = len(list)
    xfrom = 0
    li_groups = []
    while xfrom < nlist:
        li_groups.append(list[xfrom:xfrom+max_group])
        xfrom += max_group
    return li_groups
