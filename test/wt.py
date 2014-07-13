import time
import binder

#for s in  binder.listServices():
#    print s

import WifiService

WifiService.setWifiEnabled(True)

WifiService.startScan(True)

print WifiService.pingSupplicant()
print WifiService.getConfigFile()

for i in range(0):
    time.sleep(1.0)
    result = WifiService.getScanResults()
    if result:
        print result
        break
