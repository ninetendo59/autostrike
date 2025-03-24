from pathlib import Path
import os
from dtoolutil.utiltools import customcls, prnErr,spinner

class localPathUtil:
	"""class localPathUtil
		`localPathUtil.getSetDownloadDir(_dirName: str)` - set, get and return of directory anme to set
		`localPathUtil.grepDefaultPath() - set default path based on OS path format.
	"""

	@staticmethod
	def getSetDownloadDir(_dirName: str) -> str:
		try:
			_defaultPath = localPathUtil.grepDefaultPath()
			_downloadPath = os.path.join(_defaultPath, _dirName)
			if os.path.isdir(_downloadPath):
				print(f"\"{_dirName}\" directory exists in \"{_defaultPath}\". Skip creating directory.")
			else:
				print(f"\"{_dirName}\" directory does not exists in \"{_defaultPath}\".")
				os.makedirs(_downloadPath, exist_ok=True)
				print(f"\"{_dirName}\" directory has been created in \"{_defaultPath}\". Your created directory path: \"{_downloadPath}\"")
			return (_downloadPath)
		except Exception as e:
			prnErr(e)
			return ("")

	@staticmethod
	def grepDefaultPath() -> str:
		try:
			return os.path.join(Path.home(), "Documents")
		except Exception as e:
			prnErr(e)
			return("")
	
	@staticmethod
	def grepLocalDirList(base_path):
		"""Recursively lists all directories and files in the given path.

		Args:
			base_path (str): The directory path to scan.

		Returns:
			list: A list of relative file and directory paths.
		"""
		spinner("Fetching Local Directory...", "")

		all_paths = []
		
		for root, dirs, files in os.walk(base_path):
			relative_root = os.path.relpath(root, base_path)
			
			if relative_root != ".":
				all_paths.append(relative_root + "/")
			
			for file in files:
				file_path = os.path.join(relative_root, file) if relative_root != "." else file
				all_paths.append(file_path)
		return all_paths

		
	def grepCurrDirRecurse():
		return("")
