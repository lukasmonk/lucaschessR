import builtins
import gettext
import os
import locale

import Code


def _F(txt):
    return _(txt) if txt else ""


def _SP(key):
    if not key:
        return ""
    key = key.strip()
    t = _F(key)
    if t == key:
        li = []
        for x in key.split(" "):
            if x:
                li.append(_F(x))
        return " ".join(li)
    else:
        return t


def _X(key, op1, op2=None, op3=None):
    if not key:
        return ""
    resp = key.replace("%1", op1)
    if op2:
        resp = resp.replace("%2", op2)
        if op3:
            resp = resp.replace("%3", op3)
    return resp


DOMAIN = "lucaschess"
DIR_LOCALE = Code.path_resource("Locale")


def install(lang=None):
    if not lang:
        lang = "en"
        li_info = locale.getdefaultlocale()
        if len(li_info) == 2:
            if li_info[0]:
                lang = li_info[0][:2]
    if lang and os.path.isfile("%s/%s/LC_MESSAGES/%s.mo" % (DIR_LOCALE, lang, DOMAIN)):
        t = gettext.translation(DOMAIN, DIR_LOCALE, languages=[lang])
        t.install(lang)
    else:
        gettext.install(DOMAIN, DIR_LOCALE)

    builtins.__dict__["_X"] = _X
    builtins.__dict__["_F"] = _F
    builtins.__dict__["_SP"] = _SP

    Code.lucas_chess = "%s %s" % (_("Lucas Chess"), Code.VERSION)

