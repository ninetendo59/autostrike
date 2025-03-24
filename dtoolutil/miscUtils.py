import os
import requests
from dtoolutil.utiltools import prnErr, spinner, customcls, pressAnyKey, calcSHA256
from time import sleep
from tqdm import tqdm


class miscUtils:
	"""Utility class for managing and comparing local and web directory paths."""

	def __init__(self):
		"""Initialize the miscUtils class with empty lists for local and web paths."""
		self._listLocalPath = []
		self._listWebPath = []
		self.BASEWEBLINK = ""
		self.BASELOCALPATH = ""

	def listLocalPath(self):
		"""Get the list of local directory paths.

		Returns:
			list: List of local directory paths.
		"""
		return self._listLocalPath
	
	def listWebPath(self):
		"""Get the list of web directory paths.

		Returns:
			list: List of web directory paths.
		"""
		return self._listWebPath
	
	def getBasePath(self):
		return self.BASELOCALPATH
	
	def getBaseWebLink(self):
		return self.BASEWEBLINK

	def getBothPath(self):
		"""Get both the lists of local and web directory paths.

		Returns:
			tuple: A tuple containing the list of local directory paths and the list of web directory paths.
		"""
		return [self._listLocalPath, self._listWebPath]

	@staticmethod
	def cmpDirList(_listLocalPath, _listWebPath) -> bool:
		"""Compare two lists of directory paths to check if they are identical.

		Args:
			_listLocalPath (list): List of local directory paths.
			_listWebPath (list): List of web directory paths.

		Returns:
			bool: True if the lists are identical, False otherwise.
		"""
		if len(_listLocalPath) != len(_listWebPath):
			print("New file found. File will be downloaded")
			return False
		
		_listLocalPath.sort()
		_listWebPath.sort()
		
		for _loopLocalPath, _loopWebPath in zip(_listWebPath, _listLocalPath):
			if _loopLocalPath != _loopWebPath:
				print("New file found. File will be downloaded")
				return False
		
		return True
	
	def addPaths(self, _localPath, _webPath):
		"""Add local and web directory paths to the respective lists.
	
		Args:
			_localPath (list): List of local directory paths to add.
			_webPath (list): List of web directory paths to add.
		"""
		print("Web link provided: ",self.getBaseWebLink())
		flat_localPath = [item for sublist in _localPath for item in (sublist if isinstance(sublist, list) else [sublist])]
		
		flat_webPath = [item for sublist in _webPath for item in (sublist if isinstance(sublist, list) else [sublist])]
	
		self._listLocalPath = list(dict.fromkeys(self._listLocalPath + flat_localPath))
		self._listWebPath = list(dict.fromkeys(self._listWebPath + flat_webPath))
	
	def initLocalPath(self):
		
		_localpathDownloadDir = ""
		
		while _localpathDownloadDir == "":
			_localpathDownloadDir = input(
					"Provide The Folder Full path You would like to save into.\n> \033[32m"
				)
		
			print("\033[0m")
			if _localpathDownloadDir == "":
				print(f"\033[41mInput must not be empty.\033[0m\nPlease try again")
				sleep(1.5)
				customcls()
		
			elif not os.path.exists(_localpathDownloadDir) or not os.path.isdir(_localpathDownloadDir):
				print(
					f"\033[41mProvided path is not valid or does not exist: {_localpathDownloadDir}\033[0m\n"
		  			"Please provide a valid local or network-mapped directory."
					)
				
				_localpathDownloadDir = ""
				sleep(1.5)
				customcls()
		
			else:
				print(f"Your files and directories will be downloaded into \033[4;35m{_localpathDownloadDir}\033[0m")
				self.BASELOCALPATH = _localpathDownloadDir
				sleep(1)
				pressAnyKey()

	def initWebPath(self):
		_weblinkbase = ""
		while _weblinkbase == "":
			_weblinkbase = input("Provide Link Web Directory Base Path:\n> \033[32m")
			print("\033[0m")
		
			if _weblinkbase == "":
				print(f"\033[41mInput must not be empty.\033[0m\nPlease try again")
				sleep(1.5)
				customcls()
		
			elif not (_weblinkbase.startswith("https://") or _weblinkbase.startswith("http://")):
				print(f"\033[41mUser input is not a valid link: {_weblinkbase}\033[0m\nPlease provide a valid link (http:// or https://).")
				_weblinkbase = ""
				sleep(1.5)
				customcls()
		
			else:
				print(f"Your Link: \033[94m{_weblinkbase}.\033[0m")
				self.BASEWEBLINK = _weblinkbase
				sleep(2)
				customcls()

	def syncWebDir(self):
		try:
			flat_local_paths = [item for sublist in self._listLocalPath for item in (sublist if isinstance(sublist, list) else [sublist])]
			flat_web_paths = [item for sublist in self._listWebPath for item in (sublist if isinstance(sublist, list) else [sublist])]
	
			flat_local_paths.sort()
			flat_web_paths.sort()
	
			print(f"Comparing directories...")
	
			for web_path in flat_web_paths:
				if web_path not in flat_local_paths:
					if web_path.endswith('/'):
						local_folder_path = f"{self.BASELOCALPATH}/{web_path}"
						customcls()
						print(f"Creating folder: {local_folder_path}")
						os.makedirs(local_folder_path, exist_ok=True)
						customcls()
					else:
						local_file_path = f"{self.BASELOCALPATH}/{web_path}"
						customcls()
						print(f"Downloading file: {web_path} to {local_file_path}")
						self.downloadFile(web_path, local_file_path)
						
	
			print("Synchronization completed successfully.")
			customcls()
		
		except Exception as e:
			prnErr(e)
	
	def downloadFile(self, web_path, local_path, sha256_url=None):
		"""Download a file from the web directory to the local directory with a progress bar and SHA-256 verification.
	
		Args:
			web_path (str): The path of the file in the web directory.
			local_path (str): The path where the file should be saved locally.
			sha256_url (str): The URL to fetch the SHA-256 checksum for the file (optional).
		"""
		try:
			full_url = f"{self.BASEWEBLINK}/{web_path}".replace("//", "/").replace(":/", "://")
			print(f"Checking file size for {full_url}")

			head_response = requests.head(full_url, verify=False)
			head_response.raise_for_status()
			web_file_size = int(head_response.headers.get('Content-Length', 0))
			expected_sha256 = None

			if sha256_url:
				print(f"Fetching SHA-256 checksum from {sha256_url}")
				sha256_response = requests.get(sha256_url, verify=False)
				sha256_response.raise_for_status()
				expected_sha256 = sha256_response.text.strip()
	
			if os.path.exists(local_path):
				local_file_size = os.path.getsize(local_path)
				print(f"Local file size: {local_file_size} bytes, Web file size: {web_file_size} bytes")
	
				if local_file_size == web_file_size:
					if expected_sha256:
						local_sha256 = calcSHA256(local_path)
						print(f"Local SHA-256: {local_sha256}, Expected SHA-256: {expected_sha256}")
						if local_sha256 == expected_sha256:
							print(f"File already exists and is verified: {local_path}. Skipping download.")
							return
						else:
							print(f"SHA-256 mismatch. Local file will be replaced: {local_path}")
					else:
						print(f"File already exists and is up-to-date: {local_path}. Skipping download.")
						return
				else:
					print(f"File size mismatch. Local file will be replaced: {local_path}")
	
			print(f"Downloading from {full_url} to {local_path}")

			response = requests.get(full_url, stream=True, verify=False)

			response.raise_for_status()  # Raise an error for HTTP issues
			os.makedirs(os.path.dirname(local_path), exist_ok=True)
	
			with open(local_path, 'wb') as file, tqdm(
				desc=f"Downloading {web_path}",
				total=web_file_size,
				unit='B',
				unit_scale=True,
				unit_divisor=1024,
			) as progress_bar:
				for chunk in response.iter_content(chunk_size=8192):
					file.write(chunk)
					progress_bar.update(len(chunk))
	
			print(f"Downloaded: {web_path} to {local_path}")

			if expected_sha256:
				local_sha256 = calcSHA256(local_path)
				print(f"Verifying SHA-256 checksum...")
				if local_sha256 == expected_sha256:
					print(f"SHA-256 checksum verified successfully: {local_path}")
				else:
					print(f"SHA-256 checksum mismatch! Deleting corrupted file: {local_path}")
					os.remove(local_path)
					raise ValueError("SHA-256 checksum verification failed.")
		
		except requests.exceptions.RequestException as e:
			prnErr(f"Failed to download {web_path}: {e}")
		
		except Exception as e:
			prnErr(f"An error occurred while downloading {web_path}: {e}")