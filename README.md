# Network Disconnection Monitor
### v1.0 by panayator<br><br>


#### A simple Python script that helps you monitor your router's bad behavior, aka disconnections/reboots etc.
I created this for personal use, because I've been having some problems with my ISP and I wanted to see how frequently the router was rebooting on its own.<br><br><br>
The program:
- detects disconnections from the internet by attempting to connect via socket to Google's DNS server
- creates a .txt to log disconnections that meet the required criteria (disconnections longer than 1 minute)
- creates a GUI using the Tkinter library, with a text box that displays the logged disconnections as they appear in the .txt
- has a disconnection counter
- Disconnections are logged with date and duration (when it first failed to connect -> when it managed to reconnect)
- shows detection of all disconnections in the console window and displays a message if a disconnection was too short

### Useful info/notes
1. Router reboots take about 2 to 3 minutes, so it's easy to spot them from their duration
2. The way the program works is by basically detecting when the device is disconnected from the internet.
    1. Disconnecting the internet will also log a disconnection, unless it's too short (this is helpful for triggering disconnections manually and for debugging)
    2. A WiFi connection might log short disconnections (10s) that will only appear in the console, for filtering
    3. Power saving options that temporarily disable network adapters might also log short disconnections (10s) even on Ethernet (again, they'll only appear in the console, for filtering)
3. The disconnection counter works by counting the lines in the file and dividing them by 2, because there is an empty line between each disconnection

Enjoy :) and be sure to let me know for any ideas/improvements you'd like to suggest
