#include <iostream>
#include <list>		//cada usuario tiene una lista de peliculas con calificaciones
#include <cmath>	//sqrt
#include <fstream>  //Lectura de ficheros
#include <utility>  //pair

#include <stdlib.h>
#include <time.h>

#include <ctime>    //medir el tiempo de ejecucion

#define USERS 94802

using namespace std;

#define CLK_TCK 1000.0

//Las instancias de la clase movie contienen el id de una pelicula y la respectiva calificacion que un usuario le ha dado
class movie{
private:
	unsigned short id;
	char grade;
public:
	movie(unsigned short ID,char GR){
		id=ID;
		grade=GR;
	}
	
	
	unsigned short getId()const{return id;}
	char getGrade()const{return grade;}
	void print()const{cout<<id<<": "<<(int)grade<<endl;}
	movie& operator = (const movie &p){
		id=p.getId();
		grade=p.getGrade();
	}
};

//Las lineas de dataset nuevo tienen el formato "pelicula calificacion"  "17770 5" 
//computeLine recibe como parametro una de estas lineas y devuelve un pair con el id y la calificacion 

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

class user{
private:
	int id;
	list<movie> movies;
public:
	user(int Id){id=Id;};
	user(){};
	~user(){
		movies.clear();
	}
	void addMovie(movie m){
		movies.push_back(m);			
	}
	
	int size(){return movies.size();}
	
	list<movie>::iterator begin(){return movies.begin();}
	list<movie>::iterator end(){return movies.end();}
	
	bool print(){
		cout<<id<<": "<<endl;
		for(list<movie>::iterator it = movies.begin(); it != movies.end(); it++ )
			cout<<" -Id pelicula: "<<it->getId()<<"    Calificacion: "<<(int)it->getGrade()<<endl;
		return true;
		
	}

	double distance(user us){
		list<movie>::iterator big=movies.end();
		big--;    
		list<movie>::iterator bigEnd; 
		list<movie>::iterator small=us.end();
		small--;    
		list<movie>::iterator smallEnd;
		if(movies.end()->getId()>us.end()->getId()){
			big      =  movies.begin();
			small    =  us.begin();
			bigEnd   =  movies.end();
			smallEnd =  us.end();
		}else{
			big      =  us.begin();
			small    =  movies.begin();
			bigEnd   =  us.end();
			smallEnd =  movies.end();
		}
		bool limit = false;
		double sum = 0.0;
		double a;
		double b;
		unsigned short bId;
		unsigned short sId;
		//Empieza el ciclo que calcula la sumatoria dentro de la raiz
		while(big!=bigEnd){
			//Marca si la lista mas pequena ya se recorrio
			if (small==smallEnd) limit=true;
			//Si no se ha recorrido la pequena	
			if (!limit){
				bId = big->getId();
				sId = small->getId();
				if (bId<sId){
					a = big->getGrade();
					sum+= (a*a);
					big++;
				}else if (bId>sId){
					b = small->getGrade();
					sum+= (b*b);
					small++;
				}else{
					a = big->getGrade();
					b = small->getGrade();
					sum+= ((a-b)*(a-b));
					big++;
					small++;
				}
			//Si ya se recorrio la pequena	
			}else{
				a=big->getGrade();
				sum+=(a*a);
				big++;
			}
		}			
		return sqrt(sum);
	}
	
};


class netflix{
private:
	user *users;
public:
	netflix(string location,string file){
		users = new user[USERS];
		//El contenido que interesa de cada linea se guardara en las siguientes 3 variable
		double zz=0;
		ifstream input(file);
		int i=-1;
		pair <unsigned short,char> p;			
		cout<<"Se inicio la lectura del archivo"<<endl;
		int id;
		for(string line; getline( input, line );){
		    if (line[line.size()-1]!=':'){
		    	p=computeLine(line);
		    	users[i].addMovie(movie(p.first,p.second));
		    	zz++;

		    }else{
		    	id=getId(line);
		    	users[i+1]=user(id);
		    	i++;

		    }

		}
		cout<<" Se creo con "<<zz<<" calificaciones y con "<<i+1<<" usuarios"<<endl;
	}
	user *randomUsers(int size){
		user *u = new user[size];
		int du=USERS/size;
		for(int i=0;i<size;i++){
			u[i]=users[du*i];
		}		 
		return u;
	}
	~netflix(){
		delete [] users;
	}
	void print(int i){
		users[i].print();
	}
};


class kMeans{
private:
	user **groups; //cambiar por arreglo de listas
	user *centroids;
	double stop;
	int k;
public:
	kMeans(int K,double stp ,netflix n){
		stop = stp
		k=K;
		centroids=n.randomUsers(k);
		for (int i=0;i<k;i++){
			centroids[i].print();
		}
		groups = new user*[k];
		for(int i=0;i<k;i++){
			groups[i] = new
		}
		cout<<"FINAL"<<endl;
	}
	void iteration(n){
		double lowD,actualD;
		int centroid;
		//vaciar listas
		for(int i=0;i<USERS;i++){
			lowD = n.distance(i,centroids[0]);
			centroid=0;	
			for (int j=1;j<k;j++){
				actualD=n.distance(i,centroids[j]);
				if (actualD<lowD){
					lowD=actualD;
					centroid=j;
				}
			}
			//agregar a la lista de el arreglo en la posicion j
		}
	}
	~kMeans(){
		for(int i = 0; i < k; i++)
 	 		delete[] groups[i];
 	 	delete[] groups;
		delete []centroids;
	}	
};



int main(int argc, char **argv){
	srand(time(NULL));
	netflix n("","myDataSet0");
	cout << "Desde el inicio han pasado " << clock()/(CLK_TCK*1000) << " segundos\n"<<endl;
	kMeans k(3,3,n); 
	return 0;	
}