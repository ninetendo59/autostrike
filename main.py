import urllib3
import sys
from time import sleep
from dtoolutil.miscUtils import miscUtils
from dtoolutil.webPathUtil import webPathUtil
from dtoolutil.localPathUtil import localPathUtil
from dtoolutil.utiltools import customcls, prnErr


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def getIntervalTimeInput(CHECK_INTERVAL):
	while CHECK_INTERVAL < 0:
		try:
			print("\033[3;6;103mNote:\033[0m\n"
				"-> \033[42mPress Enter to skip time interval.\033[0m\n")
			user_input = input("Provide time interval (minutes) to start syncing.\n> \033[32m")
			print("\033[0m")
			if user_input.strip() == "":
				CHECK_INTERVAL = 0
			else:
				CHECK_INTERVAL = int(user_input)
		except ValueError:
			print("Please Enter a valid input.")
			CHECK_INTERVAL = -1
			sleep(1)
			customcls()
			continue
		
		if CHECK_INTERVAL >= 0:
			CHECK_INTERVAL = CHECK_INTERVAL * 60
			print(f"Time Interval to sync: \033[32m{CHECK_INTERVAL/60}\033[0m")
			sleep(1)
			customcls()
			return CHECK_INTERVAL
		else:
			print(f"Do you think there are negative time???\nPlease try again.")
			CHECK_INTERVAL = -1
			sleep(1)
			customcls()

def menuName():
	customcls()
	print("Download file from web directories tool.\n"
	"Dev: \033[3;6;104mninetendo59\033[0m")
	sleep(2)
	customcls()

def main():
	try:
		CHECK_INTERVAL = -1
		_miscUtils = miscUtils()
		menuName()
		CHECK_INTERVAL = getIntervalTimeInput(CHECK_INTERVAL)
		_miscUtils.initLocalPath()
		_miscUtils.initWebPath()
		while True:

			try:
				_miscUtils.addPaths(
					localPathUtil.grepLocalDirList(_miscUtils.getBasePath()),
					webPathUtil.grepWebPathList(_miscUtils.getBaseWebLink())
				)

				print (_miscUtils.getBothPath())

				if _miscUtils.cmpDirList(
					_miscUtils.listLocalPath(),
					_miscUtils.listWebPath()
				) == False:
					_miscUtils.syncWebDir()
			except Exception as e:
				prnErr(e)
				print("Stopping program...")
				sleep(1)
				break
			print(f"Will refresh after {CHECK_INTERVAL} seconds\nTo stop, press \033[45mctrl\033[0m + \033[45mc\033[0m")
			remaining_time = int(CHECK_INTERVAL)
			while remaining_time > 0:
				sys.stdout.write(f"\rRefreshing in {remaining_time} seconds...")
				sys.stdout.flush()
				sleep(1)
				remaining_time -= 1
			print("\rRefreshing now...                     ")
	except KeyboardInterrupt:
		print("\nProgram interrupted by user (Ctrl+C). Exiting gracefully...")
	except EOFError:
		print("\nProgram terminated by user (Ctrl+D). Exiting gracefully...")
	except Exception as e:
		prnErr(e)
	finally:
		print("Goodbye!")
	

if __name__ == "__main__":
	main()
