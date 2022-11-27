from paramiko import SSHClient
from bs4 import BeautifulSoup

import json
import os
import socket
import sys
import time
import requests


# Class that responsible to analyze IP or Webpage
# that the user is choosing.
class target_analyzer:
    def __init__(self, target):
        self.target = target

    # IP analyzer section:
    # pinging target to see if he is online.
    def ping_target(self):
        print(f"[Pinging {self.target}]")
        result = os.popen(f"ping {self.target}").read()
        print("=" * 20)
        if "Received = 4" in result:
            print(f"{self.target} is UP")
        else:
            print(f"{self.target} is DOWN")
        print("=" * 20)

    # Scanning open TCP ports
    def scan_TCP_ports(self):
        print('Scanning open ports...')
        socket.setdefaulttimeout(0.1)
        try:
            for port in range(1024):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((self.target, port))
                if result == 0:
                    print(f"{port} is UP")
        except:
            print("An error occurred!")

    # Scanning specific port
    def scan_specific_port(self, port):
        print(f"Scanning {port}...")
        try:
            socket.setdefaulttimeout(3)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((self.target, port))
            print("=" * 30)
            if result == 0:
                print(f"Port {port} is UP")
            else:
                print(f"Port {port} is not UP")
        except:
            print(f"Port {port} is not UP")
        print("=" * 30)

    # running number of accounts for SSH to see if one is validated if it does,
    # we print it to the user
    def ssh_user_result(self):
        users = get_from_db()
        for username in users:
            try:
                client = SSHClient()
                client.load_system_host_keys()
                client.connect(self.target, username=username, password=users[username])
                print(f"Username :{username}, Password: {users[username]}")
                break
            except:
                print("Failed to hack...")

    # Connect via SSH protocol
    def ssh_connect(self, username, password):
        client = SSHClient()
        client.load_system_host_keys()
        try:
            client.connect(self.target, username=username, password=password)
            print("connection succeed")
            while True:
                command = input("$ ")
                stdin, stdout, stderr = client.exec_command(command)
                print(stdout.read().decode())
                err = stderr.read().decode()
                if err:
                    print(err)
        except:
            print("connection failed")

    # Webpage analyzing section:
    # Print page source
    def print_page_source(self):
        print(self.target.text)

    # Print all links that given in the webpage
    def get_links(self):
        soup = BeautifulSoup(self.target.text, 'html.parser')
        for link in soup.find_all('a'):
            try:
                if "http" in (link.get('href')):
                    print(link.get('href'))
            except:
                pass

    # Print all paths on the webpage
    def get_paths(self):
        soup = BeautifulSoup(self.target.text, 'html.parser')
        links = soup.find_all('a')
        for link in links:
            try:
                if link.get('href')[8:14] == self.target.url[8:14]:
                    print(link.get('href'))
            except:
                pass

    # Downloading PDFs files of webpage
    def get_pdfs(self):
        soup = BeautifulSoup(self.target.text, 'html.parser')
        links = soup.find_all('a')
        links = [link['href'] for link in links]
        i = 0
        for link in links:
            if "https://" in link and ".pdf" in link:
                pdf_url_response = requests.get(link, headers={"User-Agent": "Chrome/51.0.2704.103", })
                if pdf_url_response.status_code == 200:
                    file_name = "pdf_file_" + str(i) + ".pdf"
                    i += 1
                    with open(file_name, 'wb') as file:
                        file.write(pdf_url_response.content)

    # Download all images from the webpage
    def get_images(self):
        soup = BeautifulSoup(self.target.text, 'html.parser')
        images = soup.find_all('img')
        images_urls = [img['src'] for img in images]
        name_changer = 0
        for image in images_urls:
            name_changer += 1
            file_name = "image" + str(name_changer)
            with open(file_name + '.jpg', 'wb') as file:
                img = requests.get(image)
                file.write(img.content)


# Printing welcome message
def welcome_message():
    print("=" * 30)
    print("  Welcome to IP/URL analyzing")
    print("=" * 30)


# Printing all IP analyzing options
def ip_analyze_options():
    print("=" * 30)
    options = f"Analyzing option:\n-Ping target\n-Scan TCP ports" \
              f"\n-Scan specific port\n-Hack ssh user\n-SSH connect" \
              "\n-Main menu\n-Reselect target\n-Exit"
    print(options)
    print("=" * 30)


# Printing all webpage analyzing options
def webpage_analyze_options():
    print("=" * 30)
    options = f"Analyzing option:\n-Print page source\n-Get links\n-Get paths" \
              f"\n-Get images\n-Get pdf\n-Reselect target\n-Main menu\n-Exit"
    print(options)
    print("=" * 30)


# All popular SSH connections
def get_from_db():
    with open('db.json', 'r') as file:
        return json.load(file)


# webpage's analyzing choose section
def webpage_analyze_choice(target):
    choice = input("Select analytics:").lower()
    if choice == "print page source":
        target.print_page_source()

    elif choice == "get links":
        print("=" * 15 + "Links" + "=" * 15)
        target.get_links()

    elif choice == "get paths":
        print("=" * 15 + "Paths" + "=" * 15)
        target.get_paths()

    elif choice == "get images":
        print("Downloading images to current path...")
        target.get_images()
        print("Done!")

    elif choice == "get pdf":
        print("Downloading PDFs to current path...")
        target.get_pdfs()
        print("Done")

    elif choice == "reselect target":
        webpage_choice()
        time.sleep(1)

    elif choice == "main menu":
        main()
        time.sleep(1)

    elif choice == "exit":
        print("Exiting...")
        time.sleep(1.5)
        sys.exit()

    else:
        print("Wrong input, try again...")
        time.sleep(1.5)


# IP's analyzing choose section
def ip_analyze_choice(target):
    choice = input("Select analytics:").lower()
    if choice == "ping target":
        target.ping_target()
        time.sleep(1)

    elif choice == "scan tcp ports":
        target.scan_TCP_ports()
        time.sleep(1)

    elif choice == "scan specific port":
        while True:
            try:
                port_to_scan = int(input("Enter port you would like to scan:"))
                target.scan_specific_port(port_to_scan)
                time.sleep(1.5)
                break
            except:
                print("Port number not exist, try again...")
                time.sleep(1)

    elif choice == "hack ssh user":
        target.ssh_user_result()

    elif choice == "ssh connect":
        username = input("Enter username>")
        password = input("Enter password>")
        target.ssh_connect(username, password)

    elif choice == "reselect target":
        ip_choice()
        time.sleep(1)

    elif choice == "main menu":
        main()
        time.sleep(1)

    elif choice == "exit":
        print("Exiting...")
        time.sleep(1.5)
        sys.exit()

    else:
        print("Wrong input, try again...")
        time.sleep(1.5)


# Loop for starting analyzing the chosen IP.
def ip_choice():
    ip = input("Enter the IP you would like to analyze:")
    target = target_analyzer(ip)
    while True:
        ip_analyze_options()
        ip_analyze_choice(target)


# Loop for starting analyzing the chosen webpage.
def webpage_choice():
    print("=" * 30)
    try:
        web_page = requests.get(input("Enter page web page URL to analyze:"))
        target = target_analyzer(web_page)
        while True:
            webpage_analyze_options()
            webpage_analyze_choice(target)
    except Exception:
        print("An error occurred, try again...")
        time.sleep(1)
        webpage_choice()


# Select section of webpage or IP analyzing.
def web_or_ip():
    print("Choose type of target to analyze\n-Web page\n-IP\n-Exit")
    print("=" * 30)
    target_type = input("Type of target:").lower()
    if target_type == "web page" or target_type == "webpage":
        webpage_choice()
    elif target_type == "ip":
        ip_choice()
    elif target_type == "exit":
        sys.exit()
    else:
        print("Wrong input, try again...")
        web_or_ip()


def main():
    welcome_message()
    web_or_ip()


if __name__ == "__main__":
    main()
