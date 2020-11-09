from . import NHCData, NHCDictionary
from ..errors import NHCPropertyNotCallable

class NHCDevice(NHCData):

    @staticmethod
    def from_context(ctx, api):
        if ctx['Type'] == 'action':
            if ctx['Model'] in ['light', 'socket', 'switched-fan', 'switched-generic']:
                return NHCRelayAction(ctx, api)
            elif ctx['Model'] == 'alarms':
                return NHCAlarmsAction(ctx, api)
        return NHCDevice(ctx, api)

    def __init__(self, ctx, api):
        NHCData.__init__(self, ctx, api)
        self.parameters = NHCDictionary(self.parameters)
        self.properties = NHCDictionary(self.properties)
        self.property_definitions = NHCDictionary(self.property_definitions)

    def __str__(self):
        return f"<nhc.{self.canonical_name()}[{self.name}] at {self.uuid}>"

    def get_name(self):
        return "NHC Action"

    def callable_properties(self):
        return [self.to_snake_case(x) for x in self.property_definitions.keys()]

    def control(self, **kwargs):
        for key in kwargs.keys():
            # Validate property exists
            if not key in self.callable_properties():
                raise NHCPropertyNotCallable(f"Property `{self.to_camel_case(key)}` does not exist for device {self.uuid}. Accepted properties: " + ",".join(self.callable_properties())) 
            # Validate property can be controlled
            if self.property_definitions.get(self.to_camel_case(key)).get("can_control") == "false":
                raise NHCPropertyNotCallable(f"Property `{self.to_camel_case(key)}` is read only") 

        # Publish control 
        self.api.publish('hobby/control/devices/cmd', {
            'Method': "devices.control",
            'Params': [{
                "Devices": [{
                    "Properties": list(self.chunkify_dict(self.to_camel_case(kwargs))),
                    "Uuid": self.uuid
                }]
            }]
        })


class NHCRelayAction(NHCDevice):
    def get_name(self):
        return "NHC Relay Action"

class NHCAlarmsAction(NHCDevice):
    def get_name(self):
        return "NHC Basic/Panic Alarm Action"