from . import NHCData, NHCDictionary

class NHCSystemInformation(NHCData):

    def __init__(self, ctx, api):
        NHCData.__init__(self, ctx, api)
        self.sw_versions = NHCDictionary(self.sw_versions)