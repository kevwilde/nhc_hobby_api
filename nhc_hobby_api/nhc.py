import logging
from collections import defaultdict

from .mqtt_api import MQTTApi
from .errors import NHCLocationNotFoundException, NHCDeviceNotFoundException
from .data import NHCLocation, NHCDevice, NHCSystemInformation


class NHC(MQTTApi):

    def __init__(self, hostname):
        MQTTApi.__init__(self, hostname)
        self.devices_dct = {}
        self.locations_dct = {}
        self.location_device_map = defaultdict(list)
        self.location_store_init = False
        self.device_store_init = False
    
    def devices(self):
        return self.devices_dct.values()

    def get_device(self, device_uuid):
        dev = self.devices_dct.get(device_uuid)
        if dev:
            return dev
        else:
            raise NHCDeviceNotFoundException(f"No device found with Uuid {device_uuid}")

    def locations(self):
        return self.locations_dct.values()

    def get_devices_for_location(self, location_uuid):
        return self.location_device_map[location_uuid]

    def get_location(self, location_uuid):
        loc = self.locations_dct.get(location_uuid)
        if loc:
            return loc
        else:
            raise NHCLocationNotFoundException(f"No location found with Uuid {location_uuid}")

    def has_initialized(self):
        return self.location_store_init and self.device_store_init

    # -------------------------------------------------------------------------
    # Connection Handler
    # -------------------------------------------------------------------------

    def _on_connect(self, client, userdata, flags, rc):
        MQTTApi._on_connect(self, client, userdata, flags, rc)
        # Subscribe to topics
        self.subscribe('hobby/system/rsp')
        self.subscribe('hobby/control/devices/evt')
        self.subscribe('hobby/control/devices/rsp')
        self.subscribe('hobby/control/devices/err')
        self.subscribe('hobby/control/devices/evt')
        self.subscribe('hobby/control/locations/rsp')

        # Initialize state
        self.publish('hobby/system/cmd', {'Method': 'systeminfo.publish'})
        self.publish('hobby/control/locations/cmd', {'Method': 'locations.list'})
        self.publish('hobby/control/devices/cmd', {'Method': 'devices.list'})

    # -------------------------------------------------------------------------
    # Message Handlers
    # -------------------------------------------------------------------------

    def _on_message(self, topic, payload):
        method = payload.get('Method')
        if method == 'devices.list':
            self._on_device_list_message(payload)
        elif method == 'locations.list':
            self._on_location_list_message(payload)
        elif method == 'systeminfo.publish':
            self._on_sys_info_message(payload)

    def _on_device_list_message(self, payload):
        # Save all devices
        for device_ctx in payload['Params'][0]['Devices']:
            dev = NHCDevice.from_context(device_ctx, self)
            self.devices_dct[dev.uuid] = dev
        # Generate the Location/Device mapping
        for device in self.devices_dct.values():
            self.location_device_map[device.parameters.location_id].append(device)
        self.device_store_init = True
        logging.debug("API: Devices initialized.")
    
    def _on_location_list_message(self, payload):
        for location_ctx in payload['Params'][0]['Locations']:
            loc = NHCLocation(location_ctx, self)
            self.locations_dct[loc.uuid] = loc
        self.location_store_init = True
        logging.debug("API: Locations initialized.")

    def _on_sys_info_message(self, payload):
        sysinfo = payload['Params'][0]['SystemInfo'][0]
        self.system_information = NHCSystemInformation(sysinfo, self)
        logging.debug("API: SystemInfo initialized.")

