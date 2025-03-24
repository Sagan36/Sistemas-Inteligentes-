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

# Estado dos pinguins
EstadoPin = namedtuple('EstadoPin', 'pinguins')

class EstadoPinguins(EstadoPin):
    def __hash__(self):
        return hash(tuple(sorted(self.pinguins.items())))

    def __lt__(self, other):
        return True

class PenguinsPairs(Problem):

    def process_txt(self, grid):
        """Processa a grelha e obtém as posições dos icebergues (walls), água e pinguins."""
        data = {'walls': set(), 'pinguins': {}, 'water': set()}
        lines = grid.strip().split('\n')
        for x, row in enumerate(lines):
            for y, col in enumerate(row.split()):
                if col == '##':
                    data['walls'].add((x, y))
                elif col == '()':
                    data['water'].add((x, y))
                elif col != '..':
                    data['pinguins'][col] = (x, y)
        data['dim'] = (len(lines), len(lines[0].split()))
        return data

    directions = {"N": (-1, 0), "E": (0, +1), "S": (+1, 0), "O": (0, -1)}

    def __init__(self, ice_map=grid):
        initialStatus = self.process_txt(ice_map)
        self.initial = EstadoPinguins(initialStatus['pinguins'])
        self.goal = {}
        self.obstacles = initialStatus['walls']
        self.water = initialStatus['water']
        self.dim = initialStatus['dim']

    def slide(self, state, x, y, d):
        """Verifica se um pinguim pode se deslocar numa direção."""
        (dx, dy) = self.directions[d]
        if (x + dx, y + dy) in self.obstacles:
            return False
        while (x + dx, y + dy) not in self.obstacles and (x + dx, y + dy) not in state.pinguins.values():
            if (x + dx, y + dy) in self.water:
                return False
            x += dx
            y += dy
        return True

    def actions(self, state):
        """Devolve uma lista ordenada com todas as ações possíveis para o estado."""
        actions_list = []
        for p in state.pinguins.keys():
            x, y = state.pinguins[p]
            for d in self.directions.keys():
                if self.slide(state, x, y, d):
                    actions_list.append((p, d))
        
        return sorted(actions_list, key=lambda x: int(x[0]))  # Ordena por número do pinguim

    def result(self, state, action):
        """Aplica uma ação ao estado e retorna o novo estado."""
        p, d = action
        pinguins = state.pinguins.copy()
        x, y = pinguins[p]
        (dx, dy) = self.directions[d]
    
        while (x + dx, y + dy) not in self.obstacles and (x + dx, y + dy) not in state.pinguins.values():
            x += dx
            y += dy
    
        if (x + dx, y + dy) in state.pinguins.values():  # Se encontrou outro pinguim
            for key in list(pinguins.keys()):
                if pinguins[key] == (x + dx, y + dy) or key == p:
                    del pinguins[key]  # Remove ambos os pinguins
        
        else:  # Se não encontrou par, apenas move
            pinguins[p] = (x, y)

        return EstadoPinguins(pinguins)

    def goal_test(self, state):
        """Verifica se todos os pinguins estão emparelhados."""
        return state.pinguins == {}

    def display(self, state):
        """Devolve a grelha em modo txt."""
        output = ""
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if (i, j) in state.pinguins.values():
                    for key in state.pinguins:
                        if state.pinguins[key] == (i, j):
                            ch = key
                            break
                elif (i, j) in self.obstacles:
                    ch = "##"
                elif (i, j) in self.water:
                    ch = "()"
                else:
                    ch = ".."
                output += ch + " "
            output += "\n"
        return output

    def halfPenguins(self, node):
        """Heurística que considera metade do número de pinguins."""
        return len(node.state.pinguins) // 2

    def Npairings(self, node):
        """Heurística que conta o número de pares diretos possíveis."""
        pinguins = sorted(node.state.pinguins.values())  
        np = 0  # Número de pares possíveis
        nsp = len(pinguins)  # Número de pinguins sem par
    
        visited = set()
        
        for i in range(len(pinguins)):
            if pinguins[i] in visited:
                continue
            x1, y1 = pinguins[i]
    
            for j in range(i + 1, len(pinguins)):
                x2, y2 = pinguins[j]
    
                if (x2, y2) in visited:
                    continue
    
                if x1 == x2:  # Mesma linha
                    if all((x1, y) not in self.obstacles and (x1, y) not in self.water
                           for y in range(min(y1, y2) + 1, max(y1, y2))):
                        np += 1
                        visited.add((x1, y1))
                        visited.add((x2, y2))
                        break
    
                elif y1 == y2:  # Mesma coluna
                    if all((x, y1) not in self.obstacles and (x, y1) not in self.water
                           for x in range(min(x1, x2) + 1, max(x1, x2))):
                        np += 1
                        visited.add((x1, y1))
                        visited.add((x2, y2))
                        break
    
        return np + (len(pinguins) - len(visited))  # Pares encontrados + pinguins restantes

    def highestPairings(self, node):
        """Heurística que escolhe os pinguins com maior possibilidade de emparelhamento."""
        pinguins = sorted(node.state.pinguins.items(), key=lambda x: x[0])
        emparelhamentos = {}
        for pid, (x, y) in pinguins:
            emparelhamentos[pid] = sum(1 for _, (xi, yi) in pinguins if (xi == x or yi == y) and (xi, yi) != (x, y))

        sorted_pinguins = sorted(emparelhamentos.items(), key=lambda item: (-item[1], item[0]))
        np = 0
        nsp = len(sorted_pinguins)

        while sorted_pinguins:
            pid1, _ = sorted_pinguins.pop(0)
            for i, (pid2, _) in enumerate(sorted_pinguins):
                if node.state.pinguins[pid1][0] == node.state.pinguins[pid2][0] or \
                   node.state.pinguins[pid1][1] == node.state.pinguins[pid2][1]:
                    np += 1
                    nsp -= 2
                    del sorted_pinguins[i]
                    break

        return np + nsp
