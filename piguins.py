from searchPlus import *


line1 = "## ## ## ## ## ## ## ## ##\n"
line2 = "## .. .. .. .. .. .. .. ##\n"
line3 = "## .. .. .. 00 .. .. .. ##\n"
line4 = "## .. .. .. .. .. .. .. ##\n"
line5 = "## .. .. () () () .. .. ##\n"
line6 = "## .. .. .. .. .. .. .. ##\n"
line7 = "## .. .. .. 01 .. .. .. ##\n"
line8 = "## .. .. .. .. .. .. .. ##\n"
line9 = "## ## ## ## ## ## ## ## ##\n"
grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9


def coordenadas(ice_map):
    livres = []
    pinguins = []
    icebergs = []
    agua = []
    map = ice_map.strip().split("\n")

    for x in range(len(map)):
        y = 0
        for char in map[x].split():
            y += 1 
            if char.isdigit():
                pinguins.append(((x,y-1),char))
            elif char in "..":
                livres.append((x,y-1))
            elif char in "##":
                icebergs.append((x,y-1))
            else:
                agua.append((x,y-1))
    return [livres, pinguins, icebergs, agua]

class PenguinsPairs(Problem):

    def __init__(self, ice_map=grid):
        self.ice_map = ice_map
        self.initial = coordenadas(self.ice_map)[1]
        self.data = coordenadas(self.ice_map)
        super().__init__(self.initial)
    
    def actions(self, state):
        """Retorna os movimentos possíveis para cada pinguim."""
        
        movimentos = []
        tuplos = []
        direcoes = ['N','S','E','O']
        C_R = [linha.split() for linha in self.ice_map.strip().split("\n")]
        for item in state: 
            if isinstance(item, tuple):
                tuplos.append(item)
        
        for tuplo, id in tuplos:
            for i in direcoes:
                x = int(tuplo[0])
                y =  int(tuplo[1])
                if i == 'N':
                    if (x-1,y) not in self.data[2] or (x-1,y) in self.data[3]:
                        while x >= 0:
                            x = x - 1
                            if (x,y) in self.data[3]:
                                break
                        else:
                            movimentos.append((id,i))
                elif i == 'S':    
                    if (x+1,y) not in self.data[2] or (x+1,y) in self.data[3]:
                        while x <= len(C_R):
                            x = x +1
                            if (x,y) in self.data[3]:
                                break
                        else:
                            movimentos.append((id,i))
                elif i == 'E':
                    if (x,y+1) not in self.data[2] or (x,y+1) in self.data[3]:
                        while y <= len(C_R[0]):
                            y = y + 1
                            if (x,y) in self.data[3]:
                                break
                        else:
                            movimentos.append((id,i))
                elif i == 'O':                    
                    if (x,y-1) not in self.data[2] or (x,y-1) in self.data[3]:
                        while y >= 0:
                            y = y - 1
                            if (x,y) in self.data[3]:
                                break
                        else:
                            movimentos.append((id,i))
        s = sorted(movimentos)
        return s


    def result(self, state, action = ""):
        """Aplica uma ação ao estado e retorna o novo estado."""
        new_state = [list(row) for row in state]
        #nao existe actions possiveis para os pinguins 
        
        #coisas a implementart
        #- ver o que fazer qnd os pin guisn colidem

        #extrai o action
        id , direcao = action
        
        #vai buscar a posicao atual do pinguim que queremos mexer
        for lista in new_state:
            if id in lista:
                (x,y) = lista[0]


        nx = int(x)
        ny = int(y)
        self.data[0].append((nx,ny))
        if direcao == "N":
            while (nx,ny) in self.data[0]:
                nx = nx - 1
            nx =  nx + 1 #serve para que as cords do pinguim seja um elemento dos lugares livres pois com a condicao do while vamos sempre conseguir um elemento na lista dos icebergues 
            self.data[0].remove((nx,ny))#retira o novo local do pinguim dos lugares livres
        elif direcao == "O":
            while (nx,ny) in self.data[0]:
                ny = ny - 1
            ny = ny + 1
        elif direcao == "S":
            while (nx,ny) in self.data[0]:
                nx = nx + 1
            nx = nx - 1
            self.data[0].remove((nx,ny))
        elif direcao == "E":
            while(nx, ny) in self.data[0]:
                ny = ny + 1
            ny = ny - 1
            self.data[0].remove((nx,ny))


        #Faz um novo state que vai ser returnado
        return_state = [] 
        for lista in new_state:
            if id in lista:
                return_state.append(((nx,ny), id))
            else:
                return_state.append(((lista[0]),lista[1]))
        s = sorted(return_state, key=lambda x: x[1])
        return s

        
    def goal_test (self, state):
        """
        Vê se o state atual é o objetivo, que neste caso é os
        pinguins estarem na mesma coordenada.
        """
        list_state =  [list(row) for row in state]
        list_tuple = [tuple(row[0]) for row in state]
        seen = set()
        #bem bascimanente isto ve se existe pinguins com as mesmas cordenadas se sim apaga-os
        for tuplo in list_tuple:
            if tuplo in seen:
                for lista in list_state:
                    if tuple(lista[0]) == tuplo:
                        list_state = [x for x in list_state if x != lista]
            seen.add(tuplo)       
        return len(list_state) == 0                

    def display (self, state):
        self.data[1] = state
        dih = []
        pinguins = {}

        for lista in self.data:
            for item in lista:
                if isinstance(item, tuple):
                    if len(item) == 2 and isinstance(item[0], tuple) and isinstance(item[1], str):# estes if e porque o ono
                        dih.append(item[0]) 
                        pinguins[item[0]] = item[1] #dicionario com os pinguins e seus ids
                    elif len(item) == 2 and isinstance(item[0], int) and isinstance(item[1], int):
                        dih.append(item) 
        sortedGrid = sorted(dih)
        grid = []
        current_row = []

        for i in sortedGrid:
            if i in  self.data[0]:
                printing = ".."
            elif i in pinguins:
                printing = pinguins[i]
            elif i in  self.data[2]:
                printing = "##"
            elif i in  self.data[3]:
                printing = "()"

            current_row.append(printing)


            if i[1] == sortedGrid[-1][1]:
                grid.append(current_row) 
                current_row = [] 

        grid_str = "\n".join(" ".join(row) for row in grid)
        return grid_str
            
    def executa(self, state, actions_list, verbose=False):
        """Executa uma sequência de acções a partir do estado devolvendo o triplo formado pelo estado final, 
        pelo custo acumulado e pelo booleano que indica se o objectivo foi ou não atingido. Se o objectivo 
        for atingido antes da sequência ser atingida, devolve-se o estado e o custo corrente.
        Há o modo verboso e o não verboso, por defeito."""
        cost = 0
        for a in actions_list:
            seg = self.result(state,a)
            cost = self.path_cost(cost,state,a,seg)
            state = seg
            obj = self.goal_test(state)
            if verbose:
                print('Ação:', a)
                print(self.display(state),end='')
                print('Custo Total:',cost)
                print('Atingido o objectivo?', obj)
                print()
            if obj:
                break
        return (state, cost, obj)
