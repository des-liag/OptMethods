import pandas as pd
import csv
from scipy.spatial import distance
import math
import time

start_time = time.perf_counter()
file_name = "Instance.csv"

# read file
with open(file_name) as fd:
    reader = csv.reader(fd)
    interesting_rows = [row for idx, row in enumerate(reader) if idx in (0, 1, 2, 5, 7)]
fd.close()

vehicles = int(interesting_rows[0][1])
max_capacity = int(interesting_rows[1][1])
max_duration = int(interesting_rows[2][1])
depot_position = (float(interesting_rows[3][1]), float(interesting_rows[3][2]))
customers = int(interesting_rows[4][1])

# read file and create a dataframe with file data
df = pd.read_csv(file_name, skiprows=10, index_col=0)
df['Position'] = df.apply(lambda row: (row["x"], row["y"]), axis=1)
df['Distance from 0'] = df.apply(lambda row: distance.euclidean(depot_position, (row["x"], row["y"])), axis=1)
# print(df)

# for every vehicle(route)
solutions = []
for vehicles_index in range(vehicles):
    if vehicles_index > 0:
        df.drop(solutions[vehicles_index - 1][0][1:(len(solutions[vehicles_index - 1][0]) - 1)], inplace=True)

    # find the min service time of all nodes so as to calculate how many nodes vehicles can visit according to max duration
    # service_time_limit = df["Service Time"].min()
    service_time_limit = df["Service Time"].mean()
    max_nodes_to_visit = math.ceil(max_duration / service_time_limit)
    # print("max_nodes_to_visit: " + str(max_nodes_to_visit))

    # find the min qapacity of all nodes so as to calculate how many nodes vehicles can visit according to max qapacity
    # qapacity_limit = df["Demand"].min()
    qapacity_limit = df["Demand"].mean()
    max_qapacity_to_load = math.ceil(max_capacity / qapacity_limit)
    # print("max_qapacity_to_load: " + str(max_qapacity_to_load))

    # nodes that vehicles can visit can be under the number of the min(max_nodes_to_visit, max_qapacity_to_load)
    min_value = max_qapacity_to_load
    if max_nodes_to_visit < max_qapacity_to_load:
        min_value = max_nodes_to_visit
    remaining_time = max_duration - min_value * service_time_limit
    print("Remaining time: " + str(remaining_time))

    max_profit = df["Profit"].max()
    # print("max_profit: " + str(max_profit))

    # delete from dataframe all nodes that have distance from 0 bigger than remaining time
    # this can be explained by a circle with center=depot and r=max_duration
    filtered_df = df[df['Distance from 0'] <= remaining_time]
    # print(filtered_df)
    filtered_df.loc[0] = [depot_position[0], depot_position[1], 0, 0, 0, depot_position, 0]
    for node in filtered_df.index:
        if node != 0:
            position = filtered_df.loc[node]["Position"]
            # calculate distances of all possible node transitions
            filtered_df['Distance from ' + str(node)] = filtered_df.apply(
                lambda row: distance.euclidean(position, (row["x"], row["y"])), axis=1)
    # print(filtered_df)

    nodes = filtered_df.T.to_dict()
    print("Number of possible nodes: " + str(len(nodes)))

    demand_weight = 2
    service_time_weight = 1.5
    distances_weight = 5
    profit_weight = 4.5

    solution_found = False
    solution = [0]
    solution_profit = 0
    remaining_time = max_duration
    remaining_capacity = max_capacity
    while not solution_found:
        qualities = []
        for node in nodes.keys():
            if node not in solution:
                # calculate some variables that show the quality of each node for each variable limit
                q1 = demand_weight * (1 - nodes.get(node)["Demand"] / filtered_df["Demand"].max())
                q2 = service_time_weight * (1 - nodes.get(node)["Service Time"] / filtered_df["Service Time"].max())
                columns = ["Distance from " + str(x) for x in nodes.keys()]
                q3 = distances_weight * (
                            1 - nodes.get(solution[-1])["Distance from " + str(node)] / filtered_df.loc[solution[-1]][
                        columns].max())
                q4 = profit_weight * (nodes.get(node)["Profit"] / filtered_df["Profit"].max())
                quality = q1 + q2 + q3 + q4

                qualities.append([node, quality])
        qualities = sorted(qualities, key=lambda x: x[1], reverse=True)

        local_solution_found = False
        for quality in qualities:
            if not local_solution_found:
                node = quality[0]
                if remaining_time - nodes.get(node)["Service Time"] - nodes.get(solution[-1])[
                    "Distance from " + str(node)] - nodes.get(node)["Distance from 0"] > 0 and remaining_capacity - \
                        nodes.get(node)["Demand"] > 0:
                    remaining_time = remaining_time - nodes.get(node)["Service Time"] - nodes.get(solution[-1])[
                        "Distance from " + str(node)]
                    remaining_capacity = remaining_capacity - nodes.get(node)["Demand"]
                    solution.append(node)
                    solution_profit = solution_profit + nodes.get(node)["Profit"]
                    local_solution_found = True
        if local_solution_found == False:
            solution_found = True
            solution.append(0)

    solutions.append([solution, solution_profit])
    print("----------Solution------------")
    print("Combination = " + str(solution))
    print("Total Profit = " + str(solution_profit))
    print("------------------------------")

print("Total profit = " + str(sum(x[1] for x in solutions)))
end_time = time.perf_counter()
print("Execution time = " + str(end_time - start_time) + " seconds")

file = open("sol.txt", "w+")
file.writelines(["Total Profit\n", str(sum(x[1] for x in solutions)) + "\n"])
route = 1
sol = 0
for i in range(len(solutions) * 2):
    if i % 2 == 0:
        file.write("Route " + str(route) + "\n")
        route += 1
    else:
        file.write(str(" ".join(str(x) for x in solutions[sol][0])) + "\n")
        sol += 1
file.close()
