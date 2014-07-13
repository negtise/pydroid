cdef extern from "android/log.h":
    ctypedef enum android_LogPriority:
        ANDROID_LOG_UNKNOWN = 0
        ANDROID_LOG_DEFAULT = 1   #/* only for SetMinPriority() */
        ANDROID_LOG_VERBOSE = 2
        ANDROID_LOG_DEBUG = 3
        ANDROID_LOG_INFO = 4
        ANDROID_LOG_WARN = 5
        ANDROID_LOG_ERROR = 6
        ANDROID_LOG_FATAL = 7
        ANDROID_LOG_SILENT = 8     #/* only for SetMinPriority(); must be last */

    int __android_log_print(int prio, const char *tag,  const char *fmt, ...)

cdef char *LOG_TAG="sysmonitor"

def i(char *text):
    __android_log_print(ANDROID_LOG_INFO,LOG_TAG,"%s",text)

def d(char *text):
    __android_log_print(ANDROID_LOG_DEBUG,LOG_TAG,"%s",text)

def w(char *text):
    __android_log_print(ANDROID_LOG_WARN,LOG_TAG,"%s",text)

def e(char *text):
    __android_log_print(ANDROID_LOG_ERROR,LOG_TAG,"%s",text)

def p(int level,char *tag,char *text):
    __android_log_print(level,tag,"%s",text)

