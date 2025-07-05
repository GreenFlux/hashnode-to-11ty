---
title: "Building a Knowledge Graph Locally with Neo4j & Ollama"
date: 2025-04-21
permalink: "/building-a-knowledge-graph-locally-with-neo4j-and-ollama/"
layout: "post"
excerpt: "Knowledge graphs, also known as semantic networks, are a specialized application of graph databases used to store information about entities (person, location, organization, etc) and their relationships. They allow you to explore your data with an in..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1745228584010/fca4d5d3-a89d-4467-9b81-ba978113fb87.png"
readTime: 5
tags: ["Neo4j", "graph database", "knowledge graph", "Python", "Python 3", "huggingface", "llm", "cypher", "macOS", "obsidian", "ollama", "ontology"]
---

{% raw %}
Knowledge graphs, also known as semantic networks, are a specialized application of graph databases used to store information about entities (person, location, organization, etc) and their relationships. They allow you to explore your data with an interactive network graph, and perform complex queries that would be difficult or impossible with SQL. Knowledge graphs are often used in fraud detection, social networks, recommendation engines, and RAG (retrieval-augmented generation).

Traditionally, building a knowledge graph has involved extensive work in preprocessing the input data, carefully extracting and labeling entities and relationships based on an ontology, or schema that defines the types of data to extract. But LLMs have enabled this process to be automated, allowing large datasets to be processed into knowledge graphs quickly and easily.

In this guide, we’ll be building a knowledge graph locally using a text-to-cypher model from Hugging Face, Neo4j to store and display the graph data, and Python to interact with the model and Neo4j API. This tutorial is for Mac, but Docker, Ollama and Python can all be used on Windows or Linux as well.

**This guide will cover:**

* Deploying Neo4j locally with Docker
    
* Downloading a model from HuggingFace and creating a Modelfile for Ollama
    
* Running the model with Ollama
    
* Prompting the model from a Python script
    
* Bulk processing local files into a knowledge graph

**Let’s get started!**

## Deploying Neo4j locally with Docker

Install Docker, then open it up and enter Neo4j in the search bar. Click **Run** on the top result with the ‘Docker Official Image’ badge.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745074175948/5aa90e2a-f7da-4322-93af-a34f400912ac.png)

You should see the image download and the container start up. Select the container and click the link or open [`http://localhost:7474/`](http://localhost:7474/) in the browser.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745074423486/7991504d-3cca-4bae-a841-6cdb3eff37d3.png)

Next you should see a login screen for Neo4j. The user name and password are both `neo4j`. There’s also a preview of their newer browser tool (shown below). You may see an older login screen first, then an option to try the new browser. Login on the first screen, set a new password, then choose the option to try the new browser.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745074507506/d7ecad0a-2508-4c86-adfa-964280d88daf.png)

**Note**: The browser UI serves on port 7474, but it connects to the Neo4j database instance on port 7687.

Once logged in, you’ll see a command line input to run Cypher queries, similar to SQL queries, to search and manage data in the graph. Paste in the following query and run it.

```plaintext
CREATE 
  (sisko:Character {name: "Benjamin Sisko", rank: "Captain", species: "Human"}),
  (kira:Character {name: "Kira Nerys", rank: "Major", species: "Bajoran"}),
  (odo:Character {name: "Odo", rank: "Constable", species: "Changeling"}),
  (jake:Character {name: "Jake Sisko", rank: "Civilian", species: "Human"}),
  (nog:Character {name: "Nog", rank: "Ensign", species: "Ferengi"}),

  (kira)-[:SERVES_WITH]->(sisko),
  (odo)-[:SERVES_WITH]->(sisko),
  (jake)-[:RELATED_TO]->(sisko),

  (nog)-[:FRIEND_OF]->(jake)
```

**Run** the query, then click the **(\*)** button under Relationships to view the graph.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745074934768/5161b219-a6c5-4267-8f09-a9d660a0a115.png)

Ok, we have Neo4j running locally and can create a graph. Next we need a way to generate Cypher queries. You could just ask ChatGPT, but there are several fine-tuned models on Hugging Face that are made for text-to-cypher generation. We’ll use Ollama to run one of these models locally so there’s no subscription cost, no internet required (after download), and no privacy or security concerns with sending data to a 3rd party.

But first, let’s clear out the test query we ran earlier. Run the following command to purge the database.

```plaintext
MATCH (n)
DETACH DELETE n
```

## Installing Ollama and Downloading a Model

Next, download and install [Ollama](https://ollama.com/), then run it. You should see a Llama icon in the menu bar once it’s running. The only option is `quit Ollama`. Everything else is done through the terminal.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745077078924/66ffc603-dcd5-41f5-aec6-7d888943231c.png)

Now we’ll download one of the models hosted by Ollama to test it out before trying the model from Hugging Face. This will create a Modelfile that we can use as a template, and edit it to run the Hugging Face model in Ollama.

Run the following command:

```bash
ollama run llama3.2
```

You’ll see several files download, then a message from the model asking you to send a message.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745077883623/f60d33c8-0a75-48fd-96a5-186232576d99.png)

You should be able to chat with the Llama3.2 model from the terminal now. Enter a prompt to test it out.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745077987624/b288fb35-f349-4630-8ab6-bfc171166db7.png)

Now type `/bye` to exit the model and return to the terminal.

Next, we need to copy the existing Modelfile to use as a template.

Run the following command:

```bash
ollama show --modelfile llama3.2
```

Scroll up and find the line that starts with `FROM /Users/{YOUR_USER_NAME}/.ollama/models/blobs`

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745078413277/037d5316-3fff-4049-a464-d60a51d6eebc.png)

This contains the blob reference that will be used in the next section to build our own Modelfile. Copy this line to a new text file. Then save the file in a new folder to use for this project. Name the file Modelfile (no extension) and save it to the new folder. For this guide, I’m naming my folder **Neo4j**.

## Downloading a model from Hugging Face and creating a Modelfile for Ollama

Next, we’ll be using the [neo4j/text2cypher-gemma-2-9b-it-finetuned-2024v1](https://huggingface.co/neo4j/text2cypher-gemma-2-9b-it-finetuned-2024v1) model from Hugging Face, and cloning the repo locally. Start by opening the new Neo4j folder in the terminal.

Hugging Face suggests using [Git Large File Storage (LFS)](https://git-lfs.com/) to clone the repo and minimize the download size by keeping larger files on the server. You can install it with `brew install git-lfs` if you have [Homebrew](https://brew.sh/) installed, or download the installer from their [website](https://git-lfs.com/).

Once **git-lfs** is installed, run:

```bash
git lfs install

git clone https://huggingface.co/neo4j/text2cypher-gemma-2-9b-it-finetuned-2024v1
```

You should see the repo downloaded as a new folder in the current directory.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745078920274/5988fc13-7c57-4130-88a5-0e38f27dc819.png)

Next, we need to update the Modelfile to tell Ollama how to build and serve our model, since this is a Hugging Face model, and not one hosted by Ollama.

Keep the `FROM /Users/…` line at the top, and then add the remaining text like the sample below, then save the Modelfile.

```plaintext
FROM /Users/greenflux/.ollama/models/blobs/sha256-YOUR-SHA-KEY
TEMPLATE "{{ if .System }}<|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"
PARAMETER stop <|start_header_id|>
PARAMETER stop <|end_header_id|>
PARAMETER stop <|eot_id|>
```

Ok, we have Ollama downloaded and running, the HF model cloned locally, and a Modelfile to tell Ollama how to use it. We’re now ready to run the model.

## Running the model with Ollama

Next, run:

```plaintext
ollama create text2cypher -f Modelfile
```

This tells Ollama to create a new model named *text2cypher*, using the settings in our Modelfile. You should see a few operations in the terminal, followed by a success message.

Next, run:

```plaintext
ollama run text2cypher
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745079420160/2947dbdd-a9d2-4e6a-845d-d4e9a55110e3.png)

You should see the `Send a message` prompt again, but this time we’re using the text2cypher model from Hugging Face. This model is fine-tuned to create Cypher queries. It works best when you provide it with the schema of your knowledge graph so that the generated query is limited to the entities and relationships you want in your graph.

When building a new graph, you can decide on your schema first, then provide that with the prompt to generate a CREATE query to insert the new data. And to search an existing graph, just provide it with the schema and a text description of the search.

Here are a prompt you can try out:

```plaintext
Node types:
- Character(name, rank, species)
- Station(name, location)
- Relationships:
    - ASSIGNED_TO (Character → Station)
    - ALLIES_WITH (Character ↔ Character)

Write a Cypher query to create the following data:
- Commander Benjamin Sisko, a Human, is assigned to Deep Space Nine (orbiting Bajor).
- Major Kira Nerys, a Bajoran, is also assigned to Deep Space Nine.
- Odo, a Changeling, serves as chief of security on the station.
- Jadzia Dax, a Trill, is friends with Sisko and works as the station's science officer.
- Quark, a Ferengi, is not part of the crew but owns a bar on the station and is friends with Odo.
```

This tells the model what schema to use, then provides a few lines of text data to extract entities and relationships from. The response should be a Cypher CREATE query like this:

```plaintext
CREATE (s:Character {name: "Benjamin Sisko", rank: "Commander", species: "Human"})
CREATE (d:Station {name: "Deep Space Nine", location: "orbiting Bajor"})
CREATE (s)-[:ASSIGNED_TO]->(d)

CREATE (k:Character {name: "Kira Nerys", rank: "Major", species: "Bajoran"})
CREATE (k)-[:ASSIGNED_TO]->(d)

CREATE (o:Character {name: "Odo", rank: "Chief of Security", species: "Changeling"})
CREATE (o)-[:ASSIGNED_TO]->(d)

CREATE (j:Character {name: "Jadzia Dax", rank: "Science Officer", species: "Trill"})
CREATE (j)-[:ALLIES_WITH]->(s)
CREATE (s)-[:ALLIES_WITH]->(o)

CREATE (q:Character {name: "Quark", rank: "", species: "Ferengi"})
CREATE (q)-[:OWNS_BAR_ON]->(d)
CREATE (o)-[:ALLIES_WITH]->(q)
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745080054466/96de170b-6fbb-48f3-a3c4-94f21583fb5f.png)

Now go back to Neo4j and run the query. Then click the (\*) again to view the new graph.

**Note**: You may have to remove the inline `//comments` for the query to run.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745080361233/6cfbc00e-5e63-4a9b-bb61-80466f1ef0a7.png)

Ok, now we’re able to generate Cypher queries from a text prompt. Lastly, let’s write a Python script to bulk process text files into Cypher queries and insert the data into our graph.

## Prompting the model from a Python script

Next, open up your favorite text editor or IDE and create a python script to send prompts to Ollama. This script takes a text parameter for the prompt and will return the LLM response in the terminal.

```python
import requests
import argparse

# Static schema
schema = """
Node types:
- Character(name, rank, species)
- Ship(name, class)
- Relationships:
    - SERVES_ON (Character → Ship)
    - FRIENDS_WITH (Character ↔ Character)
"""

# Parse CLI arguments
parser = argparse.ArgumentParser(description="Send prompt to Ollama text2cypher model")
parser.add_argument("prompt", type=str, help="Prompt text to send (wrap in quotes)")
args = parser.parse_args()

# Ollama local model endpoint
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "text2cypher"

# Build request payload
payload = {
    "model": MODEL_NAME,
    "prompt": f"{schema}\n\nQuestion: {args.prompt}\n\nReturn only a valid Cypher query.",
    "stream": False
}

# Send request
response = requests.post(OLLAMA_URL, json=payload)
response.raise_for_status()

# Print result
cypher = response.json().get("response")
print("Generated Cypher Query:\n", cypher)
```

Save the script to the Neo4j folder and name it *send\_prompt.py*. Then create a virtual environment and run it.

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

```bash
pip install requests
```

You should now be able to prompt the text2cypher model from the terminal using:

```bash
python3 send_prompt.py "Create nodes for Captain Jean-Luc Picard (Human), Lieutenant Worf (Klingon), and Counselor Deanna Troi (Betazoid). All of them serve on the USS Enterprise (Galaxy-class). Worf and Troi are friends."
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745085175389/4d0faa99-9bf0-442d-bd12-8842fb07dd41.png)

Alright, the Python script can return a Cypher query. Now let’s update it to run that query in Neo4j.

## Bulk processing local files into a knowledge graph

Start out by creating a new script called run\_cypher.py in the Neo4j folder. Paste in the following script and save. Be sure to update it with your password at the top of the script.

```python
# run_cypher.py
import argparse
from neo4j import GraphDatabase

# --- Configuration ---
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "YOUR_PASSWORD"

# --- Parse CLI Argument ---
parser = argparse.ArgumentParser(description="Run a Cypher query on Neo4j")
parser.add_argument("query", type=str, help="Cypher query to run (wrap in quotes)")
args = parser.parse_args()
cypher_query = args.query.strip()

# --- Run Cypher Query ---
def run_query(query):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session(database="neo4j") as session:
        try:
            result = session.run(query)
            # Collect results first before consuming
            records = list(result)
            summary = result.consume()
            print("Query executed. Stats:", summary.counters)
            for record in records:
                print(record.data())
        except Exception as e:
            print("Cypher execution error:", str(e))
    driver.close()

run_query(cypher_query)
```

Next, install the Neo4j driver:

```bash
pip install neo4j
```

Then run the script with a prompt containing a Cypher query.

```bash
python run_cypher.py "CREATE (sisko:Character {name: 'Benjamin Sisko', rank: 'Captain', species: 'Human'}), (kira:Character {name: 'Kira Nerys', rank: 'Colonel', species: 'Bajoran'}), (bashir:Character {name: 'Julian Bashir', rank: 'Doctor', species: 'Human'}), (defiant:Ship {name: 'USS Defiant', class: 'Defiant-class'}), (sisko)-[:SERVES_ON]->(defiant), (kira)-[:SERVES_ON]->(defiant), (bashir)-[:SERVES_ON]->(defiant), (sisko)-[:FRIENDS_WITH]->(kira), (bashir)-[:FRIENDS_WITH]->(sisko)"
```

Refresh the Neo4j browser, and you should see the new nodes created.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745087413634/4dbea19f-51e9-4d4f-9f92-71fe3a7ca24f.png)

Now delete all the nodes one last time before the bulk upload.

```plaintext
MATCH (n)
DETACH DELETE n
```

### Bulk Processing Text Files

Ok, we’re almost there! Lastly, we need a script to process a folder of text files, and call both of these scripts to generate a cypher then run it. For this example, I’m using 3 text files located in a *Notes* folder, inside the neo4j folder.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745087720620/06e4cbc9-80aa-4721-a222-6314cff5727a.png)

Here’s the files I used, in case you want to test with the same input data.

**prompt1.txt**

```plaintext
Captain Benjamin Sisko entered the operations center on Deep Space Nine and found Major Kira Nerys consulting with Constable Odo. The captain outlined a new security protocol and asked Kira to oversee its implementation. Odo adjusted his uniform and nodded as he scanned incoming reports. Kira offered suggestions for patrol routes while Odo confirmed gate readings. By the end of the briefing, all three had agreed on the plan to increase boarding inspections and monitor cargo manifests more closely.
```

**prompt2.txt**

```plaintext
Later that morning, Kira Nerys joined Science Officer Jadzia Dax in the lab for an experimental sensor test. Dr Julian Bashir arrived with new calibration data from Starfleet Medical. As Jadzia calibrated the particle analyzer, Kira reviewed station logs for unusual energy signatures. Julian smiled at their progress and noted that the anomaly readings matched a pattern he had seen during his medical travels. Together they prepared to present their findings to Captain Sisko before the next scheduled docking.
```

**prompt3.txt**

```plaintext
That evening, Jadzia Dax walked through the promenade to visit the bar run by Quark. She found Nog polishing glasses behind the counter. Quark greeted her with a nod and gestured toward a table near the entrance. Nog filled a fresh glass of synthehol while Jadzia described the sensor anomaly discovered earlier. Quark leaned forward, offering to check his Ferengi data logs for any related transactions. Nog made a note to share the information with Dr Bashir first thing tomorrow.
```

Create one last script to loop over the Notes folder. This script will call the `send_prompt.py` and `run_cypher.py` scripts for each file in the Notes folder.

**Note**: I had to do a bit of cleanup on the response to get only the valid Cypher CREATE queries. The model was wrapping the response with ` ``` `, but not consistently. And occasionally it would add extra text at the beginning, like `Generated Cypher Query:`. So the script is a little long on the text parsing, but the main logic for looping and running the other scripts is pretty straight-forward.

```python
#!/usr/bin/env python3
import os
import re
import subprocess
import argparse

# Configuration
NOTES_DIR = "Notes"         # directory containing .txt files
SEND_PROMPT_SCRIPT = "send_prompt.py"
RUN_CYPHER_SCRIPT = "run_cypher.py"

def extract_character_ship_info(output):
    """Extract Character and Ship information from the output."""
    characters = []
    ships = []
    relationships = []
    in_code_block = False
    
    for line in output.strip().splitlines():
        line = line.strip()
        
        # Handle code blocks and filtering
        if line.startswith("```"):
            in_code_block = not in_code_block
            continue
        if line.lower().startswith("here are") or not line or not line.upper().startswith("CREATE "):
            continue
        
        # Ensure statement ends with semicolon
        if not line.endswith(";"):
            line += ";"
            
        # Extract character creation
        character_match = re.search(r'CREATE\s+\((\w+):Character\s+\{(.+?)\}\)', line)
        if character_match:
            alias = character_match.group(1)
            props_str = character_match.group(2)
            
            # Extract properties
            name_match = re.search(r'name:\s*"([^"]+)"', props_str)
            rank_match = re.search(r'rank:\s*"([^"]*)"', props_str)
            species_match = re.search(r'species:\s*"([^"]+)"', props_str)
            
            if name_match:
                name = name_match.group(1)
                rank = rank_match.group(1) if rank_match else ""
                species = species_match.group(1) if species_match else "Unknown"
                
                characters.append({
                    "alias": alias,
                    "name": name,
                    "rank": rank,
                    "species": species
                })
            continue
                
        # Extract ship creation
        ship_match = re.search(r'CREATE\s+\((\w+):Ship\s+\{(.+?)\}\)', line)
        if ship_match:
            alias = ship_match.group(1)
            props_str = ship_match.group(2)
            
            # Extract properties
            name_match = re.search(r'name:\s*"([^"]+)"', props_str)
            class_match = re.search(r'class:\s*"([^"]*)"', props_str)
            
            if name_match:
                name = name_match.group(1)
                ship_class = class_match.group(1) if class_match else "Unknown"
                
                ships.append({
                    "alias": alias,
                    "name": name,
                    "class": ship_class
                })
            continue
        
        # Extract relationships
        rel_match = re.search(r'CREATE\s+\((\w+)\)-\[:(\w+)\]->\((\w+)\)', line)
        if rel_match:
            source_alias = rel_match.group(1)
            rel_type = rel_match.group(2)
            target_alias = rel_match.group(3)
            
            if rel_type in ["SERVES_ON", "FRIENDS_WITH", "OWNED_BY"]:
                relationships.append({
                    "source": source_alias,
                    "type": rel_type,
                    "target": target_alias
                })
    
    return characters, ships, relationships

def process_file(file_path, send_script, run_script):
    """Process a single text file, extract entities and create database entries."""
    # Read the prompt file
    with open(file_path, "r", encoding="utf-8") as f:
        prompt = f.read().strip()
    
    # Generate Cypher from text using send_prompt.py
    result = subprocess.run(
        ["python3", send_script, prompt],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"[Error] {result.stderr.strip()}")
        return
    
    # Extract entity information
    characters, ships, relationships = extract_character_ship_info(result.stdout)
    
    # Create Characters
    if characters:
        print(f"Creating {len(characters)} Character nodes:")
        for char in characters:
            # MERGE ensures we don't create duplicates
            cypher = f"""
            MERGE (c:Character {{name: "{char['name']}"}})
            ON CREATE SET 
                c.species = "{char['species']}",
                c.rank = "{char['rank']}"
            RETURN c
            """
            
            print(f"Creating character: {char['name']}")
            cypher_result = subprocess.run(
                ["python3", run_script, cypher],
                capture_output=True,
                text=True
            )
            
            if "error" in cypher_result.stdout.lower() or "error" in cypher_result.stderr.lower():
                print(f"[Error] {cypher_result.stderr.strip() or cypher_result.stdout.strip()}")
    
    # Create Ships
    if ships:
        print(f"Creating {len(ships)} Ship nodes:")
        for ship in ships:
            # MERGE ensures we don't create duplicates
            cypher = f"""
            MERGE (s:Ship {{name: "{ship['name']}"}})
            ON CREATE SET 
                s.class = "{ship['class']}"
            RETURN s
            """
            
            print(f"Creating ship: {ship['name']}")
            cypher_result = subprocess.run(
                ["python3", run_script, cypher],
                capture_output=True,
                text=True
            )
            
            if "error" in cypher_result.stdout.lower() or "error" in cypher_result.stderr.lower():
                print(f"[Error] {cypher_result.stderr.strip() or cypher_result.stdout.strip()}")
    
    # Create Relationships
    if relationships:
        print(f"Creating {len(relationships)} relationships:")
        for rel in relationships:
            # Find the actual character/ship entities from the lists
            source_type = "Character"  # Default assumption
            source_name = None
            
            # Look for source in characters
            for char in characters:
                if char["alias"] == rel["source"]:
                    source_name = char["name"]
                    break
            
            # If not found in characters, check ships
            if not source_name:
                for ship in ships:
                    if ship["alias"] == rel["source"]:
                        source_type = "Ship"
                        source_name = ship["name"]
                        break
            
            # If still not found, skip this relationship
            if not source_name:
                print(f"Skipping relationship: source alias '{rel['source']}' not found")
                continue
            
            # Now find the target
            target_type = "Character"  # Default assumption 
            target_name = None
            
            # For SERVES_ON, target should be a Ship
            if rel["type"] == "SERVES_ON":
                target_type = "Ship"
                for ship in ships:
                    if ship["alias"] == rel["target"]:
                        target_name = ship["name"]
                        break
            else:
                # For other relationships, look for target in characters
                for char in characters:
                    if char["alias"] == rel["target"]:
                        target_name = char["name"]
                        break
            
            # If target not found, skip
            if not target_name:
                print(f"Skipping relationship: target alias '{rel['target']}' not found")
                continue
            
            # Create the relationship using MATCH to find existing nodes
            cypher = f"""
            MATCH (a:{source_type} {{name: "{source_name}"}})
            MATCH (b:{target_type} {{name: "{target_name}"}})
            MERGE (a)-[r:{rel['type']}]->(b)
            RETURN a, r, b
            """
            
            print(f"Creating relationship: {source_name} -[{rel['type']}]-> {target_name}")
            cypher_result = subprocess.run(
                ["python3", run_script, cypher],
                capture_output=True,
                text=True
            )
            
            if "error" in cypher_result.stdout.lower() or "error" in cypher_result.stderr.lower():
                print(f"[Error] {cypher_result.stderr.strip() or cypher_result.stdout.strip()}")

def main():
    parser = argparse.ArgumentParser(
        description="Bulk-process text files: extract entities and create properly connected Neo4j graph"
    )
    parser.add_argument(
        "--notes-dir",
        default=NOTES_DIR,
        help="Path to folder containing text files (default: %(default)s)"
    )
    parser.add_argument(
        "--script",
        default=SEND_PROMPT_SCRIPT,
        help="Path to send_prompt.py (default: %(default)s)"
    )
    parser.add_argument(
        "--run-script",
        default=RUN_CYPHER_SCRIPT,
        help="Path to run_cypher.py (default: %(default)s)"
    )
    args = parser.parse_args()

    for fname in sorted(os.listdir(args.notes_dir)):
        if not fname.lower().endswith(".txt"):
            continue
        
        path = os.path.join(args.notes_dir, fname)
        print(f"--- Processing {fname} ---")
        
        process_file(path, args.script, args.run_script)
        print()  # blank line between files

if __name__ == "__main__":
    main()
```

Save the script, then clear out the database once more before testing.

```plaintext
MATCH (n) DETACH DELETE n
```

Then retest:

```python
python bulk_process.py
```

Refresh Neo4j and you should see a new set of connected nodes based on your input documents. To view all the nodes and relationships at once, run:

```plaintext
MATCH (n)
OPTIONAL MATCH (n)-[r]->(m)
RETURN n, r, m
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745149748625/16a7bebb-0fff-4069-a38e-40193b3ef6a7.png)

And there you have it! You can now extract entities and relationships, generate Cypher queries and run them in bulk, based on a folder of text files. This will generate a collection of connected nodes based on the schema defined in your `send_prompt.py` script.

Crafting an appropriate schema for your input data is one of the most important steps to generating a quality knowledge graph. Be sure to create a well-defined schema that accurately represents your data before bulk-processing your files.

## Conclusion

Knowledge graphs are amazing tools for visualizing data and performing complex queries to uncover new insights about relationships. They excel at tasks in fraud detection, recommendation engines, social networks, and RAG. Building a knowledge graph is as easy as running a few Cypher queries, but generating those queries from data can be challenging. This guide has shown one way you can generate these queries locally using a text-to-cypher query from Hugging Face.

Special thanks to Jason Koo from Neo4j for this excellent [video tutorial](https://www.youtube.com/watch?v=9pdxSlxfqNY) on using a Hugging Face model in Ollama.

### What’s Next?

From here you could connect the Neo4j database to an AI assistant or agent to perform RAG, or use the graph to discover relationships and communities of nodes that emerge as the bulk data is processed.
{% endraw %}