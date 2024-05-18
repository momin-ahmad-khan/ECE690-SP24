import subprocess
import csv
import re

def run_iperf():
    # Run iperf command and capture output
    process = subprocess.Popen(['iperf', '-c', 'iperf.he.net', '-n', '1M'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = process.communicate()

    pattern = r'-(\d+\.\d+)'

    # Extract interval values
    output_lines = output.decode().split('\n')
    interval_values = []
    for line in output_lines:
        if 'sec' in line:  # Look for lines containing interval values
            fields = line.split()
            # print(fields[2])
            match = re.search(pattern, fields[2])
            # print(match.group(1))
            interval_values.append(float(match.group(1)))  # Extract the interval value (penultimate field)

    return interval_values

def main():
    # Open CSV file for writing
    with open('iperf_intervals_may10_5g_1_3.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)

        # Write CSV header
        writer.writerow(['Interval'])  # Header for the interval values

        # Run iperf command 100 times and record interval values
        for i in range(250):
            interval_values = run_iperf()
            for value in interval_values:
                print("Latency for round ", i, "is: ", value)
                writer.writerow([value])

    print("RSRP is: -100dBm")
if __name__ == "__main__":
    main()
