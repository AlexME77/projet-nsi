#include "ComReseau.h"
#include <cstdlib>
#include <iostream>


using namespace std;

int main(int argc, char *argv[])
{
ComReseau Client("TCP","127.0.0.1",20000);

Client.ConnecterTCP();

Client.EcrireLireCliTCP();

}


