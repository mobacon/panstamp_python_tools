'''
Created on 02.05.2019

@author: Sven Schlender
'''

from serial.tools import list_ports

from swap.SwapException import SwapException


def resolve_portname(port_name, port_fix, ports=None):  # pylint: disable=R0912
    """Helper function for resolving given portname to COM or /dev/ttyx style
    address.
    """
    if not port_name:
        raise SwapException(_("No portname given!"))

    if not ports:
        ports = list_ports.comports()

    if not ports:
        raise SwapException(_("No ports in device list."))

    if port_fix == 0:
        # Fixed by port name
        matches = [x.device for x in ports]
        if port_name in matches:
            return str(port_name)

    elif port_fix == 1:
        # Fixed by hwid
        matches = [x.hwid for x in ports]
        try:
            found_idx = matches.index(port_name)
            return str(ports[found_idx].device)
        except ValueError:
            pass

    elif port_fix == 2:
        # Fixed by USB parameters VID, PID, serial and manufacturer
        try:
            vid, pid, serial_number, manu = port_name.split(',')
            vid = int(vid, 16)
            pid = int(pid, 16)
        except ValueError:
            pass
        else:
            for port in ports:
                if (port.vid == vid and port.pid == pid and
                        port.serial_number == serial_number and
                        port.manufacturer == manu):
                    return str(port.device)

    elif port_fix == 3:
        # Fixed by USB VID and USB PID
        vid, pid = port_name.split(',')
        try:
            vid = int(vid, 16)
            pid = int(pid, 16)
        except ValueError:
            pass
        else:
            for port in ports:
                if port.vid == vid and port.pid == pid:
                    return str(port.device)

    msg = "Did not find matching port device name for '%s'!" % port_name
    raise SwapException(msg)

def main():
    """The main function for testing this module and to get a list of
    available serial ports.
    """
    from prettytable import PrettyTable

    print("Scanning ports...")

    ports = list_ports.comports()
    tab = PrettyTable()
    tab.field_names = ["portfix 0", "portfix 1", "portfix 2", "portfix 3"]
    tab.align = 'l'
    table_rows = []
    table_row_width = [1,1,1,1]
    # Get column sizes.
    for port in ports:
        pid_vid = "%04X,%04X" % (port.vid, port.pid)
        manu = "%s,%s,%s" % (pid_vid, port.serial_number, port.manufacturer)
        tab.add_row([port.device, port.hwid, manu, pid_vid])

    print(tab)

if __name__ == '__main__':
    main()

