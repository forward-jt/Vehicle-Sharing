import pandas as pd
import numpy as np
import math

# 讀取 CSV 檔案
trip_data = pd.read_csv('yellow_tripdata_2023-01-11-09.csv')
# 删除 PULocationID 與 DOLocationID 相同，或包含264或265的資料
trip_data = trip_data[~((trip_data['PULocationID'] == trip_data['DOLocationID']) |
                        (trip_data['PULocationID'].isin([264, 265])) |
                        (trip_data['DOLocationID'].isin([264, 265])))]

#轉換日期格式
trip_data['tpep_pickup_datetime'] = pd.to_datetime(trip_data['tpep_pickup_datetime'])
trip_data['tpep_dropoff_datetime'] = pd.to_datetime(trip_data['tpep_dropoff_datetime'])

# 選擇 PULocationID 和 DOLocationID 欄位
Pickup_data = trip_data['PULocationID'].to_numpy()
Dropoff_data = trip_data['DOLocationID'].to_numpy()

#產生nodes
nodes = []
for i in range(len(Pickup_data)):
    nodes.append({'type': 'PICKUP', 'Location':Pickup_data[i]})
for i in range(len(Dropoff_data)):
    nodes.append({'type': 'DROPOFF', 'Location':Dropoff_data[i]})
nodes.append({'type': 'SOURCE', 'Location':0})
nodes.append({'type': 'SINK', 'Location':1000})
print(len(nodes))

trip_data = trip_data[['PULocationID','DOLocationID','tpep_pickup_datetime', 'tpep_dropoff_datetime']]
location_data = pd.read_csv('IDLocation.csv')

trip_data = trip_data.merge(location_data, left_on='PULocationID', right_on='LocationID', suffixes=('_start', '_end'))
trip_data = trip_data.merge(location_data, left_on='DOLocationID', right_on='LocationID', suffixes=('_start', '_end'))
trip_data = trip_data[['tpep_pickup_datetime', 'tpep_dropoff_datetime','PULocationID','DOLocationID','Latitude_start', 'Longitude_start', 'Latitude_end', 'Longitude_end']]
print(trip_data)


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


# trip_data['Distance'] = trip_data.apply(lambda row: calculate_distance(row['Latitude_start'], row['Longitude_start'],
#                                                                       row['Latitude_end'], row['Longitude_end']), axis=1)

#每小時行駛速度(公里)
DrivingSpeed=20

print(trip_data)


links=[]
for i in range(len(nodes)):
    print(i)
    links.append([])
    for j in range(len(nodes)):
        if(nodes[i]['type']=='SOURCE'):
            if(nodes[j]['type']=='SINK'):
                links[i].append({'cap': 0 , 'cost': 0 })
            elif(nodes[j]['type']=='PICKUP'):
                links[i].append({'cap': 1 , 'cost': 30+30 })
            else:
                links[i].append(None)
            
        elif(nodes[i]['type']=='PICKUP'):
            if(nodes[j]['type']=='DROPOFF')&(i+(len(nodes)-2)/2==j):
                links[i].append({'cap': 1 , 'cost': -100*calculate_distance(location_data.at[nodes[i]['Location']-1, 'Latitude'],
                                                                            location_data.at[nodes[i]['Location']-1, 'Longitude'],
                                                                            location_data.at[nodes[j]['Location']-1, 'Latitude'],
                                                                            location_data.at[nodes[j]['Location']-1, 'Longitude']) })
            else:
                links[i].append(None)
                
        elif(nodes[i]['type']=='DROPOFF'):
            
            if(nodes[j]['type']=='SINK'):
                links[i].append({'cap': 1 , 'cost': 30 })
            if(nodes[j]['type']=='PICKUP')&(j!=i-(len(nodes)-2)/2):
                
                distance=calculate_distance(location_data.at[nodes[i]['Location']-1, 'Latitude'],
                                                                          location_data.at[nodes[i]['Location']-1, 'Longitude'],
                                                                          location_data.at[nodes[j]['Location']-1, 'Latitude'],
                                                                          location_data.at[nodes[j]['Location']-1, 'Longitude'])
                
                trip_time=(trip_data.at[j,'tpep_pickup_datetime']-trip_data.at[int(i-(len(nodes)-2)/2),'tpep_dropoff_datetime'])
                trip_time=trip_time.seconds/3600
                if(distance/DrivingSpeed<trip_time):                
                    links[i].append({'cap': 1 , 'cost': 30*distance/DrivingSpeed })
                else:
                    links[i].append(None)
            else:
                links[i].append(None)


print(len(nodes))
