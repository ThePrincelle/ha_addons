import asyncio
import paho.mqtt.client as paho
import aiosnmp

# Read options.json file
import json

with open('options.json') as json_file:
    options = json.load(json_file)
    
# MQTT
mqtt_host = options['mqtt_host']
mqtt_port = options['mqtt_port']
mqtt_topic = options['mqtt_topic']
mqtt_user = options['mqtt_user']
mqtt_pass = options['mqtt_pass']

client = paho.Client()


async def handler(host: str, port: int, message: aiosnmp.SnmpV2TrapMessage) -> None:
    print(f"got packet from {host}:{port}")
    for d in message.data.varbinds:
        print(f"oid: {d.oid}, value: {d.value}")
        
        # Publish message to MQTT
        client.publish(mqtt_topic, {
            'oid': d.oid,
            'value': d.value
        })


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    trap_server = aiosnmp.SnmpV2TrapServer(host="127.0.0.1", port=8000, communities=("public",), handler=handler)
    transport, _ = loop.run_until_complete(trap_server.run())
    
    client.username_pw_set(mqtt_user, mqtt_pass)
    client.connect(mqtt_host, mqtt_port)

    try:
        print(f"running server on {trap_server.host}:{trap_server.port}")
        loop.run_forever()
    finally:
        transport.close()
