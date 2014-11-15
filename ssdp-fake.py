#!/usr/bin/python
# Copyright (C) 2014 Graham R. Cobb
# Released under GPL V2 -- see LICENSE
# Python multicast code taken from Stack Overflow (https://stackoverflow.com/questions/603852/multicast-in-python/1794373#1794373) by tolomea (https://stackoverflow.com/users/10471/tolomea) under CC BY-SA 3.0
# Other example code taken from Stack Overflow by Toddeman (under CC BY-SA 3.0), however it does not seem to be available any longer

import socket
import struct
import time
import select
import re
from optparse import OptionParser

VERSION='0.3'

DLNA_GRP = '239.255.255.250'
DLNA_PORT = 1900
MCAST_IF = '127.0.0.1'

CRLF = "\015\012"

#SERVER='192.168.0.238'
SERVER=''
UUID=''
URL=''
INTERVAL = 180

parser = OptionParser(usage="usage: %prog [options] server\n       %prog --listen-only",
	epilog="Server can be specified as hostname or IP address and should be omitted if --listen-only is used",
	version="%prog "+VERSION)
parser.add_option("-a", "--all",
                  action="store_true", dest="allif", default=False,
                  help="send announcements to all interfaces, not just the loopback interface")
parser.add_option("-i", "--interval", type="int", dest="interval", default=INTERVAL,
		  help="seconds between notification updates (default %default)")
parser.add_option("-l", "--listen-only",
                  action="store_true", dest="listen", default=False,
                  help="just listen and display messages seen, do not contact a server or send announcements")
(options, args) = parser.parse_args()
LISTEN=options.listen
if len(args) == 0 and not LISTEN:
  parser.error("server must be specified (hostname or IP address)")
if len(args) > 1:
  parser.error("incorrect number of arguments")
if not LISTEN:
  SERVER=args[0]
INTERVAL=options.interval

osock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
osock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
osock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 4)
osock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
if not options.allif:
  mreq = struct.pack("4sl", socket.inet_aton(MCAST_IF), socket.INADDR_ANY)
  osock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, mreq)

imsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
imsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
imsock.bind(('', DLNA_PORT))
mreq = struct.pack("4sl", socket.inet_aton(DLNA_GRP), socket.INADDR_ANY)
imsock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

def notify(addr, port):
  if (URL != '' and UUID != '' and not LISTEN):
    # Note: responses should have ST:, notifies should have NT:
    # We include both

    msg = 'NOTIFY * HTTP/1.1' + CRLF \
	+ 'NT: urn:schemas-upnp-org:device:MediaServer:1' + CRLF \
	+ 'USN: uuid:' + UUID + '::urn:schemas-upnp-org:device:MediaServer:1' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'NOTIFY * HTTP/1.1' + CRLF \
	+ 'NT: upnp:rootdevice' + CRLF \
	+ 'USN: uuid:' + UUID + '::upnp:rootdevice' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'NOTIFY * HTTP/1.1' + CRLF \
	+ 'NT: uuid:' + UUID + CRLF \
	+ 'USN: uuid:' + UUID + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'NOTIFY * HTTP/1.1' + CRLF \
	+ 'NT: urn:schemas-upnp-org:service:ContentDirectory:1' + CRLF \
	+ 'USN: uuid:' + UUID + '::urn:schemas-upnp-org:service:ContentDirectory:1' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'NOTIFY * HTTP/1.1' + CRLF \
	+ 'NT: urn:schemas-upnp-org:service:ConnectionManager:1' + CRLF \
	+ 'USN: uuid:' + UUID + '::urn:schemas-upnp-org:service:ConnectionManager:1' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'NOTIFY * HTTP/1.1' + CRLF \
	+ 'NT: urn:schemas-upnp-org:service:X_MS_MediaReceiverRegistrar:1' + CRLF \
	+ 'USN: uuid:' + UUID + '::urn:schemas-upnp-org:service:X_MS_MediaReceiverRegistrar:1' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))
  else:
    print "Skipping notification"

def respond(addr, port):
  if (URL != '' and UUID != '' and not LISTEN):
    # Note: responses should have ST:, notifies should have NT:
    # We include both

    msg = 'HTTP/1.1 200 OK' + CRLF \
	+ 'ST: urn:schemas-upnp-org:device:MediaServer:1' + CRLF \
	+ 'USN: uuid:' + UUID + '::urn:schemas-upnp-org:device:MediaServer:1' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'HTTP/1.1 200 OK' + CRLF \
	+ 'ST: upnp:rootdevice' + CRLF \
	+ 'USN: uuid:' + UUID + '::upnp:rootdevice' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'HTTP/1.1 200 OK' + CRLF \
	+ 'ST: uuid:' + UUID + CRLF \
	+ 'USN: uuid:' + UUID + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'HTTP/1.1 200 OK' + CRLF \
	+ 'ST: urn:schemas-upnp-org:service:ContentDirectory:1' + CRLF \
	+ 'USN: uuid:' + UUID + '::urn:schemas-upnp-org:service:ContentDirectory:1' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'HTTP/1.1 200 OK' + CRLF \
	+ 'ST: urn:schemas-upnp-org:service:ConnectionManager:1' + CRLF \
	+ 'USN: uuid:' + UUID + '::urn:schemas-upnp-org:service:ConnectionManager:1' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))

    msg = 'HTTP/1.1 200 OK' + CRLF \
	+ 'ST: urn:schemas-upnp-org:service:X_MS_MediaReceiverRegistrar:1' + CRLF \
	+ 'USN: uuid:' + UUID + '::urn:schemas-upnp-org:service:X_MS_MediaReceiverRegistrar:1' + CRLF \
	+ 'NTS: ssdp:alive' + CRLF \
	+ 'LOCATION: ' + URL + CRLF \
	+ 'HOST: 239.255.255.250:1900' + CRLF \
	+ 'SERVER: ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ 'CACHE-CONTROL: max-age=' + str(INTERVAL * 10) + CRLF \
	+ CRLF
    print "Sending ("+addr+":"+str(port)+"): \n" + msg
    osock.sendto(msg, (addr, port))
  else:
    print "Skipping response"

def server():
  if not LISTEN:
    msg = ('M-SEARCH * HTTP/1.1' + CRLF \
	+ 'Host: %s:%d' + CRLF \
	+ 'Man: "ssdp:discover"' + CRLF \
	+ 'ST: upnp:rootdevice' + CRLF \
	+ 'MX: 3' + CRLF \
	+ 'User-Agent:ssdp-fake/0 DLNADOC/1.50 UPnP/1.0 ssdp-fake/0' + CRLF \
	+ CRLF) % (SERVER, DLNA_PORT)
    print "Sending to server: \n" + msg
    osock.sendto(msg, (SERVER, DLNA_PORT))

def parse_msg(msg):
  global URL, UUID, last_update, next_notification

  if (re.match('^HTTP/1.1\s*200\s*OK', msg, re.IGNORECASE)):
    # Response to our M-SEARCH
    match = re.search(r'^LOCATION:\s*(.*)\r$', msg, re.IGNORECASE | re.MULTILINE)
    if match:
      URL = match.group(1)
    match = re.search(r'^USN:\s*uuid:([^:]+):', msg, re.IGNORECASE | re.MULTILINE)
    if match:
      UUID = match.group(1)
    print 'URL=%s, UUID=%s.' % (URL, UUID)
    last_update = time.time()
    # Bring the notifcation forward
    next_notification = time.time() + 1
    
def is_search(msg):
  return re.match('^M-SEARCH', msg, re.IGNORECASE)

# Get info from server
last_update = 0
server()

next_notification = time.time() + INTERVAL

# Note: the port is not set up until at least one send has happened
(notused, oport) = osock.getsockname()

isock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
isock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
isock.bind(('', oport))

while True:
  (readyin, notused, notused) = select.select([isock, imsock], [], [], max(next_notification - time.time(),0))

  if (isock in readyin):
    (msg, (addr, port)) = isock.recvfrom(4096)
    print "Received unicast from %s:%d\n%s" % (addr, port, msg)
    if (is_search(msg)):
      respond(addr, port)
    else:
      parse_msg(msg)

  if (imsock in readyin):
    (msg, (addr, port)) = imsock.recvfrom(4096)
    if (port == oport):
      print "Ignored multicast from ourselves (%s:%d)" % (addr, port)
    else:
      print "Received multicast from %s:%d\n%s" % (addr, port, msg)
      if (is_search(msg)):
        respond(addr, port)

  if (time.time() >= next_notification):
    next_notification = time.time() + INTERVAL

    # Has the server info been updated recently?
    if (time.time() - last_update <= INTERVAL):
      # Yes, just do the notification
      notify(DLNA_GRP, DLNA_PORT)
    else:
      # Get new info from the server
      server()


