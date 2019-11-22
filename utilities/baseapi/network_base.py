import netifaces
import time

from configs.windows import WindowsUtils


def get_interfaces():
    return netifaces.interfaces()


def get_ip(interface):
    try:
        ip = netifaces.ifaddresses(interface)[2][0]['addr']
    except:
        ip = None
    return ip


def is_local_ip(ip):
    list_ifaces = get_interfaces()
    for iface in list_ifaces:
        if get_ip(iface) == ip:
            return True
    return False


def get_lan_ips():
    """
    Get all ips of all network interface of current machine

    Examples
    --------
    get_lan_ips()
    Return:
    [
        {
            "ip" : "127.0.0.1",
            "mac" : "00:00:00:00:00:00"
        },
        {
            "ip" : "10.116.41.89",
            "mac" : "b0:83:fe:aa:d9:1a"
        },
        {
            "ip" : "172.18.0.1",
            "mac" : "02:42:bc:c2:14:6a"
        },
        {
            "ip" : "172.17.0.1",
            "mac" : "02:42:f5:91:79:a4"
        },
        {
            "ip" : "192.168.1.1",
            "mac" : "0a:00:27:00:00:00"
        }
    ]

    Returns
    -------
    List
       All network interface ips
    """
    ips = []
    interfaces = get_interfaces()
    for ifname in interfaces:
        try:
            interface_data = netifaces.ifaddresses(ifname)
            ip = interface_data[2][0]['addr']
            if WindowsUtils.is_running_on_windows():
                mac = interface_data[-1000][0]['addr']
            else:
                mac = interface_data[17][0]['addr']
            ips.append({"ip": ip, "mac": mac})
        except IOError:
            pass

        except KeyError:
            pass

    return ips
