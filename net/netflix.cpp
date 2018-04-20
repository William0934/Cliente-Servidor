#include <iostream>
#include <list>		//cada usuario tiene una lista de peliculas con calificaciones
#include <cmath>	//sqrt
#include <fstream>  //Lectura de ficheros
#include <utility>  //pair

#include <stdlib.h>
#include <time.h>

#include <ctime>    //medir el tiempo de ejecucion

#define USERS 102
#define MOVIES 17770

using namespace std;

#define CLK_TCK 1000.0

//Las instancias de la clase movie contienen el id de una pelicula y la respectiva calificacion que un usuario le ha dado
class movie{
private:
	int id;
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
	user(int Id){id=Id;}
	user(){}
	user(const user &u){
		id=u.id;
		movies = u.movies;
	}
	user(list<user> group,int Id){
		id=Id;
		int siz=MOVIES *2;
		float data[siz];
		for (int i = 0;i<siz;i++)data[i]=0;
		list<user>::iterator it;
		list<movie>::iterator temp;
		int pos;
		for(it=group.begin();it!=group.end();it++){
			for(temp = it->movies.begin();temp!=it->movies.end();temp++){
				pos=2*(temp->getId()-1);
				data[pos]=data[pos]+temp->getGrade();
				data[pos+1]=data[pos+1]+1;
			}
		}
		for(int i=0;i<siz;i=i+2)
			if((data[i])>0)
				movies.push_back(movie((i/2)+1,round(data[i]/data[i+1])));
		cout<<"CENTROIDE NUEVO "<<endl;
	}
	void addMovie(movie m){
		movies.push_back(m);			
	}
	
	int size(){return movies.size();}
	
	list<movie>::iterator begin(){return movies.begin();}
	list<movie>::iterator end(){return movies.end();}
	
	bool print(){
		cout<<id<<": "<<endl;
		int i=0;
		for(list<movie>::iterator it = movies.begin(); it != movies.end() and i<10; it++ ){
			cout<<" -Id pelicula: "<<it->getId()<<"    Calificacion: "<<(int)it->getGrade()<<endl;
			i++;
		}

		return true;
		
	}

	double distance(user us,bool over){
		if (over)cout<<" calculando para un centroide con "<<size()<<" y un centroide con "<<us.size()<<endl;
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
		return sum;
	}
	
};


class netflix{
private:
	user *users;
public:
	netflix(){}
	void load(){
		string location="";
		string file="myDataSet2";
		users = new user[USERS];
		//El contenido que interesa de cada linea se guardara en las siguientes 3 variable
		double zz=0;
		ifstream input(file);
		int i=-1;
		pair <unsigned short,char> p;			
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
		cout<<" usuarios: "<<zz<<" calificaciones: "<<i<<endl;
	}
	
	user getUser(int i){
		return users[i];
	}
	user *randomUsers(int size){
		user *u = new user[size];
		int du=USERS/size;
		for(int i=0;i<size;i++){
			u[i]=users[du*i];
		}
				 
		return u;

	}
	double distance (int i,user u ){		
		return users[i].distance(u,false);
	}
	~netflix(){
		delete [] users;
	}
	void print(int i){
		users[i].print();
	}
};


class kmeans{
private:
	list<user> *groups;
	netflix n;
	user *centroids;
	user *oldCentroids;
	double stop;
	int k;
public:
	kmeans(int K,double stp ){		
		stop = stp;		
		k=K;
		groups = new list<user>[k];
		n.load();
		centroids=n.randomUsers(k);
	}
	void updateCentroids(bool first){
		if (not first)delete [] oldCentroids;
		oldCentroids=centroids;
		centroids = new user[k];
		for(int i=0;i<k;i++)centroids[i]=user(groups[i],(i*-1)-1);
		cout<<"DESPUES"<<endl;
		for(int i=0;i<k;i++){
			cout<<"old"<<endl;
			oldCentroids[i].print();
			cout<<"new"<<endl;
			centroids[i].print();
		}			
		
	}
	void iteration(int number){
		cout<<"INICIO DE ITERACION "<<number<<endl;
		double lowD,actualD;
		int centroid;
		int j;
		int i;
		bool b=(number==0);
		for (int i=0;i<k;i++){
			groups[i].clear();
		}
		for(i=0;i<k;i++){
		}
		for(i=0;i<USERS;i++){
			lowD = n.distance(i,centroids[0]);			
			centroid=0;			
			for (j=1;j<k;j++){
				actualD=n.distance(i,centroids[j]);
				if (actualD<lowD){
					lowD=actualD;
					centroid=j;
				}
			}
			groups[centroid].push_back(user(n.getUser(i)));
		}
		cout<<"termino iteracion"<<endl;
		updateCentroids(b);
		cout<<"actualizo centroides"<<endl;
		if (not over())	iteration(number+1);
	}
	bool over(){
		double d;
		for(int i=0;i<k;i++){
			d=oldCentroids[i].distance(centroids[i],true);
			cout<<" "<<d<<endl;
			if(d>stop)return false;
		}

		cout<<"TERMINO!!!!!!!!!!!!!!"<<endl;
		return true;		
	}
	~kmeans(){
 	 	delete[] groups;
		delete []centroids;
		delete []oldCentroids;
	}	
};



main(int argc, char **argv){
	//netflix n("","myDataSet0");
	kmeans  k(2,0);
	k.iteration(0); 	
}