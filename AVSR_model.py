from gurobipy import *

nodes = []
links = [[]]
# for each l in links:
# l = {
#	'cap': the capacity of the link,
#	'cost': the cost of the link,
# }
#
# l is set to None if the link does not exist

node_cnt = len(nodes)

# Declare model
model = Model('AVSR')

# Add variables
y = []
for i in range(node_cnt):
	y.append([])
	for j in range(node_cnt):
		y[i].append(model.addVar(vtype = GRB.BINARY))

# Add constraints
for i in range(node_cnt):
	for j in range(node_cnt):
		# Fit link capacity
		if links[i][j] is not None:
			model.addConstr(y[i][j] <= links[i][j]['cap'])

	# Balance the flow at node i
	if nodes[i]['type'] == 'SOURCE':
		model.addConstr(quicksum(y[i][j] for j in range(node_cnt)) == F)
	elif nodes[i]['type'] == 'SINK':
		model.addConstr(quicksum(y[j][i] for j in range(node_cnt)) == F)
	else:
		model.addConstr(quicksum(y[i][j] for j in range(node_cnt)) == quicksum(y[j][i] for j in range(node_cnt)))

# Set objective
model.setObjective(
	quicksum(
		links[i][j]['cost'] * y[i][j] if links[i][j] is not None else 0
		for j in range(node_cnt)
		for i in range(node_cnt)), GRB.MINIMIZE)
	
