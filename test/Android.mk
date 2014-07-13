# Copyright 2005 The Android Open Source Project

LOCAL_PATH:= $(call my-dir)
include $(CLEAR_VARS)

LOCAL_C_INCLUDES := $(LOCAL_PATH)/../include/native \
	$(LOCAL_PATH)/../include/python \
	$(LOCAL_PATH)/../include/core

#LOCAL_STATIC_LIBRARIES := pydroid

LOCAL_SHARED_LIBRARIES := libpydroid

#LOCAL_LDFLAGS += -ldl -lz

LOCAL_LDFLAGS += -L$(LOCAL_PATH)/../libs/ -lpython2.7

LOCAL_LDLIBS + = 

#-llibpython2.7.so

#$(LOCAL_PATH)/libs/libapplication.so

#-L$(LOCAL_PATH)/libs libapplication.so

LOCAL_SRC_FILES := \
	main.c
	
LOCAL_MODULE := test

#include $(BUILD_SHARED_LIBRARY)



include $(BUILD_EXECUTABLE)

$(call dist-for-goals,dist_files,$(LOCAL_BUILT_MODULE))

