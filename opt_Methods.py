import pandas as pd
import csv
from scipy.spatial import distance
from itertools import combinations, permutations
import numpy as np
import math

file_name = "Instance.csv"
with open(file_name) as fd:
    reader = csv.reader(fd)
    interesting_rows = [row for idx, row in enumerate(reader) if idx in (0, 1, 2, 5, 7)]
fd.close()

# print(interesting_rows)

vehicles = int(interesting_rows[0][1])
max_capacity = int(interesting_rows[1][1])
max_duration = int(interesting_rows[2][1])
depot_position = (float(interesting_rows[3][1]), float(interesting_rows[3][2]))
# print(depot)
customers = int(interesting_rows[4][1])

# a = (1, 3)
# b = (4, 7)
# dst = distance.euclidean(a, b)
# print(dst)


# print(interesting_rows)
df = pd.read_csv(file_name, skiprows=10, index_col=0)
# min_service_time = df.sort_values(by=["Service Time"], inplace=True)
# print(df)

#find the min service time of node so as to calculate how many nodes vehicles can visit
# service_time_limit = df["Service Time"].min()
service_time_limit = df["Service Time"].mean()
max_nodes_to_visit = math.ceil(max_duration/service_time_limit)
print(max_nodes_to_visit)
# print(type(max_nodes_to_visit))
# print(service_time_limit)

# qapacity_limit = df["Demand"].min()
qapacity_limit = df["Demand"].mean()
# print(qapacity_limit)
max_qapacity_to_load = math.ceil(max_capacity/qapacity_limit)
print(max_qapacity_to_load)

#nodes that vehicles can visit can be under the number of the min(max_nodes_to_visit, max_qapacity_to_load)
min_value = max_qapacity_to_load
if max_nodes_to_visit < max_qapacity_to_load:
    min_value = max_nodes_to_visit
# remaining_time = max_duration - [(max_nodes_to_visit)*(service_time_limit)]
# remaining_time = max_duration - (max_qapacity_to_load)*(service_time_limit)
remaining_time = max_duration - min_value * service_time_limit
print(remaining_time)



# #but we have to go back to the depot
remaining_time = remaining_time/2
print(remaining_time)


max_profit = df["Profit"].max()
print(max_profit)

paok

# df['Position'] = df.apply(lambda row: (row["x"], row["y"]), axis=1)
# df.drop(['x', 'y'], axis=1, inplace=True)
nodes = df.T.to_dict()

# print(nodes)
# print(nodes[1]["Demand"])
# for key in nodes.keys():
#     print(key)


combinations_nodes = []
for i in range(len(nodes), 0, -1):
    comb = list(combinations(nodes.keys(), i))
    combinations_nodes += comb

    # cap = 0
    # service_time = 0
    # print(str(i) + "......")
    # print(comb)

# print(combinations_nodes)


# print(len(combinations_nodes))

print("Flag1")
for tup in combinations_nodes.copy():
    # print(tup)
    cap = 0
    service_time = 0
    for element in tup:
        # print(str(element) + ":::::")
        # print(nodes[element]["Demand"])
        cap += nodes[element]["Demand"]
        # print(nodes[element]["Service Time"])
        service_time += nodes[element]["Service Time"]
        if cap > max_capacity or service_time > max_duration:
            combinations_nodes.remove(tup)
            break

    # print(cap, service_time)
    # if cap > max_capacity or service_time > max_duration:
    #     combinations_nodes.remove(tup)

# print(combinations_nodes)


permutations_nodes = []
print("Flag2")
for tup in combinations_nodes:
    perm = list(permutations(tup))
    print(perm)
    permutations_nodes += perm

print("Flag3")
print(permutations_nodes)

nodes[0] = {"Position": depot_position}
solutions = []
dinstances = {}

for permutation in permutations_nodes:
    permutation_distances = sum(nodes.get(tuple_value)["Service Time"] for tuple_value in permutation)
    complete_permutation = (0,) + permutation + (0,)
    for tuple_index in range(len(complete_permutation) - 1):
        dinstances_key = tuple(sorted(complete_permutation[tuple_index:(tuple_index + 2)]))
        # print(dinstances_key)
        dst = dinstances.get(dinstances_key)

        if dst == None:
            dinstances[dinstances_key] = dst = distance.euclidean(nodes.get(dinstances_key[0])["Position"],
                                                                  nodes.get(dinstances_key[1])["Position"])
        permutation_distances += dst

    if permutation_distances <= max_duration:
        solutions.append([complete_permutation, sum(nodes.get(tuple_value)["Profit"] for tuple_value in permutation)])

print(dinstances)
final_solutions = np.array(solutions)[np.argsort(np.array(solutions)[:, 1])]
print(final_solutions)

# print(max_duration)

# paok

time_limit_matrix = []
# print(len(nodes))


for node1 in range(len(nodes)):
    for node2 in range(len(nodes)):
        pass
        # print(node)

# a = (1, 3)

# b = (4, 7)

# dst = distance.euclidean(a, b)

# print(dst)


for tup in permutations_nodes:
    service_time = 0

# def get_demand_time():

#     for tup in combinations_nodes:

#         print(tup)

#         cap = 0

#         service_time = 0

#         for element in tup:

#             print(str(element) + ":::::")

#             # print(nodes[element]["Demand"])

#             cap += nodes[element]["Demand"]

#             # print(nodes[element]["Service Time"])

#             service_time += nodes[element]["Service Time"]

#             # print(cap, service_time)

#

#

# get_demand_time()


# print(len(comb))

# for lst in range(len(comb)):

#     temp = list((int(j) for i in comb for j in i))

#     print(len(temp))

#     cap = 0

#     service_time = 0

#     for elements in range(len(temp)):

#         print("------------------------")

#         print(elements)

#     print("------------------------")

# print(nodes[elements]["Demand"])

# cap += nodes[elements]["Demand"]

# for lst in range(len(comb[i])):

#     print(lst)


# print(type(comb))

# print(comb[3])


# for lst in comb:

#     # print(lst)

#     # print(lst[2])

#     cap = 0

#     service_time = 0

#     for i in range(len(lst)):

#         pass

# print(i)

# cap += nodes[i]["Demand"]

# print(nodes[1]["Demand"])

# print(cap)