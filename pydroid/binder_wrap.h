#ifndef BINDER_WRAP_H
#define BINDER_WRAP_H


#ifdef __cplusplus
extern "C" {
#endif

typedef int (*vector_visitor)(const char16_t* str16,int length,void *data);
typedef int (*fnOnTransact)(uint32_t code,const void *data,void *reply,uint32_t flags,void *userData);
int server_create(const char *name,const char *descriptor,fnOnTransact onTrans,void *data);

void* binder_getbinder(const char *name);
int binder_releasebinder(void* binder);
int binder_listServices(vector_visitor visitor,void *data);
int binder_getInterfaceDescriptor(void *binder,char16_t *descriptor,size_t size);
int binder_transact(void* binder,int code,const void *data,void* reply,int flags);
void* parcel_new();
int parcel_destroy(void* parcel);
int parcel_writeInterfaceToken(void* parcel,const char *interface);
int parcel_writeInt32(void *parcel,int val);
int parcel_writeCString(void *parcel,const char* str);
int parcel_writeString16(void *parcel,const char16_t* str, size_t len);

int parcel_readInt32(void *parcel);
long parcel_readInt64(void *parcel);
int parcel_readString16(void *parcel,char16_t* str, size_t len);
int parcel_readInplace(void *parcel,void* data, int len);
int parcel_readExceptionCode(void *parcel);
int parcel_dataAvail(void *parcel);

#ifdef __cplusplus
}
#endif

#endif

