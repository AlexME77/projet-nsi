import socket
import sys

class Client:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def config(self,ip ,port):
        try:
            self.sock.connect((ip,port))
        except socket.error as msg:
            print("Couldnt connect with the socket-server: %s\n terminating program" % msg)
            sys.exit(1)
        print("Connexion on {}".format(port))
    def envoyer(self,message):
        print("envoi de " + message)
        self.sock.send(message.encode())

    def recevoir(self):
        reponse=self.sock.recv(100).decode()
        print("réception de " + str(reponse))
        return str(reponse)

if __name__ == "__main__":
    a = Application()
