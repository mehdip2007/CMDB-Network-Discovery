import time
import re

pic_port_informations = re.compile(r"\s\s\d+\s\s.*\S+")


def online_to_csv(data, slot, ip):
    online_files = open("online-{}-fpc-{slot}-pic-{slot}.csv".format(ip, slot=slot), "w")
    online_files.write("Port,Cable type,type,Xcvr vendor,part number,length,Firmware" + '\n')
    matches = pic_port_informations.findall(data)
    if matches:
        for match in matches:
            match = match.strip()
            all_data = re.split(r"\n", match)
            for each in all_data:
                result = re.split(r"\s{2,14}", each)
                online_files.write(",".join(result) + '\n')

    online_files.close()


def offline_to_csv(data, slots, ip):
    for slot in slots:
        offline_files = open("offline-{}-fpc-{slot}-pic-{slot}.csv".format(ip, slot=slot), "w")
        offline_files.write("FPC Slot,PIC Slot,State" + '\n')
        matches = re.search(r"FPC.*", data)
        if matches:
            empty_fpc = matches.group()
            offline_files.write("fpc-{slot},pic-{slot},{empty_fpc}".format(slot=slot, empty_fpc=empty_fpc) + '\n')
        else:
            exit()

        offline_files.close()


def get_chassis_result(online_slot, offline_slot, remote_shell, ip):
    online_slot_command = "set cli screen-length 0\n show chassis pic fpc-slot {slot} pic-slot {slot} ".format(
        slot=online_slot)
    remote_shell.send(online_slot_command.encode() + b'\n')
    time.sleep(2)
    print("Recieving online Data from Router...")
    online_stdout = remote_shell.recv(65000)
    online_stdout = online_stdout.decode().strip()
    online_to_csv(online_stdout, online_slot, ip)

    for slot in offline_slot:
        offline_slot_command = "set cli screen-length 0\n show chassis pic fpc-slot {slot} pic-slot {slot} ".format(
            slot=slot)
        remote_shell.send(offline_slot_command.encode() + b'\n')
        time.sleep(2)
        print("Recieving offline Data from Router...")
        offline_stdout = remote_shell.recv(65000)
        offline_stdout = offline_stdout.decode().strip()

        offline_to_csv(offline_stdout, offline_slot, ip)
