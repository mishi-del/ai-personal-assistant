import webbrowser
import subprocess
import platform
import requests
from datetime import datetime
from typing import Dict, Any, Optional

class TaskHandler:
    def __init__(self, config):
        self.config = config
        self.os_name = platform.system().lower()

    def browse(self, url: str) -> str:
        """Open a URL in the default web browser"""
        try:
            webbrowser.open(url)
            return f"Successfully opened {url}"
        except Exception as e:
            return f"Error opening URL: {str(e)}"

    def open_application(self, app_name: str) -> str:
        """Open a predefined application or URL"""
        app_name = app_name.lower()
        if app_name in self.config.app_urls:
            return self.browse(self.config.app_urls[app_name])
        else:
            return f"Application '{app_name}' not found in configured apps"

    def search(self, query: str) -> str:
        """Perform a web search"""
        search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
        return self.browse(search_url)

    def book_restaurant(self, details: Dict[str, Any]) -> str:
        """Open restaurant booking website with given details"""
        # For now, just open OpenTable
        return self.browse(self.config.app_urls["booking"])

    def check_weather(self, location: str) -> str:
        """Check weather for a location"""
        weather_url = f"{self.config.app_urls['weather']}/weather/today/{requests.utils.quote(location)}"
        return self.browse(weather_url)

    def get_directions(self, start: str, end: str) -> str:
        """Get directions between two locations"""
        maps_url = f"{self.config.app_urls['maps']}/dir/{requests.utils.quote(start)}/{requests.utils.quote(end)}"
        return self.browse(maps_url)

    def execute_system_command(self, command: str) -> str:
        """Execute a system command safely"""
        # List of safe commands that can be executed
        safe_commands = {
            "time": lambda: f"Current time is {datetime.now().strftime('%H:%M:%S')}",
            "date": lambda: f"Today's date is {datetime.now().strftime('%Y-%m-%d')}",
            "os": lambda: f"Operating System: {platform.system()} {platform.release()}"
        }
        
        if command in safe_commands:
            return safe_commands[command]()
        return f"Command '{command}' not allowed for security reasons"

    def process_task(self, task_type: str, **kwargs) -> str:
        """Process a task based on its type"""
        task_handlers = {
            "browse": lambda: self.browse(kwargs.get("url", "")),
            "search": lambda: self.search(kwargs.get("query", "")),
            "book": lambda: self.book_restaurant(kwargs.get("details", {})),
            "weather": lambda: self.check_weather(kwargs.get("location", "")),
            "maps": lambda: self.get_directions(kwargs.get("start", ""), kwargs.get("end", "")),
            "system_cmd": lambda: self.execute_system_command(kwargs.get("command", "")),
        }

        if task_type in task_handlers:
            return task_handlers[task_type]()
        return f"Unknown task type: {task_type}" 