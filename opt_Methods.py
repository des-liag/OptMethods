import pandas as pd
import csv
from scipy.spatial import distance
from itertools import combinations, permutations
import numpy as np
import math
import time

start_time = time.perf_counter()
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
df['Distance from 0'] = df.apply(lambda row : distance.euclidean(depot_position, (row["x"], row["y"])), axis=1)
df['Position'] = df.apply(lambda row: (row["x"], row["y"]), axis=1)
# df.drop(['x', 'y'], axis=1, inplace=True)
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

min_distance = df['Distance from 0'].min()
mean_distance = df['Distance from 0'].mean()

# #but we have to go back to the depot
remaining_time = remaining_time/2 - min_distance
print("Remaining time")
print(remaining_time)


max_profit = df["Profit"].max()
print(max_profit)



#For every track

# df['Position'] = df.apply(lambda row: (row["x"], row["y"]), axis=1)
# df.drop(['x', 'y'], axis=1, inplace=True)
fltered_df = df[df['Distance from 0'] <= remaining_time]
print(fltered_df)
fltered_df.loc[0] = [depot_position[0], depot_position[1], 0, 0, 0, 0, depot_position]
for node in fltered_df.index:
    if node != 0:
        position = fltered_df.loc[node]["Position"]
        fltered_df['Distance from ' + str(node)] = fltered_df.apply(lambda row : distance.euclidean(position, (row["x"], row["y"])), axis=1)
# print(fltered_df)

nodes = fltered_df.T.to_dict()
print("Number of possible nodes")
print(len(nodes))

# print(nodes)
# print(nodes[1]["Demand"])
# for key in nodes.keys():
#     print(key)
# nodes[0] = {"Position": depot_position, "Demand" : 0, "Service Time": 0, "Distance from 0": 0}
w1 = 1
w2 = 1
w3 = 1
w4 = 2
solution_found = False

solution = [0]
while not solution_found:
    qualities = []
    for node in nodes.keys():
        if node not in solution:
            print("Node = " + str(node))
            # print(nodes.get(node))
            q1 = w1 * (1-nodes.get(node)["Demand"] / fltered_df["Demand"].max())
            q2 = w2 * (1-nodes.get(node)["Service Time"] / fltered_df["Service Time"].max())
            q3 = w3 * (1-nodes.get(solution[-1])["Distance from " + str(node)] / fltered_df["Distance from " + str(node)].max())
            q4 = w4 * (nodes.get(node)["Profit"] / fltered_df["Profit"].max())
            quality = q1 + q2 + q3 + q4
            qualities.append([node, quality])
    qualities = sorted(qualities ,key=lambda x: x[1], reverse=True)
    print(qualities)
    paok


paok
combinations_df = pd.DataFrame(columns = ['Combination', 'Profit'])
combinations_nodes = []
for i in range(11, 10, -1):
    for combination in list(combinations(nodes.keys(), i)):
        capacity = sum(nodes.get(node)["Demand"] for node in combination)
        service_time = sum(nodes.get(node)["Service Time"] for node in combination)
        if capacity <= max_capacity and service_time <= max_duration:
            profit = sum(nodes.get(node)["Profit"] for node in combination)
            combinations_nodes.append([combination, profit])

    
combinations_nodes = sorted(combinations_nodes ,key=lambda x: x[1], reverse=True)
print("Number of combinations")
print(len(combinations_nodes))

nodes[0] = {"Position": depot_position}
# solutions = []
dinstances = {}
found_solution = False
for row in combinations_nodes:
    if not found_solution:
        print("Combination length")
        print(len(row[0]))
        combination = row[0]
        perm = list(permutations(combination))
        # print(perm)
        for permutation in perm:
            if not found_solution:
                permutation_distances = sum(nodes.get(tuple_value)["Service Time"] for tuple_value in permutation)
                complete_permutation = (0,) + permutation + (0,)
                for tuple_index in range(len(complete_permutation) - 1):
                    dinstances_key = tuple(sorted(complete_permutation[tuple_index:(tuple_index + 2)]))
                    # print(dinstances_key)
                    dst = dinstances.get(dinstances_key)
                    if dst == None:
                        dinstances[dinstances_key] = dst = distance.euclidean(nodes.get(dinstances_key[0])["Position"], nodes.get(dinstances_key[1])["Position"])
                    permutation_distances += dst

                if permutation_distances <= max_duration:
                    print("Solution found")
                    print(row)
                    found_solution = True
                    # solutions.append([complete_permutation, sum(nodes.get(tuple_value)["Profit"] for tuple_value in permutation)])

end_time = time.perf_counter()
print(end_time - start_time)