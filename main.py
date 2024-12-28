import gpxpy

gpx_file = open('2.gpx', 'r')

gpx = gpxpy.parse(gpx_file)

counter = 0
for track in gpx.tracks:
  print(str(counter) + ': ' + track.name + '\n')
  counter += 1

for waypoint in gpx.waypoints:
  print(str(counter) + ': ' + waypoint.name + '\n')
  counter += 1

operation = input('接続する順にトラックまたはウェイポイントを入力してください（例：0-3,5,7,6）:\n')
operation = operation.split(',')
for i in operation:
  if '-' in i:
    serial = i.split('-')
    