# the input file 'tcpdump.csv' has to be sorted by stream source first (for example using wireshark)
import csv

with open('tcpdump.csv', 'rb') as f:
    reader = csv.reader(f)
    your_list = list(reader)

new_list=[]
last_sn = your_list[1][4]
start_time = float(your_list[1][1])

for index in xrange(2, len(your_list)):
    current_row = your_list[index]
    if current_row[4] != last_sn:
        start_time = float(current_row[1])
        new_list.append([last_sn, total_time])
        last_sn = current_row[4]
    else:
        total_time = float(current_row[1]) - start_time

new_list.append([last_sn, total_time])

values = map(lambda x: x[1], new_list)
hehe = max(values)
values.sort()
#print new_list

#print hehe
print values[-5:]
nrof_measurements = len(values)

for percentage in (50, 80, 90, 95, 99, 100):
    print 'fastest {} percent: {}'.format(percentage, values[(nrof_measurements - 1) * percentage / 100])
