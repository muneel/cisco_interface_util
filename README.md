# cisco_interface_util
python script to get interface utilization of a given list from a cisco switch

## Usage
```
usage: get_interface_util.py [-h] -s SWITCH [-u USER] -p PASSWORD -
                           ENABLE_PASSWORD [-i INTERFACES [INTERFACES ...]]
                             [-f [FILE]]

Script to get the Input/Output Rates for a given list of Interfaces from cisco
switch

optional arguments:
  -h, --help            show this help message and exit
  -s SWITCH, --switch SWITCH
                        Switch IP Address
  -u USER, --user USER  Username
  -p PASSWORD, --password PASSWORD
                        Password
  -e ENABLE_PASSWORD, --enable_password ENABLE_PASSWORD
                        Enable Password
  -i INTERFACES [INTERFACES ...], --interfaces INTERFACES [INTERFACES ...]
                        Interfaces
  -f [FILE], --file [FILE]
                        File containing list of Interfaces
```

## Example

List of Interface as an argument
```
#python get_interface_util -s 192.168.1.1 -p password -e enable_password -i=vlan100,Gi1/45,Gi1/2

Interface Status                                             Input Rate, Output Rate
                              Vlan100 is up, line protocol is up ,  793.52 Mbps,    0.00 Mbps
       GigabitEthernet1/45 is up, line protocol is up (connected),  101.79 Mbps,   61.45 Mbps
        GigabitEthernet1/2 is up, line protocol is up (connected),  156.28 Mbps,    0.01 Mbps
```

List of Interfaces from a file
```
#cat list.txt
vlan100
Gi1/45
Gi1/2
```

```
#python get_interface_util -s 192.168.1.1 -p password -e enable_password -f list.txt
Interface Status                                             Input Rate, Output Rate
                              Vlan100 is up, line protocol is up ,  793.52 Mbps,    0.00 Mbps
       GigabitEthernet1/45 is up, line protocol is up (connected),  101.79 Mbps,   61.45 Mbps
        GigabitEthernet1/2 is up, line protocol is up (connected),  156.28 Mbps,    0.01 Mbps
```
