#! /usr/bin/env python3
import subprocess
import time
# import subprocess
import moonsModbus
import time
import redis
red= redis.Redis(host= 'localhost',port= '6379')
def ping_ip_continuously(ip_address, timeout=2,):
  
    while True:
        try:
            result = subprocess.run(['ping', '-c', '1', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout,)
            if result.returncode == 0:
                red.set('wifi','dhej')
                print(True) 
                
              
            else:
                while True:
                    red.set('wifi','false')
                    moonsModbus.stopJog()
              
                    print(False) 
            
        except subprocess.TimeoutExpired:
            while True:
                red.set('wifi','false')
                moonsModbus.stopJog()
                print(False)  
        
        

ip_address = "192.168.5.1" 
ping_ip_continuously(ip_address, timeout=1)  
