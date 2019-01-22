import usb.core
import usb.util

"""
This uses the pyusb module to read the popular LS2208 USB barcode 
scanner in Linux. This barcode scanner is sold under many labels. It
is a USB HID device and shows up as a keyboard so a scan will "type"
the data into any program. But that also becomes its limitation. Often,
you don't want it to act like it's typing on a keyboard; you just want
to get data directly from it.

This program detaches the device from the kernel so it will not "type"
anything, and reads directly from the device without needing any device-
specific USB drivers.

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
such as 55-barcode-scanner.rules with these contents:

    (TBD)
"""

def hid2ascii(lst):
    """The USB HID device sends an 8-byte code for every character. This
    routine converts the HID code to an ASCII character.
    
    See https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf
    for a complete code table. Only relevant codes are used here."""
    
    # Example input from scanner representing the string "http:":
    #   array('B', [0, 0, 11, 0, 0, 0, 0, 0])   # h
    #   array('B', [0, 0, 23, 0, 0, 0, 0, 0])   # t
    #   array('B', [0, 0, 0, 0, 0, 0, 0, 0])    # nothing, ignore
    #   array('B', [0, 0, 23, 0, 0, 0, 0, 0])   # t
    #   array('B', [0, 0, 19, 0, 0, 0, 0, 0])   # p
    #   array('B', [2, 0, 51, 0, 0, 0, 0, 0])   # :
    
    assert len(lst) == 8, 'Invalid data length (needs 8 bytes)'
    conv_table = {
        0:['', ''],
        4:['a', 'A'],
        5:['b', 'B'],
        6:['c', 'C'],
        7:['d', 'D'],
        8:['e', 'E'],
        9:['f', 'F'],
        10:['g', 'G'],
        11:['h', 'H'],
        12:['i', 'I'],
        13:['j', 'J'],
        14:['k', 'K'],
        15:['l', 'L'],
        16:['m', 'M'],
        17:['n', 'N'],
        18:['o', 'O'],
        19:['p', 'P'],
        20:['q', 'Q'],
        21:['r', 'R'],
        22:['s', 'S'],
        23:['t', 'T'],
        24:['u', 'U'],
        25:['v', 'V'],
        26:['w', 'W'],
        27:['x', 'X'],
        28:['y', 'Y'],
        29:['z', 'Z'],
        30:['1', '!'],
        31:['2', '@'],
        32:['3', '#'],
        33:['4', '$'],
        34:['5', '%'],
        35:['6', '^'],
        36:['7' ,'&'],
        37:['8', '*'],
        38:['9', '('],
        39:['0', ')'],
        40:['\n', '\n'],
        41:['\x1b', '\x1b'],
        42:['\b', '\b'],
        43:['\t', '\t'],
        44:[' ', ' '],
        45:['_', '_'],
        46:['=', '+'],
        47:['[', '{'],
        48:[']', '}'],
        49:['\\', '|'],
        50:['#', '~'],
        51:[';', ':'],
        52:["'", '"'],
        53:['`', '~'],
        54:[',', '<'],
        55:['.', '>'],
        56:['/', '?'],
        100:['\\', '|'],
        103:['=', '='],
        }

    # A 2 in first byte seems to indicate to shift the key. For example
    # a code for ';' but with 2 in first byte really means ':'.
    if lst[0] == 2:
        shift = 1
    else:
        shift = 0
        
    # The character to convert is in the third byte
    ch = lst[2]
    if ch not in conv_table:
        print "Warning: data not in conversion table"
        return ''
    return conv_table[ch][shift]



# Find our device using the VID (Vendor ID) and PID (Product ID)
dev = usb.core.find(idVendor=0x05e0, idProduct=0x1200)
if dev is None:
    raise ValueError('USB device not found')

# Disconnect it from kernel
needs_reattach = False
if dev.is_kernel_driver_active(0):
    needs_reattach = True
    dev.detach_kernel_driver(0)
    print "Detached USB device from kernel driver"

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# get an endpoint instance
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    # match the first IN endpoint
    custom_match = \
    lambda e: \
        usb.util.endpoint_direction(e.bEndpointAddress) == \
        usb.util.ENDPOINT_IN)

assert ep is not None, "Endpoint for USB device not found. Something is wrong."

# Loop through a series of 8-byte transactions and convert each to an
# ASCII character. Print output after 0.5 seconds of no data.
line = ''
while True:
    try:
        # Wait up to 0.5 seconds for data. 500 = 0.5 second timeout.
        data = ep.read(1000, 500)  
        ch = hid2ascii(data)
        line += ch
    except KeyboardInterrupt:
        print "Stopping program"
        dev.reset()
        if needs_reattach:
            dev.attach_kernel_driver(0)
            print "Reattached USB device to kernel driver"
        break
    except usb.core.USBError:
        # Timed out. End of the data stream. Print the scan line.
        if len(line) > 0:
            print line
            line = ''
