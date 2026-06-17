# # # import networkx as nx

# # # # ======================================
# # # # MEIHUA FOREST GRAPH
# # # # ======================================

# # # graph = {
# # #     1: [2, 4],
# # #     2: [1, 3, 5],
# # #     3: [2, 6],

# # #     4: [1, 5, 7],
# # #     5: [2, 4, 6, 8],
# # #     6: [3, 5, 9],

# # #     7: [4, 8, 10],
# # #     8: [5, 7, 9, 11],
# # #     9: [6, 8, 12],

# # #     10: [7, 11],
# # #     11: [8, 10, 12],
# # #     12: [9, 11]
# # # }

# # # # ======================================
# # # # CREATE NETWORKX GRAPH
# # # # ======================================

# # # G = nx.Graph()

# # # for node in graph:
# # #     for neighbor in graph[node]:
# # #         G.add_edge(node, neighbor)

# # # # ======================================
# # # # MANUALLY DEFINE SCROLLS
# # # # ======================================
# # # #
# # # # real  = real scroll
# # # # fake  = fake scroll
# # # # empty = no scroll
# # # #
# # # # Example:
# # # #
# # # # block 3 -> fake
# # # # block 5 -> real
# # # #

# # # forest_state = {
# # #     1: "real",
# # #     2: "empty",
# # #     3: "empty",

# # #     4: "fake",
# # #     5: "real",
# # #     6: "r1",

# # #     7: "empty",
# # #     8: "real",
# # #     9: "real",

# # #     10: "empty",
# # #     11: "empty",
# # #     12: "empty"
# # # }

# # # # ======================================
# # # # INITIAL ROBOT STATE
# # # # ======================================

# # # current_block = 1
# # # carrying = 0

# # # # ======================================
# # # # FIND NEAREST REAL SCROLL
# # # # ======================================

# # # def choose_next_target(current_block):

# # #     real_blocks = []

# # #     for block, value in forest_state.items():

# # #         if value == "real":
# # #             real_blocks.append(block)

# # #     if len(real_blocks) == 0:
# # #         return None

# # #     best_target = None
# # #     shortest_length = 999

# # #     for target in real_blocks:

# # #         try:
# # #             path = nx.shortest_path(
# # #                 G,
# # #                 current_block,
# # #                 target
# # #             )

# # #             if len(path) < shortest_length:

# # #                 shortest_length = len(path)
# # #                 best_target = target

# # #         except:
# # #             pass

# # #     return best_target

# # # # ======================================
# # # # MAIN LOOP
# # # # ======================================

# # # while True:

# # #     print("\n========================")
# # #     print("Current Block:", current_block)

# # #     target = choose_next_target(current_block)

# # #     if target is None:

# # #         print("No more real scrolls")

# # #         break

# # #     print("Target Scroll Block:", target)

# # #     # shortest path

# # #     path = nx.shortest_path(
# # #         G,
# # #         current_block,
# # #         target
# # #     )

# # #     print("Path:", path)

# # #     # ======================================
# # #     # MOVE STEP BY STEP
# # #     # ======================================

# # #     for next_block in path[1:]:

# # #         print(f"Moving to block {next_block}")

# # #         current_block = next_block

# # #     # ======================================
# # #     # PICKUP
# # #     # ======================================

# # #     if forest_state[current_block] == "real":

# # #         print("Picked REAL scroll")

# # #         forest_state[current_block] = "collected"

# # #         carrying += 1

# # #     elif forest_state[current_block] == "fake":

# # #         print("ERROR: touched fake scroll")

# # #         break

# # #     print("Carrying:", carrying)

# # #     # ======================================
# # #     # EXIT CONDITION
# # #     # ======================================

# # #     if carrying >= 2:

# # #         exits = [10, 11, 12]

# # #         best_exit = None
# # #         best_length = 999

# # #         for exit_block in exits:

# # #             try:

# # #                 exit_path = nx.shortest_path(
# # #                     G,
# # #                     current_block,
# # #                     exit_block
# # #                 )

# # #                 if len(exit_path) < best_length:

# # #                     best_length = len(exit_path)
# # #                     best_exit = exit_block

# # #             except:
# # #                 pass

# # #         print("\nEXITING FOREST")
# # #         print("Exit Block:", best_exit)

# # #         exit_path = nx.shortest_path(
# # #             G,
# # #             current_block,
# # #             best_exit
# # #         )

# # #         print("Exit Path:", exit_path)

# # #         break

# # import numpy as np
# # import random

# # # =========================================
# # # FOREST GRAPH
# # # =========================================

# # graph = {
# #     1: [2, 4],
# #     2: [1, 3, 5],
# #     3: [2, 6],

# #     4: [1, 5, 7],
# #     5: [2, 4, 6, 8],
# #     6: [3, 5, 9],

# #     7: [4, 8, 10],
# #     8: [5, 7, 9, 11],
# #     9: [6, 8, 12],

# #     10: [7, 11],
# #     11: [8, 10, 12],
# #     12: [9, 11]
# # }

# # # =========================================
# # # FOREST STATE
# # # =========================================

# # forest_state = {
# #     1: "real",
# #     2: "empty",
# #     3: "fake",

# #     4: "real",
# #     5: "real",
# #     6: "empty",

# #     7: "empty",
# #     8: "real",
# #     9: "empty",

# #     10: "exit",
# #     11: "exit",
# #     12: "exit"
# # }

# # # =========================================
# # # PARAMETERS
# # # =========================================

# # alpha = 0.1       # learning rate
# # gamma = 0.9       # discount
# # epsilon = 0.2     # exploration

# # episodes = 10

# # # =========================================
# # # Q TABLE
# # # state = current block
# # # action = next block
# # # =========================================

# # Q = {}

# # for state in graph:

# #     Q[state] = {}

# #     for action in graph[state]:

# #         Q[state][action] = 0

# # # =========================================
# # # REWARD FUNCTION
# # # =========================================

# # def get_reward(block, carrying):

# #     tile = forest_state[block]

# #     if tile == "real":
# #         return 100

# #     elif tile == "fake":
# #         return -300

# #     elif tile == "exit":

# #         if carrying >= 2:
# #             return 200
# #         else:
# #             return -50

# #     else:
# #         return -1

# # # =========================================
# # # TRAINING
# # # =========================================

# # for episode in range(episodes):

# #     current_block = 1
# #     carrying = 0

# #     collected = set()

# #     done = False

# #     while not done:

# #         # =================================
# #         # ACTION SELECTION
# #         # =================================

# #         possible_actions = graph[current_block]

# #         if random.uniform(0,1) < epsilon:

# #             # explore
# #             next_block = random.choice(possible_actions)

# #         else:

# #             # exploit
# #             next_block = max(
# #                 Q[current_block],
# #                 key=Q[current_block].get
# #             )

# #         # =================================
# #         # REWARD
# #         # =================================

# #         reward = get_reward(next_block, carrying)

# #         # collect scroll only once

# #         if (
# #             forest_state[next_block] == "real"
# #             and next_block not in collected
# #         ):

# #             carrying += 1
# #             collected.add(next_block)

# #         # =================================
# #         # Q UPDATE
# #         # =================================

# #         old_q = Q[current_block][next_block]

# #         next_max = max(Q[next_block].values())

# #         new_q = old_q + alpha * (
# #             reward +
# #             gamma * next_max -
# #             old_q
# #         )

# #         Q[current_block][next_block] = new_q

# #         # =================================
# #         # MOVE
# #         # =================================

# #         current_block = next_block

# #         # =================================
# #         # TERMINATION
# #         # =================================

# #         if reward == -300:
# #             done = True

# #         if (
# #             forest_state[current_block] == "exit"
# #             and carrying >= 2
# #         ):
# #             done = True

# # # =========================================
# # # TEST TRAINED AGENT
# # # =========================================

# # print("\n========================")
# # print("TRAINED POLICY")
# # print("========================")

# # current_block = 1
# # carrying = 0
# # visited = set()

# # while True:

# #     print("\nCurrent Block:", current_block)

# #     action = max(
# #         Q[current_block],
# #         key=Q[current_block].get
# #     )

# #     print("Chosen Move:", action)

# #     current_block = action

# #     tile = forest_state[current_block]

# #     print("Tile:", tile)

# #     if tile == "real" and current_block not in visited:

# #         carrying += 1
# #         visited.add(current_block)

# #         print("Collected REAL scroll")

# #     if tile == "fake":

# #         print("FAILED: touched fake")

# #         break

# #     print("Carrying:", carrying)

# #     if tile == "exit" and carrying >= 2:

# #         print("\nSUCCESSFULLY EXITED")

# #         break

# import numpy as np
# import random

# # =========================================
# # FOREST GRAPH
# # =========================================

# graph = {
#     1: [2, 4],
#     2: [1, 3, 5],
#     3: [2, 6],

#     4: [1, 5, 7],
#     5: [2, 4, 6, 8],
#     6: [3, 5, 9],

#     7: [4, 8, 10],
#     8: [5, 7, 9, 11],
#     9: [6, 8, 12],

#     10: [7, 11],
#     11: [8, 10, 12],
#     12: [9, 11]
# }

# # =========================================
# # FOREST STATE
# # =========================================

# forest_state = {
#     1: "real",
#     2: "empty",
#     3: "fake",

#     4: "real",
#     5: "real",
#     6: "empty",

#     7: "empty",
#     8: "real",
#     9: "empty",

#     10: "exit",
#     11: "exit",
#     12: "exit"
# }

# # =========================================
# # PARAMETERS
# # =========================================

# alpha = 0.1       # learning rate
# gamma = 0.9       # future reward importance
# epsilon = 0.3     # exploration chance

# episodes = 10

# # NEW
# max_steps = 15

# # =========================================
# # Q TABLE
# # =========================================

# Q = {}

# for state in graph:

#     Q[state] = {}

#     for action in graph[state]:

#         Q[state][action] = 0

# # =========================================
# # REWARD FUNCTION
# # =========================================

# def get_reward(block, carrying):

#     tile = forest_state[block]

#     # REAL SCROLL

#     if tile == "real":
#         return 100

#     # FAKE SCROLL

#     elif tile == "fake":
#         return -300

#     # EXIT

#     elif tile == "exit":

#         if carrying >= 2:
#             return 200
#         else:
#             return -50

#     # EMPTY TILE

#     else:
#         return -1

# # =========================================
# # TRAINING
# # =========================================

# for episode in range(episodes):

#     print(f"\n========== EPISODE {episode+1} ==========")

#     current_block = 1
#     carrying = 0

#     collected = set()

#     done = False

#     # NEW
#     steps = 0

#     # CHANGED
#     while not done and steps < max_steps:

#         print("\nCurrent Block:", current_block)

#         possible_actions = graph[current_block]

#         # =================================
#         # EXPLORE OR EXPLOIT
#         # =================================

#         if random.uniform(0,1) < epsilon:

#             # RANDOM MOVE

#             next_block = random.choice(possible_actions)

#             print("Exploring...")

#         else:

#             # BEST KNOWN MOVE

#             next_block = max(
#                 Q[current_block],
#                 key=Q[current_block].get
#             )

#             print("Using learned policy...")

#         print("Moving To:", next_block)

#         # =================================
#         # REWARD
#         # =================================

#         reward = get_reward(next_block, carrying)

#         print("Reward:", reward)

#         # =================================
#         # COLLECT REAL SCROLL
#         # =================================

#         if (
#             forest_state[next_block] == "real"
#             and next_block not in collected
#         ):

#             carrying += 1
#             collected.add(next_block)

#             print("Collected REAL scroll")

#         # =================================
#         # Q UPDATE
#         # =================================

#         old_q = Q[current_block][next_block]

#         next_max = max(Q[next_block].values())

#         new_q = old_q + alpha * (
#             reward +
#             gamma * next_max -
#             old_q
#         )

#         Q[current_block][next_block] = new_q

#         print(
#             f"Updated Q[{current_block}][{next_block}] =",
#             round(new_q, 2)
#         )

#         # =================================
#         # MOVE ROBOT
#         # =================================

#         current_block = next_block

#         print("Carrying:", carrying)

#         # =================================
#         # TERMINATION CONDITIONS
#         # =================================

#         # HIT FAKE

#         if reward == -300:

#             print("FAILED: touched fake scroll")

#             done = True

#         # SUCCESSFUL EXIT

#         if (
#             forest_state[current_block] == "exit"
#             and carrying >= 2
#         ):

#             print("SUCCESSFULLY EXITED")

#             done = True

#         # =================================
#         # STEP LIMIT
#         # =================================

#         steps += 1

#     print("\nEpisode Finished")

# # =========================================
# # SHOW FINAL Q TABLE
# # =========================================

# print("\n========================")
# print("FINAL Q TABLE")
# print("========================")

# for state in Q:

#     print(f"\nState {state}")

#     for action in Q[state]:

#         print(
#             f"  -> {action}:",
#             round(Q[state][action], 2)
#         )

# # =========================================
# # TEST TRAINED AGENT
# # =========================================

# print("\n========================")
# print("TESTING TRAINED AGENT")
# print("========================")

# current_block = 1
# carrying = 0

# visited = set()

# # NEW
# test_steps = 0
# max_test_steps = 20

# # CHANGED
# while test_steps < max_test_steps:

#     print("\nCurrent Block:", current_block)

#     action = max(
#         Q[current_block],
#         key=Q[current_block].get
#     )

#     print("Chosen Move:", action)

#     current_block = action

#     tile = forest_state[current_block]

#     print("Tile:", tile)

#     # =====================================
#     # COLLECT REAL
#     # =====================================

#     if tile == "real" and current_block not in visited:

#         carrying += 1
#         visited.add(current_block)

#         print("Collected REAL scroll")

#     # =====================================
#     # FAKE
#     # =====================================

#     if tile == "fake":

#         print("FAILED: touched fake")

#         break

#     print("Carrying:", carrying)

#     # =====================================
#     # SUCCESS EXIT
#     # =====================================

#     if tile == "exit" and carrying >= 2:

#         print("\nSUCCESSFULLY EXITED")

#         break

#     # NEW
#     test_steps += 1

# # =========================================
# # TEST LIMIT REACHED
# # =========================================

# if test_steps >= max_test_steps:
#     print("\nSTOPPED: max test steps reached")

import numpy as np
import random

# =========================================
# FOREST GRAPH
# =========================================

graph = {
    1: [2, 4],
    2: [1, 3, 5],
    3: [2, 6],

    4: [1, 5, 7],
    5: [2, 4, 6, 8],
    6: [3, 5, 9],

    7: [4, 8, 10],
    8: [5, 7, 9, 11],
    9: [6, 8, 12],

    10: [7, 11],
    11: [8, 10, 12],
    12: [9, 11]
}

# =========================================
# FOREST STATE
# =========================================
#
# real  = real scroll
# fake  = fake scroll
# empty = no scroll
# exit  = exit block
#
# MODIFY THIS TO TEST DIFFERENT CASES
#

forest_state = {
    1: "real",
    2: "empty",
    3: "fake",

    4: "real",
    5: "real",
    6: "empty",

    7: "empty",
    8: "real",
    9: "empty",

    10: "exit",
    11: "exit",
    12: "exit"
}

# =========================================
# RL PARAMETERS
# =========================================

alpha = 0.1       # learning rate
gamma = 0.9       # future reward importance
epsilon = 0.3     # exploration chance

episodes = 10
max_steps = 15

# =========================================
# Q TABLE
# =========================================

Q = {}

for state in graph:

    Q[state] = {}

    for action in graph[state]:

        Q[state][action] = 0

# =========================================
# REWARD FUNCTION
# =========================================

def get_reward(block, carrying):

    tile = forest_state[block]

    # REAL SCROLL

    if tile == "real":
        return 100

    # FAKE SCROLL

    elif tile == "fake":
        return -300

    # EXIT BLOCK

    elif tile == "exit":

        if carrying >= 2:
            return 200
        else:
            return -50

    # EMPTY BLOCK

    else:
        return -1

# =========================================
# TRAINING
# =========================================

for episode in range(episodes):

    print(f"\n========== EPISODE {episode+1} ==========")

    current_block = 1
    carrying = 0

    collected = set()

    done = False

    steps = 0

    while not done and steps < max_steps:

        print("\nCurrent Block:", current_block)

        possible_actions = graph[current_block]

        # =================================
        # EXPLORE OR EXPLOIT
        # =================================

        if random.uniform(0,1) < epsilon:

            # RANDOM ACTION

            next_block = random.choice(possible_actions)

            print("Exploring...")

        else:

            # BEST KNOWN ACTION

            next_block = max(
                Q[current_block],
                key=Q[current_block].get
            )

            print("Using learned policy...")

        print("Moving To:", next_block)

        # =================================
        # REWARD
        # =================================

        reward = get_reward(next_block, carrying)

        print("Reward:", reward)

        # =================================
        # COLLECT REAL SCROLL
        # =================================

        if (
            forest_state[next_block] == "real"
            and next_block not in collected
        ):

            carrying += 1
            collected.add(next_block)

            print("Collected REAL scroll")

        # =================================
        # Q UPDATE
        # =================================

        old_q = Q[current_block][next_block]

        next_max = max(Q[next_block].values())

        new_q = old_q + alpha * (
            reward +
            gamma * next_max -
            old_q
        )

        Q[current_block][next_block] = new_q

        print(
            f"Updated Q[{current_block}][{next_block}] =",
            round(new_q, 2)
        )

        # =================================
        # MOVE ROBOT
        # =================================

        current_block = next_block

        print("Carrying:", carrying)

        # =================================
        # TERMINATION CONDITIONS
        # =================================

        # TOUCHED FAKE

        if reward == -300:

            print("FAILED: touched fake scroll")

            done = True

        # SUCCESS EXIT

        if (
            forest_state[current_block] == "exit"
            and carrying >= 2
        ):

            print("SUCCESSFULLY EXITED")

            done = True

        # STEP COUNTER

        steps += 1

    print("\nEpisode Finished")

# =========================================
# SHOW FINAL Q TABLE
# =========================================

print("\n========================")
print("FINAL Q TABLE")
print("========================")

for state in Q:

    print(f"\nState {state}")

    for action in Q[state]:

        print(
            f"  -> {action}:",
            round(Q[state][action], 2)
        )

# =========================================
# FINAL R2 PATH TRAVERSAL
# =========================================

print("\n========================")
print("FINAL R2 PATH")
print("========================")

current_block = 1
carrying = 0

visited = set()

test_steps = 0
max_test_steps = 20

# STORE COMPLETE PATH

final_path = [current_block]

while test_steps < max_test_steps:

    # =====================================
    # CHOOSE BEST ACTION
    # =====================================

    action = max(
        Q[current_block],
        key=Q[current_block].get
    )

    # MOVE

    current_block = action

    # STORE PATH

    final_path.append(current_block)

    tile = forest_state[current_block]

    # =====================================
    # COLLECT REAL SCROLL
    # =====================================

    if (
        tile == "real"
        and current_block not in visited
    ):

        carrying += 1
        visited.add(current_block)

    # =====================================
    # TOUCHED FAKE
    # =====================================

    if tile == "fake":

        print("\nFAILED: touched fake scroll")
        break

    # =====================================
    # SUCCESSFUL EXIT
    # =====================================

    if tile == "exit" and carrying >= 2:

        print("\nSUCCESSFULLY EXITED")
        break

    test_steps += 1

# =========================================
# FINAL RESULTS
# =========================================

print("\nFinal Traversal Path:")

print(" -> ".join(map(str, final_path)))

print("\nTotal Real Scrolls Collected:", carrying)

print("Total Steps:", len(final_path)-1)

if test_steps >= max_test_steps:

    print("\nSTOPPED: maximum test steps reached")