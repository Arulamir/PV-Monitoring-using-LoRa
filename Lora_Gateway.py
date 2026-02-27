import paho.mqtt.client as mqtt 
import board
import busio
from digitalio import DigitalInOut
import adafruit_rfm9x
import time
import csv
from datetime import datetime

csv_filename = "tracking.csv"

MQTT_ADDRESS = '13.49.80.175'
MQTT_USER = 'labtelkom'
MQTT_PASSWORD = 'tsushima101'

# Inisialisasi koneksi SPI
spi = busio.SPI(board.SCLK, MOSI=board.MOSI, MISO=board.MISO)

# Buat objek CS (chip select) untuk RFM95
cs = DigitalInOut(board.CE1)

# Buat objek reset untuk RFM95 (jika digunakan)
reset = DigitalInOut(board.D22)

# Inisialisasi RFM95
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 915.0)

client = mqtt.Client()
client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
client.connect(MQTT_ADDRESS, 1883)

with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Datetime", "Latency(s)", "RSSI", "Bit Rate (bps)", "Total Packets", "Lost Packets", "Packet Loss Rate (%)"])

# Variabel untuk perhitungan bit rate dan packet loss
last_receive_time = time.time()
received_packets = 0
lost_packets = 0
total_packets = 0
interval = 20  # Interval dalam detik untuk mengirimkan paket

print("Menunggu data...")

while True:
    try:
        packet = rfm9x.receive()

        if packet is not None:
            current_time = time.time()
            received_packets += 1
            total_packets += 1

            data_length = len(packet)  # Hitung panjang data secara dinamis
            data = packet.decode('utf-8', errors='ignore')
            data_value = data.split(",")
            if len(data_value) == 5:
                tegangan_DC = str(data_value[1])
                tegangan_AC = str(data_value[2])
                arus_AC = str(data_value[3])
                suhu = str(data_value[4])
                time_since_last_receive = current_time - last_receive_time
                receive_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                rssi = rfm9x.rssi

                # Hitung bit rate
                elapsed_time = current_time - last_receive_time
                if elapsed_time > 0:
                    bit_rate = (received_packets * data_length * 8.0) / elapsed_time
                else:
                    bit_rate = 0

                # Simpan data ke file CSV
                with open(csv_filename, mode='a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([receive_timestamp, time_since_last_receive, rssi, bit_rate, total_packets, lost_packets, (lost_packets / total_packets) * 100])

                print(f"Latency: {time_since_last_receive}s")
                print(f"RSSI: {rssi}dBm")
                print(f"Bit Rate: {bit_rate} bps")
                print(f"Total Packets: {total_packets}")
                print(f"Lost Packets: {lost_packets}")
                print(f"Packet Loss Rate: {(lost_packets / total_packets) * 100:.2f}%")
                print("Terima: teganganDC:{}, arusAC:{}, teganganAC:{}, suhu:{} ".format(tegangan_DC, arus_AC, tegangan_AC, suhu))

                client.publish("teganganDC", tegangan_DC)
                client.publish("arusAC", arus_AC)
                client.publish("teganganAC", tegangan_AC)
                client.publish("suhu", suhu)

                last_receive_time = current_time

            # Hitung data loss jika tidak ada paket yang diterima dalam dua kali interval
            if current_time - last_receive_time > 2 * interval:
                lost_packets += 1
                total_packets += 1
                last_receive_time = current_time

        # Tunggu 20 detik sebelum menerima data berikutnya
        time.sleep(interval)

    except UnicodeDecodeError as e:
        print("Error decoding data:", e)
    except KeyboardInterrupt:
        break

while True:
    try:
        rc = 0
        while rc == 0:
            rc = client.loop()
        print("Mosquitto is running!: " + str(rc))
    except Exception as e:
        print(f"An error occurred: {e}")
