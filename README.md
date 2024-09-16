# syncclip
A tool designed to copy, paste, and sync clipboard data to a centralized server, enabling clipboard sharing between two hosts without copy/paste capability
## Setup
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn

gunicorn --config /path/to/gunicorn_config.py /path/to/syncclip_server:app

## Setup Nginx proxy
```
location ~ ^/([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12})/ {
    # Rewrite rule to remove UUID from the URL
    rewrite ^/([a-fA-F0-9-]+)/(.*)$ /$2 break;

    proxy_pass http://127.0.0.1:5000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```
