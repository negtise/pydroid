from mediaplayer_ import MediaPlayer as NativeMediaPlayer
import os
class MediaPlayer(NativeMediaPlayer):
    def setDataSource(self,url):
        ret = False
        if os.path.exists(url):
            f = open(url,'rb')
            ret = self.setDataSourceFD(f.fileno(),0,0x7fffffff)
            f.close()
        else:
            ret = NativeMediaPlayer.setDataSource(self,url)
        return ret
