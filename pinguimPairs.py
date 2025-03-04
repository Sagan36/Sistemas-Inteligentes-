from searchPlus import *

line1 = "## () () () () () () () ##\n"
line2 = "## .. .. .. .. .. .. .. ##\n"
line3 = "## .. .. .. 00 .. .. .. ##\n"
line4 = "## .. .. .. .. .. .. .. ##\n"
line5 = "## .. () () () () () .. ##\n"
line6 = "## .. .. .. .. .. .. .. ##\n"
line7 = "## .. .. .. 01 .. .. .. ##\n"
line8 = "## .. .. .. .. .. .. .. ##\n"
line9 = "## () () () () () () () ##\n"
grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9


def coordenadas(ice_map=grid):
    agua = []
    pinguins = []
    icebergs = []

    ola = ice_map.strip("\n")
    for x in range(len(ola)):
        y = 0
        for char in ola[x].split():
            y += 1 
            if char in "0123456789":
                pinguins.append((x,y-1))
            elif char in "..":
                agua.append((x,y-1))
            else:
                icebergs.append((x,y-1))
    return agua, pinguins, icebergs

class PenguinsPairs(Problem):

    def __init__(self, ice_map=grid):
        super().__init__(self.initial)
        self.ice_map = ice_map
        self.initial = coordenadas(ice_map)[1]
    
    def actions(self, state):
        """Retorna os movimentos possíveis para cada pinguim."""
        movimentos = []
        for i, j, pinguim_id in self.penguins:
            for direcao in sorted(['N', 'S', 'E', 'O']):
                if self.valid_move(state, i, j, direcao):
                    movimentos.append(((i, j), direcao))
        return movimentos

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
        pass

    def display (self, state):
        pass

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
    


print(coordenadas())
