from searchPlus import *
from collections import namedtuple


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


EstadoPin = namedtuple('EstadoPin','pinguins')

class EstadoPinguins(EstadoPin):
        
    def __hash__(self):
        return hash(tuple(sorted(self.pinguins.items())))
    
    def __lt__(self,other):
        return True
    
    
class PenguinsPairs(Problem):
    
    def process_txt(self, grid):
        """
        Função que porcessa a grelha em txt e obtém as posições dos icebergues (walls), água e pinguins.
        O output desta função é um dicionário em que as chaves identifica cada tipo de informação a ser 
        guardada. Os pinguins serão um dicionário e os icebergues e água serão um conjunto.
        """
        data = {'walls': set(), 'pinguins': {}, 'water': set()}
        lines = grid.split('\n')[:-1]
        x = 0
        for row in lines:
            ll = row.split()
            y = 0
            for col in ll:
                if col == '##':
                    data['walls'].add((x,y))
                elif col == '()':
                    data['water'].add((x,y))
                elif col != '..':
                    data['pinguins'][col] = (x,y)
                y += 1
            x += 1
        data['dim'] = (len(lines),len(ll))
        return data
    
    
    directions = {"N":(-1, 0), "E":(0, +1), "S":(+1, 0), "O":(0, -1)}  # ortogonais
    
    
    def __init__(self, ice_map=grid):
        initialStatus = self.process_txt(ice_map) # processa o txt e converte num dicionário
        self.initial = EstadoPinguins(initialStatus['pinguins']) # estado inicial
        self.goal = {} # estado vazio
        self.obstacles = initialStatus['walls'] # posições do icebergues
        self.water = initialStatus['water'] # posições da água
        self.dim = initialStatus['dim'] # dimensão do mapa (não precisa de ser quadrado)

    
    def slide(self,state,x,y,d):
        """
        Função que identifica se é possível o pinguim se deslocar numa direção.
        """
        (dx,dy) = self.directions[d]
        if (x+dx,y+dy) in self.obstacles:
            return False
        while (x+dx,y+dy) not in self.obstacles and (x+dx,y+dy) not in state.pinguins.values():
            if (x+dx,y+dy) in self.water:
                return False
            x = x+dx
            y = y+dy
        return True
    
    
    def actions (self, state):
        """
        Devolve uma lista ordenada com todas as ações possíveis para o estado.
        """
        actions_list = []
        for p in state.pinguins.keys():
            x,y = state.pinguins[p] # coordenadas da posição do pinguim 
            if self.slide(state,x,y,"N"): # verifica se o pinguim pode deslocar-se para Norte
                actions_list.append((p,"N"))
            if self.slide(state,x,y,"S"):
                actions_list.append((p,"S"))
            if self.slide(state,x,y,"E"):
                actions_list.append((p,"E"))
            if self.slide(state,x,y,"O"):
                actions_list.append((p,"O"))
        return sorted(actions_list) 
    

    def result (self, state, action):
        """
        Devolve um novo estado resultante de aplicar "action" a "state".
        """
        p,d = action # ação é um tuplo (ID pinguim, direção)
        pinguins = state.pinguins.copy()
        x,y = state.pinguins[p]
        (dx,dy) = self.directions[d]
        # desloca o pinguim até que embata num obstáculo ou noutro pinguim
        while (x+dx,y+dy) not in self.obstacles and (x+dx,y+dy) not in state.pinguins.values():
            x = x+dx
            y = y+dy
        # se o pinguim embateu num obstáculo, atualiza-se a posição do pinguim
        if (x+dx,y+dy) in self.obstacles:
            pinguins[p] = (x,y)
        # se o pinguim embateu noutro pinguim, ambos são removidos do estado
        if (x+dx,y+dy) in state.pinguins.values():
            pinguins.pop(p)
            for key in state.pinguins:
                if state.pinguins[key] == (x+dx,y+dy):
                    pinguins.pop(key)
                    break
        return EstadoPinguins(pinguins)
    

    def goal_test (self, state):
        """
        Verifica se todos os pinguins estão emparelhados, ou seja, se os estado está vazio.
        """
        return state.pinguins == {}
    

    def display (self, state):
        """
        Devolve a grelha em modo txt.
        """
        output = ""
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if (i,j) in state.pinguins.values():
                    for key in state.pinguins:
                        if state.pinguins[key] == (i,j):
                            ch = key
                            break
                elif (i,j) in self.obstacles:
                    ch = "##"
                elif (i,j) in self.water:
                    ch = "()"
                else:
                    ch = ".."
                output += ch + " "
            output += "\n"
        return output
    

    def executa(self, state, actions_list, verbose=False):
        """Executa uma sequência de acções a partir do estado devolvendo o triplo formado pelo estado, 
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
    
    
    def halfPenguins(self, node):
        """Heurística que considera metade do número de pinguins."""
        return len(node.state.pinguins) // 2

    def Npairings(self, node):
        """Heurística que conta o número de pares diretos possíveis, verificando se não há obstáculos (paredes, água ou outros pinguins) entre eles."""
        pinguins = sorted(node.state.pinguins.items())  
        np = 0  # Número de pares possíveis
        visited = set()
    
        for i in range(len(pinguins)):
            if pinguins[i][1] in visited:
                continue
            inutil, (x1, y1) = pinguins[i]
            for j in range(i + 1, len(pinguins)):
                inutil, (x2, y2) = pinguins[j]
                if (x2, y2) in visited:
                    continue
                #linha
                if x1 == x2:
                    if y1 < y2:
                        dih = 1
                    else:
                        dih = -1
                    clear_path = True
                    for y in range(y1 + dih, y2, dih):
                        if (x1, y) in self.obstacles or (x1, y) in self.water or (x1, y) in node.state.pinguins.values():
                            clear_path = False
                            break
                    if clear_path:
                        np += 1
                        visited.add((x1, y1))
                        visited.add((x2, y2))
                        break
                #coluina
                elif y1 == y2:
                    if x1 < x2:
                        div = 1
                    else:
                        div = -1
                    clear_path = True
                    for x in range(x1 + div, x2, div):
                        if (x, y1) in self.obstacles or (x, y1) in self.water or (x, y1) in node.state.pinguins.values():
                            clear_path = False
                            break
                    if clear_path:
                        np += 1
                        visited.add((x1, y1))
                        visited.add((x2, y2))
                        break
                        
        return np + (len(pinguins) - len(visited))
    
    def highestPairings(self, node):
        """Heurística que escolhe os pinguins com maior possibilidade de emparelhamento, verificando caminho livre.
        
        1º - Ordena os pinguins pelo número de emparelhamentos possíveis (maior primeiro).
        2º - Dentro de cada pinguim, ordena os possíveis pares pelo número de emparelhamentos possíveis (maior primeiro).
        3º - Em caso de empate no número de emparelhamentos, ordena pelo ID (menor primeiro).
        """
    
        pinguins = node.state.pinguins.items()
        
        # Passo 1: Contar os emparelhamentos possíveis de cada pinguim
        emparelhamentos = {}
    
        for pid, (x, y) in pinguins:
            pares_possiveis = []
            for other_pid, (ox, oy) in pinguins:
                if pid == other_pid:
                    continue
    
                # Verifica alinhamento horizontal (mesma linha)
                if ox == x and oy != y:
                    dih = 1 if y < oy else -1
                    clear = True
                    for y_pos in range(y + dih, oy, dih):
                        if (x, y_pos) in self.obstacles or (x, y_pos) in self.water or (x, y_pos) in node.state.pinguins.values():
                            clear = False
                            break
                    if clear:
                        pares_possiveis.append(other_pid)
    
                # Verifica alinhamento vertical (mesma coluna)
                if oy == y and ox != x:
                    div = 1 if x < ox else -1
                    clear = True
                    for x_pos in range(x + div, ox, div):
                        if (x_pos, y) in self.obstacles or (x_pos, y) in self.water or (x_pos, y) in node.state.pinguins.values():
                            clear = False
                            break
                    if clear:
                        pares_possiveis.append(other_pid)
    
            emparelhamentos[pid] = pares_possiveis
    
        # Passo 2: Ordenar os pinguins pelo número de emparelhamentos possíveis (decrescente)
        sorted_pinguins = sorted(emparelhamentos.keys(), key=lambda pid: (-len(emparelhamentos[pid]), pid))
    
        # Passo 3: Ordenar a lista de pares possíveis de cada pinguim pelo número de emparelhamentos possíveis (decrescente)
        # Em caso de empate, ordenar pelo ID (crescente)
        for pid in sorted_pinguins:
            emparelhamentos[pid].sort(key=lambda other_pid: (-len(emparelhamentos[other_pid]), other_pid))
    
        np = 0  # Número de pares formados
        visited = set()
    
        # Passo 4: Emparelhar pinguins na ordem correta
        for pid1 in sorted_pinguins:
            if pid1 in visited:
                continue
    
            for pid2 in emparelhamentos[pid1]:
                if pid2 in visited:
                    continue
    
                x1, y1 = node.state.pinguins[pid1]
                x2, y2 = node.state.pinguins[pid2]
    
                # Confirma se o caminho está livre antes de emparelhar
                clear_path = True
                if x1 == x2:  # Mesma linha
                    dih = 1 if y1 < y2 else -1
                    for y in range(y1 + dih, y2, dih):
                        if (x1, y) in self.obstacles or (x1, y) in self.water or (x1, y) in node.state.pinguins.values():
                            clear_path = False
                            break
                elif y1 == y2:  # Mesma coluna
                    vih = 1 if x1 < x2 else -1
                    for x in range(x1 + vih, x2, vih):
                        if (x, y1) in self.obstacles or (x, y1) in self.water or (x, y1) in node.state.pinguins.values():
                            clear_path = False
                            break
    
                if clear_path:
                    np += 1
                    visited.add(pid1)
                    visited.add(pid2)
                    break
    
        nsp = len(node.state.pinguins) - len(visited)
        return np + nsp
