import sys
import math
sys.setrecursionlimit(10**8)
class segki():
    #modeで関数を選べます。(min,max,sum,prd(product),gcd,lmc,^,&,|)
    def __init__(self,N,ls,mode='min'): #葉の数N,要素ls
        self.mode = mode
        self.default = self.setdef()
        self.N = N
        self.K = len(bin(self.N))-3
        if self.N%(2**(self.K)) != 0:
            self.K += 1
        self.dat = [self.default]*(2**(self.K+1))
        for i in range(self.N): #葉の構築
            self.dat[2**self.K-1+i] = ls[i]
        self.build()
    
    def setdef(self):
        if self.mode == 'min':return 1 << 60
        elif self.mode == 'max':return -(1 << 60)
        elif self.mode == 'sum':return 0
        elif self.mode == 'prd':return 1
        elif self.mode == 'gcd':return 0
        elif self.mode == 'lmc':return 1
        elif self.mode == '^':return 0
        elif self.mode == '&':return (1 << 60)-1
        elif self.mode == '|':return 0
    
    def build(self):
        for j in range(2**self.K-2,-1,-1):
            self.dat[j] = self.func(self.dat[2*j+1],self.dat[2*j+2]) #親が持つ条件

    def func(self,x,y):#関数を指定
        if self.mode == 'min': return min(x,y)
        elif self.mode == 'max': return max(x,y)
        elif self.mode == 'sum': return x+y
        elif self.mode == 'prd': return x*y
        elif self.mode == 'gcd': return math.gcd(x,y)
        elif self.mode == 'lmc': return (x*y)//math.gcd(x,y)
        elif self.mode == '^': return x^y
        elif self.mode == '&': return x&y
        elif self.mode == '|': return x|y
    
    def leafvalue(self,x):
        return self.dat[x+2**self.K-1]

    def update(self,x,y): #index(x)をyに変更
        i = x+2**self.K-1
        self.dat[i] = y
        while (i>0): #親の値を変更
            i = (i-1)//2
            self.dat[i] = self.func(self.dat[2*i+1],self.dat[2*i+2])
        return

    def query(self,a,b): #区間a,bの処理
        return self.query_sub(a,b,0,0,2**self.K)
    
    def query_sub(self,a,b,k,l,r):
        if r <= a or b <= l:
            return self.default
        if (a <= l and r <= b):
            return self.dat[k]
        else:
            vl = self.query_sub(a, b, k * 2 + 1, l, (l + r) // 2)
            vr = self.query_sub(a, b, k * 2 + 2, (l + r) // 2, r)
            return self.func(vl,vr)


if __name__ == "__main__":
    SG = segki(10,[2,4,6,8,10,1,3,5,7,9],mode='min')
    SG.update(0,10)
    print(SG.dat)