Lucas Chess on Ubuntu
======================

Author: Michaël George

Tested on Linux Mint 19.1 with Lucas Chess (R) 1.16.


1. Download the [latest version](https://github.com/lukasmonk/lucaschessR/) from GitHub.
----------------------------------------------------------------------------------------
Extract the content of the archive to your home folder (for instance).


2. Update your system
---------------------
```bash
    sudo apt-get update  
    sudo apt-get upgrade
```

3. Fulfill dependencies
-----------------------

Current requirements are:

* Python 3.7
* PySide2
* PyAudio
* psutil
* Python for windows extensions
* chardet
* python-chess
* pyllow
* photohash
* cython
* sortedcontainers

So our task is to install them:
```bash
    sudo add-apt-repository universe  
    sudo apt-get install python3.7  
    sudo apt-get install python3-pip  
    sudo apt-get install python3-dev  
    sudo apt-get install python3-pyqt5  
    sudo apt-get install python3-pyaudio  
```
```bash
    sudo pip3 install pyside2  
    sudo pip3 install psutil  
    sudo pip3 install chardet  
    sudo pip3 install python-chess  
    sudo pip3 install Pillow  
    sudo pip3 install PhotoHash  
    sudo pip3 install Cython  
    sudo pip3 install sortedcontainers  
    sudo pip3 install scandir  
    sudo pip3 install pygal
```

4. Compile FasterCode
---------------------

### 4.1 Get your Python version:
```bash
    python3 -V
```

    You should get something like:
```bash
    Python 3.6.9
```

### 4.2 Modify linux64.sh
If you have uncompressed the archive in your home folder:
```bash
    cd ~/lucaschessR-R1.16/bin/_fastercode/
```

Change the last line of linux64.sh to reflect your Python version:
```bash
    cp ./FasterCode.cpython-38-x86_64-linux-gnu.so ../../OS/linux
```
to
```bash
    cp ./FasterCode.cpython-36m-x86_64-linux-gnu.so ../../OS/linux
```

**Remark:** A quick look under `~/lucaschessR-R1.16/bin/bin/_fastercode/source/`, can help you to determine the right `.so` file name if necessary.

### 4.3 Launch it
```bash
    chmod +x linux64.sh
    ./linux64.sh
```

5. Run Lucas Chess (R)
----------------------

```bash
    python3 LucasR.py
```

6. Troubleshooting
------------------

If the following does not work. Do not hesitate to open an [issue](https://github.com/lukasmonk/lucaschessR/issues). The developer seems to be a cool guy.

As a last resort, you can use the Windows version via either:

* Wine or
* VirtualBox.






