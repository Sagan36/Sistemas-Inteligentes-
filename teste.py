from piguins import *




t1 = PenguinsPairs()
def test_penguin_surrounded_by_water():
    line1 = "## () () () ## () () () ##\n"
    line2 = "## .. .. .. () .. .. .. ##\n"
    line3 = "## .. .. () 00 () .. .. ##\n"
    line4 = "## .. .. () () () .. .. ##\n"
    line5 = "## .. .. () () () .. .. ##\n"
    line6 = "## .. .. () () () .. .. ##\n"
    line7 = "## .. .. .. .. .. .. .. ##\n"
    line8 = "## .. .. .. .. .. .. .. ##\n"
    line9 = "## () () () () () () () ##\n"
    grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    p = PenguinsPairs(grid)
    state = p.initial
    actions = p.actions(state)
    expected_actions = []
    assert actions == expected_actions, f"Expected {expected_actions}, but got {actions}"

def test_penguin_surrounded_by_ice():
    line1 = "## () () () () () () () ##\n"
    line2 = "## .. .. .. .. .. .. .. ##\n"
    line3 = "## .. .. ## 00 ## .. .. ##\n"
    line4 = "## .. .. ## ## ## .. .. ##\n"
    line5 = "## .. .. ## ## ## .. .. ##\n"
    line6 = "## .. .. ## ## ## .. .. ##\n"
    line7 = "## .. .. .. .. .. .. .. ##\n"
    line8 = "## .. .. .. .. .. .. .. ##\n"
    line9 = "## () () () () () () () ##\n"
    grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    p = PenguinsPairs(grid)
    state = p.initial
    actions = p.actions(state)
    expected_actions = []
    assert actions == expected_actions, f"Expected {expected_actions}, but got {actions}"

def test_penguin_at_edge():
    line1 = "## () () () () () () () ##\n"
    line2 = "## .. .. .. .. .. .. .. ##\n"
    line3 = "## 00 .. .. .. .. .. .. ##\n"
    line4 = "## .. .. .. .. .. .. .. ##\n"
    line5 = "## .. .. () () () .. .. ##\n"
    line6 = "## .. .. .. .. .. .. .. ##\n"
    line7 = "## .. .. .. .. .. .. .. ##\n"
    line8 = "## .. .. .. .. .. .. .. ##\n"
    line9 = "## () () () () () () () ##\n"
    grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    p = PenguinsPairs(grid)
    state = p.initial
    actions = p.actions(state)
    expected_actions = [('00', 'E')]
    assert actions == expected_actions, f"Expected {expected_actions}, but got {actions}"

def test_penguin_no_possible_moves():
    line1 = "## () () () () () () () ##\n"
    line2 = "## .. .. .. .. .. .. .. ##\n"
    line3 = "## .. .. ## ## ## .. .. ##\n"
    line4 = "## .. .. ## 00 ## .. .. ##\n"
    line5 = "## .. .. ## ## ## .. .. ##\n"
    line6 = "## .. .. ## ## ## .. .. ##\n"
    line7 = "## .. .. .. .. .. .. .. ##\n"
    line8 = "## .. .. .. .. .. .. .. ##\n"
    line9 = "## () () () () () () () ##\n"
    grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    p = PenguinsPairs(grid)
    state = p.initial
    actions = p.actions(state)
    expected_actions = []
    assert actions == expected_actions, f"Expected {expected_actions}, but got {actions}"

line1 = "## () () () () () () () ##\n"
line2 = "## .. .. .. .. .. .. () ##\n"
line3 = "## .. .. ## ## ## .. .. ##\n"
line4 = "## .. .. ## 00 ## .. .. ##\n"
line5 = "## .. .. ## ## ## .. .. ##\n"
line6 = "## .. .. ## ## ## .. .. ##\n"
line7 = "## .. .. .. .. .. .. .. ##\n"
line8 = "## .. .. .. .. .. .. .. ##\n"
line9 = "## () () () () () () () ##\n"
grid = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
p1 = PenguinsPairs(grid)
p2 = PenguinsPairs()
print(p1.initial == p2.initial)


	
line1 = "## ## ## ## ## ## ## ## ##\n"
line2 = "## .. .. .. .. .. .. .. ##\n"
line3 = "## .. .. .. 00 .. .. .. ##\n"
line4 = "## .. .. .. .. .. .. .. ##\n"
line5 = "## .. .. ## ## ## .. .. ##\n"
line6 = "## .. .. () .. .. .. .. ##\n"
line7 = "## ## .. 01 .. .. .. () ##\n"
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


def test_initial_state():
    p = PenguinsPairs()
    expected_initial = {'00': (2, 4), '01': (6, 4)}
    assert p.initial == expected_initial, f"Expected {expected_initial}, but got {p.initial}"

def test_actions():
    p = PenguinsPairs()
    state = p.initial
    actions = p.actions(state)
    expected_actions = [('00', 'E'), ('00', 'N'), ('00', 'O'), ('01', 'E'), ('01', 'O'), ('01', 'S')]
    assert actions == expected_actions, f"Expected {expected_actions}, but got {actions}"

def test_result():
    p = PenguinsPairs()
    state = p.initial
    action = ('00', 'E')
    new_state = p.result(state, action)
    expected_state = {'00': (2, 7), '01': (6, 4)}
    assert new_state == expected_state, f"Expected {expected_state}, but got {new_state}"

def test_goal_test():
    p = PenguinsPairs()
    state = {}
    assert p.goal_test(state) == True, "Expected True, but got False"
    state = {'00': (2, 4)}
    assert p.goal_test(state) == False, "Expected False, but got True"

def test_display():
    p = PenguinsPairs()
    state = p.initial
    display = p.display(state)
    expected_display = """## ## ## ## ## ## ## ## ##
## .. .. .. .. .. .. .. ##
## .. .. .. 00 .. .. .. ##
## .. .. .. .. .. .. .. ##
## .. .. () () () .. .. ##
## .. .. .. .. .. .. .. ##
## .. .. .. 01 .. .. .. ##
## .. .. .. .. .. .. .. ##
## ## ## ## ## ## ## ## ##
"""
    assert display == expected_display, f"Expected:\n{expected_display}\nBut got:\n{display}"

def test_executa():
    p = PenguinsPairs()
    state = p.initial
    actions_list = [('00', 'E'), ('01', 'S')]
    final_state, cost, goal_reached = p.executa(state, actions_list)
    expected_final_state = {'00': (2, 7), '01': (7, 4)}
    assert final_state == expected_final_state, f"Expected {expected_final_state}, but got {final_state}"
    assert cost == 2, f"Expected cost 2, but got {cost}"
    assert goal_reached == False, f"Expected goal_reached False, but got {goal_reached}"

# Additional tests based on the guide

def test_actions_with_water():
    line1 = "## () () () () () () () ##\n"
    line2 = "## .. .. .. .. .. .. .. ##\n"
    line3 = "## .. .. .. .. .. .. 00 ##\n"
    line4 = "## .. .. .. .. .. .. .. ##\n"
    line5 = "## .. .. () () () .. .. ##\n"
    line6 = "## .. .. .. .. .. .. .. ##\n"
    line7 = "## .. .. .. .. .. .. 01 ##\n"
    line8 = "## .. .. .. .. .. .. .. ##\n"
    line9 = "## () () () () () () () ##\n"
    grid2 = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    p = PenguinsPairs(grid2)
    state = p.initial
    action = ('00', 'S')
    new_state = p.result(state, action)
    expected_state = {}
    assert new_state == expected_state, f"Expected {expected_state}, but got {new_state}"


def test_actions_surrounded_water():
    line1 = "() () () () () () () () ()\n"
    line2 = "() .. .. .. .. .. .. .. ()\n"
    line3 = "() .. .. .. .. .. .. 00 ()\n"
    line4 = "() .. .. .. .. .. .. .. ()\n"
    line5 = "() .. .. () () () .. .. ()\n"
    line6 = "() .. .. .. .. .. .. .. ()\n"
    line7 = "() 01 .. .. .. .. .. .. ()\n"
    line8 = "() .. .. .. .. .. .. .. ()\n"
    line9 = "() () () () () () () () ()\n"
    grid2 = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    p = PenguinsPairs(grid2)
    state = p.initial
    actions = p.actions(state)
    expected_actions = []
    assert actions == expected_actions, f"Expected {expected_actions}, but got {actions}"

def test_result_with_collision():
    p = PenguinsPairs()
    state = p.initial
    actions_list = [('00', 'E'), ('01', 'E'), ('01', 'N')]
    new_state, cost, goal_reached = p.executa(state, actions_list)
    expected_state = {}
    assert new_state == expected_state, f"Expected {expected_state}, but got {new_state}"

def test_actions_surrounded_ice():
    line1 = "## () () () () () () () ##\n"
    line2 = "## .. .. .. .. .. .. ## ##\n"
    line3 = "## .. .. .. .. .. ## 00 ##\n"
    line4 = "## .. .. .. .. .. .. ## ##\n"
    line5 = "## .. .. () () () .. .. ##\n"
    line6 = "## .. .. .. .. .. .. ## ##\n"
    line7 = "## .. .. .. .. .. ## 01 ##\n"
    line8 = "## .. .. .. .. .. .. ## ##\n"
    line9 = "## () () () () () () () ##\n"
    grid2 = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    p = PenguinsPairs(grid2)
    state = p.initial
    actions = p.actions(state)
    expected_actions = []
    assert actions == expected_actions, f"Expected {expected_actions}, but got {actions}"

def test_complete_game():
    line1 = "## () () () () () () () ##\n"
    line2 = "## .. .. .. .. .. .. ## ##\n"
    line3 = "## .. .. .. .. .. .. 00 ##\n"
    line4 = "## 01 .. .. .. .. .. .. ##\n"
    line5 = "## .. .. () () () .. .. ##\n"
    line6 = "## .. .. .. .. .. .. .. ##\n"
    line7 = "## .. .. .. .. .. .. .. ##\n"
    line8 = "## .. .. .. .. .. .. .. ##\n"
    line9 = "## () () () () () () () ##\n"
    grid2 = line1 + line2 + line3 + line4 + line5 + line6 + line7 + line8 + line9
    p = PenguinsPairs(grid2)
    state = p.initial
    new_state, cost, goal = p.executa(state, [("01","E")])
    goal_reached = False
    assert goal_reached == goal, f"Expected {goal_reached}, but got {goal}"


# # Run the tests
test_initial_state()
test_actions()
test_result()
test_goal_test()
test_display()
test_executa()
test_actions_with_water()
test_actions_surrounded_water()
test_result_with_collision()
test_actions_surrounded_ice()
test_complete_game()



print("All tests passed!")

# Run the additional tests
test_penguin_surrounded_by_water()
test_penguin_surrounded_by_ice()
test_penguin_at_edge()
test_penguin_no_possible_moves()

print("Additional tests passed!")