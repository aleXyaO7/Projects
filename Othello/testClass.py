class test:
    t = []
    def __init__(self):
        self.t = []
        self.t.append(0)
        l = 1
        self.ad(l)
    def ad(self, l):
        self.t.append(l)

t1 = test
print(t1.t)
t1.ad(t1, 1)
print(t1.t)