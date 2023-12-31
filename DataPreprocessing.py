import datetime as dt
import pandas as pd
import numpy as np
import math

# 計算距離(歐式距離)
def calculate_distance(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_earth = 6371  # 地球半徑（公里）
    distance = radius_earth * c

    return distance

class DataReader:
	def __init__(self, data_path, loc_id_path):
# 讀取 CSV 檔案
		trip_data = pd.read_csv(data_path)

# 删除 PULocationID 與 DOLocationID 相同，或包含264或265的資料
		trip_data = trip_data[~((trip_data['PULocationID']  ==  trip_data['DOLocationID']) |
								(trip_data['PULocationID'].isin([264, 265])) |
								(trip_data['DOLocationID'].isin([264, 265])))]

#轉換日期格式
		trip_data['tpep_pickup_datetime'] = pd.to_datetime(trip_data['tpep_pickup_datetime'])
		trip_data['tpep_dropoff_datetime'] = pd.to_datetime(trip_data['tpep_dropoff_datetime'])

		earliest = latest = trip_data['tpep_pickup_datetime'][0]
		for pud in trip_data['tpep_pickup_datetime']:
			if pud < earliest:
				earliest = pud

			if pud > latest:
				latest = pud

		self.begin = dt.datetime(earliest.year, earliest.month, earliest.day, hour = earliest.hour)
		self.end = dt.datetime(latest.year, latest.month, latest.day, hour = latest.hour) + dt.timedelta(hours = 1)
		self.slot_cnt = int((self.end - self.begin) / dt.timedelta(hours = 1))

		self.trip_data = trip_data

		location_data = pd.read_csv(loc_id_path)
		self.dist_table = [None]
		for r in location_data.iterrows():
			lat1 = r[1]['Latitude']
			lon1 = r[1]['Longitude']

			if np.isnan(lat1) or np.isnan(lon1):
				self.dist_table.append([None] * 256)
				continue

			dist = [None]
			for _r in location_data.iterrows():
				lat2 = _r[1]['Latitude']
				lon2 = _r[1]['Longitude']

				if np.isnan(lat2) or np.isnan(lon2):
					dist.append(None)
				else:
					dist.append(calculate_distance(lat1, lon1, lat2, lon2))

			self.dist_table.append(dist)

	def get_slot_cnt(self):
		return self.slot_cnt

	def get_data(self, veh_cnt, serv_cnt, speed, slot_range = None, end_services = []):
		if slot_range is None:
			slot_range = (0, self.slot_cnt)

		nodes = self.gen_nodes(slot_range, end_services, serv_cnt)
		links = self.gen_links(veh_cnt, nodes, speed)

		return (nodes, links)

	def gen_nodes(self, slot_range, end_services, serv_cnt):
		slot_cnt = slot_range[1] - slot_range[0]
		serv_in_slot = serv_cnt // slot_cnt

		nodes = []
		nodes.append({'type': 'SOURCE', 'Location':0, 'id': -1})
		for es in end_services:
			nodes.append({'type': 'DROPOFF', 'Location': self.trip_data.loc[es]['DOLocationID'], 'id': es})

		for slb in range(slot_range[0], slot_range[1]):
			slot_begin = self.begin + dt.timedelta(hours = slb)
			slot_end = self.begin + dt.timedelta(hours = slb + 1)

			trip_data = self.trip_data[self.trip_data['tpep_pickup_datetime'] >= slot_begin]
			trip_data = trip_data[trip_data['tpep_pickup_datetime'] < slot_end]

			i = 0
			for serv_id, serv in trip_data.iterrows():
				pickup = serv['PULocationID']
				dropoff = serv['DOLocationID']
				if self.dist_table[pickup][dropoff] is None:
					continue

				nodes.append({'type': 'PICKUP', 'Location': pickup, 'id': serv_id})
				nodes.append({'type': 'DROPOFF', 'Location': dropoff, 'id': serv_id})
				i += 1
				if i >= serv_in_slot:
					break

		nodes.append({'type': 'SINK', 'Location':1000, 'id': -1})

		return nodes

	def gen_links(self, veh_cnt, nodes, speed):
		dist_table = self.dist_table
		trip_data = self.trip_data

		links=[]
		for n1 in nodes:
			link=[]
			for n2 in nodes:
				if n1['type'] == 'SOURCE':
					if n2['type'] == 'SINK':
						link.append({'cap': veh_cnt, 'cost': 0})
					elif n2['type'] == 'PICKUP':
						link.append({'cap': 1, 'cost': 60})
					else:
						link.append(None)
				elif n1['type'] == 'PICKUP':
					if n2['type'] == 'DROPOFF' and n1['id'] == n2['id']:
						link.append({'cap': 1, 'cost': -100 * dist_table[n1['Location']][n2['Location']]})
					else:
						link.append(None)
				elif n1['type'] == 'DROPOFF':
					if n2['type'] == 'SINK':
						link.append({'cap': 1, 'cost': 30})
					elif n2['type'] == 'PICKUP' and n1['id'] != n2['id']:
						dist = dist_table[n1['Location']][n2['Location']]

						do_time = trip_data.at[n1['id'], 'tpep_dropoff_datetime']
						pu_time = trip_data.at[n2['id'], 'tpep_pickup_datetime']

						trip_time = pu_time - do_time
						trip_time = trip_time.seconds / 3600

						if pu_time > do_time and dist / speed < trip_time:
							link.append({'cap': 1, 'cost': 30 * dist / speed})
						else:
							link.append(None)
					else:
						link.append(None)
				else:
					link = [None] * len(nodes)

			links.append(link)

		return links

# Usage:
#	reader = DataReader('yellow_tripdata_2023-01-11.csv', 'IDLocation.csv')
#	print(reader.get_data(3, 20))
