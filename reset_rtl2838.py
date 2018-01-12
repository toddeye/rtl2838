#!/usr/bin/env python3
''' Find rtl2838 and issue usb reset:
Adapted from
https://raspberrypiandstuff.wordpress.com/2017/08/04/rtl_433-on-a-raspberry-pi-made-bulletproof
https://gist.github.com/x2q/5124616
'''

import sys, os
import subprocess
import fcntl

USBDEVFS_RESET = ord('U') << (4*2) | 20

def find_rtl2838():
    USBNAME = 'RTL2838'

    for line in subprocess.check_output(["lsusb"]).decode().split('\n'):
        if USBNAME in line: break
    usbbus = line.split(' ')[1]
    usbdevice = line.split(' ')[3].strip(':')
    device = '/dev/bus/usb/{}/{}'.format(usbbus, usbdevice)

    return device

try:
    filename = find_rtl2838()
    fd = os.open(filename, os.O_WRONLY)
    fcntl.ioctl(fd, USBDEVFS_RESET, 0)
    os.close(fd)
except Exception as err:
    sys.stderr.write('{}\n'.format(err))
    exit(1)

exit(0)