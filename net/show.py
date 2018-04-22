import matplotlib.pyplot as plt

f = open("testData");
x=[]
y=[]
linea=f.readline()
while linea!="":
	if linea[-2]==':':
		x.append(int(f.readline()[2:-1]))
		y.append(int(f.readline()[2:-1]))
		linea=f.readline()
f.close()

plt.plot(x,y, 'ro')
plt.axis("equal")
plt.show()

