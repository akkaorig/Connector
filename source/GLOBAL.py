#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

#Определение домашней папки пользователя
HOMEFOLDER = os.getenv('HOME')

#Директория в домашней папке пользователя для хранения настроек и подключений
WORKFOLDER = HOMEFOLDER + '/.connector/'

#Установки по умолчанию для параметров программы (какие приложения использовать)
DEFAULT = dict(RDP = 1, VNC = 1, TAB = '0')

#Версия и релиз приложения
VERSION = "1.4.1"
RELEASE = "1"

#Исходные данные для ярлыка подключения
DESKTOP_INFO ="""#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Icon=/usr/share/connector/data/emblem.png
"""

#Запускаемый файл приложения
EXEC = "/usr/bin/connector "

#Папка монтирования устройств
USBPATH = "/media/$USER"

#Ведение логов
LOGFOLDER = WORKFOLDER + "logs/"
LOGFILE = LOGFOLDER + "connector.log"
STDLOGFILE = LOGFOLDER + "all.log"
STD_TO_LOG = ' >> ' + STDLOGFILE + " 2>&1 &"

#Определение путей до папок пользователя
dirs = {}
try:
    for string in open(HOMEFOLDER + "/.config/user-dirs.dirs"):
        if string[0] != "#":
            name, value = string.strip().split('=')
            dirs[name] = value
    DESKFOLDER = dirs["XDG_DESKTOP_DIR"]
    DOWNFOLDER = dirs["XDG_DOWNLOAD_DIR"]
    DOCSFOLDER = dirs["XDG_DOCUMENTS_DIR"]
except FileNotFoundError:
    DESKFOLDER = HOMEFOLDER + "Desktop"
    DOWNFOLDER = HOMEFOLDER + "Downloads"
    DOCSFOLDER = HOMEFOLDER + "Documents"
