import binder
from binder import Parcel

DESCRIPTOR = "android.net.ethernet.IEthernetManager"
FIRST_CALL_TRANSACTION=1
TRANSACTION_getDeviceNameList = (FIRST_CALL_TRANSACTION + 0)
TRANSACTION_setEthState = (FIRST_CALL_TRANSACTION + 1)
TRANSACTION_getEthState = (FIRST_CALL_TRANSACTION + 2)
TRANSACTION_UpdateEthDevInfo = (FIRST_CALL_TRANSACTION + 3)
TRANSACTION_isEthConfigured = (FIRST_CALL_TRANSACTION + 4)
TRANSACTION_getSavedEthConfig = (FIRST_CALL_TRANSACTION + 5)
TRANSACTION_getTotalInterface = (FIRST_CALL_TRANSACTION + 6)
TRANSACTION_setEthMode = (FIRST_CALL_TRANSACTION + 7)
TRANSACTION_isEthDeviceUp = (FIRST_CALL_TRANSACTION + 8)
TRANSACTION_isEthDeviceAdded = (FIRST_CALL_TRANSACTION + 9)
TRANSACTION_getDhcpInfo = (FIRST_CALL_TRANSACTION + 10)

ETH_STATE_UNKNOWN = 0
ETH_STATE_DISABLED = 1
ETH_STATE_ENABLED = 2

mRemote = binder.Binder('ethernet')

def getDeviceNameList():
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_getDeviceNameList, data,reply,0)
    reply.readExceptionCode()
    result = reply.readInt32()
    arr = []
    for i in range(result):
        arr.append(reply.readString16())
    return arr

def setEthState(state):
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    data.writeInt(state)
    mRemote.transact(TRANSACTION_setEthState, data,reply,0)
    reply.readExceptionCode()

def getEthState():
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_getEthState, data,reply,0)
    reply.readExceptionCode()
    return reply.readInt32()

class ProxyProperties:
    name = 'android.net.ProxyProperties'
    def __init__(self,host=None,port=None,exList=None,parsedExcList=None):
        self.host = host #string
        self.port = port #int
        self.exclusionList = exList #string
        self.parsedExclusionList = parsedExcList #string list
    def writeToParcel(self,dest,flags):
        if mHost:
            dest.writeByte(1)
            dest.writeString16(self.host)
            dest.writeInt32(self.port)
        else:
            dest.writeByte(0)
        dest.writeString(self.exclusionList)
        dest.writeStringArray(self.parsedExclusionList)
    @staticmethod
    def getName(cls):
        return name

class EthernetDevInfo(object):
    def __init__(self,devName=None,ipaddr=None,netmask=None,route=None,dns=None,mode=None,proxy=None):
        self.devName = devName
        self.ipAddr = ipaddr
        self.netmask = netmask
        self.route = route
        self.dns = dns
        self.mode = mode
        self.proxy = proxy
    def writeToParcel(self,dest,flags):
		dest.writeString16(this.dev_name)
		dest.writeString16(this.ipaddr)
		dest.writeString16(this.netmask)
		dest.writeString16(this.route)
		dest.writeString16(this.dns)
		dest.writeString16(this.mode)
		dest.writeParcelable(self.proxy,flags)

def UpdateEthDevInfo():
    pass
def isEthConfigured():
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_isEthConfigured, data,reply,0)
    reply.readExceptionCode()
    return 0 != reply.readInt32()
    
def getSavedEthConfig():
    pass

def getTotalInterface():
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_getTotalInterface, data,reply,0)
    reply.readExceptionCode()
    return reply.readInt32()

def setEthMode(mode):
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    data.writeInt(mode)
    mRemote.transact(TRANSACTION_setEthMode, data,reply,0)
    reply.readExceptionCode()

def isEthDeviceUp():
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_isEthDeviceUp, data,reply,0)
    reply.readExceptionCode()
    return 0 != reply.readInt32()

def isEthDeviceAdded():
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_isEthDeviceAdded, data,reply,0)
    reply.readExceptionCode()
    return 0 != reply.readInt32()

def getDhcpInfo():
    data = Parcel()
    reply = Parcel()
    data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_getDhcpInfo, data,reply,0)
    reply.readExceptionCode()
    result = reply.readInt32()
    
    def get_readable_address(addr):
        return "%d:%d:%d:%d"%(addr&0xff,(addr>>8)&0xff,(addr>>16)&0xff,(addr>>24)&0xff)
    
    if not result:
        return None

    ipAddress = get_readable_address(reply.readInt32())
    gateway = get_readable_address(reply.readInt32())
    netmask = get_readable_address(reply.readInt32())
    dns1 = get_readable_address(reply.readInt32())
    dns2 = get_readable_address(reply.readInt32())
    serverAddress = get_readable_address(reply.readInt32())
    leaseDuration = get_readable_address(reply.readInt32())
    info = (ipAddress,gateway,netmask,dns1,dns2,serverAddress,leaseDuration)
    print "ipAddress %s,\ngateway %s,\nnetmask %s,\ndns1 %s,\ndns2 %s,\nserverAddress %s,\nleaseDuration %s"%info
    return info
