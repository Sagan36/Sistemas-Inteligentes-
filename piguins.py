from searchPlus import *
from copy import deepcopy



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

cardeais = { 
    "E": (0, 1),
    "N": (-1, 0),
    "O": (0, -1),
    "S": (1, 0)
}



class PenguinsPairs(Problem):

    def __init__(self, ice_map=grid):
        initial = {}
        #matriz para criar o mapa
        linhas = ice_map.strip().split('\n')
        matriz = [linha.split() for linha in linhas]
        for i in range(len(matriz)):
            for j in range(len(matriz[i])):
                if matriz[i][j].isdigit():
                    initial[matriz[i][j]] = (i, j)
                    matriz[i][j] = '..'
        #os pinguins sao um dicionario onde o value e a loc e a key e o id
        super().__init__(initial)
        self.icemap =  matriz
        
    def actions (self, state):
        acoes = []
        sentidos = ['E','N','O','S']
        for p in state.keys():
            for sentido in sentidos:
                px = state[p][0]
                py = state[p][1]

                px += cardeais[sentido][0]
                py += cardeais[sentido][1]       
                if self.icemap[px][py] != '##' and self.icemap[px][py] != '()': #se nas roedondezxas for iceberg ou agua
                    while self.icemap[px][py] != '##': #enquanto nao for iceberg
                        if self.icemap[px][py] == '()': #se for agua 
                            break
                        elif (px,py) in state.values():#aquele caso em que existe um pinguim ao pe mas atras desse pinguim ta agua
                            acoes.append((p,sentido))
                            break
                        px += cardeais[sentido][0]
                        py += cardeais[sentido][1]
                    else:   
                        acoes.append((p,sentido))
        return sorted(acoes, key=lambda x: (x[0], x[1]))
    
    def result(self, state, action):
        pid, sentido = action
        px, py = state[pid]
        dx, dy = cardeais[sentido]
        
        # Criar novo estado sem modificar o original
        novo_estado = deepcopy(state)
        # Mover o pinguim até encontrar um obstáculo ou outro pinguim
        while True:
            px += dx
            py += dy
            
            # Verifica se saiu do limite do mapa
            if px < 0 or px >= len(self.icemap) or py < 0 or py >= len(self.icemap[0]):
                return novo_estado  # Retorna o estado original se sair do mapa
            
            if self.icemap[px][py] == "##" or self.icemap[px][py] == "()":
                # Para antes do obstáculo
                px -= dx
                py -= dy
                break
            
            for p, (p_x, p_y) in state.items():
                if (px, py) == (p_x, p_y):
                    # Caso encontre outro pinguim, remove ambos do estado
                    novo_estado.pop(pid, None)
                    novo_estado.pop(p, None)
                    return novo_estado
        
        # Atualiza a posição do pinguim se ele conseguiu parar num local válido
        novo_estado[pid] = (px, py)
        return novo_estado

    def display(self, state):
        # Criar uma cópia do mapa original
        mapa_visual = [linha[:] for linha in self.icemap]  # Garantir cópia correta
        
        # Colocar os pinguins no mapa
        for pid, (x, y) in state.items():
            mapa_visual[x][y] = pid
        
        # Criar uma string do mapa formatado
        resultado = "\n".join(" ".join(linha) for linha in mapa_visual)
        resultado += "\n"
        return resultado

    def goal_test(self, state):
        # O objetivo é ter todos os pinguins emparelhados e removidos
        return len(state) == 0



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

