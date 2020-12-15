import sys
import math
sys.setrecursionlimit(10**7)
class segki():
    def __init__(self,N,ls,mode='min'): #葉の数N,要素ls
        self.mode = mode
        self.default = self.setdef()
        self.N = N
        self.K = len(bin(self.N))-3
        if self.N%(2**(self.K)) != 0:
            self.K += 1
        self.N0 = 2**self.K
        self.dat = [self.default]*(2**(self.K+1)) #全体の配列を用意(maxなら-inf,minなら+infで未構築を表現)　
        self.lazy = [0]*(2**(self.K+1)) #遅延評価
        for i in range(self.N): #葉の構築
            self.dat[2**self.K-1+i] = ls[i]
        self.build()
    
    def setdef(self):
        if self.mode == 'min': return 1<<60
        elif self.mode == 'max': return -(1<<60)

    def build(self):
        for j in range(2**self.K-2,-1,-1):
            self.dat[j] = self.func(self.dat[2*j+1],self.dat[2*j+2]) #親が持つ条件
        return self.dat[j]
        
    def func(self,x,y):
        if self.mode == 'min': return min(x,y) 
        elif self.mode == 'max': return max(x,y)

    def leafvalue(self,x): #x番目の値を出力
        return self.query(x,x+1)

    def update_add(self,x,y): #x番目にyを足す
        return self.updatel_add(x,x+1,y)

    def gindex(self,l, r): #伝播するインデックス列挙
        L = l + self.N0; R = r + self.N0
        lm = (L // (L & -L)) >> 1
        rm = (R // (R & -R)) >> 1
        while L < R:
            if R <= rm:
                yield R
            if L <= lm:
                yield L
            L >>= 1; R >>= 1
        while L:
            yield L
            L >>= 1

    def propagates(self,*ids):
        for i in reversed(ids):
            v = self.lazy[i-1]
            if not v:
                continue
            self.lazy[2*i-1] += v; self.lazy[2*i] += v
            self.dat[2*i-1] += v; self.dat[2*i] += v
            self.lazy[i-1] = 0            

    def updatel_add(self,l, r, x):#区間にyを足す
        L = self.N0 + l; R = self.N0 + r
        while L < R:
            if R & 1:
                R -= 1
                self.lazy[R-1] += x; self.dat[R-1] += x
            if L & 1:
                self.lazy[L-1] += x; self.dat[L-1] += x
                L += 1
            L >>= 1; R >>= 1       
        for i in self.gindex(l, r):
            self.dat[i-1] = self.func(self.dat[2*i-1], self.dat[2*i]) + self.lazy[i-1]

    def query(self,l, r):
        self.propagates(*self.gindex(l, r))
        L = self.N0 + l; R = self.N0 + r

        s = self.default
        while L < R:
            if R & 1:
                R -= 1
                s = self.func(s, self.dat[R-1])
            if L & 1:
                s = self.func(s, self.dat[L-1])
                L += 1
            L >>= 1; R >>= 1
        return s

if __name__ == "__main__":
    SG = segki(10,[2,4,6,8,10,1,3,5,7,9],mode='min')
    print(SG.dat)
    print(SG.leafvalue(2))
    SG.update_add(0,5)
    print(SG.query(0,10))
    SG.updatel_add(0,6,-3)
    print(SG.query(0,10))
    SG.updatel_add(0,10,2)
    print(SG.query(0,10))
    print([SG.leafvalue(i) for i in range(10)])
    SG.updatel_add(2,5,5)
    print([SG.leafvalue(i) for i in range(10)])
    print(SG.lazy)
    print(SG.query(3,4))
    print(SG.query(2,3))
    print(SG.query(2,4))
    print([SG.leafvalue(i) for i in range(10)])

    
    

