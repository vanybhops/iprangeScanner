from sys import argv as arguments
from sys import exit
import time
import requests
import socket
import re
from threading import Thread
ports = [80,81,82,83,8080]
threadRange=int(input("number of threads: "))

def check_for_axis(uri): 
    try:
        out = requests.get(uri,headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:88.0) Gecko/20100101 Firefox/88.0"}).text 
        reout = re.findall(r"<title>(.+)<\/title>",out)
        with open("working.txt","a") as f:
            f.write(uri+":"+reout[0]+"\n")
            f.close()
    except:
        pass

def scan(ip):
    open_ports = []
    for port in ports:
        try:
            sock = socket.create_connection((ip, port), timeout=1)
            print(f"[+] Port {str(port)} -- OPEN -- IP -- {str(ip)}")
            open_ports.append("http://" + str(ip) + ":" + str(port))
        except socket.timeout:
            pass
        except KeyboardInterrupt:
            exit()
        except:
            print("[!]connection refused")
    
    if(len(open_ports) > 0):
        for uri in open_ports:
            check_for_axis(uri)

def main():
    ip_range = arguments[1]
    splited = ip_range.split("-")
    from_range = splited[0]
    to_range = splited[1]

    splited_from_range = from_range.split(".")

    num_1 = int(splited_from_range[0])
    num_2 = int(splited_from_range[1])
    num_3 = int(splited_from_range[2])
    num_4 = int(splited_from_range[3])
    
    def go():
        x=0
        for i in range(num_1,256):
            for e in range(num_2,256):
                for r in range(num_3,256):
                    for p in range(num_4,256,int(threadRange)):
                        threadz=[]
                        for x in range(int(threadRange)):
                            if p>=256:
                                continue
                            ip = str(i) + "." + str(e) + "." + str(r) + "." + str(p)
                            p += 1
                            thread=Thread(target=scan,args=(ip,),daemon=False)
                            thread.start()
                            threadz.append(thread)
                        for thr in threadz:
                            thr.join()
                    if(str(ip) == str(to_range)):
                        return
    go()
if __name__ == "__main__":
    if(len(arguments)==2):
        main()
    print("Usage is python ipRange.py 0.0.0.0-255.255.255.255")
    exit()