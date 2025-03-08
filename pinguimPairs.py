from searchPlus import *

line1 = "## () () () () () () () ##\n"
line2 = "## .. .. .. .. .. .. 05 ##\n"
line3 = "## .. .. .. 00 .. .. .. ##\n"
line4 = "## 04 .. .. 02 .. .. 03 ##\n"
line5 = "## .. () () () () () .. ##\n"
line6 = "## .. .. .. .. .. .. .. ##\n"
line7 = "## .. .. .. 01 .. .. .. ##\n"
line8 = "## .. .. .. .. .. .. .. ##\n"
line9 = "## () () () () () () () ##\n"
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
        posicao = ""
        for (pos,pinguim_id) in state:
            for direcao in ['N', 'S', 'E', 'O']:
                if self.valid_move(state, pos, direcao):  
                    movimentos.append((pinguim_id, direcao))
        vski = sorted(movimentos)
        return vski

    def valid_move(self, state, pos, direcao):
        """Verifica se um pinguim pode mover-se sem cair na água, parando apenas contra icebergs ou noutro pinguim."""
        movimentos = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
        dx, dy = movimentos[direcao]
        x, y = pos 
        print(type(x))
        nx, ny = x + dx, y + dy  

        # Converter state numa matriz
        state_grid = [linha.split() for linha in self.ice_map.split("\n")]

        # Extrair apenas as coordenadas dos pinguins no estado atual
        pinguim_coords = {pos for pos, _ in state}  

        # Verificar se a posição inicial está dentro dos limites
        if not (0 <= x < len(state_grid) and 0 <= y < len(state_grid[0])):
            return False  

        # Percorre até encontrar um destino válido ou sair do mapa
        while 0 <= nx < len(state_grid) and 0 <= ny < len(state_grid[0]):
            if state_grid[nx][ny] in ('##', '()'):
                return False  
            elif state_grid[nx][ny] == '..' or (nx, ny) in pinguim_coords:
                return True 
            
            nx, ny = nx + dx, ny + dy  

        return False 
    

    def result(self, state, action):
        """Aplica uma ação ao estado e retorna o novo estado."""
        (x, y), direcao = action
        new_state = [list(row) for row in state]
        nx, ny = x, y
        if direcao == 'N':
            while nx > 0 and new_state[nx - 1][ny] == '..':
                nx -= 1
        elif direcao == 'S':
            while nx < len(state) - 1 and new_state[nx + 1][ny] == '..':
                nx += 1
        elif direcao == 'E':
            while ny < len(state[0]) - 1 and new_state[nx][ny + 1] == '..':
                ny += 1
        elif direcao == 'O':
            while ny > 0 and new_state[nx][ny - 1] == '..':
                ny -= 1
        
        new_state[x][y] = ".."
        new_state[nx][ny] = state[x][y]
        return tuple(tuple(row) for row in new_state)

    def goal_test (self, state):
        """
        Vê se o state atual é o objetivo, que neste caso é os
        pinguins estarem na mesma coordenada.
        """
        return len(set(state)) == 1

    def display (self, state):
        self.data[1] = state
        dih = []
        data = coordenadas()

        #este for faz com que tudo o que não é tuplos fique na lista
        for lista in state:
            for item in lista:
                if isinstance(item, tuple):
                    dih.append(item)
        sortedGrid = sorted(dih)
        grid = []
        current_row = []

        for i in sortedGrid:
            if i in data[0]:
                printing = ".."
            elif i in data[1]:
                index = data[1].index(i)
                printing = data[1][index + 1]
            elif i in data[2]:
                printing = "##"
            else:
                printing = "()"

            current_row.append(printing)

            # Check if it's the end of a row
            if i[1] == sortedGrid[-1][1]:
                grid.append(current_row)  # Add the row to the grid
                current_row = []  # Start a new row

        # Print the grid in a structured way
        for row in grid:
            print(" ".join(row))  # Join row elements with spaces

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
    
# if __name__ == "__main__":
#     jogo = PenguinsPairs(grid)  
#     _, pinguins, _, _ = coordenadas(grid)  

#     print("Testando movimentos válidos:")
#     for (pos, pinguim_id) in pinguins: 
#         for direcao in ['N', 'S', 'E', 'O']:
#             pode_mover = jogo.valid_move(pinguins, pos, direcao) 
#             print(f"Pinguim {pinguim_id} em {pos} pode mover-se para {direcao}? {pode_mover}")

x = coordenadas(grid)

if __name__ == "__main__":
    jogo = PenguinsPairs(grid)  # Criar o jogo com o mapa dado
    movimentos_possiveis = jogo.actions(x[1])  # Obter os movimentos possíveis para o estado inicial
    print(movimentos_possiveis)
