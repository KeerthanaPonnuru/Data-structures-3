import math 
import random
import sys
from functools import reduce
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class VirtualBitmap:

    def __init__(self,n,m,l):
        self.n = n
        self.m = m
        self.l = l
        self.data = []
        self.true = []
        self.estimated_size = []
        self.genR = []
        self.x = random.randint(0, sys.maxsize)
        self.B = [0 for i in range(self.m)]
        self.id = [0 for i in range(self.n)]

    def reading(self):
        file = open("project5input.txt", 'r')
        for line in file:
            line = line.split()
            self.data.append(line)
        self.data = self.data[1:]
        file.close()

    def solve(self):
        i=0
        while(i<self.n):
            self.id[i] = hash(self.data[i][0])
            self.true.append(int(self.data[i][1]))
            i=i+1

    def gen(self):
        self.genR = random.sample(range(0, sys.maxsize), self.l)

    def recording(self):
        i=0
        while(i<self.n):
            elements = random.sample(range(0, sys.maxsize), self.true[i])
            
            for j in elements:

                z=[j,self.x]
                res = reduce(lambda x, y: x ^ y, z)
                a = self.genR[(res) % self.l]

                y=[a,self.id[i]]
                res2=reduce(lambda x, y: x ^ y, y)
                self.B[abs(res2 % self.m)] = 1
 
            i=i+1

    def query(self):
        Vb = (self.m - sum(self.B)) / self.m
        log_Vb = math.log(Vb)
        for i in self.id:
            u = 0
            for j in self.genR:
                z=[j,i]
                res3=reduce(lambda x, y: x^y, z)

                if self.B[abs((res3) % self.m)] == 0:
                    u += 1
            Vf = u / self.l         
            if Vf == 0.0:
                log_Vf=sys.maxsize

            else:
                log_Vf = math.log(Vf)
            e = self.l * (log_Vb - log_Vf)
            if e >= 0:
                self.estimated_size.append(e)
                
            else:
                self.estimated_size.append(0)
                

    def graph(self, true, estimated_size):
        x = true
        y = estimated_size
        plt.xlim([0, 500])
        plt.ylim([0, 700])
        plt.ylabel("Estimated")
        plt.xlabel("Actual")
        plt.scatter(x, y, marker="+")
        plt.plot([0, 500], [0, 500],"r-") # y=x
        pp.savefig()
        plt.show()


if __name__ == '__main__':


    n = int(input("no. of flows: "))
    m = int(input("no. of bits in physical array: "))
    l = int(input("no. of bits in virtual bitmap : "))

    vb = VirtualBitmap(n,m,l)
    vb.reading()
    vb.solve()
    vb.gen()
    vb.recording()
    vb.query()

    pp = PdfPages('output1.pdf')
    vb.graph(vb.true, vb.estimated_size)
    pp.close()
