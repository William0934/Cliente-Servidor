
numberOfBytes = 4


from math import pow

def next(value,list):
    if int(list[-1])<value:
        return list[0]
    else:
        for id in list:
            if value<=int(id):
                return id

def getFingerTable(nodes,id):
    table=[]
    keys = list(nodes.keys())
    temp=[]
    for k in keys:
        temp.append(int(k))
    keys=sorted(temp)
    max=pow(2,numberOfBytes)
    for i in range(numberOfBytes):
        table.append(str(int(next(pow(2,i)+int(id),keys)%max)))
    table=sorted(table)
    d={}
    return  [ (d.setdefault(x,x)) for x in table if x not in d ]


nodes={'0':7,'3':3,'4':5,'5':5,'6':5,'7':5,'9':5,'10':5}
print(getFingerTable(nodes,'3'))

