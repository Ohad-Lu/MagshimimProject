import urllib.request
url = "http://127.0.0.1:5000/sendcmd/"

def send_cmd(cmd):
    r = urllib.request.urlopen(url + cmd.replace(" ", "%20"))
    r = r.read().decode("utf-8")
    return r

def main():
    while True:
        cmd = input("[+] Enter command -> \n[+] ")
        try:
            print(send_cmd(cmd))
        except:
            pass

main()
