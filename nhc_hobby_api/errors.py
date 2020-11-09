class NHCException(Exception):
    pass

class NHCGatewayNotFoundException(NHCException):
    pass


class NHCDeviceNotFoundException(NHCException):
    pass

class NHCLocationNotFoundException(NHCException):
    pass

class NHCPropertyNotCallable(NHCException):
    pass