# ovenControl
Simple Python program for controlling the UN30 Memmert oven. 

### IP settings
The oven has to be connected via a network interface to a computer running this program; the following settings were found to work. Set the oven to the following:

    IP address: 192.168.100.100
    Subnet mask: 255.255.0.0
    Default gateway: 192.168.5.1

Be sure to set the `Remote control` to `write`.

By using a USB-to-LAN adapter it's still possible to use the wired network of the computer. In Windows, the following network settings for the adapter were found to work. (In the Network and Sharing Center, go into `Change adapter settings`, right click `Properties`, and then go into the `Properties` of the `Internet Protocol Version 4` item.)

    IP address: 192.168.5.2
    Subnet mask: 255.255.0.0
    Default gateway: 192.168.5.1
    (Leave DNS empty)

### Running
Run `ovenControl.py` from a terminal, be sure that there is a `.csv` file with the schedule. This takes the format of

    temperature, duration
    
with one step per line. It will save a logfile in the same directory in which it is placed. This has the following structure:

    epoch time (in s), set temperature (in °C), current temperature (in °C)
