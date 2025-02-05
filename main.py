import gpxpy
import requests
import math

gpx_file = open('test/3.gpx', 'r')

gpx = gpxpy.parse(gpx_file)

counter = 0
tr_way = []

print('\nトラック')
for track in gpx.tracks:
  print(str(counter) + ': ' + track.name)
  tr_way.append([track, 'track'])
  counter += 1

print('\nウェイポイント')
for waypoint in gpx.waypoints:
  print(str(counter) + ': ' + waypoint.name)
  tr_way.append([waypoint, 'waypoint'])
  counter += 1

while True:
  operation_raw = input('\n接続する順にトラックまたはウェイポイントを入力してください（例：0-3,5,7,6）:\n')
  try:
    operation_raw = operation_raw.split(',')
    operation = []
    for i in operation_raw:
      if '-' in i:
        serial_range = i.split('-')
        if len(serial_range) != 2:
          raise ValueError
        for j in range(int(serial_range[0]), int(serial_range[1]) + 1):
          operation.append(j)
      else:
        operation.append(int(i))
    for i in operation:
      if i > counter - 1:
        raise ValueError
  except ValueError:
    print('適切な値を入力してください')

  print('\n指定した順番は以下のとおりです')
  for i in operation:
    print(str(i) + ': (' + tr_way[i][1] + ') ' + tr_way[i][0].name)

  while True:
    start = input('\n処理を開始します。よろしいですか[y/n]')
    if start == 'y' or start == 'n':
      break
  if start == 'y':
    break

latlonele = []
for i in operation:
  if tr_way[i][1] == 'track':
    for segment in tr_way[i][0].segments:
      for point in segment.points:
        latlonele.append([point.latitude, point.longitude, point.elevation])
  elif tr_way[i][1] == 'waypoint':
    latlonele.append([tr_way[i][0].latitude, tr_way[i][0].longitude, tr_way[i][0].elevation])
print('\n緯度経度標高')
[print(i) for i in latlonele]

xy = []
url = 'http://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2xy.pl'
for i in latlonele:
  params = {'outputType': 'json', 'refFrame': '2', 'zone': '12', 'latitude': i[0], 'longitude': i[1]}
  r = requests.get(url, params=params)
  r = r.json()
  xy.append([r['OutputData']['publicX'],r['OutputData']['publicY']])
print('\nXY座標')
[print(i) for i in xy]

if len(tr_way) == 1:
  raise ValueError('トラックまたはウェイポイントが1つしか選択されていません')

def degDisLatlonele():
  degDis = []
  url = 'http://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/bl2st_calc.pl?'
  for i in range(len(latlonele) - 1):
    params = {'outputType': 'json', 'ellipsoid': 'GRS80', 'latitude1': latlonele[i][0], 'longitude1': latlonele[i][1], 'latitude2': latlonele[i + 1][0], 'longitude2': latlonele[i + 1][1]}
    r = requests.get(url, params=params)
    r = r.json()
    degDis.append([float(r['OutputData']['azimuth1']), float(r['OutputData']['geoLength'])])
  params = {'outputType': 'json', 'ellipsoid': 'GRS80', 'latitude1': latlonele[-1][0], 'longitude1': latlonele[-1][1], 'latitude2': latlonele[0][0], 'longitude2': latlonele[0][1]}
  r = requests.get(url, params=params)
  r = r.json()
  degDis.append([float(r['OutputData']['azimuth1']), float(r['OutputData']['geoLength'])])
  return degDis

def degDisXY():
  degDis = []
  url = 'http://vldb.gsi.go.jp/sokuchi/surveycalc/surveycalc/xy2st.pl?'
  for i in range(len(xy) - 1):
    params = {'outputType': 'json', 'refFrame': '2', 'zone': '12', 'publicX1': xy[i][0], 'publicY1': xy[i][1], 'publicX2': xy[i + 1][0], 'publicY2': xy[i + 1][1]}
    r = requests.get(url, params=params)
    r = r.json()
    degDis.append([float(r['OutputData']['azimuth1-2']), float(r['OutputData']['distance1-2'])])
  params = {'outputType': 'json', 'ellipsoid': 'GRS80', 'publicX1': xy[-1][0], 'publicY1': xy[-1][1], 'publicX2': xy[0][0], 'publicY2': xy[0][1]}
  r = requests.get(url, params=params)
  r = r.json()
  degDis.append([float(r['OutputData']['azimuth1-2']), float(r['OutputData']['distance1-2'])])
  return degDis

degDis = degDisLatlonele()
print('\n方位角と距離')
[print(i) for i in degDis]

degNdisKdeg = []

for i in range(len(latlonele) - 1):
  hyokosa = abs(float(latlonele[i][2]) - float(latlonele[i + 1][2]))
  dis = degDis[i][1]
  nanameDis = math.sqrt((hyokosa ** 2) + (dis ** 2))
  kdeg = math.degrees(math.atan(hyokosa / dis))
  degNdisKdeg.append([degDis[i][0], nanameDis, kdeg])
hyokosa = abs(float(latlonele[-1][2]) - float(latlonele[0][2]))
dis = degDis[-1][1]
nanameDis = math.sqrt((hyokosa ** 2) + (dis ** 2))
kdeg = math.degrees(math.atan(hyokosa / dis))
degNdisKdeg.append([degDis[-1][0], nanameDis, kdeg])
print('\n方位角と斜距離と傾斜角')
[print(i) for i in degNdisKdeg]

print('\nfox出力\n')
print('BEGIN')
for i in range(len(degNdisKdeg)):
  print(str(i + 1) + ' ' + str(degNdisKdeg[i][0]) + ' ' + str(degNdisKdeg[i][2]) + ' ' + str(degNdisKdeg[i][1]))
print('end')