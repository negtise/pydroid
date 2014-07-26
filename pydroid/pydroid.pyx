cdef extern void initbinder_()
cdef extern void initmediaplayer_()
cdef extern void initandroidlog()
cdef extern void pydroid_init()

def init():
    pydroid_init()
    initbinder_()
    initmediaplayer_()
    initandroidlog()
def import_binder():
    initbinder_()
def import_mediaplayer():
    initmediaplayer_()
def import_android_log():
    initandroidlog()
init()

