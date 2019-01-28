# barcode_scanner_python
Linux Python code to read from a USB barcode scanner directly. A symbol LS2208 was used for testing.

![LS2208 Barcode Scanner](Symbol%20LS2208%20Barcode%20Scanner.png "Symbol LS2208 Barcode Scanner")

This uses the pyusb module to read the popular LS2208 USB barcode 
scanner in Linux. This barcode scanner is sold under many labels.

## What's the big deal?

This barcode scanner acts like a keyboard so scanning a bar code types out
the data as if you were typing. Easy-peesy, right?

Well, the problem is, I don't want a console user logged into the computer. For
security reasons, I want my program to just read directly from the barcode
reader as if it were some other data device without having to read "keyboard
input". Otherwise, someone can just plug in a keyboard, hit Ctrl-C, and get a
console prompt to control the computer. (Yeah, there's ways to disable this
but the method presented here is probably more bullet proof.)

So this program detaches the device from the kernel so it will not "type"
anything, and then reads directly from the barcode scanner. It does not
need any special drivers for the barcode scanner.

# Installation

This uses pyusb to do low-level USB comm. See 
https://github.com/pyusb/pyusb for installation requirements. Basically, 
you need to install pyusb:

    pip install pyusb

To install the backend that pyusb uses, you can use libusb (among
others):

    sudo apt install libusb-1.0-0-dev
    
You need to make sure your user is a member of plugdev to use USB 
devices (in Debian linux):

    sudo addgroup <myuser> plugdev
    
You also need to create a udev rule to allow all users to access the
barcode scanner. In /etc/udev/rules.d, create a file that ends in .rules
such as `55-barcode-scanner.rules` with these contents:

    # Set permissions to let anyone use barcode scanner
    SUBSYSTEM=="usb", ATTR{idVendor}=="05e0", ATTR{idProduct}=="1200", MODE="666"

This tells the computer, if a USB device with Vendor ID = 0x05e0 and Product ID = 0x1200 is plugged in
(which is this LS2208 Symbol/Motorola barcode scanner), then set mode to "666" (any user can read
and write to the device).

To get the updated permissions, reboot or just unplug and replug the barcode scanner.

# Testing Environment
This was tested on a Raspberry Pi Zero W running Rasbian Stretch Lite. USB interface was using a USB-OTG cable.
This should work as-is with any Debian-based Linux system.

# The MIT License

Copyright (c) 2019 Vince Patron, http://vince.patronweb.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
