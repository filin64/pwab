#!/usr/bin/python
# encoding: utf8

"""
    Public Wi-Fi Autorization Bypass
    Copyright (C)
"""

import sys
from scapy.all import srp, get_if_list, Ether, ARP, get_if_addr
from subprocess import getstatusoutput
import logging

VERSION = '1.0.0'
_os = None
_iface = None
_ip = None
_netmask = None

logging.basicConfig(level=logging.DEBUG)

def def_os():
    return sys.platform

def get_iface():
    iface_list = get_if_list()
    for iface in iface_list:
        status, shell_out = getstatusoutput('ifconfig ' + str(iface))
        if status:
            logging.critical('ifconfig service error')
            return None
        if 'active' in shell_out:
            return iface
    logging.critical('no active interfaces')
    return None

def get_netmask(iface):
    status, shell_out = getstatusoutput('ifconfig ' + iface)
    if status:
        logging.critical('ifconfig service error')
        return None
    if 'netmask' in shell_out:
        iface_params = shell_out.split()
        netmask_idx = iface_params.index('netmask')
        logging.debug('netmask is '+ iface_params[netmask_idx + 1])
        return iface_params[netmask_idx + 1]
    logging.critical('no netmask on interface')
    return None



def scan_local_devices(ip_addr, netmask):
    netmask_prefix = sum([1 if i == '1' else 0 for i in bin(int(netmask, 16))])
    print (ip_addr + str(netmask_prefix))
    ans, unans = srp(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=ip_addr + str(netmask_prefix)),
                               timeout=10)
    for s, r in ans:
        print (r[Ether].src)
    return 0

def spoof_my_mac():
    return


def main(argv):
    _iface = get_iface()
    if _iface is None:
        return 1
    _ip = get_if_addr(_iface)
    logging.debug("IP is " + _ip)
    _netmask = get_netmask(_iface)
    if _netmask is None:
        return 1
    scan_local_devices(_ip, _netmask)
    return 0




if __name__ == '__main__':
    main(sys.argv[1:])
