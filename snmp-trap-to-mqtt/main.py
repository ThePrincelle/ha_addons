import paho.mqtt.client as paho
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
import logging

# Read options.json file
import json

with open('data/options.json') as json_file:
    options = json.load(json_file)
    
# MQTT
mqtt_host = options['mqtt_host']
mqtt_port = options['mqtt_port']
mqtt_topic = options['mqtt_topic']
mqtt_user = options['mqtt_user']
mqtt_pass = options['mqtt_pass']

client = paho.Client()
client.username_pw_set(mqtt_user, mqtt_pass)
client.connect(mqtt_host, mqtt_port)

snmpEngine = engine.SnmpEngine()

TrapAgentAddress='127.0.0.1'; #Trap listerner address
Port=8000;  #trap listerner port

logging.basicConfig(filename='received_traps.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

logging.info("Agent is listening SNMP Trap on "+TrapAgentAddress+" , Port : " +str(Port))
logging.info('--------------------------------------------------------------------------')

print("Agent is listening SNMP Trap on "+TrapAgentAddress+" , Port : " +str(Port));

config.addTransport(
    snmpEngine,
    udp.domainName + (1,),
    udp.UdpTransport().openServerMode((TrapAgentAddress, Port))
)

#Configure community here
config.addV1System(snmpEngine, 'my-area', 'public')

def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
    print("Received new Trap message");
    logging.info("Received new Trap message")
    for name, val in varBinds:   
        logging.info('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))
        
        # Publish message to MQTT
        client.publish(mqtt_topic, {
            'oid': name.prettyPrint(),
            'value': val.prettyPrint()
        })

    logging.info("==== End of Incoming Trap ====")
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1)  

try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
