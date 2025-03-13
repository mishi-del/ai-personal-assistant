import os
import sys
import json
from typing import Dict, Any
import openai
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
import typer
from config import default_config
from task_handlers import TaskHandler

# Initialize console for rich output
console = Console()

def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        console.print("[red]Error: OPENROUTER_API_KEY not found in .env file[/red]")
        sys.exit(1)
    return api_key

class AIAgent:
    def __init__(self, config=default_config):
        self.config = config
        self.client = openai.OpenAI(
            api_key=load_environment(),
            base_url=self.config.base_url,
            default_headers={
                "HTTP-Referer": "https://github.com/your-repo",  # Replace with your site
                "X-Title": "AI Agent"  # Replace with your app name
            }
        )
        self.conversation_history = []
        self.task_handler = TaskHandler(config)
    
    def add_to_history(self, role: str, content: str):
        """Add a message to the conversation history"""
        self.conversation_history.append({"role": role, "content": content})
    
    def parse_task(self, response: str) -> Dict[str, Any]:
        """Parse the AI response to extract task information"""
        try:
            # Look for JSON-like structure in the response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end != -1:
                task_json = response[start:end]
                return json.loads(task_json)
            return {"type": "unknown", "error": "No task information found"}
        except Exception as e:
            return {"type": "error", "error": str(e)}

    def process_command(self, user_input: str) -> str:
        """Process a user command and return the response"""
        try:
            # Add user input to conversation history
            self.add_to_history("user", user_input)
            
            # Create a system message that guides the AI to return structured responses
            system_message = """You are a helpful AI assistant that can perform various tasks. 
            When a user requests an action, analyze it and return a JSON response with the following structure:
            {
                "type": "task_type",
                "action": "specific_action",
                "parameters": {
                    "param1": "value1",
                    "param2": "value2"
                }
            }
            Available task types: browse, search, book, weather, maps, system_cmd
            """

            # Get response from OpenRouter
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_message},
                    *self.conversation_history,
                    {"role": "user", "content": f"Parse this request and return a JSON response: {user_input}"}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Extract and parse the response
            ai_response = response.choices[0].message.content
            task = self.parse_task(ai_response)
            
            # Execute the task if valid
            if task.get("type") in self.config.allowed_operations:
                result = self.task_handler.process_task(task["type"], **task.get("parameters", {}))
                self.add_to_history("assistant", f"I've completed the task: {result}")
                return f"I've completed the task: {result}"
            else:
                self.add_to_history("assistant", ai_response)
                return ai_response
            
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")
            return f"An error occurred: {str(e)}"
    
    def execute_task(self, task: Dict[str, Any]) -> str:
        """Execute a specific task based on the command type"""
        if task["type"] not in self.config.allowed_operations:
            return f"Operation {task['type']} is not allowed"
        
        return self.task_handler.process_task(task["type"], **task.get("parameters", {}))

def main():
    """Main function to run the AI agent"""
    agent = AIAgent()
    console.print("[bold green]AI Agent initialized. Type 'exit' to quit.[/bold green]")
    console.print("[bold blue]You can ask me to:[/bold blue]")
    console.print("- Open websites (e.g., 'open google')")
    console.print("- Search the web (e.g., 'search for restaurants near me')")
    console.print("- Get directions (e.g., 'get directions from New York to Boston')")
    console.print("- Check weather (e.g., 'what's the weather in London')")
    console.print("- Book restaurants (e.g., 'book a table for dinner')")
    console.print("- And more!")
    
    while True:
        try:
            # Get user input
            user_input = typer.prompt("\nWhat can I help you with?")
            
            if user_input.lower() == 'exit':
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            # Process the command
            response = agent.process_command(user_input)
            
            # Display the response
            console.print(Markdown(response))
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]An error occurred: {str(e)}[/red]")

if __name__ == "__main__":
    typer.run(main) 