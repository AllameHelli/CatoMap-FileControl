# -*- coding: utf-8 -*-
#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from kivy.metrics import *
#A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol
from plyer import notification

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.sm.current_screen.pars(data)


class EchoFactory(protocol.ReconnectingClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        ErrorPop(reason).open()
        self.retry()

    def clientConnectionFailed(self, conn, reason):
        ErrorPop(reason).open()

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.config import Config
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition, WipeTransition, SlideTransition, SwapTransition
from kivy.lang import Builder
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.graphics import Color, Ellipse, Line, Rectangle, Point
from kivy.uix.listview import ListView,ListItemButton,ListItemLabel
from kivy.adapters.dictadapter import DictAdapter
from kivy.logger import Logger
Builder.load_file('Main')
import os

SETTING = {'ICONSIZE':{'SMALL':("100sp","100sp"),'LARGE':(500,500)}}
Icons = os.listdir('icons')
Tfile = None


class ErrorPop(Popup):
    def __init__(self, exeption, **kw):
        super(ErrorPop, self).__init__(**kw)
        self.Error = Label(text=str(exeption))
        self.CloseButton = Button(text='ok', on_press=self.close,size_hint=(.3,.3),pos_hint={'right':.65})
        self.title = "Error"

        self.size_hint = (None,None)
        self.size = (Window.width/4*3,Window.height/3)
        self.pos = (Window.width/2-self.size[0]/2,Window.height/2-self.size[1]/2)
        box = BoxLayout(orientation='vertical')
        box.add_widget(self.Error)
        box.add_widget(self.CloseButton)
        self.add_widget(box)


    def close(self, bt):
        self.dismiss()


class Icon(Image):
    def on_touch_down(self, touch):
        super(Image, self).on_touch_down(touch)
        if self.pos[0]<touch.x<self.pos[0]+self.size[0] and self.pos[1]<touch.y<self.pos[1]+self.size[1]:
            self.color = (.1,0,1,1)

    def on_touch_up(self, touch):

        if self.pos[0]<touch.x<self.pos[0]+self.size[0] and self.pos[1]<touch.y<self.pos[1]+self.size[1] and self.parent.looded:
            if touch.is_double_tap:
                self.color = (1,1,1,1)
                if self.parent.mode == 16895 or self.parent.mode ==16749:
                    self.parent.parent.parent.parent.parent.root = os.path.join(self.parent.parent.parent.parent.parent.root,self.parent.name)
                    self.parent.parent.parent.parent.parent.build1()
                else:
                    os.system('"'+os.path.join(self.parent.parent.parent.parent.parent.root,self.parent.name)+'"')
            else:
                if not self.parent.selected:
                    self.color = (.1,1,0,1)
                    self.parent.parent.parent.parent.parent.selected.append(self.parent)
                    self.parent.parent.parent.parent.parent.select()
                    self.parent.selected = True
                else:
                    self.color = (1,1,1,1)
                    self.parent.parent.parent.parent.parent.selected.remove(self.parent)
                    self.parent.parent.parent.parent.parent.select()
                    self.parent.selected = False
        if not self.parent.selected:
            self.color = (1,1,1,1)

class File(BoxLayout):
    def __init__(self, *args, **kwargs):
        super(File, self).__init__(**kwargs)
        self.name = args[0]
        self.path = args[1]
        self.icon = Icon(allow_stretch=True,source="loading.gif",pos_hint={'x':.0,'y':0})
        self.add_widget(self.icon)
        self.looded = False
        self.orientation = 'vertical'
        name = ''
        i = 0
        for s in self.name:
            if i == 10:
                name += '...'
                break
            name += s
            i += 1
        size = "14sp"
        if len(name)>5:
            size = '12sp'
        self.add_widget(Label(text=name,shorten=True,split_str='...',halgin='center',valgin='center',font_size=size))
        self.size_hint = (None,None)
        self.size = SETTING['ICONSIZE']['SMALL']
        self.selected = False


    def send(self):
        self.parent.parent.parent.parent.app.connection.write('s*?!"'+os.path.join(self.path,self.name)+'"*?!|&*')

    def build(self,stat):
        self.mode, self.ino, self.dev, self.nlink, self.fuid, self.gid, self.fsize, self.atime, self.mtime, self.ctime = stat
        'self.check = CheckBox()'
        self.looded = True
        self.clear_widgets()
        name = ''
        i = 0
        for s in self.name:
            if i == 13:
                name += '...'
                break
            name += s
            i += 1
        self.icon = Icon(source=self.getIcon(),pos_hint={'x':0,'y':0},allow_stretch=True)


        'self.check.bind(active=self.on_checkbox_active)'
        'self.add_widget(self.check)'
        self.add_widget(self.icon)
        size = "14sp"
        if len(name)>5:
            size = '12sp'
        self.add_widget(Label(text=name,shorten=True,split_str='...',halgin='center',valgin='center',font_size=size))

    def on_checkbox_active(self, c, value):
        if value:
            self.parent.parent.parent.parent.selected.append(self)
            self.parent.parent.parent.parent.select()
        else:
            self.parent.parent.parent.parent.selected.remove(self)
            self.parent.parent.parent.parent.select()

    def getIcon(self):
        if self.parent.parent.parent.parent.root == '':
            return os.path.join('icons/'+"drive.png")
        if self.mode == 16895 or self.mode ==16749:
            return os.path.join('icons/'+"folder.png")

        for f in Icons:
            if self.name.endswith('.' + f.replace(".png",'')):
                return os.path.join('icons/'+f)

        return os.path.join('icons/'+"_blank.png")

    def __setattr__(self, key, value):
        super(File, self).__setattr__(key,value)
        if key=='parent' and value:
            self.send()


class tfile:
    def __init__(self,n,size):
        self.f = open(os.path.join("Downloads/",n),'wb')
        self.n = n
        self.recvs = 0
        self.size = size
        self.finish = False
        self.value = ''

    def close(self):
        self.f.close()
        self.finish = True

    def part(self,p):
        self.value += p
        self.recvs += len(p)
        self.f.write(p)


class MainScreen(Screen):
    def __init__(self, app, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.root = ""
        self.ids.Grid.bind(minimum_height=self.ids.Grid.setter('height'))
        self.selected = []
        self.app = app
        self.copy_s = False
        self.copy_l = []
        self.looding = Image(source='loading.gif')
        self.downloading = False
        self.build1()
        self.select()


    def select(self):
        if self.copy_s:
            self.ids.Action.title = "select the destenatin"
        else:
            s = '"'+self.root+'"' + ' Selected Files: '
            for i in self.selected:
                s += "<"+i.name+">"

            self.ids.Action.title = s

    def build(self,file_list):
        file_list = file_list.replace('[','').replace(']','').replace("'",'')
        if '\\\\x00' in file_list:
            file_list = file_list.split('\\\\x00')[:-1]
        if ',' in file_list:
            file_list = file_list.split(',')
        try:
            self.remove_widget(self.looding)
            self.ids.Grid.cols = int(sp(Window.width))//(int(SETTING['ICONSIZE']['SMALL'][0].replace("sp",''))+30)-1
            if len(file_list) == 0:
                self.ids.grid.add_widget(Label('No files or directories found.'))
            for f in file_list:
                if f[0]==' ':
                    f = f[1:]
                self.ids.Grid.add_widget(File(f, self.root))
        except Exception as e:
            ErrorPop(e).open()
            raise e
            if self.root == os.path.split(self.root)[0]:
                self.root = ''
            else:
                self.root = os.path.split(self.root)[0]
            self.build1()
            self.select()

    def back(self):
        if self.root == os.path.split(self.root)[0]:
            self.root = ''
        else:
            self.root = os.path.split(self.root)[0]
        self.build1()

    def copy(self):
        if not self.copy_s:
            if len(self.selected)==0:
                ErrorPop("Please select").open()
            else:
                self.copy_s = True
                self.copy_l = self.selected

                self.select()
                self.ids.Copy.text = "Paste"
        else:
            for i in self.copy_l:
                self.app.connection.write("c*?!'"+os.path.join(i.path,i.name)+"','"+self.root+"'*?!|&*")
            self.copy_s = False
            self.select()
            self.build1()

    def download(self):
        if len(self.selected)!=1:
            ErrorPop("Please select one file").open()
        elif self.selected[0].mode==16895 or self.selected[0].mode==16749:
            ErrorPop("Please select File not Folder").open()
        else:
            for i in self.selected:
                self.app.connection.write("sf*?!"+os.path.join(i.path,i.name)+"*?!|&*")

    def build1(self):
        try:
            self.add_widget(self.looding)
        except:pass
        if self.root == '':
            self.ids.Action.disabled = True
        else:
            self.ids.Action.disabled = False
        self.selected = []
        self.ids.Grid.clear_widgets()
        self.select()

        if self.root == '':
            self.app.connection.write('d*?!|&*')
        else:
            self.app.connection.write('l*?!'+self.root+'*?!|&*')

    def pars(self,data):
        global Tfile
        if '|&*' not in data and "*?!" not in data and data!='':
            Tfile.part(data)
        data = data.split('|&*')
        if len(data) == 1:
            data = data[0].split('*?!')
            if data[0]=='l' or data[0]=='d':
                self.build(data[len(data)-1])
            if data[0]=='s':
                data1 = data[1].replace('"','')
                data2 = data[2].replace('nt.stat_result',"").replace('=',':')
                for w in self.ids.Grid.children:
                    if os.path.join(w.path,w.name)== data1:
                        data2 = data2.replace('st_mode:',"").replace('st_ino:',"").replace('st_dev:',"").replace('st_nlink:',"").replace('st_uid:',"").replace('st_gid:',"").replace('st_atime:',"").replace('st_size:',"").replace('st_mtime:',"").replace('st_ctime:',"")
                        Logger.info('title: '+ data2)
                        w.build(eval(data2))

            if data[0]=='SfH':
                Tfile = tfile(data[1],int(data[2]))
                self.downloading = True

            if '@eND$' in data[0]:
                data[0] = data[0].replace('@eND$','')
                Tfile.part(data[0])
                Tfile.close()
                notification.notify(message="Download completed:"+Tfile.n ,title="Catomap")
                Tfile = None




                #print TFILES['9.png'].value

        else:
            for d in data:
                self.pars(d)


class History(Screen):
    lists = {}

    def on_enter(self, *args):
        self.clear_widgets()

    def update(self):
        f = open("Downloads/History")
        f = f.read().split("\n")
        for i in f:
            i = i.split(',')
            self.lists[i[0]] = i[1:]
        dict_adapter = DictAdapter(sorted_keys=sorted(self.lists.keys()),
                                   data=self.lists,
                                   selection_mode='single',
                                   allow_empty_selection=False,
                                   cls=ListItemButton)



class MainApp(App):
    def build(self):
        self.connect_to_server()
        sm = ScreenManager()

        self.sm = sm
        return sm

    def connect_to_server(self):
        reactor.connectTCP('192.168.1.121', 646, EchoFactory(self))

    def on_connection(self, connection):
        print("connected succesfully!")
        self.connection = connection
        self.sm.add_widget(MainScreen(self, name='main'))
        self.sm.current = 'main'

    def send(self,msg):
        self.connection.write(msg)



if __name__ == '__main__':
    MainApp().run()