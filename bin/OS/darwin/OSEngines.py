import logging
import os
import platform
import sys
import yaml

# assume it is darwin, just need to figure out if x86 or ARM
isARM = False
useCpuUtil = False
machineStr = platform.machine()

if machineStr == 'x86_64':
# detect for x86
    import CpuUtil
    useCpuUtil = True
elif machineStr == 'arm64':
# detect for ARM
    isARM = True

from Code.Engines import Engines

def read_config(config_yaml):
    configs = []
    try:
        with open(config_yaml, 'r') as file:
            for c in yaml.safe_load_all(file):
              configs.append(c)
        file.close
    except FileNotFoundError:
        logging.debug('File not found, it is okay!')
        pass
    except:
        logging.error('Exception: ', sys.exc_info()[0], ' occured')
        pass
    return configs

# trying to avoid rereading config files
engines = {}
def read_engines(folder_engines):
    global engines
    dic_engines = {}
    def mas(clave, autor, version, url, path_exe, elo):
        #path_exe = os.path.join(folder_engines, clave, exe)
        engine = Engines.Engine(clave, autor, version, url, path_exe)
        engine.elo = elo
        engine.ordenUCI("Log", "false")
        engine.ordenUCI("Ponder", "false")
        engine.ordenUCI("Hash", "16")
        engine.ordenUCI("Threads", "1")
        dic_engines[clave] = engine
        return engine

    bmi2 = ""
    if useCpuUtil:
        bmi2 = "-bmi2" if CpuUtil.bmi2() else ""

# return cached engines to avoid rereading config files
    if len(engines) > 0:
        return engines

    with os.scandir(folder_engines) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_dir():
                logging.debug(entry.name)
                configs = read_config(folder_engines +'/' +entry.name +'/engine.yaml')
                for c in configs:
                  logging.debug(c)
                  eid = c.get('eid', '')
                  if eid.startswith(entry.name):
                      # checks, validator would be convenient
                      author = c.get('author', '')
                      version = c.get('version', '')
                      url = c.get('url', '')
                      # decide on which bin to run
                      l_bin = ''
                      bins = c.get('bin')
                      if bins is not None:
                          if isARM:
                              l_bin = bins.get('arm64', '')
                              # skip out early when no bin for arm64
                              if len(l_bin) < 1:
                                  continue
                          else:
                              l_bin = bins.get('x86_64', '')
                              if useCpuUtil:
                                  t_bin = bins.get('x86_64-bmi2', '')
                                  if len(t_bin) > 0:
                                      l_bin = t_bin
                                      version = f"{version}{bmi2}"
                      else:
                          log.warn('missing configuration, bin')
                          continue
                      elo = c.get('elo')
                      if len(eid) > 0 and len(author) > 0 and len(version) > 0 and len(url) > 0 and len(l_bin) > 0 and elo is not None:
                          path_exe = os.path.join(folder_engines, entry.name, l_bin)
                          cm = mas(eid, author, version, url, path_exe, elo)
                          uci = c.get('UCI')
                          if uci is not None:
                              for k, v in uci.items():
                                  cm.ordenUCI(k, v)
                          pv = c.get('PV')
                          if pv is not None:
                              num = pv.get('num')
                              maximo = pv.get('maximo')
                              if num is not None and maximo is not None:
                                  cm.ponMultiPV(num, maximo)
    engines = dic_engines
    return dic_engines

def dict_engines_fixed_elo(folder_engines):
    d = read_engines(folder_engines)
    dic = {}
# read config file
    configs = read_config(folder_engines +'/engine-fixed-elo.yaml')
    for nm, xfrom, xto in configs:
        logging.debug(nm)
        engine = d.get(nm)
# check that engine exist
        if engine is not None:
            logging.debug('Found: ' +nm)
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
