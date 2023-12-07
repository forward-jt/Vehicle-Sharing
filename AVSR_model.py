from gurobipy import *
import argparse
from DataPreprocessing import DataReader

parser = argparse.ArgumentParser(description = 'Modeling AVSR network with given parameters')
parser.add_argument('-s', '--service', type = int, required = True, help = 'The number of services')
parser.add_argument('-v', '--vehicle', type = int, required = True, help = 'The number of available vehicles')
parser.add_argument('-m', '--speed', type = float, required = True, help = 'The moving speed of vehicles')
parser.add_argument('-o', '--output', type = str, default = 'stdout', help = 'The output destination')
args = parser.parse_args()

print(args)

vehicle = args.vehicle
service = args.service
speed = args.speed

print('Initializing data reader')
reader = DataReader('Data/yellow_tripdata_2023-01-11.csv', 'Data/IDLocation.csv')

print('Forming AVSR network with %d vehicles at %.2f km/h and %d services' % (vehicle, speed, service))
nodes, links = reader.get_data(vehicle, service, speed)
node_cnt = len(nodes)

# for each l in links:
# l = {
#	'cap': the capacity of the link,
#	'cost': the cost of the link,
# }
#
# l is set to None if the link does not exist

print('Forming LP formulation model')
# Declare model
model = Model('AVSR')

# Add variables
y = []
for i in range(node_cnt):
	y.append([])
	for j in range(node_cnt):
		y[i].append(model.addVar(lb = 0))

# Add constraints
for i in range(node_cnt):
	for j in range(node_cnt):
		# Fit link capacity
		if links[i][j] is not None:
			model.addConstr(y[i][j] <= links[i][j]['cap'])
		else:
			model.addConstr(y[i][j] == 0)

	# Balance the flow at node i
	if nodes[i]['type'] == 'SOURCE':
		model.addConstr(quicksum(y[i][j] for j in range(node_cnt)) == vehicle)
	elif nodes[i]['type'] == 'SINK':
		model.addConstr(quicksum(y[j][i] for j in range(node_cnt)) == vehicle)
	else:
		model.addConstr(quicksum(y[i][j] for j in range(node_cnt)) == quicksum(y[j][i] for j in range(node_cnt)))

# Set objective
model.setObjective(
	quicksum(
		links[i][j]['cost'] * y[i][j] if links[i][j] is not None else 0
		for j in range(node_cnt)
		for i in range(node_cnt)) +
	quicksum(
		-links[i][j]['cost'] * (1 - y[i][j])
		if links[i][j] is not None and nodes[i]['type'] == 'PICKUP' and nodes[j]['type'] == 'DROPOFF' else 0
		for j in range(node_cnt)
		for i in range (node_cnt))
	, GRB.MINIMIZE)

print('Optimizing')
# Optimize
model.optimize()

# Show Result
print('Form routes from programming result')
routes = []
ignore_list = []
ignore_cnt = 0
for i in range(node_cnt):
	for j in range(node_cnt):
		if model.getAttr('x', [y[i][j]])[0] == 0:
			if nodes[i]['id'] == nodes[j]['id'] and nodes[i]['type'] == 'PICKUP' and nodes[j]['type'] == 'DROPOFF':
				ignore_list.append(nodes[i]['id'])
				ignore_cnt += 1
			continue

		na = nodes[i]['type']
		if na == 'PICKUP' or na == 'DROPOFF':
			na += "(" + str(nodes[i]['id']) + ")"

		nb = nodes[j]['type']
		if nb == 'PICKUP' or nb == 'DROPOFF':
			nb += "(" + str(nodes[j]['id']) + ")"


		add = False
		for r in routes:
			if na == r[-1]:
				ext = False
				for k in range(len(routes)):
					if routes[k][0] == nb:
						r.extend(routes[k])
						del routes[k]
						ext = True
						break

				if not ext:
					r.append(nb)
				add = True
				break

		if not add:
			routes.append([na, nb])

if args.output == 'stdout':
	print('Used vehicles: %d' % (len(routes)))
	print('# ignored services: %d' % (ignore_cnt))
	print('Ignored services: ', ignore_list)
	for r in routes:
		print(' -> '.join(r))
else:
	print('Writing result to %s' % (args.output))
	with open(args.output, 'w') as out:
		out.write('{\n')
		out.write('\t"used_vehicle": %d,\n' % (len(routes)))
		out.write('\t"ign_serv_cnt": %d,\n' % (ignore_cnt))
		out.write('\t"ign_servs": %s,\n' % (str(ignore_list)))
		out.write('\t"routes": [\n\t\t%s\n\t]\n' % (',\n\t\t'.join([str(r) for r in routes])))
		out.write('}')
