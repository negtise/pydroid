# Copyright 2005 The Android Open Source Project

LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)

LOCAL_C_INCLUDES := \
	$(LOCAL_PATH)/../include/python \

LOCAL_LDFLAGS += -ldl -lz
LOCAL_SHARED_LIBRARIES += liblog libutils libbinder libcutils

LOCAL_LDFLAGS += -L$(LOCAL_PATH)/../libs/ -lpython2.7 

LOCAL_SRC_FILES := \
	main.c \
	pybinder.cpp \
    binder_wrap.cpp \
    pyandroidlog.c


LOCAL_MODULE := libpydroid

include $(BUILD_SHARED_LIBRARY)
