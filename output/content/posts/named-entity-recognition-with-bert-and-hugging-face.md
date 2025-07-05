---
title: "Named Entity Recognition with BERT and Hugging Face 🤗"
date: 2025-03-17
permalink: "/named-entity-recognition-with-bert-and-hugging-face/"
layout: "post"
excerpt: "What is NER (Named Entity Recognition)?
Named Entity Recognition is a technique in Natural Language Processing (NLP), which involves identifying and classifying entities—such as names of people, organizations, locations, dates, and numerical values—w..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1742040197681/d61321ec-9deb-4d30-8bbd-09df008439fb.png"
readTime: 5
tags: ["NER", "BERT", "nlp", "nlp transformers", "llm", "knowledge graph", "named entity recognition", "unstructured data", "huggingface"]
series: "Artificial Intelligence"
---

{% raw %}
## What is NER (Named Entity Recognition)?

*Named Entity Recognition* is a technique in Natural Language Processing (NLP), which involves identifying and classifying entities—such as names of people, organizations, locations, dates, and numerical values—within unstructured text. This process transforms raw text into structured data, enhancing information retrieval, content categorization, and the functionality of applications like email, document editors, search engines and chatbots. Once the structured data is extracted, it can be used to create tags, knowledge graphs, or metadata, or to trigger automations.

In this guide, we’ll cover the basics of NER, and how to use it to extract structured data from your own documents. From there you can trigger automations based on the extracted data, update records with metadata, or send the data to a human-reviewer before triggering a workflow.

**This guide will cover:**

* History of NER and use cases
    
* BERT Model for NER
    
* Hugging Face Platform for Model Hosting
    
* Connecting to Models in Hugging Face from Appsmith
    
* Extracting Data from Local Files with NER/BERT

## A Brief History of NER

Rule-Based NER has been around since the **1990’s** with email applications and document editors detecting email addresses, names, dates, etc. These approaches use REGEX, dictionaries, and other text-parsing rules to match predefined patterns. Then in the **2000’s**, search engines like Google began to use machine-learning NER with knowledge graphs to store data extracted from web pages, and enhance search results. In the **2010’s** we saw Siri and Alexa using NER to interpret voice commands. And now in the **2020’s**, NER has become a key component of tagging, metadata, and Retrieval-Augmented Generation Pipelines.

The tools for performing NER have advanced significantly with the rise of large language models and transformers. And with these new tools, you can automate NER tasks that enrich data in your RAG pipeline, generate knowledge graphs for GraphRAG, or power automations and agents.

## Who’s BERT?

BERT, (Bidirectional Encoder Representations from Transformers), is an open-source machine learning framework for natural language processing developed by Google in 2018. Designed to help computers understand the meaning of ambiguous language in text by using surrounding text to establish context, BERT marked a significant advancement in NLP. Unlike traditional models that read text sequentially, BERT reads entire sequences of words simultaneously, allowing it to grasp context and nuance more effectively. This bidirectional approach enables BERT to achieve state-of-the-art performance on various NLP tasks, including Named Entity Recognition, by considering both preceding and following words in a sentence.

### Fine-Tuned Models for Specialized Fields

Since BERT Is open-source, anyone can modify it and fine-tune a specialized version for specific domains. There are several popular variants already published, like:

| **Specialized Models** | **Reasoning** | **Domains** |
| --- | --- | --- |
| **BioBERT** | Optimized for biomedical NER, clinical entities extraction. | Biomedical / Clinical |
| **SciBERT** | Optimized for extracting entities from scientific texts. | Scientific / Research Papers |
| **CamemBERT** | NER for French-language corpora. | General French NER |
| **LegalBERT** | Specialized for legal-domain entity extraction. | Legal texts |
| **mBERT** | Multilingual entity extraction across various languages. | Multilingual / Cross-lingual |
| **RoBERTa** | General-purpose, improved accuracy, robust for general NER. | General English |

In this guide, I’ll be using [`bert-large-cased-finetuned-conll03-english`](https://huggingface.co/dbmdz/bert-large-cased-finetuned-conll03-english), a model that’s fine-tuned for NER using the [conll2003](https://huggingface.co/datasets/eriktks/conll2003) dataset.

## [What’s Hugging Face?](https://huggingface.co/dbmdz/bert-large-cased-finetuned-conll03-english)

[​Hugging Face](https://huggingface.co/dbmdz/bert-large-cased-finetuned-conll03-english) is a popular open-source platform specializing in machine learning and natural language processing (NLP). Hugging Face enables developers to build, train, and deploy machine learning models easily, and in the cloud. Their Transformers library has become a standard in NLP tasks. In this guide, we’ll be using Hugging Face’s API to process text with the BERT model.

### Creating an Access Token

Start out by creating an account with Hugging Face, and then go to the [Access Token page](https://huggingface.co/settings/tokens). Create a new token, give it a name, and enable the options to *make calls to Inference providers and Endpoints.*

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1742036543027/f5ce84be-0e1a-4f86-bd8a-b3dc9a0d0318.png)

Scroll down and click **Create token**, then leave this page open so we can copy the token to Appsmith in the next section.

## Connecting to Hugging Face Models from Appsmith

Click the **Query** tab from the Appsmith editor and add a new REST API. Configure the API as follows:

| Name | NER\_BERT |
| --- | --- |
| Method | POST |
| URL | [https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english](https://api-inference.huggingface.co/models/dbmdz/bert-large-cased-finetuned-conll03-english) |
| Body Type | JSON |
| Body | {{ { "inputs": "Jesse and Mr. White went to the car wash." } }} |
| Header | Authorization: Bearer YOUR\_API\_TOKEN |

Click **RUN** and you should get back a response from Hugging Face.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1742037165541/1edfd8fa-7887-423f-ade9-e69680260236.png)

Notice the response structure. Each entity that was extracted has an `entity_group` (`PER` in this case, for Person), and a confidence score, along with the extract word and its start and end position. You’ll also see `ORG` used for organization, `LOC` for location, and `MISC` for miscellaneous. Other specialized models may have additional groups based on their specific domain and use case.

### Saving the Credentials to a Datasource

Next, click the **Save URL** button (below Run button), so we can move the API token to a secure datasource.

Name the datasource, then change the *Authentication type* to **Bearer Token**. Then copy the bearer token to the encrypted *Bearer token* field with the green lock icon.

Lastly, delete the original Authorization Header that was stored in plain text, then click **Save**.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1742037952832/1b6fafb0-c344-429e-bbc1-333331e2e9c8.png)

Retest the API. If everything is set up correctly, you should get back the same response as before, and the API token will no longer be stored in the API in plain text. This saves the credentials securely on your self-hosted Appsmith server (or the free cloud), and removes it from the app definition.

### Building the UI to Upload Files

Lastly, we’ll add a UI to select files from the local file system, then send the data to Hugging Face/BERT. Click the UI tab and drag in a Text widget, Table widget and a FilePicker widget. Set the FilePicker’s data type to `Text`.

Next, click the FilePicker and upload a local text or markdown file. In my case, I’m using markdown from a page of the Appsmith documentation on the OpenAI connector.

With a file loaded in the FilePicker, update the Text widget content to display the file’s name, using the following binding:

```json
{{FilePicker1.files[0].name}}
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1742038453982/54ed237d-713e-42ed-a162-3a1f34a4fdcb.png)

Then go back to the **Query** tab, and update the API body to use the data from the FilePicker.

```json
{{ 
{
	"inputs": FilePicker1.files[0].data
}
}}
```

You should see the file’s text inserted into the API body.

***Note****: If the text still shows as Base64, you may have to refresh the page after changing the FilePicker data type from Base64 to Text.*

Click **Run** and this time you should get back a new list of named entities, extracted from your text document.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1742038904797/ed420d41-0762-4c3e-b8aa-9d577532e3cf.png)

Now go back to the **UI** tab, and set the Table widget to display this response data.

```json
{{NER_BERT.data}}
```

You can also set the FilePicker to run the NER\_BERT query when a new file is uploaded, using the `onFileSelected` event.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1742039108379/dd8e7207-1890-4f95-86a5-a3c246c44ccc.png)

**Deploy!** 🚀

Deploy the app and test it out! You should now be able to upload a local text or markdown file and extract named entities from the document. From here, you can integrate with any REST or GraphQL API, database, or S3 storage to save the response. Or you could query data from an API or database and use that as the input to perform NER, and enrich existing data.

## Conclusion

Named Entity Recognition has a wide range of use cases, from tagging files and creating metadata, to automations and knowledge graphs for retrieval-augmented generation. The BERT series of models excels at NER, and Hugging Face makes it easy to integrate it into any app. From here you can save the data to any API or database, trigger automations, or send the data to a human reviewer before running a workflow.
{% endraw %}