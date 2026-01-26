#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define	MAXLINE		4096	/* Nombre de lignes maximum*/
#define	MaxConnec  128	/* nombre de client maximum*/
#define	BUFSIZE	8192	/* taille maximun du buffer en écriture et en lecture */
#define	SA	struct sockaddr
#define longm 255
class ComReseau
{
	private:
		int mPort, mAccept, mSocket;
        char* mAdresseIP;
        struct sockaddr_in mAdresse;
		socklen_t mt;

      	public:
                ComReseau(char *,char*, int );
                ComReseau(char *, int );		// constructeur de la socket avec argument (TCP ou UDP)
             	~ComReseau();
             	void Config();
             	void LireUDP();
             	void EcrireUDP();
               	void AttenteConnexionTCP();
                void ConnecterTCP();
                int AccepterTCP();
                void LireEcrireServTCP(int ,char *);
                void EcrireLireCliTCP();


};


