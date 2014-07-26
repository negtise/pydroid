
"""
from binder import Binder,Parcel

MP_SERVICE = 'media.player'
DESCRIPTOR = "android.net.wifi.IWifiManager";
FIRST_CALL_TRANSACTION = 1

mRemote = Binder(MP_SERVICE)
print mRemote.getInterfaceDescriptor()
"""
#I/amplayer( 5686): file::::[/storage/external_storage/sdcard1/gee.avi],len=41

import pydroid
pydroid.import_binder()
pydroid.import_mediaplayer()
pydroid.import_android_log()

from MediaPlayer import MediaPlayer
mp = MediaPlayer()

print '1111111'

video_path = r'/storage/external_storage/sdcard1/gee.avi'

#video_path = "http://beijing-mobile.tvvod.wasu.tv/data10/ott/344/2013-12/24/1387861279484_288967.ts?userID=2014042417684060&sessionID=1404722920916&proTitle=wasu"

print mp.setDataSource(video_path)

mp.prepare()
mp.start()

while mp.isPlaying():
    import time;time.sleep(1.0)
for i in range(10):
    import time;time.sleep(1.0)
    print 'zzz...'

mp.stop()


