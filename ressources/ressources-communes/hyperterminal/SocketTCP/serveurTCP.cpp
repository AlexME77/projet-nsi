#include "ComReseau.h"
#include <cstdlib>
#include <iostream>


using namespace std;

int main(int argc, char *argv[])
{
char message[512]="";

ComReseau Serveur("TCP","127.0.0.1",20000);
Serveur.AttenteConnexionTCP();

for ( ; ; )
{
int client_socket=Serveur.AccepterTCP();

switch (fork())
{
    case-1:
        perror("erreur fork");
        exit(EXIT_FAILURE);

    case 0:                     //processus fils
        Serveur.LireEcrireServTCP(client_socket,message);

    default:                    //processus père
     close(client_socket);

}

}

}


