# the input file 'tcpdump.csv' has to be sorted by stream source first (for example using wireshark)
# change TCP_SOURCE_STREAM_COLUMN accordingly if not on the fifth column
# similarly for TCP_TIME

import csv
import sys

SECOND_ROW = 1
TOTAL_TIME_COLUMN = 1

TCP_TIME_COLUMN = 1
TCP_SOURCE_STREAM_COLUMN = 4

with open('tcpdump.csv', 'rb') as f:
    reader = csv.reader(f)
    tcp_dump_data = list(reader)

extracted_stream_time = []
last_stream_number = tcp_dump_data[SECOND_ROW][TCP_SOURCE_STREAM_COLUMN]
start_time = float(tcp_dump_data[SECOND_ROW][TCP_TIME_COLUMN])

for index in xrange(2, len(tcp_dump_data)):
    current_row = tcp_dump_data[index]
    if current_row[TCP_SOURCE_STREAM_COLUMN] != last_stream_number:
        start_time = float(current_row[TCP_TIME_COLUMN])
        extracted_stream_time.append([last_stream_number, total_time])
        last_stream_number = current_row[TCP_SOURCE_STREAM_COLUMN]
    else:
        total_time = float(current_row[TCP_TIME_COLUMN]) - start_time

extracted_stream_time.append([last_stream_number, total_time])

total_times = map(lambda x: x[TOTAL_TIME_COLUMN], extracted_stream_time)
total_times.sort()

last_columns_to_print = int(sys.argv[1] if len(sys.argv) > 0 else 5)

for value in total_times[-last_columns_to_print:]:
    print " %2.3f" % value

number_of_measurements = len(total_times)

for percentage in (50, 80, 90, 95, 99, 100):
    print 'fastest {} percent: {}'.format(percentage, total_times[(number_of_measurements - TCP_TIME_COLUMN) * percentage / 100])

#print extracted_stream_time
