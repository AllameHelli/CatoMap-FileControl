# install_twisted_rector must be called before importing  and using the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()

import win32api
from twisted.internet import reactor
from twisted.internet import protocol
import os
import shutil

class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)

    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

class EchoFactory(protocol.Factory):
    protocol = EchoProtocol

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label

EXE = {'l' : 'os.listdir("{}")','d' : 'win32api.GetLogicalDriveStrings().replace(" ","").split()[:3]','s':'os.stat({})','c':'shutil.copy({})','sf':"self.send_file(file('{}'))"}


class file:
    def __init__(self,s):
        self.name = os.path.split(s)[len(os.path.split(s))-1]
        self.f = open(s,'rb')
        self.v = self.f.read()
        self.size = len(self.v)
        self.parts_sended = 0

    @property
    def header(self):
        return "SfH*?!"+self.name+"*?!"+str(self.size)+"*?!|&*"

    @property
    def end(self):
        return "|&*@eND$*?!all*?!|&*"


    def __getitem__(self, item):
        if item == "header":
            return(self.header)
        if item == "end":
            return self.end


class TwistedServerApp(App):
    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenTCP(646, EchoFactory(self))
        return self.label

    def handle_message(self, msg):
        print msg
        self.ParsMsg(msg)

    def ParsMsg(self, msg):
        msg = msg.split('|&*')
        print msg
        for m in msg:
            if m:
                self.ExecMsg(m)

    def ExecMsg(self, msg):
        msg.replace('\\','\\\\')
        msg=msg.replace('\\','\\\\')
        print msg
        msg = msg.split('*?!')
        print msg
        res = EXE[msg[0]]
        for i in msg[1:]:
            if i:
                res = res.format(i)
                print res

        if msg[0]=='s':
            msg[0] = msg[0] + '*?!' + msg[1].replace('\\\\','\\')
        if msg[1]!='sf':
            self.connection.write(msg[0]+'*?!'+str(eval(res))+'|&*')
        else:
            exec res

    def on_connection(self,c):
        self.connection = c

    def send_file(self,f):
        self.connection.write(f.header)
        self.connection.write(f.v)
        self.connection.write(f.end)


if __name__ == '__main__':
    TwistedServerApp().run()