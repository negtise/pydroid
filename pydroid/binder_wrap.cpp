#include <sys/types.h>
#include <unistd.h>
#include <grp.h>

#include <binder/IPCThreadState.h>
#include <binder/ProcessState.h>
#include <binder/IServiceManager.h>
#include <utils/Log.h>

#include <binder/Parcel.h>

#include "binder_wrap.h"

using namespace android;

void* binder_getbinder(const char *name)
{
    android::sp<android::IServiceManager> sm = android::defaultServiceManager();
    sp<IBinder> *binder = new sp<IBinder>();
    do {
        *binder = sm->getService(android::String16(name));
        if (binder != 0)
        {
            break;
        }
        usleep(500000); // 0.5 s
    } while(true);
    return reinterpret_cast<void *>(binder);
}

int binder_releasebinder(void* binder)
{
    sp<IBinder> *bp = reinterpret_cast<sp<IBinder> *>(binder);

    if(bp == 0)
    {
        return 0;
    }

    delete bp;
    
    return 1;
}

//Vector<String16>    listServices() = 0;
int binder_listServices(vector_visitor visitor,void *data)
{
    android::sp<android::IServiceManager> sm = android::defaultServiceManager();

    Vector<String16> list = sm->listServices();

    for (int i=0;i<list.size();i++)
    {
        visitor(list[i].string(),list[i].size(),data);
    }
    
    return list.size();
}

int binder_getInterfaceDescriptor(void *binder,char16_t *descriptor,size_t size)
{
    sp<IBinder> *bp = reinterpret_cast<sp<IBinder> *>(binder);

    if(bp == 0)
    {
        return 0;
    }
    
    if (descriptor == NULL || size <= 0)
    {
        return 0;
    }
    
    String16 des = (*bp)->getInterfaceDescriptor();

    if (size > des.size())
    {
        size = des.size();
    }

    memcpy(descriptor,des.string(),size*2);

    return size;
}

//int binder_transact(void* binder,int code,const Parcel& data,Parcel* reply,int flags = 0)
int binder_transact(void* binder,int code,const void *data,void* reply,int flags)
{
    sp<IBinder> *bp = reinterpret_cast<sp<IBinder> *>(binder);
 
    if(bp == 0 || data == 0 || reply == 0)
    {
        return 0;
    }
    return (*bp)->transact(code,*(Parcel*)data,(Parcel*)reply,flags);
}

void* parcel_new()
{
    return (void*)new Parcel();
}

int parcel_destroy(void* parcel)
{
    if(parcel == 0)
    {
        return 0;
    }
    delete (Parcel*)parcel;
    return 1;
}

int parcel_writeInterfaceToken(void* parcel,const char *interface)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);
    
    if(p == 0)
    {
        return 0;
    }
    return p->writeInterfaceToken(String16(interface));
}

int parcel_writeInt32(void *parcel,int val)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);
    
    if(p == 0)
    {
        return 0;
    }

    return p->writeInt32(val);
}

int parcel_writeCString(void *parcel,const char* str)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);

    if(p == 0)
    {
        return 0;
    }
    return p->writeCString(str);
}

int parcel_writeString16(void *parcel,const char16_t* str, size_t len)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);
    
    if(p == 0)
    {
        return 0;
    }
    
    if (str == 0 || len <= 0)
    {
        return 0;
    }
    
    return p->writeString16(str,len);
}


int parcel_readInt32(void *parcel)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);
    
    if(p == 0)
    {
        return 0;
    }
    return p->readInt32();
}

long parcel_readInt64(void *parcel)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);

    if(p == 0)
    {
        return 0;
    }
    return p->readInt64();
}

int parcel_readString16(void *parcel,char16_t* str, size_t len)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);

    if(p == 0)
    {
        return 0;
    }

    if (str == NULL || len <= 0)
    {
        return 0;
    }
    
    String16 str16 = p->readString16();
    
    if (len > str16.size())
    {
        len = str16.size();
    }
    
    memcpy(str,str16.string(),len*2);

    return len;
}

int parcel_readExceptionCode(void *parcel)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);

    if(p == 0)
    {
        return 0;
    }
    return p->readExceptionCode();
}


int parcel_readInplace(void *parcel,void* data, int len)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);

    if(p == 0)
    {
        return 0;
    }

    if (len >= 0 && len <= (int32_t)p->dataAvail())
    {
        const void *d = p->readInplace(len);
        memcpy(data,d,len);
        return len;
    }
    return 0;
}

int parcel_dataAvail(void *parcel)
{
    Parcel *p = reinterpret_cast<Parcel *>(parcel);

    if(p == 0)
    {
        return 0;
    }

    return p->dataAvail();
    
}

#define  LOGI(...)  __android_log_print(ANDROID_LOG_INFO,LOG_TAG,__VA_ARGS__)
#define  LOGE(...)  __android_log_print(ANDROID_LOG_ERROR,LOG_TAG,__VA_ARGS__)
#define  LOGW(...)  __android_log_print(ANDROID_LOG_ERROR,LOG_TAG,__VA_ARGS__)

using namespace android;

class PythonBBinder : public BBinder
{
public:
    static  status_t                instantiate(const char *name,const char *descriptor,fnOnTransact onTrans,void *data);

                            PythonBBinder(const char *name,const char *descriptor,fnOnTransact onTrans,void *data);
    virtual                 ~PythonBBinder();

    virtual status_t onTransact(uint32_t code,
                                 const android::Parcel &data,
                                 android::Parcel *reply,
                                 uint32_t flags);

private:
    android::String16 name;
    android::String16 descriptor;
    fnOnTransact mOnTransact;
    void *mData;
};

status_t PythonBBinder::instantiate(const char *name,const char *descriptor,fnOnTransact onTrans,void *data)
{
    if(name == NULL || descriptor == NULL)
    {
        return -1;
    }
	return android::defaultServiceManager()->addService(String16(name),new PythonBBinder(name,descriptor,onTrans,data));
    ProcessState::self()->startThreadPool();
}

PythonBBinder::PythonBBinder(const char *name,const char *descriptor,fnOnTransact onTrans,void *data)
{
    LOGE("PythonBBinder created");
    this->name = String16(name);
    this->descriptor = String16(descriptor);
    this->mOnTransact = onTrans;
    this->mData = data;
}

PythonBBinder::~PythonBBinder()
{
    LOGE("PythonBBinder destroyed");
}

android::status_t PythonBBinder::onTransact(uint32_t code,
                                                const android::Parcel &data,
                                                android::Parcel *reply,
                                                uint32_t flags)
{
        LOGE("OnTransact(%u,%u)", code, flags);
        if (this->mOnTransact) 
        {
            if (!data.enforceInterface(this->descriptor)) 
            {
                return android::PERMISSION_DENIED;
            }
//            CHECK_INTERFACE(IPythonBBinder, data, reply);
            return this->mOnTransact(code,reinterpret_cast<const void*>(&data),reinterpret_cast<void *>(reply),flags,this->mData);
        }
        else
        {
            return BBinder::onTransact(code, data, reply, flags);            
        }
        return android::NO_ERROR;
}

int server_create(const char *name,const char *descriptor,fnOnTransact onTrans,void *data)
{
    return PythonBBinder::instantiate(name,descriptor,onTrans,data);
}
