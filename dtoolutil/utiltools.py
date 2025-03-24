import sys
import msvcrt
import hashlib
from time import sleep

def spinner(_stringLoad, _stringDone):
	spinner = ['\033[91m|\033[0m', '\033[92m/\033[0m', '\033[93m-\033[0m', '\033[94m\\\033[0m']
	for _ in range(20):
		for symbol in spinner:
			sys.stdout.write(f"\r{_stringLoad}... {symbol}")
			sys.stdout.flush()
			sleep(0.1)
	sys.stdout.write(f"\r{_stringDone}        \n")
	sleep(1)
	print("\033c", end="")

def customcls():
	print("\033c", end="")
	sleep(1)

def prnErr(e) -> None:
		print(f"Error: \033[41m{e}\033[0m\n")

def pressAnyKey():
	sys.stdout.write("Press any key to continue...")  # Print message
	sys.stdout.flush()

	# Simulate blinking cursor effect
	while not msvcrt.kbhit():  # Wait for a key press
		sys.stdout.write("_")  # Simulate cursor
		sys.stdout.flush()
		sleep(0.5)
		sys.stdout.write("\b \b")  # Erase cursor effect
		sys.stdout.flush()
		sleep(0.5)

	msvcrt.getch()  # Capture key press
	customcls()

def calcSHA256(file_path):
	"""Calculate the SHA-256 checksum of a file."""
	sha256_hash = hashlib.sha256()
	with open(file_path, "rb") as file:
		for chunk in iter(lambda: file.read(8192), b""):
			sha256_hash.update(chunk)
	return sha256_hash.hexdigest()