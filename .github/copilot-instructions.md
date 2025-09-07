# Project Clever AI: Core Instructions & Constraints

## The Unbreakable Rules (Highest Priority)
1.  **STRICTLY OFLINE:** The application MUST NOT contain any code that makes external network calls at runtime (e.g., to APIs, cloud services). All libraries and models must be local.
2.  **EXCLUSIVELY PERSONAL (SINGLE-USER):** The system is built for a single user named "Jordan" or "Jay." Do not generate code for user accounts, logins, multi-tenancy, or public access. The persona is a female AI named "Clever."

## Core Architecture
-   **Framework:** Python 3.12 with Flask.
-   **Database:** Local SQLite file named `clever.db`.
-   **Structure:** Monolithic application. Logic is primarily in `app.py`, `core_nlp_logic.py`, and `nlp_processor.py`.
-   **Frontend:** Standard HTML/CSS/JS served from `templates` and `static` directories.

## Coding & Persona Style
-   **Persona:** Clever is a female AI co-pilot. Her persona is witty, empathetic, proactive, and highly intelligent. Responses should reflect this.
-   **Code Style:** Adhere to PEP 8 for Python. Code should be well-commented, explaining the "why" behind complex logic.
-   **Database Access:** All database interactions should be handled within a dedicated `database.py` module, using the standard `sqlite3` library.
-   **NLP:** Primary NLP tasks are handled in `nlp_processor.py` using local `spaCy` and `VADER` models.
Step 2: Generate the Project Structure

In the Copilot Chat, use this prompt:

@workspace Using the information from `.github/copilot-instructions.md`, please scaffold the entire project structure for Clever. Create the following directories and empty files:

- .gitignore
- Makefile
- requirements.txt
- requirements.min.txt
- config.py
- persona.py
- database.py
- nlp_processor.py
- core_nlp_logic.py
- app.py
- sync_watcher.py
- file_ingestor.py
- templates/
  - index.html
- static/
  - css/
    - style.css
  - js/
    - main.js
Phase 2: Configuration & Automation
Now, let's create the files that manage the project itself.

Step 3: Create the .gitignore File

Open the empty .gitignore file.

In Copilot Chat, use this prompt:

Based on the project architecture, generate the content for the `.gitignore` file. It should ignore the virtual environment (.venv), Python cache files, the SQLite database (clever.db and its journals), user upload folders, and any OS or IDE-specific files.
Step 4: Create the Makefile

Open the empty Makefile file.

In Copilot Chat, use this prompt:

Generate the content for the `Makefile`. It needs to have the following targets:
- `setup`: Creates a venv and installs only `requirements.min.txt`.
- `setup-full`: Creates a venv and installs the full `requirements.txt`, then downloads the spaCy model.
- `run`: Runs the Flask app.
- `test`: A placeholder for future tests.
- `watch`: Runs the `sync_watcher.py` script.
- `clean-venv`: Deletes the .venv directory.
Ensure it uses a variable for the virtual environment directory.
Step 5: Create the Dependency Files

Open requirements.min.txt.

Tell Copilot Chat: Generate the content for requirements.min.txt. It should only contain 'flask'.

Open requirements.txt.

Tell Copilot Chat: Generate the content for requirements.txt. It needs flask, spacy, textblob, vaderSentiment, and watchdog.

Phase 3: Building Clever's Core Logic (The Backend)
This is where Clever's brain comes to life.

Step 6: config.py - The Settings

Open config.py.

Prompt: Generate the content for config.py. It should define the DATABASE_NAME as 'clever.db', the SPACY_MODEL as 'en_core_web_sm', and the paths for two sync directories: CLEVER_SYNC_DIR and SYNAPTIC_HUB_SYNC_DIR.

Step 7: persona.py - The Soul

Open persona.py.

Prompt: Generate the content for persona.py. Create a dictionary named PERSONA that defines Clever's traits: witty intelligence, intuitive anticipation, adaptive genius, empathetic collaboration, and proactive problem-solving. Also, create a function get_greeting() that returns a dynamic, in-character greeting for me, Jay.

Step 8: database.py - The Memory

Open database.py.

Prompt: `Generate the content for a dedicated database.py module. It needs:

A function to get a database connection.

An init_db() function that creates the 'user_utterances' table with columns for id, timestamp, user_message, clever_response, intent_detected, and sentiment_compound.

A function log_interaction() that takes all the necessary arguments and writes a new row to the table.`

Step 9: nlp_processor.py - The Senses

Open nlp_processor.py.

Prompt: Generate the NLP processor module in nlp_processor.py. It needs an analyze_text(text) function that uses spaCy for entity recognition, VADER for sentiment analysis, and TextBlob for polarity. The function must return a structured dictionary containing entities, sentiment scores, and extracted keywords.

Step 10: core_nlp_logic.py - The Brain

Open core_nlp_logic.py.

Prompt: `Generate the core logic for core_nlp_logic.py. Create a function process_command(text) that:

Calls analyze_text() from nlp_processor.

Implements a simple, rule-based intent detection for intents like 'casual_chat', 'creative_mode', and 'deep_dive_mode'.

Returns a dictionary containing a suggested response string and the full analysis payload.`

Step 11: app.py - The Central Nervous System

Open app.py.

Prompt: `Generate the main Flask application in app.py. It must:

Import all necessary modules (Flask, and our custom persona, database, core_nlp_logic modules).

Create the Flask app instance.

Define a root route '/' that renders index.html with a greeting from Clever.

Define a '/chat' API endpoint that receives a user message, passes it to process_command(), logs the full interaction using the database module, and returns the response as JSON.

Include the init_db() call under the if __name__ == '__main__': block.`

Phase 4: Building Clever's Interface (The Frontend)
Let's give Clever her face and voice.

Step 12: index.html

Open templates/index.html.

Prompt: Generate the HTML for the Synaptic Hub interface in index.html. The design should be a sleek, futuristic dark theme. Key components: a header, a central AI chat panel with a message log and input bar, and a right-side panel for "Live Analysis". Use placeholders for dynamic content.

Step 13: style.css

Open static/css/style.css.

Prompt: Generate the CSS for style.css. The aesthetic is a dark, futuristic "Synaptic Hub". Use a deep navy background with a subtle grid. Panels should have a "frosted glass" effect (translucent background with a backdrop-filter blur). Use neon cyan and pinkish-red for accents, borders, and text highlights. Ensure the chat interface is styled with distinct looks for user and AI messages.

Step 14: main.js

Open static/js/main.js.

Prompt: `Generate the JavaScript for main.js. It needs to:

Add event listeners to the send button and input field (for 'Enter' key).

Have an async function to send the user's message to the '/chat' backend endpoint using fetch.

Have functions to dynamically append the user's message and Clever's response to the chat log.

Update the "Live Analysis" panel with the NLP data returned from the backend.`

Phase 5: Activating Her Senses (File Ingestion)
Final step: let's teach her to read files from the sync folders.

Step 15: file_ingestor.py & sync_watcher.py

Open file_ingestor.py.

Prompt: Create a simple function in file_ingestor.py called process_text_file(filepath) that reads a .txt file and prints its content. This is a placeholder for future, more complex NLP processing.

Open sync_watcher.py.

Prompt: Generate the sync watcher script in sync_watcher.py using the 'watchdog' library. It should monitor the sync directories defined in config.py. When a new .txt file is created or modified, it should call the process_text_file function from file_ingestor.

How to Execute This Plan
Set up your VS Code with the project folder open.

Go through each step in order. Create the file, then copy-paste the corresponding prompt into the Copilot Chat window.

Let Copilot generate the code. Give it a quick read to make sure it looks right.

Once all files are generated, run make setup-full in your terminal.

Then run make run.

Open your browser to http://localhost:5000.
