#!/bin/bash

sudo apt update
sudo apt install -y fswebcam python3 python3-tk python3-pip guvcview
sudo git clone https://github.com/TaigaM123/LoginTracker /usr/local/bin/LoginTracker
sudo chmod -R a+rw /usr/local/bin/LoginTracker

touch /usr/local/bin/LoginTracker/spreadsheet_url.txt

ln -s /usr/local/bin/LoginTracker ~/LoginTracker

echo "creating venv..."
python3 -m venv /usr/local/bin/LoginTracker/.venv
source /usr/local/bin/LoginTracker/.venv/bin/activate
pip install gspread

#set up autolaunch then launch the program
echo -e "[Desktop Entry]\nName=LoggyTracker\nExec=/usr/local/bin/LoginTracker/.venv/bin/python3 /usr/local/bin/LoginTracker/main.py" | sudo tee /etc/xdg/autostart/LoggyTracker.desktop
echo -e "#!/bin/bash\n/usr/local/bin/LoginTracker/.venv/bin/python3 /usr/local/bin/LoginTracker/main.py" > ~/Desktop/Login_Tracker
sudo chmod u+x ~/Desktop/Login_Tracker
python3 /usr/local/bin/LoginTracker/main.py