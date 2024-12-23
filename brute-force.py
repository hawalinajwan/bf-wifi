import subprocess
import texttable as tt
from termcolor import cprint
import time

class WifiTool:

    def __init__(self, interface):
        cprint("                        - A Wifi Toolkit for all\n", "magenta")                                           
        cprint("Starting the WifiTool . . . \n", "green")
        self.interface = interface
        time.sleep(2)

    def scanWifi(self):
        tab = tt.Texttable()
        headings = ['SSID', 'SIGNAL', 'CHANNEL', '  MAC ADDRESS  ', 'ENCRYPTION']
        tab.header(headings)
        
        ssid = []
        signl = []
        chnl = []
        addr = []
        encry = []
        connection = 0

        cprint("\n[*] Scanning for WiFi connections . . . \n", "yellow")

        try:
            # Menjalankan perintah `netsh` untuk melihat jaringan WiFi yang tersedia
            output = subprocess.check_output("netsh wlan show networks mode=bssid", shell=True, text=True)
            lines = output.split('\n')
            
            # Parsing output `netsh` untuk mendapatkan detail SSID, Sinyal, Channel, MAC Address, Encryption
            ssid_value = ""
            for line in lines:
                if "SSID" in line and "BSSID" not in line:
                    ssid_value = line.split(":")[-1].strip()
                if "Signal" in line:
                    signl.append(line.split(":")[-1].strip())
                if "Channel" in line:
                    chnl.append(line.split(":")[-1].strip())
                if "BSSID" in line:
                    addr.append(line.split(":")[-1].strip())
                    ssid.append(ssid_value)
                    encry.append("WPA2" if "WPA" in line else "OPEN")
                    connection += 1

            # Tambahkan data ke tabel untuk ditampilkan
            for row in zip(ssid, signl, chnl, addr, encry):
                tab.add_row(row)

            s = tab.draw()
            cprint(s, "green")

            if connection == 0:
                cprint("\n[-] No WiFi connection in your area\n", 'red')
            else:
                cprint("\n[+] " + str(connection) + " WiFi connection(s) found\n", 'cyan')
        except subprocess.CalledProcessError as e:
            cprint(f"[!!] Error: {e}\n", "yellow")
            cprint("[!!] Something went wrong\n", "yellow")

    def connect_wifi(self, ssid, passkey):
        try:
            # Menggunakan netsh untuk menyambung ke WiFi dengan nama (SSID) yang diberikan
            cprint(f"[+] Trying to connect to '{ssid}' ...", "cyan")
            # netsh wlan connect name=<SSID> key=<password> (Windows)
            command = f'netsh wlan connect name="{ssid}"'
            output = subprocess.check_output(command, shell=True, text=True)
            if "successfully" in output:
                cprint(f"[+] WiFi '{ssid}' successfully connected with '{passkey}'\n", "green")
                return True
            else:
                cprint("[-] Connection failed\n", "red")
                return False
        except Exception as e:
            cprint(f"[!!] Connection Failed: {e}\n", "yellow")
            return False

    def brute_force_pass(self, ssid, wordlist):
        try:
            with open(wordlist, 'rt') as file:
                for line in file.readlines():
                    password = line.strip()
                    if self.connect_wifi(ssid, password):
                        break
        except FileNotFoundError:
            cprint(f"[-] Wordlist file '{wordlist}' not found.\n", 'red')

    @staticmethod
    def menu():
        cprint("----------------------------Menu---------------------------", "yellow")
        cprint(" | * scan - scan wifi connections", 'magenta', attrs=['bold'])
        cprint(" | * connect - connect to wifi connection", 'magenta', attrs=['bold'])
        cprint(" | * bruteforce - brute force wifi connection", 'magenta', attrs=['bold'])
        cprint(" | * exit - exit", 'magenta', attrs=['bold'])
        cprint("_|_________________________________________________________\n", "yellow")


if __name__ == "__main__":
    try:
        wifi = WifiTool("wlan0")  
        while True:
            wifi.menu()
            cprint("\nroot@WifiScanner:~$ ", "green", end="")
            c = input()
            if c in "scan":
                wifi.scanWifi()
            elif c in "connect":
                cprint("\n[+] Enter SSID : ", "green", end="")
                ssid = input()
                cprint("[+] Enter PASSWORD : ", "green", end="")
                passkey = input()
                wifi.connect_wifi(ssid, passkey)
            elif c in "bruteforce":
                cprint("\n[+] Enter SSID : ", "green", end="")
                ssid = input()
                cprint("[+] Enter PASSWORD File path : ", "green", end="")
                wordlist = input()
                wifi.brute_force_pass(ssid, wordlist)
            elif c in "exit":
                cprint("\n[+] Exiting ...\n", 'red')
                exit()
    except KeyboardInterrupt:
        cprint("\n\n[-] Forced Exit By User!!!\n", "red")
