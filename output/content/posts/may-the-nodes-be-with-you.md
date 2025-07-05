---
title: "May the Nodes Be with You"
date: 2025-05-04
permalink: "/may-the-nodes-be-with-you/"
layout: "post"
excerpt: "Knowledge graphs are powerful tools to visualize and explore your data, and can help uncover new insights and patterns in how your data is related. They are easy to search and navigate, but getting your data into the graph database in the right forma..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1746150077731/71d015b3-4354-4934-83ba-ef5098e40faa.png"
readTime: 5
tags: ["may the 4th", "star wars day", "knowledge graph", "ontology", "Neo4j", "graph database", "obsidian", "JavaScript", "star wars", "cypher"]
---

{% raw %}
Knowledge graphs are powerful tools to visualize and explore your data, and can help uncover new insights and patterns in how your data is related. They are easy to search and navigate, but getting your data *into the graph database* in the right format can be challenging. And the resulting graph is only as good as the data— or as they say, garbage in, garbage out. So it’s important to define a good schema, or ontology, that describes the entities and relationships you want to extract from your data.

With unstructured text, you can use an LLM to extract entities and relationships, and then generate a Cypher query using the model ([guide](https://blog.greenflux.us/building-a-knowledge-graph-locally-with-neo4j-and-ollama)). This can take a lot of the work out of generating the Cypher queries but it comes with the risk of hallucinations, and the security and privacy concerns of sending your data to a 3rd party.

When working with structured data though, you can just write a function to map over the data and build the Cypher query programmatically, without the risk of hallucinations, or sharing your data with a 3rd party. With just a few lines of JavaScript, you can map over API responses and bulk insert data into a knowledge graph to use for exploring data visually, or building a RAG pipeline.

In this guide, we’ll be using the **Star Wars API** to fetch data about an episode, and all of the planets, star ships, vehicles and species mentioned in it. Then, we’ll map over that data to build a Cypher query, and run it to build a new graph.

**Topics Covered:**

* Using the Star Wars API
    
* Merging data from multiple endpoints with JavaScript
    
* Mapping the results to a Cypher query
    
* Running the query via Neo4j’s REST API

*Let’s get to it!*

## Using the Star Wars API

The original Star Wars API (swapi.co) was a free API with data on Star Wars characters, planets, ships, etc. It is no longer maintained, but a few newer API providers offer a similar service. For this guide, I’ll be using [swapi.info](https://swapi.info/). Just like the original API, swapi.info works without a login and is completely free to use.

Take a look at the JSON structure for a record from the [`/films`](https://swapi.info/api/films) endpoint.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746144140833/b50a8d3e-c3e7-4b30-b2da-24e72e53c7d8.png)

There’s a title, and a few other data points, and then arrays for `characters`, `planets`, `starships`, `vehicles`, and `species`. Each one of those array entries link to another endpoint, and record, with more details. We can use this data to build a knowledge graph by mapping over it and building a Cypher query to insert the data into Neo4j.

### Local Neo4j and Appsmith

For this guide, I’ll be using Neo4j as the graph database, and Appsmith to run the API calls and write the JavaScript. Check out this [tutorial](https://community.appsmith.com/tutorial/self-hosted-knowledge-graph-neo4j-and-appsmith) on how to deploy both in Docker, or you can use the cloud versions of Appsmith and Neo4j/AuraDB.

Alright, let’s graph the planets and species in the first 3 movies and see how they are related. Notice how in the JSON above, each related record is just a link, and doesn’t include the title or name of the entity. This means we’ll have to loop through all the related records to lookup the name or title before the graph can be built.

Normally I would use the REST API query in Appsmith, but in this case the looping can be handled nicely with `fetch()`, and a dynamic URL.

## Merging data from multiple endpoints with JavaScript

In Appsmith, create a new JSObject named `SWAPI` and paste in the following:

```javascript
export default {
  filmData: [],

  async loadFilms() {
    const base = 'https://swapi.info/api';
    const fetchJson = async url => {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`Failed to fetch ${url}`);
      return res.json();
    };

    const rawFilms = await Promise.all(
      [1, 2, 3].map(id => fetchJson(`${base}/films/${id}`))
    );
    const planetUrls = [...new Set(rawFilms.flatMap(f => f.planets))];
    const speciesUrls = [...new Set(rawFilms.flatMap(f => f.species))];

    const [planetObjs, speciesObjs] = await Promise.all([
      Promise.all(planetUrls.map(fetchJson)),
      Promise.all(speciesUrls.map(fetchJson))
    ]);
    const planetMap = new Map(planetObjs.map(p => [p.url, p.name]));
    const speciesMap = new Map(speciesObjs.map(s => [s.url, s.name]));

    this.filmData = rawFilms.map(f => ({
      episode_id: f.episode_id,
      title:      f.title,
      planets:    f.planets.map(url => planetMap.get(url)),
      species:    f.species.map(url => speciesMap.get(url))
    }));
    return this.filmData;
  }
}
```

This loops over each related endpoint and returns a new films object with the actual names/titles of the related entities, instead of the URL.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746360424377/168d6859-25cc-452f-bd89-6610e3b24f10.png)

Ok, now that we have all the names, we can loop over all the child arrays and generate a Cypher query.

## Mapping the results to a Cypher query

The most important step in building a knowledge graph is planning out an ontology, or schema for the entities and relationships you want to represent. For this example, I’ll be representing the first 3 films (episodes 4-6), and a portion of the planets and species, to limit the graph size to 20 nodes.

Add a new function to the JSObject to map the `filmData` to a Cypher query.

```javascript
  generate20NodeGraphRequest(data = this.filmData) {
    const films      = data;
    const allPlanets = [...new Set(films.flatMap(f => f.planets))];
    const allSpecies = [...new Set(films.flatMap(f => f.species))];

    // allocate 20 nodes: 3 films + X planets + Y species = 20
    let remaining = 20 - films.length;       // 17
    const planets = allPlanets.slice(0, remaining);
    remaining   -= planets.length;           // leftover for species
    const species = allSpecies.slice(0, remaining);

    const cypher = `
UNWIND $films AS filmObj
WITH filmObj

MERGE (f:Film {episode_id: filmObj.episode_id, title: filmObj.title})

WITH filmObj, f

CALL {
  WITH filmObj, f
  UNWIND filmObj.planets AS pname
  WITH f, pname
  WHERE pname IN $planets
  MERGE (p:Planet {name: pname})
  MERGE (p)-[:FEATURED_IN]->(f)
  RETURN COUNT(*) AS planetCount
}

CALL {
  WITH filmObj, f
  UNWIND filmObj.species AS spname
  WITH f, spname
  WHERE spname IN $species
  MERGE (s:Species {name: spname})
  MERGE (s)-[:FEATURED_IN]->(f)
  RETURN COUNT(*) AS speciesCount
}

RETURN f
`.trim();

    return {
      statements: [{
        statement:  cypher,
        parameters: { films, planets, species }
      }]
    };
  }
```

This uses the `MERGE` command to *create-or-update* the entities, and avoid duplicates. Each name or title is mapped into an array, and then turned into multiple records using `UNWIND` in the Cypher query.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746360673788/325aaa4c-26f9-4424-bf0c-6619cf6d7683.png)

## Running the query via Neo4j’s REST API

Ok, we have a Cypher query built from the Star Wars API data. Next, let’s add an API to insert the data into Neo4j.

Once you have Neo4j running locally in Docker, create a new API in Appsmith to run a Cypher query.

| Name | RunCypher |
| --- | --- |
| Method | POST |
| URL | http://host.docker.internal/7474/db/neo4j/tx/commit |
| Body type | JSON |
| Body | {{ SWAPI.generate20NodeGraphRequest.data }} |

Then click the **Save URL** button to save the credentials to an Appsmith datasource.

Choose *Basic* for the **Authentication type**, and then enter your Neo4j user name and password, then click **Save**.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746315921720/375880ab-abdc-46d6-83ae-1ec9d2ffbfe1.png)

This will keep the credentials on the Appsmith server instead of in the app itself.

Since we’re using Docker to run both Neo4j and Appsmith locally, the `localhost` URLs are replaced with `host.docker.internal`.

Run the query in Appsmith, and then open the Neo4j dashboard.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746361254617/4d1a11c8-b8d1-4fc0-92a4-fa86bad9534c.png)

In Neo4j, select all the nodes and relationships by running the query:

```sql
MATCH p=()-[]->() RETURN p
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746360808779/b8e96d7d-888e-4aa1-86a9-9c271b1e68e8.png)

![](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjk5Z3BrMjJ6d2ZhMWZqNWw0NXk2amN5MGRsYjc1aGhlNnd3OW1vMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ZwxpIHk5LutMc/giphy.gif)

Nice! Now we can easily see how all the planets and characters relate back to each movie. Or we can query the graph to answer questions like:

> Which species appeared in all 3 films?

```sql
MATCH (s:Species)-[:FEATURED_IN]->(f:Film)
WHERE f.episode_id IN [4,5,6]
WITH s, count(DISTINCT f) AS appearances
WHERE appearances = 3
RETURN s.name AS Species
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746361497700/1b935c9b-599e-4974-be22-8eee33bcfd03.png)

![Video gif. C3PO dances jerkily before we cut to R2D2 gliding our way.](https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExemd0cGg4Nzl0emZwb25jNGUzNjk3ODU5d2FoMTJmamdhaWZkOW5maiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/3oOWASkCzFuP6/200.gif)

From here, you can use the Neo4j browser to explore the data, or query Neo4j via the API has part of a RAG pipeline.

## Conclusion

It can be tempting to use LLMs to generate Cypher queries to insert graph data, but that comes with inherent risks of hallucination, and potential security and privacy issues. When working with structured data like JSON or SQL, you can map over the data using JavaScript to build the Cypher query programmatically, avoiding the risks of using an LLM to generate the query.

This allows you to build knowledge graphs with clearly defined relationships and a more repeatable structure than using LLMs to generate Cypher queries. With a little planning and a few lines of code, you can easily convert structured data into interactive knowledge graphs.
{% endraw %}