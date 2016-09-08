#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

#Определение домашней папки пользователя
HOMEFOLDER = os.getenv('HOME')

#Директория в домашней папке пользователя для хранения настроек и подключений
WORKFOLDER = HOMEFOLDER + '/.connector/'

#Установки по умолчанию для параметров программы (какие приложения использовать)
DEFAULT = dict(RDP = 1, VNC = 0, TAB = '0', KIOSK = '0') 

#Версия приложения
VERSION = "1.4.0_beta"

#Исходные данные для ярлыка подключения
DESKTOP_INFO = """#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Icon=/usr/share/connector/data/emblem.png
"""

#Режим киоска
KIOSK_MARCO = """marco &
while true
do
connector
done
"""

KIOSK_OPENBOX = """openbox &
while true
do
connector
done
"""

KIOSK_X = """#!/usr/bin/env xdg-open
[Desktop Entry]
Version=1.0
Type=Application
Terminal=false
Icon[ru_RU]=start
Name[ru_RU]=Ctor_kiosk
Exec=startx
Name=Ctor_kiosk
Icon=start
"""


#Запускаемый файл приложения
EXEC = "/usr/bin/connector "
