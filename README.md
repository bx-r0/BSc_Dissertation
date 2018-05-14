# "Compromised and Degraded Network Simulation"

The aim of the dissertation was:

**_"Create a custom simulated network that can demonstrate and visualise network degradation and common DoS attacks, so that network engineers can identify weak spots and points of strain"_**

# Repository Layout
Project code for the project:

  - /PacketCapture - Contains the script that perfoms different degradation effects on a network connection
  - /ClientServer - Contains the programs used in the test network

# Report download
The dissertation report that this project is based of can be downloaded [here](https://github.com/AidanFray/Dissertation_Report/releases)

# Required Packages and Install

## Ubuntu or Debian

  ```sudo apt-get install build-essential python-dev libnetfilter-queue-dev```
  
## Arch

  ```sudo pacman -Sy build-essential python-dev libnetfilter-queue-dev ```
  
# Install for Python

Note: Python 3.6 is required

  ```
  sudo pip install NetfilerQueue
  sudo pip install scapy
  sudo pip install python-nmap
  sudo pip install matplotlib
  sudi pip install gi
  ```

# Configuring PI as a router
https://jacobsalmela.com/2014/05/19/raspberry-pi-and-routing-turning-a-pi-into-a-router/
https://raspberrypihq.com/how-to-turn-a-raspberry-pi-into-a-wifi-router/


# Hostapd Settings
```
  interface=wlan0
  driver=rtl871xdrv
  ssid=diss_network_test
  hw_mode=g
  channel=3
  wpa=2
  wpa_passphrase=PASSWORD
  wpa_key_mgmt=WPA-PSK
  wpa_pairwise=TKIP
  rsn_pairwise=CCMP
  auth_algs=1
  macaddr_acl=0
````
# DHCP Settings
```
ddns-update-style none;

default-lease-time 600;
max-lease-time 7200;

authoritative;

subnet 192.168.10.0 netmask 255.255.255.0 {
 range 192.168.10.10 192.168.10.20;
 option broadcast-address 192.168.10.255;
 option routers 192.168.10.1;
 default-lease-time 600;
 max-lease-time 7200;
 option domain-name "local-network";
 option domain-name-servers 8.8.8.8, 8.8.4.4;
 option subnet-mask 255.255.255.255;
}
```
