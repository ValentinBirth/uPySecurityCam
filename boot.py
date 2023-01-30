# This file is executed on every boot (including wake-boot from deepsleep)
import utime
import network
import machine
import config


def wifi_connect():
    """Connects to WIFI Network given in config.py"""
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(config.wifi_config["ssid"],
                     config.wifi_config["password"])
    start = utime.time()
    while not wlan.isconnected():
        utime.sleep(1)
        if utime.time()-start > 10:
            print("connect timeout!")
            break
    if wlan.isconnected():
        print('network config:', wlan.ifconfig())


wifi_connect()
machine.freq(240000000)
