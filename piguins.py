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

        for item in self.data[1]: 
            if isinstance(item, tuple):
                tuplos.append(item)

        for (i, j), pinguim_id in tuplos:  
            for direcao in sorted(['N', 'S', 'E', 'O']):
                if self.valid_move(state, i, j, direcao):
                    movimentos.append((pinguim_id, direcao))  
        print(movimentos)
        return movimentos


    def valid_move(self, state, x, y, direcao):
        """Verifica se um pinguim pode mover-se sem cair na água, parando apenas contra icebergs ou noutro pinguim."""
        movimentos = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
        dx, dy = movimentos[direcao]
        nx, ny = x + dx, y + dy  
        # Converter state numa matriz
        state_grid = [linha.split() for linha in self.ice_map.strip().split("\n")]
        #print(state_grid)   
        # verifica se a posicao mesmo ao lado do pinguim esta livre
        if (nx,ny) in self.data[2] or (nx,ny) in self.data[3]:
            return False  

        # Desliza até encontrar um obstáculo ou cair na água
        while 0 <= nx < len(state_grid) and 0 <= ny < len(state_grid[0]):
            celula = state_grid[nx][ny]
            if celula in ('##'):  
                return True 
            elif any(c.isdigit() for c in celula):  
                return True  
            elif celula == '()':  
                return False 

            nx += dx
            ny += dy  

        return False  


    def result(self, state, action = ""):
        """Aplica uma ação ao estado e retorna o novo estado."""
        new_state = [list(row) for row in state]
        list_tuple = [tuple(row[0]) for row in state]
        #nao existe actions possiveis para os pinguins 
        
        print(action)
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


        self.data[0].append((nx,ny))#este append e crucial para duas coisas 1-Deixa nos investigar a lista de lugares
                                #livres passando a frente o local inicial do pinguim 2-Vai atualizar a lista de espacoes livres
                                #para no futuro ser preciso uma outra acao


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


        seen = set()
        #bem bascimanente isto ve se existe pinguins com as mesmas cordenadas se sim apaga-os
        for tuplo in list_tuple:
            if tuplo in seen:
                for lista in new_state:
                    if tuple(lista[0]) == tuplo:
                        new_state = [x for x in new_state if x != lista]
            seen.add(tuplo)
        #Faz um novo state que vai ser returnado
        return_state = [] 
        for lista in new_state:
            if id in lista:
                return_state.append(((nx,ny), id))
            else:
                return_state.append(((lista[0]),lista[1]))
        print(return_state)
        return return_state

        
    def goal_test (self, state):
        """
        Vê se o state atual é o objetivo, que neste caso é os
        pinguins estarem na mesma coordenada.
        """
        list_state =  [list(row) for row in state]
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


 	

line1 = "## ## ## ## ## ## ## ## ##\n"
line2 = "## .. .. .. .. .. .. .. ##\n"
line3 = "## .. .. .. 00 .. .. .. ##\n"
line4 = "## .. .. .. .. .. .. .. ##\n"
line5 = "## .. .. ## ## ## .. .. ##\n"
line6 = "## .. .. ## .. .. .. .. ##\n"
line7 = "## .. .. 01 .. .. .. .. ##\n"
line8 = "## .. .. .. .. .. .. .. ##\n"
line9 = "## ## ## ## ## ## ## ## ##\n"
grid2 = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9

p = PenguinsPairs(grid2)
resultado = breadth_first_graph_search(p)
if resultado:
    print("Solução Larg-prim (grafo) com custo", str(resultado.path_cost)+":")
    print(resultado.solution())
else:
    print("Sem solução!")