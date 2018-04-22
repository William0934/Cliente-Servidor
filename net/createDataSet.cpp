#include <iostream>
#include <list>		//cada usuario tiene una lista de peliculas con calificaciones
#include <cmath>	//sqrt
#include <fstream>  //Lectura de ficheros
#include <utility>  //pair

#include <stdlib.h>
#include <time.h>

#include <ctime>    //medir el tiempo de ejecucion

using namespace std;

pair <unsigned short,char> computeLine(string line){
	char i=0;
	char c=line[0];
	char temp[8];
	while (c!=' '){
		temp[i]=c;
		i++;
		c=line[i];
	}
	temp[i]='\0';
	unsigned short id=atoi(temp);
	i++;
	c=line[i]-48;
	pair <unsigned short,char> p(id,c);	
	return p;
}


int getId(string line){
	char i=0;
	char c=line[0];
	char temp[9];
	while (c!=':'){
		temp[i]=c;
		i++;
		c=line[i];
	}
	temp[i]='\0';
	int id=atoi(temp);
	return id;
}


void create(){
	string location="";
	string file="myDataSet1";
	string out="myDataSet2";
	//El contenido que interesa de cada linea se guardara en las siguientes 3 variable
	ifstream input(file);
	ofstream of(out);
	int i=-1;
	pair <unsigned short,char> p;			
	int id;
	for(string line; getline( input, line );){
	    if (line[line.size()-1]!=':'){	    	
	    	p=computeLine(line);
	    	if (p.first<=1000){
	    		of<<int(p.first)<<" "<<int(p.second)<<endl;
	    	}
	    }else{
	    	if(i<=100){	    		
				id=getId(line);
				of<<id<<":"<<endl;
				i++;
	    	}else break;

	    }
	}
}

main(){
	create();	
}