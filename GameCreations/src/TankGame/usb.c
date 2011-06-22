#include <usb.h>

#define MAX_DEVICES_OPEN    10

usb_dev_handle *open_devices[MAX_DEVICES_OPEN];
int devices_open;

void initialize(void) {
    int i;
    
    usb_init();

    devices_open = 0;
    for (i = 0; i<MAX_DEVICES_OPEN; i++)
        open_devices[i] = NULL;
}

int open_device(int vendorID, int productID) {
    struct usb_bus *bus;
    struct usb_device *dev;
    int i;
    
    usb_find_busses();
    usb_find_devices();
    
    for (bus = usb_get_busses(); bus; bus = bus->next) {
        for (dev = bus->devices; dev; dev = dev->next) {
            if ((dev->descriptor.idVendor==vendorID) && (dev->descriptor.idProduct==productID)) {
                for (i = 0; i<MAX_DEVICES_OPEN; i++) {
                    if (open_devices[i]==NULL) {
                        if (open_devices[i] = usb_open(dev)) {
                            devices_open++;
                            return i;
                        } else {
                            return -1;
                        }
                    }
                }
            }
        }
    }
    return -2;
}

int close_device(int device) {
    if ((device<0) || (device>=MAX_DEVICES_OPEN))
        return -1;
    if (open_devices[device]) {
        usb_close(open_devices[device]);
        devices_open--;
        open_devices[device] = NULL;
        return 0;
    }
    return -2;
}

int num_devices_open(void) {
    return devices_open;
}

int control_transfer(int device, unsigned char bmRequestType, unsigned char bRequest, int wValue, int wIndex, int wLength, unsigned char *buffer) {
    if ((device<0) || (device>=MAX_DEVICES_OPEN))
        return -1;
    if (open_devices[device])
        return usb_control_msg(open_devices[device], bmRequestType, bRequest, wValue, wIndex, buffer, wLength, 100);
    return -2;
}
