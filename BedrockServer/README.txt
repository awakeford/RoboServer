## systemctl for web-server

sudo cp -f web_server.service /etc/systemd/system/web_server.service


sudo systemctl start  web_server.service 
sudo systemctl enable web_server.service
sudo systemctl status web_server.service
sudo journalctl -u web_server.service
