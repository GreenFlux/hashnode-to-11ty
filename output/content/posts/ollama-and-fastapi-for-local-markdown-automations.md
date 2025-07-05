---
title: "Ollama & FastAPI for Local Markdown Automations"
date: 2025-05-11
permalink: "/ollama-and-fastapi-for-local-markdown-automations/"
layout: "post"
excerpt: "Markdown is a great format for storing text files that need to be compatible with multiple systems. And LLMs excel at generating Markdown. If you regularly copy/paste responses from ChatGPT to a text document, the context-switching can become a frict..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1746962748212/be77b440-e4eb-43dc-be91-59fe78abf063.png"
readTime: 5
tags: ["Python", "Python 3", "ollama", "LLaMa", "chatgpt", "markdown", "llm", "FastAPI", "self-hosted"]
series: "Artificial Intelligence"
---

Markdown is a great format for storing text files that need to be compatible with multiple systems. And LLMs excel at generating Markdown. If you regularly copy/paste responses from ChatGPT to a text document, the context-switching can become a friction point or bottle-neck in repetitive tasks.

There are countless AI-powered automation platforms out there that could solve this, but what if the data is sensitive/private, and can’t be shared with a 3rd party API? Or maybe you have vast amounts of data to process, and a paid service is not scalable? In cases like these, you can run an LLM locally using Ollama.

But what about automating the Markdown file creation? Ollama provides a local API for the LLM, but we need a local API for creating/editing Markdown files. It only takes a few lines of Python to handle the text file management, and that can easily be turned into an API using FastAPI.

**This guide will cover:**

* Running LLMs locally with Ollama
    
* Prompting the model from a Python Script
    
* Markdown CRUD with FastAPI
    
* Saving LLM Responses to Markdown with Python

*Let’s get to it!*

## Running LLMs locally with Ollama

Start out by downloading Ollama and installing it.

[**ollama.com/download**](http://ollama.com/download)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1729380535005/1c86f951-2e50-4d0a-a5e3-faf03d073ccf.png?auto=compress,format&format=webp&auto=compress,format&format=webp)

Once the download finishes, move the `Ollama.app` file to your **Applications** folder, then open it. Then click through the installer and approve the drive access. You’ll notice a new llama icon in the menu bar, with a single option to *Quit Ollama*.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731150387579/b9ce4790-220e-4721-8346-8e4cbdd4d05c.png?auto=compress,format&format=webp&auto=compress,format&format=webp)

There’s no other GUI— everything else is done from the terminal.

## Downloading and Prompting Models

Next, open the terminal and run:

```bash
ollama run llama3.2:1b
```

This will download the smaller, 1 billion parameter Llama3.2 model, then run it and let you begin prompting from the terminal. You’ll see several files download the first time running a model, but after that it should load quickly and be ready to start prompting.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746880539273/d64ce232-ab23-451d-b481-e1f69624c61e.png)

Type a prompt and hit Enter. You should see a response in the terminal.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746880613961/d434b073-7a5c-44c9-be91-04d2db99bb54.png)

Ok, Ollama and the Llama3.2 model are running locally. Next, we’ll send a prompt from Python using the Ollama API. Leave this terminal window open to keep Ollama and Llama3.2 running, and open a new terminal window for the next section.

**Note**: You can type `/bye` to exit Ollama and return to the main terminal, or `/?` for a list of other Ollama commands. But for now, keep it running to use in the next step.

## Prompting the model from a Python Script

Open the terminal and create a new folder for the project, then cd into it.

```bash
mkdir MarkdownAPI && cd MarkdownAPI
```

### **Install Python 3.10** (if not already)

Using [Homebrew](https://docs.brew.sh/Installation):

```bash
brew install python@3.10
```

Add it to your shell:

```bash
echo 'export PATH="/opt/homebrew/opt/python@3.10/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

Verify:

```bash
python3.10 --version
```

Then create a virtual environment:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

And install the required packages:

```bash
pip install --upgrade pip
pip install fastapi uvicorn aiofiles requests
```

Ok, the environment is set up. Next create a new Python script and save it in the root folder for the environment.

**send\_prompt.py**

```python
#!/usr/bin/env python3
"""
CLI wrapper for Ollama’s HTTP API (chat endpoint).

Usage
-----
$ ./send_prompt.py "Explain RAG in one paragraph"

Environment
-----------
- Expects the Ollama daemon to be running locally (default: http://localhost:11434).
- Adjust `OLLAMA_HOST` if your daemon is on a different host/port.
"""

import argparse
import json
import sys
from pathlib import Path

import requests

# --------------------------------------------------------------------------- #
# Configuration                                                               #
# --------------------------------------------------------------------------- #
OLLAMA_HOST   = "http://localhost:11434"        # Change if Ollama runs elsewhere
MODEL_NAME    = "llama3.2:1b"                  # FQN of the model to query
SYSTEM_PROMPT = (
    "You are a concise technical assistant. "
    "Respond in short, precise language with no fluff."
)

# --------------------------------------------------------------------------- #
# Helpers                                                                     #
# --------------------------------------------------------------------------- #
def chat(user_prompt: str) -> str:
    """Send a single-turn chat request to Ollama and return the assistant reply."""
    url = f"{OLLAMA_HOST}/api/chat"
    payload = {
        "model": MODEL_NAME,
        "stream": False,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt},
        ],
    }

    try:
        r = requests.post(url, json=payload, timeout=300)
    except requests.exceptions.RequestException as exc:
        sys.exit(f"[error] HTTP request failed: {exc}")

    if r.status_code != 200:
        sys.exit(f"[error] Ollama returned {r.status_code}: {r.text}")

    data = r.json()
    return data["message"]["content"].strip()

# --------------------------------------------------------------------------- #
# Main                                                                        #
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send a prompt to an Ollama model and print the response."
    )
    parser.add_argument("prompt", help="User prompt text (wrap in quotes).")
    args = parser.parse_args()

    reply = chat(args.prompt)
    print(reply)

if __name__ == "__main__":
    main()
```

Then change the file permissions to allow executing, and then run the script with a prompt:

```bash
chmod +x send_prompt.py
./send_prompt.py "List 3 use cases for local LLMs."
```

You should see the Llama3.2 response in the new terminal window now.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746910949196/a2cc42b1-d57d-491f-bd12-6601ef07bea7.png)

This allows you to prompt the model and receive responses *while staying at the main terminal*, where you can run other scripts.

Next, we need a way to create and update Markdown files from an API.

## Markdown CRUD with FastAPI

FastAPI is a framework for building APIs with Python. We can write a few functions for Markdown CRUD, and route them to HTTP methods like `POST => Create`, `PUT => Update`, and `Delete => Delete` .

Create a new script called app.py:

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import PlainTextResponse
import aiofiles
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

app = FastAPI()

@app.post("/files/{filename}")
async def create_file(filename: str, request: Request):
    path = DATA_DIR / filename
    if path.exists():
        raise HTTPException(status_code=400, detail="File already exists")
    body = await request.body()
    async with aiofiles.open(path, "wb") as f:
        await f.write(body)
    return {"status": "created", "filename": filename}

@app.get("/files/{filename}", response_class=PlainTextResponse)
async def read_file(filename: str):
    path = DATA_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Not found")
    async with aiofiles.open(path, "rb") as f:
        return await f.read()

@app.put("/files/{filename}")
async def update_file(filename: str, request: Request):
    path = DATA_DIR / filename
    body = await request.body()
    async with aiofiles.open(path, "wb") as f:
        await f.write(body)
    return {"status": "updated", "filename": filename}

@app.delete("/files/{filename}")
async def delete_file(filename: str):
    path = DATA_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="Not found")
    path.unlink()
    return {"status": "deleted", "filename": filename}
```

Save it in the project’s root folder, and then start up the server. Be sure to start the uvicorn server in the virtual environment.

```bash
pip install fastapi uvicorn aiofiles
.venv/bin/uvicorn app:app --reload
```

Next, test it out with a few different cUrl requests from the terminal.

```bash
curl -X POST http://localhost:8000/files/test.txt --data-binary "Hello"
curl http://localhost:8000/files/test.txt
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746912173429/6c2c4142-ffa3-40cf-9940-9bff8a05d89e.png)

Check your local folder and you should see the new file. Now try updating then deleting the file.

```bash
curl -X PUT http://localhost:8000/files/test.txt --data-binary "Updated"
curl -X DELETE http://localhost:8000/files/test.txt
```

Alright, now we just need to tie these two together.

## Saving LLM Responses to Markdown with Python

Add a `save_response()` function to the **send\_prompt.py** script, and update the `main()` function to call it after the LLM responds:

```python
def save_response(content: str, filename: str = "output.md") -> None:
    """Save the assistant's response to a Markdown file via local FastAPI endpoint."""
    url = f"http://localhost:8000/files/{filename}"
    try:
        r = requests.post(url, data=content.encode("utf-8"), timeout=10)
    except requests.exceptions.RequestException as exc:
        sys.exit(f"[error] Failed to save file: {exc}")

    if r.status_code != 200:
        sys.exit(f"[error] File save failed: {r.status_code} {r.text}")

    print(f"[saved] {filename}")

# --------------------------------------------------------------------------- #
# Main                                                                        #
# --------------------------------------------------------------------------- #
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Send a prompt to an Ollama model and print/save the response."
    )
    parser.add_argument("prompt", help="User prompt text (wrap in quotes).")
    parser.add_argument("--save", help="Filename to save output as .md", default=None)
    args = parser.parse_args()

    reply = chat(args.prompt)
    print(reply)

    if args.save:
        save_response(reply, args.save)

if __name__ == "__main__":
    main()
```

Save it and then test it out from the terminal. You should be able to send a prompt and save the response to a text or Markdown file.

```python
./send_prompt.py "Write a Markdown tutorial summary" --save tutorial.md
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746913221473/3dc1151c-f6b3-402f-a99f-6bd050775199.png)

Well look at that! A new tutorial.md Markdown file just appeared. The LLM response still shows in the terminal, but now it also gets saved to a text file if the `—save file_name.md` option is used. So you can chat with the LLM first and refine the prompt, then save the final version when you’re ready.

## Conclusion

Generating text with AI can easily be done on local hardware using Ollama. And with a little Python, you can save the LLM response to a local file, to avoid the copy/pasting and enable automations or bulk processing of prompts. From here you could integrate a file syncing tool, build a UI to upload files and send prompts, or set up an MCP client to add other features.