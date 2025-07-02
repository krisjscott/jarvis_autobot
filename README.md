# 🤖 Jarvis Autobot

A Python-powered **personal assistant bot** that listens, processes commands, and responds—featuring regex-based conversation handling, modular structure, and ready-to-expand architecture.

## 👨‍💻 Author

**Krish Kumar**
GitHub: [@krisjscott](https://github.com/krisjscott)

---

## 🐍 Requirements

* Python 3.7 or higher
* Key libraries (install via `pip`):

  * `speech_recognition`
  * `pyttsx3`
  * `regex`
  * `flask` (if using REST APIs)
  * Any additional dependencies listed in `requirements.txt`

---

## ✨ Features

* 🗣️ **Voice and text** input handling using regular expressions
* 🤖 Multiple Python modules for structured conversation (`general.py`, `quiry.py`, etc.)
* 🌐 **REST API hooks** to integrate bot functions into web services
* 🔧 Modular setup: easily add new commands and modules

---

## 🚀 Setup & Usage

### 1. Clone the repo

```bash
git clone https://github.com/krisjscott/jarvis_autobot.git
cd jarvis_autobot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the bot

```bash
python general.py
```

Customize command patterns in `quiry.py` or other modules to fit your use cases.

---

## 🛠️ Module Overview

* `general.py`: Core entry point — parses input, dispatches commands
* `quiry.py`: Defines regex-based command-response mappings
* `utils/*.py`: Utility functions (e.g. text-to-speech, logging, APIs)

---

## 🧠 Extending the Bot

1. Add intent pattern in `quiry.py`:

   ```python
   (r"tell me a joke", tell_joke)
   ```
2. Implement the handler in `general.py` or a new module:

   ```python
   def tell_joke():
       speak("Why did the Python developer cross the road? To get to the other side!")
   ```
3. Hook into REST: modify `app.route()` in `general.py` to expose APIs.

---

## 🧩 Example: Add Weather Command

1. Add regex in `quiry.py`:

   ```python
   (r"weather in (.*)", get_weather)
   ```
2. In `general.py`, implement:

   ```python
   def get_weather(location):
       # call weather API, format, and speak the response
   ```

---

## 🤝 Contributing

Contributions are welcome! Suggestions for new modules, cleaner regex patterns, or improved REST support? Open an issue or PR.

---

## 📝 License

[MIT License](LICENSE) — freely use, modify, and distribute.

---

