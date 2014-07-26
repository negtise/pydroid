# Copyright 2005 The Android Open Source Project

LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)

LOCAL_C_INCLUDES := \
	$(LOCAL_PATH)/../include/python \

LOCAL_LDFLAGS += -ldl -lz

LOCAL_SHARED_LIBRARIES := \
	libstagefright liblog libutils libbinder libstagefright_foundation \
        libmedia libmedia_native libgui libcutils libui

LOCAL_LDFLAGS += -L$(LOCAL_PATH)/../libs/ -lpython2.7 

LOCAL_SRC_FILES := \
    pydroid.c \
	main.cpp \
	pybinder_.cpp \
    binder_wrap.cpp \
    pyandroidlog.c \
    mediaplayer_wrap.cpp \
    pymediaplayer_.c


LOCAL_MODULE := pydroid

include $(BUILD_SHARED_LIBRARY)
