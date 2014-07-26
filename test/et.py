import EthernetService

#getDeviceNameList()
print EthernetService.isEthDeviceUp()
print EthernetService.getEthState()
print EthernetService.isEthConfigured()
print 'getTotalInterface:',EthernetService.getTotalInterface()
EthernetService.getDhcpInfo()

#get_dhcp_info()



