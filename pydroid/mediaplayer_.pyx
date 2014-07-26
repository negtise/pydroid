cdef extern from "mediaplayer_wrap.h":
    void *mediaplayer_new()
    void mediaplayer_destroy(void *mediaplayer)
    int mediaplayer_invoide(void *mediaplayer,void *request,void *reply)
    int mediaplayer_setMetadataFilter(void *mediaplayer,void *filter)
    int mediaplayer_setDataSourceFD(void *mediaplayer,int fd,int offset,int length)
    int mediaplayer_setDataSource(void *mediaplayer,const char *url)
    void mediaplayer_prepare(void *mediaplayer)
    void mediaplayer_start(void *mediaplayer)
    void mediaplayer_stop(void *mediaplayer)
    bint mediaplayer_isPlaying(void *mediaplayer)


cdef class MediaPlayer:
    cdef void *ptr
    def __cinit__(self):
        self.ptr = mediaplayer_new()
    def __dealloc__(self):
        mediaplayer_destroy(self.ptr)
    def setDataSource(self,url):
        return mediaplayer_setDataSource(self.ptr,url)
    def setDataSourceFD(self,int fd,int offset,int length):
        return mediaplayer_setDataSourceFD(self.ptr,fd,offset,length)
    def prepare(self):
        mediaplayer_prepare(self.ptr)
    def start(self):
        mediaplayer_start(self.ptr)
    def stop(self):
        mediaplayer_stop(self.ptr)
    def isPlaying(self):
        return mediaplayer_isPlaying(self.ptr)    

