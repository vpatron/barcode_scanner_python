# barcode_scanner_python
Linux Python code to read from a USB barcode scanner directly. A symbol LS2208 was used for testing.

![LS2208 Barcode Scanner](Symbol%20LS2208%20Barcode%20Scanner.png "Symbol LS2208 Barcode Scanner")

This uses the pyusb module to read the popular LS2208 USB barcode 
scanner in Linux. This barcode scanner is sold under many labels. It
is a USB HID device and shows up as a keyboard so a scan will "type"
the data into any program. But that also becomes its limitation. Often,
you don't want it to act like it's typing on a keyboard; you just want
to get data directly from it.

This program detaches the device from the kernel so it will not "type"
anything, and reads directly from the device without needing any device-
specific USB drivers.

# Installation
It does use pyusb to do low-level USB comm. See 
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
