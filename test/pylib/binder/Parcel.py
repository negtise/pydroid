from binder_ import Parcel as NativeParcel
class Parcel(NativeParcel):
    def writeStringArray(self,strList):
        if strList:
            N = len(strList)
            self.writeInt32(N)
            for s in strList:
                if isinstance(s,str):
                    self.writeCString(s)
                elif isinstance(s,unicode):
                    self.writeString16(s)
        else:
            self.writeInt32(-1)
    def writeByte(self,b):
        self.writeInt32(b)
    def writeParcelable(self,p,flags):
        if not p:
            self.writeString16(None)
            return
        self.writeString16(p.getName)
        self.writeToParcel(self,flags)
    @classmethod
    def obtain(cls):
        return Parcel()
    @classmethod
    def recycle(cls):
        pass