from gurobipy import *
import argparse
from DataPreprocessing import DataReader

parser = argparse.ArgumentParser(description = 'Modeling AVSR network with given parameters')
parser.add_argument('-s', '--service', type = int, required = True, help = 'The number of services')
parser.add_argument('-v', '--vehicle', type = int, required = True, help = 'The number of available vehicles')
parser.add_argument('-m', '--speed', type = float, required = True, help = 'The moving speed of vehicles')
parser.add_argument('-t', '--slot', type = int, default = 0, help = 'The size of slot')
parser.add_argument('-o', '--output', type = str, default = 'stdout', help = 'The output destination')
args = parser.parse_args()

print(args)

vehicle = args.vehicle
service = args.service
speed = args.speed
slot_size = args.slot

print('Initializing data reader')
reader = DataReader('Data/yellow_tripdata_2023-01-11.csv', 'Data/IDLocation.csv')

slot_size = slot_size if slot_size > 0 or slot_size <= reader.get_slot_cnt() else reader.get_slot_cnt()
end_services = []
routes = []
ignore_list = []
profit = 0

print('Forming AVSR network with %d vehicles at %.2f km/h and %d services in each slot with size %d' % (vehicle, speed, service, slot_size))

for slot_begin in range(0, reader.slot_cnt, slot_size):
	slot_end = slot_begin + slot_size
	nodes, links = reader.get_data(vehicle, service, speed, slot_range = (slot_begin, slot_end), end_services = end_services)
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
			model.addConstr(quicksum(y[i][j] for j in range(node_cnt)) == vehicle - len(end_services))
		elif nodes[i]['type'] == 'SINK':
			model.addConstr(quicksum(y[j][i] for j in range(node_cnt)) == vehicle)
		elif nodes[i]['type'] == 'DROPOFF' and nodes[i]['id'] in end_services:
			model.addConstr(quicksum(y[i][j] for j in range(node_cnt)) == 1)
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

	profit += model.getAttr('objVal')

# Show Result
	print('Form routes from programming result')
	end_services = []
	for i in range(node_cnt):
		for j in range(node_cnt):
			if model.getAttr('x', [y[i][j]])[0] == 0:
				if nodes[i]['id'] == nodes[j]['id'] and nodes[i]['type'] == 'PICKUP' and nodes[j]['type'] == 'DROPOFF':
					ignore_list.append(nodes[i]['id'])
				continue

			na = nodes[i]['type']
			if na == 'PICKUP' or na == 'DROPOFF':
				na += "(" + str(nodes[i]['id']) + ")"

			nb = nodes[j]['type']
			if nb == 'PICKUP' or nb == 'DROPOFF':
				nb += "(" + str(nodes[j]['id']) + ")"

			if na != 'SOURCE' and nb == 'SINK':
				end_services.append(nodes[i]['id'])

			if nb == 'SINK' and slot_end != 15:
				continue

			add = False
			for r in routes:
				if na == r[-1][0]:
					ext = False
					for k in range(len(routes)):
						if routes[k][0][0] == nb:
							r.extend(routes[k])
							del routes[k]
							ext = True
							break

					if not ext:
						r.append((nb, str(slot_begin)))
					add = True
					break

			if not add:
				routes.append([(na, str(slot_begin)), (nb, str(slot_begin))])

if args.output == 'stdout':
	print('Used vehicles: %d' % (len(routes)))
	print('# ignored services: %d' % (len(ignore_list)))
	print('Ignored services: ', ignore_list)
	for r in routes:
		print(' -> '.join(['@'.join(pt) for pt in r]))
	print('Total profit: ', -profit)
else:
	print('Writing result to %s' % (args.output))
	with open(args.output, 'w') as out:
		out.write('{\n')
		out.write('\t"used_vehicle": %d,\n' % (len(routes)))
		out.write('\t"ign_serv_cnt": %d,\n' % (len(ignore_list)))
		out.write('\t"ign_servs": %s,\n' % (str(ignore_list)))
		out.write('\t"profit" %f\n' % (-profit))
		out.write('\t"routes": [\n\t\t%s\n\t]\n' % (',\n\t\t'.join([','.join(['"%s@%s"' % (pt[0], pt[1]) for pt in r]) for r in routes])))
		out.write('}')
