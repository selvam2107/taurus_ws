#!/usr/bin/env python3
import serial
import time
import rospy
from hw_t.msg import taurus_bms


# UART Configuration
uart_config = {
    "port": "/dev/ttyUSB3",  # Replace with your UART port
    "baudrate": 9600,
    "bytesize": serial.EIGHTBITS,
    "parity": serial.PARITY_NONE,
    "stopbits": serial.STOPBITS_ONE,
    "timeout": 2,  # Timeout for read operations
}

def calculate_checksum(data):
    """Calculate checksum by summing all bytes and taking modulo 256."""
    return sum(data) & 0xFF


def send_command(command_id):
    """Send a command to the BMS and receive a response."""
    try:
        with serial.Serial(**uart_config) as ser:
            # Construct the command
            command = [0xA5, 0x40, command_id, 0x08] + [0x00] * 8
            checksum = calculate_checksum(command)
            command.append(checksum)

            print(f"Sending Command for ID {hex(command_id)}:", [hex(x) for x in command])
            ser.write(bytes(command))  # Send the command

            time.sleep(1)  # Wait for the response
            
            response = ser.read(12)  # Read 12 bytes (expected length)
            print(f"Received Response for ID {hex(command_id)}:", response)
            return response
    except serial.SerialException as e:
        print(f"Error communicating with UART: {e}")
        return None
def parse_voltage_current_response(response):
    """Parse response from Command ID 0x90."""
    if len(response) < 8:
        print("Incomplete response for voltage and current.")
        return None

    cumulative_voltage = int.from_bytes(response[4:6], byteorder='big') * 0.1  # V
    acquisition_voltage = int.from_bytes(response[6:8], byteorder='big') * 0.1  # V
    current = (int.from_bytes(response[8:10], byteorder='big') - 30000) * 0.1  # A
    soc = int.from_bytes(response[10:12], byteorder='big') * 0.1  # %

    return {
        "cumulative_voltage": cumulative_voltage,
        "acquisition_voltage": acquisition_voltage,
        "current": current,
        "soc": soc
    }




def parse_mos_status_response(response):
    """Parse response from Command ID 0x93."""

    if len(response) < 12:
        print("Incomplete response for MOS status.")
        return None
    print("actual charge state",response[4])
    
    global charge_state,count
    
    # charge_state = response[4]
    charge_state = charge_state
    charge_mos_status = response[5]
    discharge_mos_status = response[6]
    bms_life = response[7]
    remaining_capacity = int.from_bytes(response[8:12], byteorder='big')
    
    if response[4] == 0:
        count = count+1
        print("**************",count)
        if count == 3:
                charge_state = 0
        else :
            print(count)
            if response[4]==2:
                charge_state = 2
            if response[4]==1:
                charge_state = 1
            else:
                 charge_state = charge_state
        print("@@@@@@@@@@@@@@@@",charge_state)
    if response[4]==2:
                charge_state = 2
                count = 0
    if response[4]==1:
                charge_state = 1
                count = 0

    

    return {
        "charge_state": charge_state,
        "charge_mos_status": charge_mos_status,
        "discharge_mos_status": discharge_mos_status,
        "bms_life": bms_life,
        "remaining_capacity": remaining_capacity
    }


def main():
    rospy.init_node('status_node', anonymous=True)
    pub = rospy.Publisher('/taurus_status',taurus_bms, queue_size=10)
    rate=rospy.Rate(10)
    global count
    global charge_state
    charge_state = 7
    count = 0

  


    while not rospy.is_shutdown():
        time.sleep(1)
        try:
              # Read voltage and current (Command ID: 0x90)
            voltage_current_response = send_command(0x90)
            voltage_current_data = parse_voltage_current_response(voltage_current_response)

            # Read MOS status (Command ID: 0x93)
            mos_status_response = send_command(0x93)
            mos_status_data = parse_mos_status_response(mos_status_response)

            if voltage_current_data and mos_status_data:


                        
                print("\nVoltage and Current Data:")
                print(f"Cumulative Voltage: {voltage_current_data['cumulative_voltage']} V")
                print(f"Acquisition Voltage: {voltage_current_data['acquisition_voltage']} V")
                print(f"Current: {voltage_current_data['current']} A")
                print(f"SOC: {voltage_current_data['soc']} %")


                print("\nMOS Status Data:")
                print(f"Charge State: {mos_status_data['charge_state']} (0: Rest, 1: Charging, 2: Discharging)")
                print(f"Charge MOS Status: {mos_status_data['charge_mos_status']} (0: Off, 1: On)")
                print(f"Discharge MOS Status: {mos_status_data['discharge_mos_status']} (0: Off, 1: On)")
                print(f"BMS Life: {mos_status_data['bms_life']} cycles")
                print(f"Remaining Capacity: {mos_status_data['remaining_capacity']} mAh")


                cumulative_voltage =  voltage_current_data['cumulative_voltage'] 
                Acquisition_Voltage = voltage_current_data['acquisition_voltage'] 
                Current = voltage_current_data['current']
                SOC= voltage_current_data['soc']
                Charge_State = mos_status_data['charge_state']
                Charge_MOS_Status = mos_status_data['charge_mos_status']
                Discharge_MOS_Status = mos_status_data['discharge_mos_status']
                BMS_Life = mos_status_data['bms_life']
                Remaining_Capacity = mos_status_data['remaining_capacity']


                msg = taurus_bms()
                msg.cumulative_voltage = cumulative_voltage 
                msg.acquisition_voltage = Acquisition_Voltage
                msg.current = Current
                msg.soc = SOC
                msg.charge_state = Charge_State
                msg.charge_mos_state = Charge_MOS_Status
                msg.discharge_mos_state = Discharge_MOS_Status
                msg.bms_life = BMS_Life
                msg.remaining_capacity = Remaining_Capacity

                pub.publish(msg)
                rate.sleep()
            else:
                print("unable to publish a message")

        
            

        except Exception as e:
            print(f"Error in loop: {e}")


   

if __name__ == "__main__":
    main()
