import random
import math
import sys
from functools import reduce

class BHll:
    
    
    
    def __init__(self,n,m,lr,k,true):
        self.total_bits = 32
        self.m=m
        self.registerSize = 5
        self.lr = lr
        self.n = n
        self.true = true
        self.estimated_size={}
        self.fv={}
        self.k = k
        self.data=[]
        self.A = [ [ 0 for _ in range(self.lr)] for _ in range(self.m)]
        self.randomHashValues=[0 for i in range(self.k)]
        self.id=[0 for i in range(self.k)]

        self.pack()


    
    def pack(self):
        for flow in self.true:
            ia=flow
            sv=self.true[flow]
            uv=set()

            i=0
            while(i<sv):
                while True:
                    hashing=random.randint(1,sys.maxsize-1)
                    if hashing in uv:
                        pass
                    else:
                        uv.add(hashing)
                        break
                i=i+1
            uvArray=[]

            for i in uv:
                uvArray.append(int(i))
            self.fv.update({ia:uvArray})
    
    def counting(self,x):
        res=0
        while ((x & (1 << (self.total_bits - 1))) == 0):
            x = (x << 1)
            res += 1
        return res+1



    def solve(self):
        
        i=0
        while(i<self.k):
            self.randomHashValues[i]=random.randint(1,sys.maxsize-1)
            i=i+1

        randomHashVal=random.randint(1,sys.maxsize-1)
        for fid in self.true:
            svues=self.fv[fid]
            for value in svues:
                j=0
                while(j<self.k):

                    a=[hash(fid),self.randomHashValues[j]]
                    res = reduce(lambda x, y: x ^ y, a)
                    index=res%self.m

                    self.id[j]=index

                    b=[value,randomHashVal]
                    hashval=reduce(lambda x, y: x ^ y, b)
                    temp=self.counting(value)
                    hashval=hashval%self.lr
                    self.A[index][hashval]=max(self.A[index][hashval],temp)
                    j=j+1
        
        for fid in self.true:
            alpha=0.7213 / (1 + (1.079 / self.lr))
            esti=sys.maxsize
            k=0
            t=0
            while(k<len(self.id)):
                index=(hash(fid)^self.randomHashValues[k])%self.m
                estimatedVal=0
                for t in range(len(self.A[0])):
                    suma=2**(self.A[index][t])
                    estimatedVal=estimatedVal+(1/suma)
                    
                esti=min(esti,(alpha*(self.lr**2))*(1/estimatedVal))
                k=k+1
            self.estimated_size[fid]=int(esti)

if __name__ == '__main__':

    n= int(input("Enter number of flows: "))
    m=int(input("Enter number of estimators: "))
    lr= int(input("Enter number of registers: "))
    k=int(input("Enter k: "))


    data=[]
    file = open("project5input.txt", 'r')
    for line in file:
        line = line.split()
        data.append(line)
    data = data[1:]
    file.close()
    
    Y={}
    for i in range(n):
        Y.update({data[i][0]:int(data[i][1])})

    b=BHll(n,m,lr,k,Y)
    b.solve()

    doc = open("output2.txt", "w")
    ans=dict(sorted(b.estimated_size.items(), key=lambda item: item[1],reverse=True))
    count=0

    for fid in ans:
        count+=1
        if count>25:
            break
        doc.write(" "+str(fid)+ " "+str(ans[fid])+"\n")
