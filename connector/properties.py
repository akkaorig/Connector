#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Модуль управления параметрами Коннектора"""
import pickle, gui
from gi.repository import Gtk
from GLOBAL import *

def loadFromFile(fileName, window = None):
    """Загрузка сохраненных параметров из файла"""
    try: 
        dbfile = open(WORKFOLDER + fileName, 'rb')
        obj = pickle.load(dbfile)
        dbfile.close()
        return obj
    except FileNotFoundError:
        if fileName.find('default.conf') != -1: #если загружаем параметры программы
            #при неудаче - создает файл со значениями по умолчанию
            saveInFile(fileName, DEFAULT)
            return DEFAULT
        else: #если загружаем параметры одного из сохраненных подключений
            dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                    "Файл " + fileName + "\nc сохраненными настройками не найден")
            response = dialog.run()
            dialog.destroy()
            return None
    except pickle.UnpicklingError:
        dialog = Gtk.MessageDialog(window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK,
                 "Файл " + fileName + "\nимеет неверный формат")
        response = dialog.run()
        dialog.destroy()
        return None

def importFromFile(fileName):
    """Импорт параметров из файла .ctor"""
    dbfile = open(fileName, 'rb')
    obj = pickle.load(dbfile)
    dbfile.close()
    return obj	        

def saveInFile(fileName, obj):
    """Запись параметров в файл:
    saveInFile(<имя файла>, <имя объекта для записи>)"""
    dbfile = open(WORKFOLDER+fileName, 'wb')
    pickle.dump(obj, dbfile)
    dbfile.close()

def searchSshUser(query):
    """Определение имени пользователя и сервера 
    в формате адреса SSH и SFTP - логин@адрес"""
    try:
        login, server = query.strip().split('@')
    except ValueError:
        login = ''
        server = query
    return server, login

class Properties(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "Параметры программы")
        builder = Gtk.Builder()        
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_resizable(False)
        self.set_modal(True)
        self.set_default_icon_name("gtk-preferences")
        builder.add_from_file("data/properties.glade")
        builder.connect_signals(self)
        box = builder.get_object("box_properties")
        cancel = builder.get_object("button_cancel")
        self.changeRdpRem = builder.get_object("radio_RDP_remmina")
        self.changeVncRem = builder.get_object("radio_VNC_remmina")
        self.statusbar = builder.get_object("statusbar")
        self.check_kiosk = builder.get_object("check_kiosk")
        self.combo_tabs = builder.get_object("combo_tabs")
        changeRdpFree = builder.get_object("radio_RDP_freeRDP")
        changeVncView = builder.get_object("radio_VNC_viewer")
        self.defaultConf = loadFromFile('default.conf')
        if self.defaultConf['RDP']:
            changeRdpFree.set_active(True)
        if self.defaultConf['VNC']:
            changeVncView.set_active(True)
        if self.defaultConf['KIOSK']:
            self.check_kiosk.set_active(True)
        try: self.combo_tabs.set_active_id(self.defaultConf['TAB'])
        except KeyError: self.combo_tabs.set_active_id('0')
        self.add(box)        
        self.connect("delete-event", self.onClose)
        cancel.connect("clicked", self.onCancel, self)
        self.show_all()

    def onCancel (self, button, window):
        window.destroy()

    def onClose (self, window, *args):
        window.destroy()
    
    def onSave (self, *args):
        """Сохранение настроек программ по умолчанию"""
        if self.changeRdpRem.get_active():
            self.defaultConf['RDP'] = 0
        else: self.defaultConf['RDP'] = 1
        if self.changeVncRem.get_active():
            self.defaultConf['VNC'] = 0
        else: self.defaultConf['VNC'] = 1
        if self.check_kiosk.get_active():
            self.enableKiosk()
        else: 
            self.defaultConf['KIOSK'] = 0
            self.disableKiosk()
        self.defaultConf['TAB'] = self.combo_tabs.get_active_id()
        saveInFile('default.conf',self.defaultConf)
        gui.viewStatus(self.statusbar, "Настройки сохранены в файле default.conf...")

    def clearFile (self, filename, title, message):
        """Функция для очисти БД серверов или списка подключений"""
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK_CANCEL, title)
        dialog.format_secondary_text(message)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            f = open(WORKFOLDER + filename,"w")
            f.close()
            gui.viewStatus(self.statusbar, "Выполнено, изменения вступят в силу после перезапуска...")
        dialog.destroy()    

    def onClearServers (self, widget):
        self.clearFile("servers.db", "Подтвердите очистку БД",
                      "Вы потеряете всю историю посещений!!!")

    def onClearConnects (self, widget):
        self.clearFile("connections.db", "Подтвердите очистку списка подключений",
                      "Все Ваши сохраненные подключения удалятся!!!")

    def enableKiosk (self):
        """Включение режима киоска, создание необходимых для этого файлов"""
        def saveXsession(wm):                   
            xsession = open (HOMEFOLDER + "/.xsession", "w")
            xsession.write(wm)
            xsession.close()
            return True
        existsXs = False #будет ли записан файл
        marco = int(os.popen('which marco > /dev/null 2> /dev/null; echo $?').read()) #0 если установлено.
        if marco == 0: existsXs = saveXsession(KIOSK_MARCO)
        else:
            openbox = int(os.popen('which openbox > /dev/null 2> /dev/null; echo $?').read())
            if openbox == 0: existsXs = saveXsession(KIOSK_OPENBOX)
            else:
                dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Оконный менеджер не найден!")
                dialog.format_secondary_text("Для работы в режиме киска необходимо\nустановить один из оконных менеджеров:\n- marco\n- openbox")
                response = dialog.run()
                dialog.destroy()
                self.check_kiosk.set_active(False)#автоматическое снятие чекбокса
        if existsXs:
            try: os.chmod(HOMEFOLDER+"/.xsession", 0o766) #chmod +x            
            except FileNotFoundError: pass
            autostartFile = HOMEFOLDER + "/.config/autostart/Ctor_kiosk.desktop"
            autostart = open (autostartFile, "w")
            autostart.write(KIOSK_X)
            autostart.close()
            os.chmod(autostartFile, 0o766)
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.OK, 'Программа настроена на режим "Киоск"')
            dialog.format_secondary_text("При следующем входе в сеанс пользователя запуститься только Connector.\nCtrl+Alt+F1 - откроется рабочий стол")
            response = dialog.run()
            dialog.destroy()
            self.defaultConf['KIOSK'] = 1

    def disableKiosk (self):
        try:
            os.remove(HOMEFOLDER + "/.config/autostart/Ctor_kiosk.desktop")
            os.remove(HOMEFOLDER + "/.xsession")
        except: pass

if __name__ == '__main__':
    pass
