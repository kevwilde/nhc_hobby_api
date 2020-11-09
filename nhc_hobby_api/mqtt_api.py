import ssl
import json
import time
import logging

import dns.resolver
import paho.mqtt.client as mqtt

from .errors import NHCGatewayNotFoundException


class MQTTApi(object):
    """Responsible on handling interactions with the Hobby API on the MQTT level"""

    def __init__(self, hostname):
        """Finds the Gateway endpoint"""
        self.ip = self._find_ip(hostname)

    def connect(self, username, password):
        """Connects using username and password credentials"""
        self.client = self._connect_to_mqtt(self.ip, username, password)
        return self

    def wait_until_init_done(self):
        """Blocks the execution thread until the service 
        has initialized"""
        while not self.has_initialized():
            time.sleep(.2)
        return self
            

    def publish(self, topic, payload=None):
        """Sends a message to the gateway"""
        json_payload = json.dumps(payload)
        self.client.publish(topic, json_payload)
        logging.debug(f"SND: {topic}: {json_payload}")

    def subscribe(self, topic):
        """Subscribe to a specific `topic`"""
        self.client.subscribe(topic, 2)
        logging.info(f"SUB: Subscribed to topic '{topic}''")

    def _find_ip(self, hostname):
        """Resolves the hostname for the gateway into its IP address"""
        res = dns.resolver.Resolver()
        try:
            a = res.query(f'{hostname}.local', 'A')
        except:
            raise NHCGatewayNotFoundException(f"Gateway {hostname} was not found")
        return a[0].to_text()

    def has_initialized(self):
        return True

    #
    # Handlers to be extended
    #

    def _on_connect(self, client, userdata, flags, rc):
        """Handle connect events"""
        logging.info(f"CON: Connected with MQTT broker with result code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        """Handle disconnect events"""
        logging.info(f"CON: Disconnected from MQTT broker")

    def _on_message(self, topic, payload):
        """Handle incoming NHC messages received"""
        pass

    def _on_mqtt_message(self, client, userdata, msg):
        """Handle incoming MQTT messages for subscribed topics"""
        logging.debug(f"RCV: {msg.topic}: {str(msg.payload)}")
        payload = json.loads(msg.payload)
        self._on_message(msg.topic, payload)

    def _connect_to_mqtt(self, ip, username, password):
        """Authenticate to the gateways MQTT"""
        client = mqtt.Client()
        client.on_connect = self._on_connect
        client.on_disconnect = self._on_disconnect
        client.on_message = self._on_mqtt_message
        client.tls_set(tls_version=ssl.PROTOCOL_TLSv1_2, cert_reqs=ssl.CERT_NONE)
        client.username_pw_set(username=username, password=password)
        client.connect(self.ip, 8884, 60)
        client.loop_start()
        return client



