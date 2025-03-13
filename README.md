# AI Personal Assistant

A web-based AI personal assistant that can help you with various tasks using natural language commands. Built with Python, Flask, and OpenAI's GPT models.

## Features

- 🌐 Open websites and perform web searches
- 🗺️ Get directions and location information
- 🍽️ Book restaurants and find places
- 🌤️ Check weather information
- 💻 Execute system commands
- 📝 File management capabilities
- 🎨 Beautiful web interface
- 🔄 Real-time responses

## Screenshots

![AI Assistant Interface](screenshots/interface.png)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-personal-assistant.git
cd ai-personal-assistant
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Usage

1. Start the server:
```bash
python web_agent.py
```

2. Open your web browser and go to:
```
http://localhost:5000
```

3. Start chatting with your AI assistant!

Example commands:
- "open google"
- "search for restaurants near me"
- "get directions from New York to Boston"
- "what's the weather in London"
- "book a table for dinner"

## Project Structure

```
ai-personal-assistant/
├── agent.py           # Main agent logic
├── config.py         # Configuration settings
├── task_handlers.py  # Task execution handlers
├── web_agent.py     # Web server and routes
├── templates/       # HTML templates
│   └── index.html  # Main web interface
├── requirements.txt # Project dependencies
└── README.md       # Project documentation
```

## Technologies Used

- Python 3.8+
- Flask
- OpenAI GPT Models
- HTML/CSS
- JavaScript

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 