---
title: "Knowledge Graph Generator with Claude Desktop and Neo4j MCP"
date: 2025-06-09
permalink: "/knowledge-graph-generator-with-claude-desktop-and-neo4j-mcp/"
layout: "post"
excerpt: "Knowledge graphs are more than just interesting data visualizations. They’re also extremely effective as a data source for RAG (Retrieval-Augmented Generation), and can significantly improve LLM responses when compared to vector RAG. But building a q..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1749393402402/d4f8d4a9-a959-4d2c-9d75-d6642ad2191e.png"
readTime: 5
tags: ["Neo4j", "knowledge graph", "claude.ai", "#anthropic", "mcp server", "RAG ", "llm", "named entity recognition", "AI"]
series: "Artificial Intelligence"
---

Knowledge graphs are more than just interesting data visualizations. They’re also extremely effective as a data source for RAG (Retrieval-Augmented Generation), and can significantly improve LLM responses when compared to vector RAG. But building a quality knowledge graph requires careful planning of the ontology, or system of entities and relationships to extract.

AI tools like ChatGPT can help in parsing unstructured text and generating Cypher queries to insert the data into a graph database, but that still leaves you copying/pasting to run the queries. Fortunately, Neo4j recently released an MCP server, enabling AI agents to interact directly with the database.

In this guide, I’ll show you how to use Claude Desktop with the Neo4j MCP server on MacOS to automatically generate graphs from unstructured text.

**This guide will cover:**

* Deploying Neo4j locally with Docker
    
* Installing Claude Desktop
    
* Adding the Neo4j MCP Server
    
* Generating graphs from unstructured text

*Let’s get to it!*

## Deploying Neo4j Locally with Docker

Start out by installing [Docker Desktop](https://www.docker.com/products/docker-desktop/) if not already installed. Then open it and go to the Images section. Type `neo4j` in the search, then click **Run** on the top result.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1749307825004/594959c3-883b-4149-b686-19f52d0ad995.png)

Give the container a minute to start up, then select the **Containers** section on the left. Click `Show all ports` on the Neo4j container, then click to open the web console on [port 7474](http://localhost:7474/).

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1749308298439/fa7cd9a8-6c92-4649-bbd3-a0f16a46b168.png)

### Neo4j Dashboard

You’ll be prompted to login to the database and then change your password on first login. The default user name and password are both `neo4j`.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1749308464054/83d7d852-e4ce-4c1b-b2a0-aa9aa38cd7bb.png)

**Note**: The web interface runs on port 7474, but it uses port 7687 to connect to the database.

Click **Connect**, then run a query to create a few related nodes.

```plaintext
CREATE
  (bb:Show {title: "Breaking Bad"}),
  (crime:Genre {name: "Crime Drama"}),

  (walter:Character {name: "Walter White"}),
  (jesse:Character {name: "Jesse Pinkman"}),
  (skyler:Character {name: "Skyler White"}),
  (hank:Character {name: "Hank Schrader"}),

  (walter)-[:APPEARS_IN]->(bb),
  (jesse)-[:APPEARS_IN]->(bb),
  (skyler)-[:APPEARS_IN]->(bb),
  (hank)-[:APPEARS_IN]->(bb),

  (bb)-[:HAS_GENRE]->(crime),

  (walter)-[:PARTNER]->(jesse),
  (walter)-[:MARRIED_TO]->(skyler),
  (skyler)-[:SIBLING_IN_LAW]->(hank),
  (hank)-[:INVESTIGATES]->(walter);
```

You should see the new node and relationship types appear on the left sidebar. Now run a query to show all the nodes and relationships.

```plaintext
MATCH (n)-[r]->(m)
RETURN n, r, m
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1749309493119/91f82139-957c-4a92-b24a-a926c9129bb4.png)

Ok, Neo4j is up and running. Now clear out the database so we can start fresh in the next section.

```plaintext
MATCH (n) DETACH DELETE n
```

## Installing Claude Desktop

Next, install [Claude Desktop](https://claude.ai/download), open it and go to the **Settings**, then **Developer**. Then click **Edit Config**.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1749309770123/c5f96851-4d46-4de0-b416-a17ee202ef38.png)

## Adding the Neo4j MCP Server

Since Claude Desktop is running locally, we can connect to any local server also running on the same machine, without having to expose it to the internet.

That will open up the folder containing the `claude_desktop_config.json` file. Open it with any text editor, and paste in the MCP config from the [mcp-neo4j-cypher](https://pypi.org/project/mcp-neo4j-cypher/) server.

```json
{
  "mcpServers": {
    "neo4j-aura": {
      "command": "uvx",
      "args": [
        "mcp-neo4j-cypher@0.2.2",
        "--transport",
        "stdio"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USERNAME": "neo4j",
        "NEO4J_PASSWORD": "YOUR_PASSWORD",
        "NEO4J_DATABASE": "neo4j"
      }
    }
  }
}
```

Enter your Neo4j password in place of `YOUR_PASSWORD` and then save the file.

Next, install the uvx Python library if not already installed.

```bash
pip install --user pipx
pipx install uvx            
pipx ensurepath
```

This will allow Claude Desktop to communicate with the MCP server and Neo4j with the same environment.

If you have any issues (or you want to use an existing install of uvx), you may need to change `“command”: “uvx“` to *your path* for uvx. Run `which uvx` in the terminal to get the path, then replace “uvx” with the full path in the claude\_desktop\_config.json.

Lastly, restart Claude Desktop so the MCP server config changes can take effect. If you see an error about connecting to the MCP, try changing the “uvx” command to your path.

## Generating graphs from unstructured text

Ok, time to test it out. Claude Desktop should be able to access the Neo4j database now. Start a new chat and upload any text file that you want to turn into a graph. For this example, I’m using the text from the Wikipedia article on The Hitch Hiker’s Guide to the Galaxy.

Once the file is attached, ask Claude to create a Neo4j graph based on the entities and relationships in the document.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1749310973308/5c0dc616-8f5d-483f-83fc-9862e6b6a37f.png)

You should be prompted to approve permission for each function or tool in the Neo4j MCP server. You can *approve once*, or *approve all* so that it doesn’t have to ask every time.

Give it a few minutes, and you should see several queries ran during the chat.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1749311092403/bca7733f-23c9-48b6-bf11-24943cb9214f.png)

Now head back to Neo4j and refresh the dashboard. Then run a query to display all the nodes and edges.

```plaintext
MATCH (n)-[r]->(m)
RETURN n, r, m
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1749311179941/5602a5a2-97b5-4fd1-8aeb-40fbc3a61b19.png)

Look at that! A complete graph with multiple node and relationship types, complex, multi-hop relationships, and metadata, all generated from a simple prompt! And this is just a basic example. You can get more detailed with the prompt and relationships to extract, or use JSON or CSVs as input to build relationships based on foreign keys.

## Conclusion

Knowledge graphs are amazing tools for data visualization and RAG, but building them has traditionally been difficult and time-consuming. AI tools are becoming more useful for graph generation though, and now MCPs can be used to automate the entire process of NER (Named-Entity Recognition) data extraction, Cypher query writing, and running the actual queries. With just a simple prompt, you can now convert unstructured input data into a complex knowledge graphs in only a few seconds.