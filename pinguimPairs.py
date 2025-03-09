from searchPlus import *

line1 = "## ## ## ## ## ## ## ## ##\n"
line2 = "## .. .. .. .. .. .. .. ##\n"
line3 = "## .. .. .. 00 .. .. .. ##\n"
line4 = "## .. .. .. .. .. .. .. ##\n"
line5 = "## .. () () () () () .. ##\n"
line6 = "## .. .. .. .. .. .. .. ##\n"
line7 = "## .. .. .. 01 .. .. .. ##\n"
line8 = "## .. .. .. .. .. .. .. ##\n"
line9 = "## ## ## ## ## ## ## ## ##\n"
grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9


def coordenadas(ice_map=grid):
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
        self.initial = coordenadas(ice_map)[1]
        self.data = coordenadas()
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
        
        return movimentos


    def valid_move(self, state, x, y, direcao):
        """Verifica se um pinguim pode mover-se sem cair na água, parando apenas contra icebergs ou noutro pinguim."""
        movimentos = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
        dx, dy = movimentos[direcao]
        nx, ny = x + dx, y + dy  

        # Converter state numa matriz
        state_grid = [linha.split() for linha in self.ice_map.strip().split("\n")]

        # Verificar se a posição inicial está dentro dos limites
        if not (0 <= nx < len(state_grid) and 0 <= ny < len(state_grid[0])):
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


    def result(self, state, action):
        """Aplica uma ação ao estado e retorna o novo estado."""
        (x, y), direcao = action
        new_state = [list(row) for row in state]  # Create a mutable copy of the state
        nx, ny = x, y
        
        if direcao == 'N':
            while nx > 0 and new_state[nx - 1][ny] == '..':  # Check if the cell is free (gelo)
                nx -= 1
        elif direcao == 'S':
            while nx < len(state) - 1 and new_state[nx + 1][ny] == '..':  # Check for down movement
                nx += 1
        elif direcao == 'E':
            while ny < len(state[0]) - 1 and new_state[nx][ny + 1] == '..':  # Check for right movement
                ny += 1
        elif direcao == 'O':
            while ny > 0 and new_state[nx][ny - 1] == '..':  # Check for left movement
                ny -= 1

        # Make sure to set the current position to "empty" and update the new position with the penguin
        new_state[x][y] = ".."  # Mark the old position as free (gelo)
        new_state[nx][ny] = state[x][y]  # Move the penguin to the new position
        
        return tuple(tuple(row) for row in new_state)  # Return the new state as an immutable tuple


    def goal_test (self, state):
        """
        Vê se o state atual é o objetivo, que neste caso é os
        pinguins estarem na mesma coordenada.
        """
        return len(set(state)) == 1

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