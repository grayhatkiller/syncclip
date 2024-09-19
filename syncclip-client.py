import requests
import pyperclip
import time

SERVER_URL = 'https://example.com/syncclip'  # CHANGEME
TOKEN = None

def get_token():
    global TOKEN
    if TOKEN is None:
        response = requests.get(f'{SERVER_URL}/token')
        if response.status_code == 201:
            TOKEN = response.json()['token']
        else:
            raise Exception("Failed to get token from server")
    return TOKEN

def sync_clipboard():
    last_content = ""
    token = get_token()
    
    while True:
        try:
            # Check local clipboard
            current_content = pyperclip.paste()
            if current_content != last_content:
                # Update server
                response = requests.post(f'{SERVER_URL}/clipboard/{token}', 
                                         data=current_content,
                                         headers={'Content-Type': 'text/plain'})
                if response.status_code == 200:
                    print("Clipboard synced to server")
                    last_content = current_content
                else:
                    print("Failed to sync clipboard to server")
            
            # Check server clipboard
            response = requests.get(f'{SERVER_URL}/clipboard/{token}')
            if response.status_code == 200:
                server_content = response.json().get('content', '')
                if server_content and server_content != current_content:
                    pyperclip.copy(server_content)
                    print("Clipboard updated from server")
                    last_content = server_content
        
        except Exception as e:
            print(f"Error: {str(e)}")
        
        time.sleep(5)

def main():
    token = get_token()
    print(f"Your clipboard token is: {token}")
    print(f"View clipboard at {SERVER_URL}/display/{token}")
    print("Clipboard syncing started. Press Ctrl+C to stop syncing.")
    try:
        sync_clipboard()
    except KeyboardInterrupt:
        print("Clipboard syncing stopped.")

if __name__ == "__main__":
  main()
