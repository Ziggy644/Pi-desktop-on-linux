# Pi-desktop-on-linux
Script to install/update Pi Desktop on linux and receive node bonus
Tested on ubuntu 24.04

# Requirements

-python 3.x

-virtualization enabled in BIOS 

-Docker (installed via ./run command)

-p7zip (installed via ./run command) 

# Installation

git clone https://github.com/Ziggy644/Pi-desktop-on-linux.git

cd Pi-desktop-on-linux

chmod +x ./run

./run

# Known issues

Sometimes, The Pi node app cannot create the node container by itself. If this happens, manually create the container by running:

sudo docker compose -f '/root/.config/Pi Network/docker-compose.json' create

# Credits: @pjkgijp (Pi Network)
Pi donation address: GDL2JCVEQNGNYMO6XQN2CCNMT2EGBDB65VS5QLIQN3UHQ2MI2NIEA7TP
