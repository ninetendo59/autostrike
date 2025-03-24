import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dtoolutil.utiltools import customcls, spinner



class webPathUtil:

	@staticmethod
	def grepWebPathList(_url, _base_url=None, _visited=None):
		"""Recursively lists directories and files from a web URL if directory listing is enabled.
	
		Args:
			_url (str): The current URL to scan.
			_base_url (str, optional): The root URL to extract relative paths.
			_visited (set, optional): Keeps track of visited URLs to avoid loops.
	
		Returns:
			list: A list of discovered files and directories as relative paths.
		"""
		
		spinner("Fetching Web...", "")
		if _visited is None:
			_visited = set()
	
		if _base_url is None:
			_base_url = _url.rstrip("/")  
		
		paths = []
		
		try:
			response = requests.get(_url, timeout=5, verify=False)  
			if response.status_code != 200:
				return paths
			
			soup = BeautifulSoup(response.text, "html.parser")
			links = soup.find_all("a")
			
			for link in links:
				href = link.get("href")
				if href and not href.startswith("?") and href != "../":  
					full_url = urljoin(_url, href)
					relative_path = full_url.replace(_base_url, "").lstrip("/")
					
					if full_url not in _visited:
						_visited.add(full_url)
						paths.append(relative_path)
						
						if full_url.endswith("/"):
							paths.extend(webPathUtil.grepWebPathList(full_url, _base_url, _visited))
			
			paths = [item for item in paths if item]
	
		except Exception as e:
			customcls()
			print(f"\033[4;33;4:3;41mThere is an error occurred while fetching the web.\033[0m\n"
				  f"Error: \033[1;31m{e}\033[0m\n")
		
		return paths