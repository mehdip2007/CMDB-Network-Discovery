from modules.init_packages import os


class Connection:
    router_ip = ""

    @staticmethod
    def check_ping(router_ip):
        response = os.system("ping -c 1 " + router_ip)

        if response == 0:
            print("Successfully Ping ---> ", router_ip)
            pingstatus = "Network Active"
            print(pingstatus)

            return True
        else:
            print("Failed to Ping ---> ", router_ip)
            pingstatus = "Network Error"
            print(pingstatus)

            return False
