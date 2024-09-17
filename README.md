# syncclip
A tool designed to copy, paste, and sync clipboard data to a centralized server, enabling clipboard sharing between two hosts without copy/paste capability
## Setup
```
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn
pip install -r requirements.txt
gunicorn --bind 127.0.0.1:5000 /path/to/syncclip-server:app
```
