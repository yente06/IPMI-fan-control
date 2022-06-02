# IPMI-fan-control
A python script to make the fans of a dell server quiet.<br/>
It has been tested with a Dell PowerEdge R720 with 2 x E5-2690.<br/>
It has the following fan curve:<br/>
`MIN(5%, (temp in %)^5)`<br/>
This fan curve has a good balance between performance and noise. It hit a maximum temperature of 80°C when stress testing.

## Prerequisites
IPMI Over LAN must be enabled on the iDRAC module. Without this, the module won't respond to IPMI commands.

## Installation
1. Install python, ipmitool and lm-sensors:
   ### Debian/Ubuntu:
   ```
   sudo apt install python3 ipmitool lm-sensors
   ```
   ### Fedora
   ```
   sudo dnf install python3 ipmitool lm_sensors
   ```
   ### CentOS/RHEL
   ```
   sudo yum install python3 ipmitool lm_sensors
   ```
   ### Arch Linux
   ```
   sudo pacman -S python3 ipmitool lm_sensors
   ```
   ### openSUSE
   ```
   sudo zypper install python3 ipmitool sensors
   ```
2. Change the config variables in `fanControl.py`:
   - `minTemp`: the minimum temperature set in the server
   - `maxTemp`: the maximum temperature set in the server
   - `ipmiAddress`: the IP address of the iDRAC module (IPMI)
   - `ipmiUser`: the username of the iDRAC module (IPMI)
   - `ipmiPassword`: the password of the iDRAC module (IPMI)
   - `fanCurve`: the fan curve given the temperature in percent (`minTemp`: 0%, `maxTemp`: 100%)
3. Move `fanControl.py` to `/usr/bin/fanControl.py`:
   ```
   sudo mv fanControl.py /usr/bin/fanControl.py
   ```
4. Create and open the following file: `/etc/systemd/system/fanControl.service`:
   ```
   sudo nano /etc/systemd/system/fanControl.service
   ```
   And add the following content:
   ```
   [Unit]
   Description=IPMI fan control
   After=multi-user.target
   [Service]
   Type=simple
   Restart=always
   ExecStart=/usr/bin/python3 -u /usr/bin/fanControl.py
   [Install]
   WantedBy=multi-user.target
   ```
   Now give it the appropriate permissions:
   ```
   sudo chmod 644 /etc/systemd/system/fanControl.service
   ```
5. Enable the service on startup:
   ```
   sudo systemctl enable --now fanControl
   ```

## Reading the stats
You can get the fan speed and corresponding temperature using the following command:
```
sudo journalctl -u fanControl
```