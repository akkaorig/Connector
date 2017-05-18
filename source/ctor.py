#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, properties, subprocess
from GLOBAL import *

def f_write(f_name, cfg):
    """Создание файла с конфигурацией для remmina"""
    f = open(WORKFOLDER+f_name,"w")
    f.write("[remmina]\n")
    for key in cfg.keys():
        print(key,cfg[key], sep='=',file=f)
    f.close()

class Remmina:
    """Класс, обеспечивающий подключение через remmina"""
    cfg = {}
    f_name = ".tmp.remmina"
    def create_cfg_file(self, args):
        """Создание файла конфигурации для соединения"""
        if type(args) == list:
            protocol = self.cfg['protocol']
            server, login = properties.searchSshUser(args[0])
            self.cfg['server'] = server
            self.cfg['name'] += server
            if protocol == 'RDP':
                #[user, domain, color, quality, resolution, viewmode, folder, printer, clipboard, sound]
                self.cfg['username'] = args[1]                              
                self.cfg['domain'] = args[2]
                self.cfg['colordepth'] = args[3]
                self.cfg['quality'] = args[4]
                self.cfg['resolution'] = args[5]
                self.cfg['viewmode'] = args[6]
                self.cfg['sharefolder'] = args[7]
                self.cfg['shareprinter'] = args[8]
                self.cfg['disableclipboard'] = args[9]
                self.cfg['sound'] = args[10]
                self.cfg['sharesmartcard'] = args[11]                                
            if protocol == 'NX':
                #[user, quality, resolution, viewmode, keyfile, crypt, clipboard, _exec]
                self.cfg['username'] = args[1]
                self.cfg['quality'] = args[2]
                self.cfg['resolution'] = args[3]
                self.cfg['viewmode'] = args[4]
                self.cfg['nx_privatekey'] = args[5]
                self.cfg['disableencryption'] = args[6]
                self.cfg['disableclipboard'] = args[7]
                self.cfg['exec'] = args[8] 
            if protocol == 'VNC': 
                #[user, quality, color, viewmode, viewonly, crypt, clipboard, showcursor]
                self.cfg['username'] = args[1]
                self.cfg['quality'] = args[2]
                self.cfg['colordepth'] = args[3]
                self.cfg['viewmode'] = args[4]
                self.cfg['viewonly'] = args[5]
                self.cfg['disableencryption'] = args[6]
                self.cfg['disableclipboard'] = args[7]
                self.cfg['showcursor'] = args[8] 
            if protocol == 'XDMCP':
                #[color, viewmode, resolution, once, showcursor, _exec]
                self.cfg['colordepth'] = args[1]
                self.cfg['viewmode'] = args[2]
                self.cfg['resolution'] = args[3]
                self.cfg['once'] = args[4]
                self.cfg['showcursor'] = args[5]
                self.cfg['exec'] = args[6]
            if protocol == 'SSH':
                #[user, SSH_auth, keyfile, charset, _exec] 
                if login: self.cfg['ssh_username'] = login
                else: self.cfg['ssh_username'] = args[1]
                self.cfg['ssh_auth'] = args[2]
                self.cfg['ssh_privatekey'] = args[3]
                self.cfg['ssh_charset'] = args[4]
                self.cfg['exec'] = args[5]
            if protocol == 'SFTP':
                #[user, SSH_auth, keyfile, charset, execpath]
                if login: self.cfg['ssh_username'] = login
                else: self.cfg['ssh_username'] = args[1]
                self.cfg['ssh_auth'] = args[2]
                self.cfg['ssh_privatekey'] = args[3]
                self.cfg['ssh_charset'] = args[4]
                self.cfg['execpath'] = args[5]
        else:
            server, login = properties.searchSshUser(args)
            if login: self.cfg['ssh_username'] = login
            self.cfg['server'] = server
            self.cfg['name'] += server
        f_write(self.f_name, self.cfg)        

    def start(self, parameters):
        """Запуск remmina с необходимыми параметрами"""
        self.create_cfg_file(parameters)
        properties.log.info ("Remmina: подключение по протоколу %s к серверу: %s", self.cfg['protocol'], self.cfg['server'])
        os.system('cd $HOME && remmina -c "' + WORKFOLDER + self.f_name + '"' + STD_TO_LOG)

class VncRemmina(Remmina):
    """Класс для настройки VNC-соединения через Remmina"""
    def __init__(self):
        self.cfg = dict(keymap='', quality=9, disableencryption=0, colordepth=24, 
                       hscale=0, group='', password='', name='VNC-connection: ', viewonly=0, 
                       disableclipboard=0, protocol='VNC', vscale=0, username='', 
                       showcursor=0, disableserverinput=0, server='',aspectscale=0,
                       window_maximize=1, window_width=800, window_height=600, viewmode=1)
        self.f_name = '.tmp_VNC.remmina' 

class VncViewer:
    """Класс для настройки VNC-соединения через VncViewer"""
    def start(self, args):
        if type(args) == str:
            properties.log.info ("RealVNC: подключение к серверу %s", args)
            os.system('vncviewer ' + args + STD_TO_LOG)
        else:
            command = 'vncviewer ' + args[0] + ' '
            if args[1]: command += args[1]
            if args[2]: command += args[2]
            command += STD_TO_LOG
            properties.log.info ("RealVNC: подключение к серверу %s", args[0])
            os.system(command)

class RdpRemmina(Remmina):
    """Класс для настройки RDP-соединения через Remmina"""
    def __init__(self):
        self.cfg = dict(disableclipboard=0, clientname='', quality=0, console=0, sharesmartcard=0, 
                       resolution='', group='', password='', name='RDP-connection: ',
                       shareprinter=0, security='', protocol='RDP', execpath='', 
                       sound='off', username='', sharefolder='', domain='', viewmode=3,
                       server='', colordepth=32, window_maximize=1, window_width=800, window_height=600)
        self.cfg['exec'] = ''
        self.f_name = '.tmp_RDP.remmina'

class XFreeRdp:
    """Класс для настройки RDP-соединения через xfreerdp"""
    def start(self, args):
        params = ' +auto-reconnect /cert-ignore'
        if type(args) == str:
            properties.log.info ("FreeRDP: подключение к серверу %s", args)
            os.system('xfreerdp /f -sec-nla /v:' + args + params + STD_TO_LOG)
        else:
            command = 'xfreerdp /v:' + args[0]
            if args[1]: command += ' /u:' + args[1]
            if args[2]: command += ' /d:' + args[2]
            if args[3]: command += ' /f'
            if args[4]: command += ' +clipboard'
            if args[5]: command += ' /size:' + args[5]
            if args[6]: command += ' /bpp:' + args[6]
            if args[7]: command += ' /drive:LocalFolder,"' + args[7] + '"'
            if args[8]: command += ' /g:' + args[8]
            if args[9]: command += ' /gu:' + args[9]
            if args[10]: command += ' /gd:' + args[10]
            if args[11]:
                command = "GATEPWD='" + args[11] + "' && " + command 
                command += ' /gp:$GATEPWD'
            if args[12]: command += ' /admin'
            if args[13]: command += ' /smartcard'
            if args[14]: command += ' /printer'
            if args[15]: command += ' /sound:sys:alsa'
            if args[16]: command += ' /microphone:sys:alsa'
            if args[17]: command += ' /multimon'
            if args[18]: command += ' +compression'
            if args[19]: command += ' /compression-level:' + args[19]
            if args[20]: command += ' +fonts'
            if args[21]: command += ' +aero'
            if args[22]: command += ' +window-drag'
            if args[23]: command += ' +menu-anims'    
            if args[24]: command += ' -themes'
            if args[25]: command += ' -wallpaper'
            if args[26]: command += ' /nsc'
            if args[27]: command += ' /jpeg'
            if args[28]: command += ' /jpeg-quality:' + str(args[28])
            if args[29]: command += ' /drive:MEDIA,' + USBPATH
            if args[30]: command += ' /p:$(zenity --entry --title="Аутентификация (with NLA)" --text="Введите пароль для пользователя '+ args[1] + ':" --hide-text)'
            else: command += ' -sec-nla'
            if args[31]: command += ' /workarea'
            try: #Добавлена совместимость с предыдущей версией; < 1.4.0
                if args[32]: command += ' /span'
            except IndexError: pass
            try: #Добавлена совместимость с предыдущей версией; < 1.4.1
                if args[33]: command += ' /drive:Desktop,' + DESKFOLDER
                if args[34]: command += ' /drive:Downloads,' + DOWNFOLDER
                if args[35]: command += ' /drive:Documents,' + DOCSFOLDER
            except IndexError: pass
            command += params + STD_TO_LOG
            properties.log.info ("FreeRDP: подключение к серверу %s", args[0])
            os.system(command)

class NxRemmina(Remmina):
    """Класс для настройки NX-соединения через Remmina"""
    def __init__(self):
        self.cfg = dict(name='NX-connection: ', protocol='NX', quality=0, disableencryption=0,
                        resolution='',group='',password='',username='',NX_privatekey='',
                        showcursor=0, server='', disableclipboard=0, window_maximize=1,
                        window_width=800, window_height=600, viewmode=4)
        self.cfg['exec'] = ''
        self.f_name = '.tmp_NX.remmina'

class XdmcpRemmina(Remmina):
    """Класс для настройки XDMCP-соединения через Remmina"""
    def __init__(self):
        self.cfg = dict(resolution='', group='', password='', name='XDMCP-connection: ',
                        protocol='XDMCP', once=0, showcursor=0, server='',colordepth=0,
                        window_maximize=1, viewmode=1, window_width=800, window_height=600)
        self.cfg['exec'] = ''
        self.f_name = '.tmp_XDMCP.remmina'

class SftpRemmina(Remmina):
    """Класс для настройки SFTP-соединения через Remmina"""
    def __init__(self):
        self.cfg = dict(name='SFTP-connection: ', protocol='SFTP', ssh_enabled=1, ssh_auth=0, 
                        ssh_charset='UTF-8', ssh_privatekey='', username='', ssh_username='',
                        group='', password='', execpath='/', server='', window_maximize=0, 
                        window_height=600, window_width=800, ftp_vpanedpos=360, viewmode=0)
        self.f_name = '.tmp_SFTP.remmina'

class SshRemmina(Remmina):
    """Класс для настройки SSH-соединения через Remmina"""
    def __init__(self):
        self.cfg = dict(name='SSH-connection: ', protocol='SSH', ssh_auth=0, ssh_charset='UTF-8', 
                        ssh_privatekey='', group='', password='', username='', ssh_username='', ssh_enabled=1,
                        server='', window_maximize=0, window_width=500, window_height=500, viewmode=0)
        self.cfg['exec'] = ''
        self.f_name = '.tmp_SSH.remmina'

class Vmware:
    """Класс для настройки соединения к VMWare серверу"""
    def start(self, args):
        if vmwareCheck():
            if type(args) == str:
                properties.log.info ("VMware: подключение к серверу %s", args)
                os.system('vmware-view -q -s ' + args + STD_TO_LOG)
            else:
                command = 'vmware-view -q -s ' + args[0]
                if args[1]: command += ' -u ' + args[1]
                if args[2]: command += ' -d ' + args[2]
                if args[3]: command += ' -p ' + args[3]
                if args[4]: command += ' --fullscreen'
                command += STD_TO_LOG
                properties.log.info ("VMware: подключение к серверу %s", args[0])
                os.system(command)
        else:
            properties.log.warning ("VMware Horizon Client не установлен!")
            os.system("zenity --error --text='VMware Horizon Client не установлен!'")

class Citrix:
    """Класс для настройки ICA-соединения к Citrix-серверу"""
    def start(self, args):
        if type(args) == list:
            addr = args[0]
        else: addr = args
        if citrixCheck():
            properties.log.info ("Citrix: подключение к серверу %s", addr)
            os.system('/opt/Citrix/ICAClient/util/storebrowse --addstore ' + addr + STD_TO_LOG)
            os.system('/opt/Citrix/ICAClient/selfservice --icaroot /opt/Citrix/ICAClient' + STD_TO_LOG)
        else:
            properties.log.warning ("Citrix Receiver не установлен!")
            os.system("zenity --error --text='Citrix Receiver не установлен!'")

    def preferences():
        if citrixCheck():
            properties.log.info ("Citrix: открытие настроек программы")
            os.system('/opt/Citrix/ICAClient/util/configmgr --icaroot /opt/Citrix/ICAClient' + STD_TO_LOG)
        else:
            properties.log.warning ("Citrix Receiver не установлен!")
            os.system("zenity --error --text='Citrix Receiver не установлен!'")

class Web:
    """Класс для настройки подключения к WEB-ресурсу"""
    def start(self, args):
        if type(args) == list:
            addr = args[0]
        else: addr = args
        if  not addr.find("://") != -1:
            addr = "http://" + addr
        properties.log.info ("WWW: открытие web-ресурса %s", addr)
        os.system ('python3 -m webbrowser -t "' + addr + '"' + STD_TO_LOG)

def definition(protocol):
    """Функция определения протокола"""
    whatProgram = properties.loadFromFile('default.conf') #загрузка параметров с выбором программ для подключения
    if protocol == 'VNC':
        if whatProgram['VNC'] == 0:
            connect = VncRemmina()
        else: connect = VncViewer()
    elif protocol == 'RDP':
        if whatProgram['RDP'] == 0:
            connect = RdpRemmina()
        else: connect = XFreeRdp()
    elif protocol == 'NX':
        connect = NxRemmina()
    elif protocol == 'XDMCP':
        connect = XdmcpRemmina()
    elif protocol == 'SSH':
        connect = SshRemmina()
    elif protocol == 'SFTP':
        connect = SftpRemmina()
    elif protocol == 'VMWARE':
        connect = Vmware()
    elif protocol == 'CITRIX':
        connect = Citrix()
    elif protocol == 'WEB':
        connect = Web()
    return connect

def citrixCheck():
    """Фунцкия проверки наличия в системе Citrix Receiver"""
    check = int(subprocess.check_output("dpkg -s icaclient > /dev/null 2>&1; echo $?", shell=True, universal_newlines=True).strip())
    check = not bool(check)
    return check

def vmwareCheck():
    """Фунцкия проверки наличия в системе VMware Horizon Client"""
    check = int(subprocess.check_output("which vmware-view > /dev/null 2>&1; echo $?", shell=True, universal_newlines=True).strip())
    check = not bool(check)
    return check

if __name__ == "__main__":
    pass
