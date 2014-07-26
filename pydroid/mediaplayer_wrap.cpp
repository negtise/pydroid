#include "utils/Log.h"

#include <media/mediaplayer.h>
#include <media/MediaPlayerInterface.h>
#include <stdio.h>
#include <assert.h>
#include <limits.h>
#include <unistd.h>
#include <fcntl.h>
#include <utils/threads.h>
#include "utils/Errors.h"  // for status_t
#include "utils/KeyedVector.h"
#include "utils/String8.h"
#include <binder/Parcel.h>
#include <gui/ISurfaceTexture.h>
#include <gui/Surface.h>
#include <binder/IPCThreadState.h>
#include <binder/IServiceManager.h>

#include "mediaplayer_wrap.h"


#include <gui/ISurfaceComposer.h>
#include <gui/SurfaceComposerClient.h>
#include <ui/DisplayInfo.h>

using namespace android;

class PyMediaPlayerListener: public MediaPlayerListener
{
    
};

#include <string.h>

#include <media/stagefright/foundation/ABase.h>
#include <media/stagefright/foundation/AString.h>
#include <utils/Log.h>

#define LITERAL_TO_STRING_INTERNAL(x)    #x
#define LITERAL_TO_STRING(x) LITERAL_TO_STRING_INTERNAL(x)

#define CHECK(condition)                                \
    LOG_ALWAYS_FATAL_IF(                                \
            !(condition),                               \
            "%s",                                       \
            __FILE__ ":" LITERAL_TO_STRING(__LINE__)    \
            " CHECK(" #condition ") failed.")

#define MAKE_COMPARATOR(suffix,op)                          \
    template<class A, class B>                              \
    AString Compare_##suffix(const A &a, const B &b) {      \
        AString res;                                        \
        if (!(a op b)) {                                    \
            res.append(a);                                  \
            res.append(" vs. ");                            \
            res.append(b);                                  \
        }                                                   \
        return res;                                         \
    }

MAKE_COMPARATOR(EQ,==)
MAKE_COMPARATOR(NE,!=)
MAKE_COMPARATOR(LE,<=)
MAKE_COMPARATOR(GE,>=)
MAKE_COMPARATOR(LT,<)
MAKE_COMPARATOR(GT,>)


#define CHECK_OP(x,y,suffix,op)                                         \
    do {                                                                \
        AString ___res = Compare_##suffix(x, y);                        \
        if (!___res.empty()) {                                          \
            AString ___full =                                           \
                __FILE__ ":" LITERAL_TO_STRING(__LINE__)                \
                    " CHECK_" #suffix "( " #x "," #y ") failed: ";      \
            ___full.append(___res);                                     \
                                                                        \
            LOG_ALWAYS_FATAL("%s", ___full.c_str());                    \
        }                                                               \
    } while (false)

#define CHECK_EQ(x,y)   CHECK_OP(x,y,EQ,==)
#define CHECK_NE(x,y)   CHECK_OP(x,y,NE,!=)
#define CHECK_LE(x,y)   CHECK_OP(x,y,LE,<=)
#define CHECK_LT(x,y)   CHECK_OP(x,y,LT,<)
#define CHECK_GE(x,y)   CHECK_OP(x,y,GE,>=)
#define CHECK_GT(x,y)   CHECK_OP(x,y,GT,>)

void test()
{

    sp<SurfaceComposerClient> composerClient;
    sp<SurfaceControl> control;
    sp<Surface> surface;
    
    bool playback = true;
    bool useSurface = true;
    bool useVideo = true;
    
    if (playback || (useSurface && useVideo)) {
        composerClient = new SurfaceComposerClient;
        CHECK_EQ(composerClient->initCheck(), (status_t)OK);

        sp<IBinder> display(SurfaceComposerClient::getBuiltInDisplay(ISurfaceComposer::eDisplayIdMain));
        DisplayInfo info;
        SurfaceComposerClient::getDisplayInfo(display, &info);
        ssize_t displayWidth = info.w/2;
        ssize_t displayHeight = info.h/2;

        ALOGV("display is %ld x %ld\n", displayWidth, displayHeight);

        printf("display is %ld x %ld\n", displayWidth, displayHeight);

        control = composerClient->createSurface(String8("A Surface"),displayWidth,displayHeight,PIXEL_FORMAT_RGB_565,0);

        CHECK(control != NULL);
        CHECK(control->isValid());

        SurfaceComposerClient::openGlobalTransaction();
        CHECK_EQ(control->setLayer(INT_MAX), (status_t)OK);
        CHECK_EQ(control->show(), (status_t)OK);
        SurfaceComposerClient::closeGlobalTransaction();

        surface = control->getSurface();
        CHECK(surface != NULL);
    }

    const char *url = "http://beijing-mobile.tvvod.wasu.tv/data10/ott/344/2013-12/24/1387861279484_288967.ts?userID=2014042417684060&sessionID=1404722920916&proTitle=wasu";
//    const char *url = "/storage/external_storage/sdcard1/gee.avi";
    sp<MediaPlayer> mp = new MediaPlayer();

//    mp->setDataSource("/storage/external_storage/sdcard1/gee.avi",0);
//    mp->setDataSource("/mnt/nfs/system/extras/sysmonitor/py/ding.wav",0);
    ALOGE("++++++++++++++++++++++setDataSource(%s)", url);
#if 1
    int fd = open(url,O_RDONLY);
    mp->setDataSource(fd,0,0x7fffffffffffffffL);
#else

    mp->setDataSource(url,0);
#endif
    mp->setVideoSurfaceTexture(surface->getSurfaceTexture());
    printf("+++++++++prepare\n");
    mp->prepare();
//    mp->prepareAsync();
    sleep(5);
    printf("start\n");
    mp->start();
    while (mp->isPlaying()) {
        printf("++++++++playing...");
        sleep(1);
    }
}
void *mediaplayer_new()
{
//    test();
//    return 0;

    sp<MediaPlayer> mp = new MediaPlayer();
    mp->incStrong(mp.get());
    return (void*)mp.get();
}

void mediaplayer_destroy(void *mediaplayer)
{
    if (mediaplayer == 0)
    {
        return;
    }
    sp<MediaPlayer> mp = (MediaPlayer*)mediaplayer;
    mp->decStrong(mp.get()) ;
    if (mp != NULL) {
        // this prevents native callbacks after the object is released
        mp->setListener(0);
        mp->disconnect();
    }
}

int mediaplayer_invoide(void *mediaplayer,void *request,void *reply)
{
    if (mediaplayer == 0 || request == 0 || reply == 0)
    {
        return 0;
    }
    MediaPlayer *mp = (MediaPlayer*) mediaplayer;
    Parcel *req = (Parcel *)request;
    Parcel *rep = (Parcel *)reply;
    return mp->invoke(*req, rep);
}

//status_t MediaPlayer::setMetadataFilter(const Parcel& filter)
int mediaplayer_setMetadataFilter(void *mediaplayer,void *filter)
{
    if(mediaplayer == 0 || filter == 0)
    {
        return 0;
    }
    Parcel *f = (Parcel*)filter;
    MediaPlayer *mp = (MediaPlayer *)mediaplayer;
    return mp->setMetadataFilter(*f);
}

int mediaplayer_setDataSourceFD(void *mediaplayer,int fd,int offset,int length)
{
    if (mediaplayer == 0)
    {
        return 0;
    }
    
    MediaPlayer *mp = (MediaPlayer*)mediaplayer;
    return mp->setDataSource(fd,offset,length);
}

int mediaplayer_setDataSource(void *mediaplayer,const char *url)
{
    if (mediaplayer == 0)
    {
        return 0;
    }
    
    MediaPlayer *mp = (MediaPlayer*)mediaplayer;
    return mp->setDataSource(url,0);
}

void mediaplayer_prepare(void *mediaplayer)
{
    if (mediaplayer == 0)
    {
        return;
    }
    MediaPlayer *mp = (MediaPlayer*)mediaplayer;
    mp->prepare();    
}


void mediaplayer_start(void *mediaplayer)
{
    if (mediaplayer == 0)
    {
        return;
    }
    MediaPlayer *mp = (MediaPlayer*)mediaplayer;
    mp->start();
}

void mediaplayer_stop(void *mediaplayer)
{
    if (mediaplayer == 0)
    {
        return;
    }
    
    MediaPlayer *mp = (MediaPlayer*)mediaplayer;
    mp->stop();
}

int mediaplayer_isPlaying(void *mediaplayer)
{
    if (mediaplayer == 0)
    {
        return 0;
    }
    sp<MediaPlayer> mp = (MediaPlayer*)mediaplayer;
    return mp->isPlaying();
}

