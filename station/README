USB ISSUES
==========


There are currently performances issue with USB bus. Changing speed solve it

Add "dwc_otg.speed=1" in file /boot/cmdline.txt and restart


ETHERNET ISSUES
===============

Occasionally ethernet stops to work and does not recover until an HW reboot. I attached the serial console and checked that raspberry was actually on and running but dmesg was full of error messages related to ethernet. 

I followed tips at https://github.com/raspberrypi/linux/issues/151 and ethernet immediately recovered, without reboot.

After that, I also update firmware using rpi-update. Let's see if this solves permanently.

