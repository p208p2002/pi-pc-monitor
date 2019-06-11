# LED電腦資源監控燈 / Pi PC monitor
A Pi PC state monitor design for NUTC final project.

Monitor with CPU and RAM usage state.

![component](https://raw.githubusercontent.com/p208p2002/pi-pc-monitor/master/component_bb.png)

[Video 1](https://www.youtube.com/watch?v=h-WTSqjy7dE)

[Video 2](https://www.youtube.com/watch?v=xZc-PM7hHug)

# Usage
- put `server_pi.py` on Rasbperry Pi and run with Python 3
- put `client_pc.py` on your PC and run with `python3 --host=YOUR_PI_SERVER_IP`

# File description
file name     | description
--------------|------------
client_pc.py  | client code
core.py       | get PC state info (for client)
server_pi.py  | server code
ic.py         | ic driver class (for server)
component.fzz | Fritzing file
document.docx | design document

