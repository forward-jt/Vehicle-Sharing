
import pandas as pd

# 指定您的 CSV 檔案路徑
file_path = 'yellow_tripdata_2023-01.csv'

# 使用 pandas 的 read_csv 函式匯入 CSV 檔案到 DataFrame
TaxiData = pd.read_csv(file_path)
# 顯示 DataFrame 的前幾行資料
print(TaxiData.head())

# 設定起始時間和結束時間
start_time = '2023-01-11 09:00:00'
end_time = '2023-01-11 24:00:00'

# 使用條件選擇符合時間範圍的資料
selected_data = TaxiData[
    (TaxiData['tpep_pickup_datetime'] >= start_time) &
    (TaxiData['tpep_pickup_datetime'] <= end_time)
]

# 顯示所選擇的資料
print(selected_data)


# 將 DataFrame 存儲為 CSV 檔案，並命名為 'yellow_tripdata_2023-01-11-09.csv'
# index=False 可以避免寫入 CSV 時產生多餘的索引列
selected_data.to_csv('yellow_tripdata_2023-01-11.csv', index=False)



