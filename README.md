# syncclip
This Python tool is designed to facilitate clipboard sharing between two hosts that lack the native capability to copy and paste data between them. It securely synchronizes clipboard content through a centralized server, enabling seamless data transfer across systems.

**Key Features:**
1. **Clipboard Synchronization**: Automatically sync clipboard content from one host to the centralized server, making it available for retrieval by another host.
2. **Cross-Host Clipboard Sharing**: Enables clipboard sharing between hosts that cannot natively interact or share data directly.
3. **Server-Based Clipboard Management**: All clipboard data is temporarily stored and managed on a centralized server, ensuring both hosts have a point of synchronization.
4. **End-to-End Encryption**: Ensures clipboard data is securely transmitted between the hosts and the server, protecting sensitive content during transfer.
5. **Multi-Host Support**: The tool supports multiple hosts, allowing each to register with the server and access its own clipboard history securely.
6. **Platform Independence**: Designed to be compatible with multiple operating systems, allowing flexible deployment across diverse environments.
7. **Capacity Limitations**: The tool supports the copying and pasting of content up to 30,000 lines, ensuring robust functionality for most use cases while maintaining performance and efficiency.

This tool simplifies the process of clipboard sharing between disconnected systems while maintaining security and data integrity through centralized control.

## Setup & Installation
```
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn
pip install -r requirements.txt
gunicorn --bind 127.0.0.1:5000 /path/to/syncclip-server:app
```
Setup Nginx reverse proxy which acts as a buffer between clients and your application server.
```
location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
    }
```
