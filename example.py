import json

from nhc_hobby_api import NHC


with open('./config.json') as f:
    config = json.load(f)

nhc = NHC(hostname=config['nhc']['hostname'])\
        .connect(
          username=config['nhc']['auth']['username'],
          password=config['nhc']['auth']['password']
        )\
        .wait_until_init_done()

print("Example 1. List devices")
for dev in nhc.devices():
    print(dev)

print("\nExample 1. Controlling a device (you will have to update the UUID)")
device = nhc.get_device('0395174f-f595-4267-b65a-8f5d92e63847') # lamp action
# device = nhc.get_device('2666b2d9-0f53-4ece-a16c-108e958cda97') # smart plug
device.control(status='on')

print("\nExample 2. Fetching the NHC version")
print(f"NHC Version in use: {nhc.system_information.sw_versions.nhc_version}\n")

print("Example 3. Show devices in each location")
for location in nhc.locations():
    print(location)
    for device in location.get_devices():
        print(f"- {device}")
        print(f"  properties: {device.property_definitions}")


# wait to see other events occur
while True:
    pass

