import paho.mqtt.client as mqtt
import mysql.connector
import time

MQTT_ADDRESS = '13.49.80.175'
MQTT_USER = 'labtelkom'
MQTT_PASSWORD = 'tsushima101'  
# MQTT_arusDC_topic = 'arusDC'
MQTT_teganganDC_topic = 'teganganDC'
MQTT_arusAC_topic = 'arusAC'
MQTT_teganganAC_topic = 'teganganAC'
MQTT_suhu = 'suhu'


DB_HOST = 'labtelkom'
DB_USER = 'labtelkom'
DB_PASSWORD = 'tsushima101'
DB_DATABASE = 'db_lora'

tegdc = 0.0
arac = 0.0
tegac = 0.0
suhu = 0.0
coba = 0
def on_connect(client, userdata, flags, rc):
    print(f'Connected with Code: {rc}')

    client.subscribe(MQTT_teganganDC_topic)
    client.subscribe(MQTT_arusAC_topic)
    client.subscribe(MQTT_teganganAC_topic)
    client.subscribe(MQTT_suhu)

def on_message(client, userdata, msg):

    global tegdc, coba, arac, tegac, suhu

    if(msg.topic == 'teganganDC'):
        tegdc = msg.payload
        coba = 1
        print("TeganganDC: " +str(tegdc))
    elif(msg.topic == 'arusAC'):
        arac = msg.payload
        coba = 0
        print("arusAC: " +str(arac))
    elif(msg.topic == 'teganganAC'):
        tegac = msg.payload
        coba = 0
        print("TeganganAC: " +str(tegac))
    elif(msg.topic == 'suhu'):
        suhu = msg.payload
        print("suhu: " +str(suhu))

    query = ("INSERT INTO tb_pv_fix"
          "(Tegangan_pv, Arus, Tegangan, Suhu) "
          "VALUES (%s, %s, %s, %s)")
        
    data_received = (tegdc, arac, tegac, suhu)

    print("Data berhasil disimpan ke database.")
    if (coba==1):
        try :
          
            connection = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_DATABASE
            )
            cursor = connection.cursor()
            cursor.execute(query, data_received)
            connection.commit()
            print("Data berhasil disimpan ke database.")
        except mysql.connector.Error as error:
            print("Error: {}".format(error))
        finally:
            if 'connection' in locals():
                if connection.is_connected():
                    cursor.close()
                    connection.close()

def main():
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_ADDRESS, 1883)
    mqtt_client.loop_forever()

if __name__ == '__main__':
    print('MQTT to InfluxDB bridge')
    main()