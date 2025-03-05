from searchPlus import Problem

# Representação do mapa da ilha com gelo, água e icebergues.
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
                pinguins.append((x,y-1))
                pinguins.append(char)
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
        self.state = [line.split() for line in ice_map.strip().split('\n')]  # Representação do mapa como lista de listas
        self.initial = coordenadas(ice_map)[1]  # Posições dos pinguins
        self.data = coordenadas(ice_map)  # Informações sobre água, pinguins, icebergs, e espaços livres
        super().__init__(self.initial)
    
    def actions(self, state):
        """Retorna os movimentos possíveis para cada pinguim."""
        movimentos = []
        tuplos = []
        for item in self.data[1]: #Retirar o tuplo com as coordenadas do pinguim que se encontra na lista juntamente com o id do mesmo
            if isinstance(item, tuple):
                tuplos.append(item)
        for i, j in tuplos:  # Para cada pinguim
                for direcao in sorted(['N', 'S', 'E', 'O']):
                    if self.valid_move(state, i, j, direcao):
                        movimentos.append(((i, j), direcao))
        return movimentos
    
    def valid_move(self, state, x, y, direcao):
        """Verifica se um pinguim pode deslizar até encontrar um obstáculo ou outro pinguim."""
        movimentos = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
        dx, dy = movimentos[direcao]
        nx, ny = x, y  # Mantém as coordenadas iniciais do pinguim
        
        while True:
            nx += dx
            ny += dy
            
            # Verifica se saiu dos limites do mapa
            if not (0 <= nx < len(self.state) and 0 <= ny < len(self.state[0])):
                return (nx - dx, ny - dy)  # Retorna a posição antes de sair dos limites
            
            celula = self.state[nx][ny]
            
            # Se encontrar um icebergue, o pinguim para na posição anterior
            if celula == "##":
                return (nx - dx, ny - dy)
            
            # Se encontrar água, o pinguim morre e o movimento não é válido
            if celula == "()":
                return None
            
            # Se encontrar outro pinguim, verifica se é um emparelhamento válido
            if celula.isdigit():
                return (nx, ny)  # Pinguins emparelhados
            
            return (nx, ny)

    def result(self, state, action):
        """Aplica uma ação ao estado e retorna o novo estado."""
        (x, y), direcao = action
        new_state = [row.copy() for row in state] 
        movimentos = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}
        dx, dy = movimentos[direcao]
        nx, ny = x + dx, y + dy
        
        new_state[x][y] = ".."  
        new_state[nx][ny] = state[x][y]  # O pinguim vai para a nova posição
        
        return tuple(tuple(row) for row in new_state)  # Retorna o novo estado

    def goal_test(self, state):
        """Verifica se todos os pinguins estão emparelhados."""
        pass

    def display(self, state):
        """Exibe o estado da ilha."""
        return "\n".join(" ".join(row) for row in state)

    def executa(self, state, actions_list, verbose=False):
        """Executa uma sequência de ações a partir do estado devolvendo o triplo formado pelo estado final, 
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
    

# Criar uma instância do problema com a tua grid original
penguin_test = PenguinsPairs(grid)

# Definir coordenadas iniciais dos pinguins
pinguins = coordenadas(grid)[1]  # Obtém as posições dos pinguins

test_cases = [
    (pinguins[1], "N"),  # Deve ser None (não pode subir)
    (pinguins[1], "S"),  # Deve deslizar para baixo até parar
    (pinguins[1], "E"),  # Deve deslizar para a direita até parar
    (pinguins[1], "O"),  # Deve deslizar para a esquerda até parar
]

# Executar os testes
for (x, y), direction in test_cases:
    result = penguin_test.valid_move(penguin_test.initial, x, y, direction)
    print(f"Pinguim em ({x},{y}) movendo-se para {direction}: {result}")
