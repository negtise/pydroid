cdef extern from "utils/Unicode.h":
    ctypedef short char16_t
    ctypedef unsigned int uint32_t

cdef extern from "Python.h":
    ctypedef short Py_UNICODE
    ctypedef size_t Py_ssize_t
    object PyString_FromStringAndSize(const char *v, Py_ssize_t len) 
    int PyString_AsStringAndSize(object obj, char **buffer, Py_ssize_t *length) 
    object PyUnicode_FromUnicode(const Py_UNICODE *u, Py_ssize_t size) 
    Py_UNICODE* PyUnicode_AS_UNICODE(object)
    Py_ssize_t PyUnicode_GetSize(object)
    void Py_INCREF(object)
    void Py_DECREF(object)

cdef extern from "binder_wrap.h":
    ctypedef int (*vector_visitor)(const char16_t* str16,int length,void *data)
    int binder_listServices(vector_visitor visitor,void *data)
    ctypedef int (*fnOnTransact)(uint32_t code,const void *data,void *reply,uint32_t flags,void *userData)
    int server_create(const char *name,const char *descriptor,fnOnTransact onTrans,void *data)
    void* binder_getbinder(const char *name)
    int binder_releasebinder(void* binder)
    int binder_getInterfaceDescriptor(void *binder,char16_t *descriptor,int size)
    int binder_transact(void* binder,int code,const void *data,void* reply,int flags)

    void* parcel_new()
    int parcel_destroy(void* parcel)
    int parcel_writeInterfaceToken(void* parcel,const char *interface)
    int parcel_writeInt32(void *parcel,int val)
    int parcel_writeCString(void *parcel,const char* str)
    int parcel_writeString16(void *parcel,const char16_t* str, size_t len)

    int parcel_readInt32(void *parcel)
    int parcel_readInt64(void *parcel)
    int parcel_readString16(void *parcel,char16_t* str, size_t len)
    int parcel_readExceptionCode(void *parcel)
    int parcel_readInplace(void *parcel,void* data, int len)

    int parcel_dataAvail(void *parcel)


cdef int visitor(const char16_t* str16,int length,void *data):
    arr = <object>data
    o = PyUnicode_FromUnicode(<Py_UNICODE*>str16,length)
    arr.append(o)
    
def listServices():
    arr = []
    Py_INCREF(arr)
    binder_listServices(visitor,<void *>arr)
    Py_DECREF(arr)
    return arr

cdef class NativeBinder:
    cdef void *ptr
    def __cinit__(self,char *name): #, sp[IBinder] service):
        self.ptr = binder_getbinder(name)

    def __dealloc__(self):
        binder_releasebinder(self.ptr)

    def getInterfaceDescriptor(self):
        cdef char16_t descriptor[256]
        cdef int ret
        ret = binder_getInterfaceDescriptor(self.ptr,descriptor,sizeof(descriptor))
        if not ret:
            return None
        return PyUnicode_FromUnicode(<Py_UNICODE*>descriptor,ret)

    def transact(self,int code,data,reply,int flags):
        cdef int dataPtr = data.getNativePtr()
        cdef int replyPtr = reply.getNativePtr()
        binder_transact(self.ptr,code,<void *>dataPtr,<void*>replyPtr,flags)
        return reply

cdef class NativeParcel:
    cdef void *ptr
    cdef int nativePtr
    def __cinit__(self,unsigned int nativePtr=0): #, sp[IBinder] service):
        self.nativePtr = nativePtr
        if not nativePtr:
            self.ptr = parcel_new()
        else:
            self.ptr = <void *>nativePtr

    def __dealloc__(self):
        if not self.nativePtr:
            parcel_destroy(self.ptr)

    def getNativePtr(self):
        return <int>self.ptr

    def writeInterfaceToken(self,const char *interface):
        return parcel_writeInterfaceToken(<void *>self.ptr,interface)

    def writeInt(self,int val):
        self.writeInt32(val)
    def writeInt32(self,int val):
        return parcel_writeInt32(<void *>self.ptr,val)

    def writeCString(self,const char* cstr):
        return parcel_writeCString(<void *>self.ptr,cstr)

    def writeString16(self,ustr):
        cdef char16_t *un
        cdef int size
        if not ustr:
            return parcel_writeString16(<void *>self.ptr,<char16_t*>0,0)
        elif isinstance(ustr,unicode):
            un = <char16_t*>PyUnicode_AS_UNICODE(ustr)
            size = PyUnicode_GetSize(ustr)
            return parcel_writeString16(<void *>self.ptr,un,size)

    def readInt32(self):
        return parcel_readInt32(self.ptr)
    def readInt(self):
        return self.readInt32()

    def readInt64(self):
        return parcel_readInt64(self.ptr)

    def readExceptionCode(self):
        return parcel_readExceptionCode(self.ptr)

    def readString16(self):
        cdef char16_t str16[256]
        cdef int ret
        ret = parcel_readString16(self.ptr,str16,sizeof(str16))
        if not ret:
            return None
        return PyUnicode_FromUnicode(<Py_UNICODE*>str16,ret)

    def readByteArray(self):
        return self.createByteArray()

    def createByteArray(self):
        length = self.readInt()
        print 'createByteArray:',length
        return self.readInplace(length)

#    int parcel_readInplace(void *parcel,void* data, size_t len)
    def readInplace(self,length):
        cdef char arr[512]
        ret = parcel_readInplace(self.ptr,arr,length)
        if ret == length:
            return PyString_FromStringAndSize(arr,length)
        else:
            return None

#    int parcel_dataAvail(void *parcel)
    def dataAvail(self):
        return parcel_dataAvail(self.ptr)

    def createTypedArrayList(self,creator):
        N = self.readInt()
        if N <= 0:
            return None
        arr = []
        for i in range(N):
            if self.readInt() == 0:
                continue
            else:
                result = creator.createFromParcel(self)
                arr.append(result)
        return arr

cdef int OnTransact(uint32_t code,const void *data,void *reply,uint32_t flags,void *userData) with gil:
    d = Parcel(<unsigned int>data)
    r = Parcel(<unsigned int>reply)
    service = <object>userData
    return service.OnTransact(code,d,r,flags)

class Service(object):
    def __init__(self,const char *name,const char *descriptor):
        Py_INCREF(self)
        server_create(name,descriptor,OnTransact,<void *>self)
    def OnTransact(self,code,data,reply,flags):
        return 0
