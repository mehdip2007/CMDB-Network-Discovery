import os


class Availability:
    router_ip = ""

    @staticmethod
    def check_ping(router_ip):
        response = os.system("ping -c 1 " + router_ip)

        if response == 0:
            print("Successfully Ping ---> ", router_ip)
            pingstatus = "Network Active"
        else:
            print("Failed to Ping ---> ", router_ip)
            pingstatus = "Network Error"

        return pingstatus
