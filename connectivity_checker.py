import os


def check_ping(router_ip):
    response = os.system("ping -c 1 " + router_ip)

    if response == 0:
        print("Successfully Ping ---> ", router_ip)
        pingstatus = True
    else:
        print("Failed to Ping ---> ", router_ip)
        pingstatus = False

    return pingstatus
