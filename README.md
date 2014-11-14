#ssdp-fake

Spoof SSDP announcements for devices off-lan

This is a quick hack to send out SSDP announcements for devices which are not on the LAN.
Currently it is very hacky, and it only works for Media Servers.

This allows access to media servers which are not on the same LAN, as long as they are
accessible by both UDP and TCP.

It works by sending a unicast request to the server (you have to know the IP address of
the server), picking the URL from the response, and then sending out local multicast
announcements for the server.  It is very simple: it sends all the multicast
announcements whenever it sees any traffic to the multicast address, or periodically.

Note: all it handles is the NOTIFY.  The client then uses the URL to contact the server
directly.

## Versions

There are two files: a Python version (`ssdp-fake.py`) and a Perl version
(`ssdp-fake`).  At the moment, the python version is more recent -- but check
the dates to see if that is still true when you read this!

## Bugs

The most serious bug is that if you have two of these on the same LAN, they will
probably cause a multicast storm, because each one sends out several announcements
whenever it sees any traffic to the multicast address.

I told you it is a hack.  Hopefully that bug will be fixed soon by making it pay
more attention to what it sees.

## Real Solution

The real solution to this problem, would be a real SSDP proxy, which would collect
announcements from one LAN, forward them to a program on another LAN which would manage
the announcements on that LAN.  Apparently this is harder than it seems, because
I am aware that this has been looked into but I don't know of any solutions.

## Credits
Python multicast code taken from Stack Overflow (https://stackoverflow.com/questions/603852/multicast-in-python/1794373#1794373) by tolomea (https://stackoverflow.com/users/10471/tolomea)

Other example code taken from Stack Overflow by Toddeman, however it does not seem to be available any longer
