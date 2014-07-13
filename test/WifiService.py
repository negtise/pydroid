from binder import Binder,Parcel

WIFI_SERVICE = "wifi";
DESCRIPTOR = "android.net.wifi.IWifiManager";
FIRST_CALL_TRANSACTION = 1
TRANSACTION_getConfiguredNetworks = (FIRST_CALL_TRANSACTION + 0);
TRANSACTION_addOrUpdateNetwork = (FIRST_CALL_TRANSACTION + 1);
TRANSACTION_removeNetwork = (FIRST_CALL_TRANSACTION + 2);
TRANSACTION_enableNetwork = (FIRST_CALL_TRANSACTION + 3);
TRANSACTION_disableNetwork = (FIRST_CALL_TRANSACTION + 4);
TRANSACTION_pingSupplicant = (FIRST_CALL_TRANSACTION + 5);
TRANSACTION_startScan = (FIRST_CALL_TRANSACTION + 6);
TRANSACTION_getScanResults = (FIRST_CALL_TRANSACTION + 7);
TRANSACTION_disconnect = (FIRST_CALL_TRANSACTION + 8);
TRANSACTION_reconnect = (FIRST_CALL_TRANSACTION + 9);
TRANSACTION_reassociate = (FIRST_CALL_TRANSACTION + 10);
TRANSACTION_getConnectionInfo = (FIRST_CALL_TRANSACTION + 11);
TRANSACTION_setWifiEnabled = (FIRST_CALL_TRANSACTION + 12);
TRANSACTION_getWifiEnabledState = (FIRST_CALL_TRANSACTION + 13);
TRANSACTION_setCountryCode = (FIRST_CALL_TRANSACTION + 14);
TRANSACTION_setFrequencyBand = (FIRST_CALL_TRANSACTION + 15);
TRANSACTION_getFrequencyBand = (FIRST_CALL_TRANSACTION + 16);
TRANSACTION_isDualBandSupported = (FIRST_CALL_TRANSACTION + 17);
TRANSACTION_saveConfiguration = (FIRST_CALL_TRANSACTION + 18);
TRANSACTION_getDhcpInfo = (FIRST_CALL_TRANSACTION + 19);
TRANSACTION_acquireWifiLock = (FIRST_CALL_TRANSACTION + 20);
TRANSACTION_updateWifiLockWorkSource = (FIRST_CALL_TRANSACTION + 21);
TRANSACTION_releaseWifiLock = (FIRST_CALL_TRANSACTION + 22);
TRANSACTION_initializeMulticastFiltering = (FIRST_CALL_TRANSACTION + 23);
TRANSACTION_isMulticastEnabled = (FIRST_CALL_TRANSACTION + 24);
TRANSACTION_acquireMulticastLock = (FIRST_CALL_TRANSACTION + 25);
TRANSACTION_releaseMulticastLock = (FIRST_CALL_TRANSACTION + 26);
TRANSACTION_setWifiApEnabled = (FIRST_CALL_TRANSACTION + 27);
TRANSACTION_getWifiApEnabledState = (FIRST_CALL_TRANSACTION + 28);
TRANSACTION_getWifiApConfiguration = (FIRST_CALL_TRANSACTION + 29);
TRANSACTION_setWifiApConfiguration = (FIRST_CALL_TRANSACTION + 30);
TRANSACTION_startWifi = (FIRST_CALL_TRANSACTION + 31);
TRANSACTION_stopWifi = (FIRST_CALL_TRANSACTION + 32);
TRANSACTION_addToBlacklist = (FIRST_CALL_TRANSACTION + 33);
TRANSACTION_clearBlacklist = (FIRST_CALL_TRANSACTION + 34);
TRANSACTION_getWifiServiceMessenger = (FIRST_CALL_TRANSACTION + 35);
TRANSACTION_getWifiStateMachineMessenger = (FIRST_CALL_TRANSACTION + 36);
TRANSACTION_getConfigFile = (FIRST_CALL_TRANSACTION + 37);
TRANSACTION_captivePortalCheckComplete = (FIRST_CALL_TRANSACTION + 38);

mRemote = Binder(WIFI_SERVICE)

def transact(TRANSACTION):
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION, _data, _reply, 0)
    _reply.readExceptionCode()
    return _reply.readInt32()

def getConfiguredNetworks():
    pass
def addOrUpdateNetwork():
    pass
def removeNetwork():
    pass
def enableNetwork(netId,disableOthers):
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    _data.writeInt32(netId)
    if disableOthers:
        _data.writeInt32(1)
    else:
        _data.writeInt32(0)
    mRemote.transact(TRANSACTION_enableNetwork, _data, _reply, 0)
    _reply.readExceptionCode()
    return _reply.readInt32() != 0
def disableNetwork(netId):
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    _data.writeInt32(netId)
    mRemote.transact(TRANSACTION_disableNetwork, _data, _reply, 0)
    _reply.readExceptionCode()
    return _reply.readInt32() != 0

def pingSupplicant():
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_pingSupplicant, _data, _reply, 0)
    _reply.readExceptionCode()
    return _reply.readInt32() != 0

def startScan(forceActive):
    _data = Parcel()
    _reply = Parcel()
    ret = 0
    try:
        _data.writeInterfaceToken(DESCRIPTOR)
        if forceActive:
            _data.writeInt(1)
        else:
            _data.writeInt(0)
        mRemote.transact(TRANSACTION_startScan, _data, _reply, 0)
        ret = _reply.readExceptionCode()
    finally:
        _reply.recycle()
        _data.recycle()
    return ret == 0
class WifiSsid:
    pass
    
def WifiSsid_createFromParcel(reply):
    ssid = WifiSsid()
    length = reply.readInt()
    arr = reply.readByteArray()
#    ssid.octets.write(b, 0, length)
    return ssid

class ScanResult:
    def __init__(self,ssid,bssid,caps,level,frequency,timestamp):
        self.ssid = ssid
        self.bssid = bssid
        self.caps = caps
        self.level = level
        self.frequency = frequency
        self.timestamp = timestamp
    @classmethod
    def createFromParcel(cls,reply):
        has_ssid = reply.readInt32()
        ssid = None
        if has_ssid:
            ssid_lengt = reply.readInt()
            ssid = reply.readByteArray()
        BSSID = reply.readString16()
        caps = reply.readString16()
        level = reply.readInt()
        frequency = reply.readInt()
        timestamp = reply.readInt64()
        
        print 'BSSID:',BSSID    
        print 'caps:',caps
        print 'level:',level
        print 'frequency:',frequency
        print 'timestamp:',timestamp
        return ScanResult(ssid,BSSID,caps,level,frequency,timestamp)

def getScanResults():
    _data = Parcel.obtain()
    _reply = Parcel.obtain()
    _result = None
    try:
        _data.writeInterfaceToken(DESCRIPTOR)
        mRemote.transact(TRANSACTION_getScanResults, _data, _reply, 0)
        if 0 != _reply.readExceptionCode():
            return None
        _result = _reply.createTypedArrayList(ScanResult)
    finally:
        _reply.recycle()
        _data.recycle()
    return _result

def disconnect():
    return transact(TRANSACTION_disconnect) != 0

def reconnect():
    return transact(TRANSACTION_reconnect) != 0

def reassociate():
    return transact(TRANSACTION_reassociate) != 0

"""
class WifiInfo:
    def __init__():
        pass
    @classmethod
    def createFromParcel(cls,r):
        info = WifiInfo();
        info.networkId  = r.readInt32()
        info.rssi = r.readInt32()
        info.linkSpeed = r.readInt32()
        if r.readByte() == 1:
            info.setInetAddress(InetAddress.getByAddress(in.createByteArray()))
        if r.readInt() == 1:
            info.mWifiSsid = WifiSsid.CREATOR.createFromParcel(r)
        info.mBSSID = r.readString16()
        info.mMacAddress = r.readString16()
        info.mMeteredHint = r.readInt32() != 0
"""

def getConnectionInfo():
    pass
def setWifiEnabled(enable):
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    if enable:
        _data.writeInt32(1)
    else:
        _data.writeInt32(0)
    mRemote.transact(TRANSACTION_setWifiEnabled, _data,_reply,0)
    _reply.readExceptionCode()
    _result = (0!=_reply.readInt32())
    return _result;

def getWifiEnabledState():
    return transact(TRANSACTION_getWifiEnabledState)
    
def setCountryCode(country,persist):
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    if isinstance(country,str):
        country = unicode(contry)
    _data.writeString16(country)
    if persist:
        _data.writeInt32(1)
    else:
        _data.writeInt32(0)
    mRemote.transact(TRANSACTION_setCountryCode, _data,_reply,0)
    _reply.readExceptionCode()
    _result = (0!=_reply.readInt32())
    return _result;
    
def setFrequencyBand(band, persist):
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    if isinstance(country,str):
        country = unicode(contry)
    _data.writeInt32(band)
    if persist:
        _data.writeInt32(1)
    else:
        _data.writeInt32(0)
    mRemote.transact(TRANSACTION_setFrequencyBand, _data,_reply,0)
    _reply.readExceptionCode()
    _result = (0!=_reply.readInt32())
    return _result;

def getFrequencyBand():
    return transact(TRANSACTION_getFrequencyBand)

def isDualBandSupported():
    return transact(TRANSACTION_isDualBandSupported) != 0
def saveConfiguration():
    pass

def get_readable_address(addr):
    return "%d:%d:%d:%d"%(addr&0xff,(addr>>8)&0xff,(addr>>16)&0xff,(addr>>24)&0xff)

def getDhcpInfo():
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_getDhcpInfo, _data,_reply,0)
    _reply.readExceptionCode()
    if 0 == _reply.readInt32():
        return None

    ipAddress = get_readable_address(reply.readInt32());
    gateway = get_readable_address(reply.readInt32());
    netmask = get_readable_address(reply.readInt32());
    dns1 = get_readable_address(reply.readInt32());
    dns2 = get_readable_address(reply.readInt32());
    serverAddress = get_readable_address(reply.readInt32());
    leaseDuration = get_readable_address(reply.readInt32());

    info = (ipAddress,gateway,netmask,dns1,dns2,serverAddress,leaseDuration)
    print "ipAddress %s,\ngateway %s,\nnetmask %s,\ndns1 %s,\ndns2 %s,\nserverAddress %s,\nleaseDuration %s"%info
    return info
        
def acquireWifiLock():
    pass
def updateWifiLockWorkSource():
    pass
def releaseWifiLock():
    pass
def initializeMulticastFiltering():
    pass
def isMulticastEnabled():
    pass
def acquireMulticastLock():
    pass
def releaseMulticastLock():
    pass
def setWifiApEnabled(wifiConfig,enable):
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    if wifiConfig:
        _data.writeInt32(1)
        wifiConfig.writeToParcel(_data)
    else:
        _data.writeInt32(0)
    if enable:
        _data.writeInt32(1)
    else:
        _data.writeInt32(0)
        
    mRemote.transact(TRANSACTION_setWifiApEnabled, _data,_reply,0)
    _reply.readExceptionCode()

def getWifiApEnabledState():
    return transact(TRANSACTION_getWifiApEnabledState)

def getWifiApConfiguration():
    pass
def setWifiApConfiguration():
    pass
def startWifi():
    return transact(TRANSACTION_startWifi)
def stopWifi():
    return transact(TRANSACTION_stopWifi)
def addToBlacklist(bssid):
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    if isinstance(bssid,str):
        bssid = unicode(bssid)
    _data.writeString16(bssid)
    mRemote.transact(TRANSACTION_addToBlacklist, _data,_reply,0)
    _reply.readExceptionCode()
    
def clearBlacklist():
    return transact(TRANSACTION_clearBlacklist)
def getWifiServiceMessenger():
    pass
def getWifiStateMachineMessenger():
    pass
def getConfigFile():
    _data = Parcel()
    _reply = Parcel()
    _data.writeInterfaceToken(DESCRIPTOR)
    mRemote.transact(TRANSACTION_getConfigFile, _data,_reply,0)
    _reply.readExceptionCode()
    return _reply.readString16()

def captivePortalCheckComplete():
    return transact(TRANSACTION_captivePortalCheckComplete) != 0
