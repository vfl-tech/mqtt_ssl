import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
import time
import ssl 

adc = ADC(Pin(34))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

ssid = 'REDE_WIFI'
password = 'SENHA_REDE'
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)

while not wifi.isconnected():
    pass
print('Conectado ao wifi')

broker = 'BROKER_DNS_OR_IP'
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
client = MQTTClient(client_id = 'esp32_client', server = broker, port = 8883, ssl = context)
client.connect()

while True:
    try:
        topic = 'sensores/temperatura'
        valor_sensor = adc.read()
        device_address = wifi.ifconfig()[0]
        mensagem = {'device': str(device_address), 'temp': str(25+(valor_sensor/4095)*175)}
        client.publish(topic, str(mensagem))
        print(f'Mensagem publicada com sucess', mensagem)
        time.sleep(0.5)
    except Exception as e:
        print(e)
    



