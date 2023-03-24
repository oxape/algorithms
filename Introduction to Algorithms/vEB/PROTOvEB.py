
class PROTOvEB:
    def __init__(self, u):
        super().__init__()
        if u == 2:
            self.n = 0
            self.u = 2
            self.A = [0, 0]
        else:
            self.n = 0
            self.sqrt_u = int(u**0.5)
            self.u = u
            self.summary = PROTOvEB(self.sqrt_u)
            self.cluster = [PROTOvEB(self.sqrt_u) for _ in range(self.sqrt_u)]

    def high(self, x):
        return x//self.sqrt_u
    
    def low(self, x):
        return x%self.sqrt_u

    def insert(self, x):
        if self.u == 2:
            if self.A[x] == 0:
                self.n += 1
            self.A[x] = 1
        else:
            h = self.high(x)
            l = self.low(x)
            self.summary.insert(h)
            # self.high返回x在self.cluster数组中的索引
            self.cluster[h].insert(l)

    def member(self, x):
        if self.u == 2:
            if self.A[x] == 1:
                return True
        else:
            return self.cluster[self.high(x)].member(self.low(x))

def printIfValueInContainPVEB(pvEB, x):
    if pvEB.member(x):
        print(f'{x} in vEB')
    else:
        print(f'{x} not in vEB')

if __name__ == '__main__':
    pvEB = PROTOvEB(16)
    pvEB.insert(8)
    
    printIfValueInContainPVEB(pvEB, 8)
    printIfValueInContainPVEB(pvEB, 0)