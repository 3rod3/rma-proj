class bloco:
    # Tem uma parede nessa direção?
    n: bool
    S: bool
    L: bool
    O: bool

    def __init__(self, n, s, l, o):
        self.N = n
        self.S = s
        self.L = l
        self.O = o

class mapa:
    blocos: list[list[bloco]]

    def __init__(self):
        self.blocos = []

    # transforma a matriz quadrada (ordem n) do mapa em uma matriz de ordem n+1. 
    def aumenta(self, m):
        for i in range(len(m)+1):
            l = []
            for j in range(len(m)+1):
                if m[i][j]:
                    l.append(m[i][j])
                else:
                    l.append(bloco(False,False,False,False))
            m[i] = l
            
        self.blocos = m

    def atualiza(self, p: list[bool], i, j):
        if p[0]:
            self.blocos[i][j].N = True
        if p[1]:
            self.blocos[i][j].S = True
        if p[2]:
            self.blocos[i][j].L = True
        if p[3]:
            self.blocos[i][j].O = True