# 1995年以前のデータも変換する

### Convert the JMA format to csv ###
### Coded by Tomoaki Nishikawa ###
### June 7, 2024 ### 
import pandas as pd
import numpy as np
import glob

file_list = sorted(glob.glob('./JMAcatalog/h*'))

for input_file in file_list:
    ### JMA Original File ###
    output_file = input_file[13:]+'.csv'
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    ### Origin Time ###
    years = [line[1:5] for line in lines if line.startswith('J')]
    months = [line[5:7] for line in lines if line.startswith('J')]
    days = [line[7:9] for line in lines if line.startswith('J')]
    
    hours = [line[9:11] for line in lines if line.startswith('J')]
    minutes = [line[11:13] for line in lines if line.startswith('J')]
    seconds1 = [line[13:15] for line in lines if line.startswith('J')]
    seconds2 = [line[15:16] for line in lines if line.startswith('J')]
    seconds3 = [line[16:17] for line in lines if line.startswith('J')]
    
    float_seconds1 = np.array([float(value) for value in seconds1])
    float_seconds2 = np.array([float(value) if value else 0 for value in seconds2])
    #1995年以前はおそらくsecond3に値が入っておらず空白。値があれば入力、なければ0を代入する操作をする
    float_seconds3 = np.array([float(value) if value not in [None, " "] else 0 for value in seconds3])
    seconds = float_seconds1 + float_seconds2*0.1 + float_seconds3*0.01
    
    ### Hypocentral Location ###
    lats1 = [line[21:24] for line in lines if line.startswith('J')]
    lats2 = [line[24:28].strip() for line in lines if line.startswith('J')]
    float_lats1 =  np.array([float(value) for value in lats1])
    float_lats2 =  np.array([float(value) if value else 0 for value in lats2])
    lats = float_lats1 + float_lats2*0.01/60
    
    lons1 = [line[32:36] for line in lines if line.startswith('J')]
    lons2 = [line[36:40].strip() for line in lines if line.startswith('J')]
    float_lons1 =  np.array([float(value) for value in lons1])
    float_lons2 =  np.array([float(value) if value else 0 for value in lons2])
    lons = float_lons1 + float_lons2*0.01/60
    
    depths1 = [line[44:47] for line in lines if line.startswith('J')]
    depths2 = [line[47:48].strip() for line in lines if line.startswith('J')]
    depths3 = [line[48:49].strip() for line in lines if line.startswith('J')]
    float_depths1 = np.array([float(value) for value in depths1])
    float_depths2 = np.array([float(value) if value else 0 for value in depths2])
    float_depths3 = np.array([float(value) if value else 0 for value in depths3])
    depths = float_depths1+float_depths2*0.1+float_depths3*0.01
    
    ### JMA Magnitude ###
    magnitudes = [line[52:54].strip() for line in lines if line.startswith('J')]
    magnitudes = [str(-10+float(value[1])) if value.startswith('A') else value for value in magnitudes]
    magnitudes = [str(-20+float(value[1])) if value.startswith('B') else value for value in magnitudes]
    magnitudes = [str(-30+float(value[1])) if value.startswith('C') else value for value in magnitudes]
    
    float_magnitudes = np.array([float(value) * 0.1 if value else np.nan for value in magnitudes])
    # データフレームに変換
    df = pd.DataFrame(years, columns=['Year'])
    df['Month'] = months
    df['Day'] = days
    
    df['Hour'] = hours
    df['Minute'] = minutes
    df['Second'] = seconds
    
    df['Latitude'] = lats
    df['Longitude'] = lons
    df['Depth'] = depths
    df['Magnitude'] = float_magnitudes
    
    # データフレームを表示
    print(df)
    
    # データフレームを保存（必要に応じて）
    df.to_csv('./JMA_csv/'+output_file, index=True)