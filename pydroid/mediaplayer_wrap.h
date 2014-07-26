#ifndef __MEDIAPLAYER_WRAP_H_
#define __MEDIAPLAYER_WRAP_H_

#ifdef __cplusplus
extern "C" {
#endif

void *mediaplayer_new();
void mediaplayer_destroy(void *mediaplayer);
int mediaplayer_invoide(void *mediaplayer,void *request,void *reply);
//status_t MediaPlayer::setMetadataFilter(const Parcel& filter)
int mediaplayer_setMetadataFilter(void *mediaplayer,void *filter);
int mediaplayer_setDataSourceFD(void *mediaplayer,int fd,int offset,int length);
int mediaplayer_setDataSource(void *mediaplayer,const char *url);
void mediaplayer_prepare(void *mediaplayer);
void mediaplayer_start(void *mediaplayer);
void mediaplayer_stop(void *mediaplayer);
int mediaplayer_isPlaying(void *mediaplayer);

#ifdef __cplusplus
}
#endif

#endif //