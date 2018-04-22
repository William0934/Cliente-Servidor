#include <iostream>
#include <list>		//cada usuario tiene una lista de peliculas con calificaciones
#include <cmath>	//sqrt
#include <fstream>  //Lectura de ficheros
#include <utility>  //pair

#include <stdlib.h>
#include <time.h>


using namespace std;



#define PI 3.14159265

void create(int n,int cen,int rad,int max){
	string out="testData";
	srand(time(NULL));

	int **centroids = new int*[cen];
	for(int i=0;i<cen;i++) centroids[i]=new int[2];
	
	centroids[0][0]=rad+max;
	centroids[0][1]=rad+max;

	double da=2*PI/(cen-1);
	double ang;
	
	ofstream of(out);
	for(int c=1;c<cen;c++){
		ang=c*da;
		centroids[c][0]=centroids[0][0]+cos(ang)*rad;
		centroids[c][1]=centroids[0][1]+sin(ang)*rad;
		cout<<" se creo un centroide con x "<<centroids[c][0]<<" y "<<centroids[c][1]<<endl;
	}
	int which,dx,dy;
	int v[2]={-1,1};
	float temp;
	for(int id=1;id<=n;id++){
		which=rand()%cen;
		dx=(rand()%max)*(v[rand()%2]);
		temp=sqrt((max*max)-(dx*dx));
		dy=(rand()%int(temp))*(v[rand()%2]);
		of<<id<<":"<<endl;
		of<<"1 "<<centroids[which][0]+dx<<endl;
		of<<"2 "<<centroids[which][1]+dy<<endl;
	}
	for(int i=0;i<cen;i++) delete [] centroids[i];
	delete [] centroids;

	  
}

main(){
	cout<<"empezo"<<endl;
	create(10000,50,60,20);	
}