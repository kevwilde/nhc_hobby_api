from . import NHCData

class NHCLocation(NHCData):
    
    def get_devices(self):
        return self.api.get_devices_for_location(self.uuid)