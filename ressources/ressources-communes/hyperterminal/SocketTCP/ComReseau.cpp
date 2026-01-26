#include "ComReseau.h"
#include <cstdlib>
#include <iostream>

ComReseau::ComReseau(char * t, char* a, int p): mAdresseIP(a), mPort(p)
{
if (strcmp(t,"TCP")==0){mSocket=socket(AF_INET, SOCK_STREAM, 0);}
else if (strcmp(t,"UDP")==0){mSocket = socket(AF_INET, SOCK_DGRAM, 0);}

	memset(&mAdresse, 0, sizeof(mAdresse));
	mAdresse.sin_family = AF_INET;
	mAdresse.sin_addr.s_addr = inet_addr(mAdresseIP);
    mAdresse.sin_port= htons(mPort);
    mt=sizeof(mAdresse);
}

ComReseau::ComReseau(char * t, int p): mPort(p)
{
if (strcmp(t,"TCP")==0){mSocket=socket(AF_INET, SOCK_STREAM, 0);}
else if (strcmp(t,"UDP")==0){mSocket = socket(AF_INET, SOCK_DGRAM, 0);}

	memset(&mAdresse, 0, sizeof(mAdresse));
	mAdresse.sin_family = AF_INET;
	mAdresse.sin_addr.s_addr = htonl(INADDR_ANY);
    mAdresse.sin_port= htons(mPort);
    mt=sizeof(mAdresse);
}

ComReseau::~ComReseau()
{
close(mSocket);
}

void ComReseau::LireUDP()
{
    char mesg[longm]="";
    recvfrom(mSocket, mesg, longm, 0, (SA *) &mAdresse, &mt);
    printf("\n message recu:\n");
    fprintf(stderr,"%s\n",mesg);
}

void ComReseau::EcrireUDP()
{
    char mesg[longm]="";
    printf("\n Taper votre message:\n");
    scanf("%s", mesg);
	sendto(mSocket, mesg, longm, 0, (SA *) &mAdresse, mt);
}

void ComReseau::Config()
{
    if(bind(mSocket,(struct sockaddr *) &mAdresse, mt)==-1)
	{
	    perror("bind");
        exit(EXIT_FAILURE);
    }
}

void ComReseau::AttenteConnexionTCP()
{
    if(bind(mSocket,(struct sockaddr *) &mAdresse, mt)==-1)
	{
	    perror("bind");
        exit(EXIT_FAILURE);
    }

	if (listen(mSocket, MaxConnec)==-1)
    {printf("erreur d'écoute");}
}


void ComReseau::ConnecterTCP()
{
	if (connect(mSocket, (struct sockaddr *) &mAdresse, mt) == -1)
	{
    perror("erreur de connexion");
	exit(EXIT_FAILURE);
	}
}


int ComReseau::AccepterTCP()
{
     struct sockaddr_in client;

   socklen_t ad_ip = sizeof(client);
    mAccept = accept(mSocket,(SA *) &client,&ad_ip);
if (mAccept ==-1)
{
    perror("accept");
    exit(EXIT_FAILURE);
}
	return mAccept;
}

void ComReseau::LireEcrireServTCP(int n_client_socket,char *message)
{
	char message2[512]="";
	  for(;;)
	{

		read(n_client_socket,message,512);
		fprintf(stderr," Client:%s\n",message);
		 if (strcmp(message,"end")==0)  // si le message est “end”, on rompt la communication
		{
			printf("cmp ok");
			exit(0);
		}
		printf("\n serveur:");
		scanf("%s", message2);
		write(n_client_socket,message2,512);
		sleep(1);
	}
}
void ComReseau::EcrireLireCliTCP()
{
	char buffer[512], message[512]="vide";
	  for(;;)
	{
		if (strcmp(buffer,"end")==0)  // si le message est “end”, on rompt la communication
		{
			printf("cmp ok");
			exit(0);
		}
		printf("\n client:");
		scanf("%s", message);
		write(mSocket,message,sizeof(message)); // envoie du message au serveur
		sleep(5);
		read(mSocket,buffer,512);               // lecture du message envoyé par le serveur
		fprintf(stderr," Serveur:%s\n",buffer);                 // Affichage du message serveur coté client
	}
}
