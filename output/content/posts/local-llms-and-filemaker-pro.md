---
title: "Local LLMs and FileMaker Pro"
date: 2024-10-21
permalink: "/local-llms-and-filemaker-pro/"
layout: "post"
excerpt: "In just the last year or so, nearly every app and web service has integrated some form of AI into their product. Even many development platforms like FileMaker now include LLMs for building custom solutions with AI features. And for older versions, y..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1729379781736/ca0487f9-4ca1-4391-94c6-1f230bfa88e2.webp"
readTime: 5
tags: ["llm", "LLaMa", "AI", "filemaker", "ollama"]
series: "FileMaker Pro"
---

In just the last year or so, nearly every app and web service has integrated some form of AI into their product. Even many development platforms like FileMaker now include LLMs for building custom solutions with AI features. And for older versions, you can easily integrate with the OpenAI API or other AI services.

These are good options, but they might not work for all organizations. Some companies may have restrictions on sharing customer data with 3rd party AI services, or work in locations where there’s no internet access and everything has to be hosted locally.

In this guide, I’ll show you how to set up your own **self-hosted, local LLM** that works *completely offline*, and integrate it with FileMaker Pro. We’ll be using the Ollama client for Mac, and downloading the Llama3.2 model. No special hardware is needed. I’m running this on my M1 Macbook with no issues, and I’m able to quickly get an AI response in FileMaker, all without sending any data away from my machine.

Whether you’re concerned about privacy, need AI features offline, or just want to avoid the subscription costs, hosting your own LLM is a great alternative to relying on paid services. Sound interesting? **Let’s get started!**

## Installing Ollama

For this guide, I’ll be using Ollama, an open-source tool for running LLMs locally. With Ollama, you can download and run different models, then interact with them in the terminal, or via REST API. I’ll be using the Llama3.2 model, which is a 2GB model containing 3 billion parameters.

Start out by downloading Ollama and installing it.

[https://ollama.com/download](https://ollama.com/download)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1729380535005/1c86f951-2e50-4d0a-a5e3-faf03d073ccf.png)

I’ll be using MacOS in this guide, but Ollama also has Windows and Linux installers. Connecting from FileMaker will be the same on any OS once you have Ollama running, so feel free to follow along with other OS’es.

Once the download finishes, move the `Ollama.app` file to your **Applications** folder, then open it. Then click through the installer and approve the drive access.

After install, you’ll be given a command to run in the terminal, which will download and run the Llama3.2 model.

`ollama run llama3.2`

Run the command in the terminal and you’ll see several files download, just over 2GB total. Ollama will start running the Llama3.2 model as soon as it’s done downloading, and you can instantly begin chatting with it in the terminal!

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1729381431666/a4030407-7443-4a0e-b0f3-528c791b851f.png)

You’ll notice a new llama icon in the menu bar, with a single menu option to *Quit Ollama*. There’s no GUI with Ollama; just an installer to get the service running. Everything else is done through the CLI.

**Note**: You can check that the server is running, by going to:

[http://localhost:11434/](http://localhost:11434/)

You should see a message saying that Ollama is running.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1729380789293/2b8356f1-e0f1-435b-893d-d156d67b6e92.png)

## Testing the API

Next, open up Postman or your favorite API client. Lately I’ve been using [Yaak](https://yaak.app/), since Insomnia and Postman now require login to save requests.

Add a new request with the following configuration:

| Method | POST |
| --- | --- |
| URL | [http://localhost:11434/api/generate](http://localhost:11434/api/generate) |
| Body | `{ "model": "llama3.2", "prompt": "Does FileMaker have any AI features?", "stream": false }` |

Run the request, and you should get back a response from the model.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1729381951388/48b4d50b-d773-474c-8e84-5d5f8321afa2.png)

**Note**: The `streaming=false` parameter tells the server to wait until the model is done generating a response before replying, instead of sending multiple partial responses.

**Congratulations!** 🎉

You now have a working AI API running locally! You can even disconnect from the internet and continue to use it completely offline. The Llama3.2 model is lightweight enough to run locally and still powerful enough for many use cases. Now let’s connect it to FileMaker.

## Connecting From FileMaker Pro

Now open up FileMaker and add two text fields for `Prompt`, and `Reply`.

Then add a new script:

```plaintext
Set Variable [ $body; Value:JSONSetElement ( "{}" ;
["stream" ; "false" ; JSONBoolean ];
["model" ; "llama3.2" ; JSONString ];
["prompt" ; OllamaChat::Prompt ; JSONString ]
)]
Insert from URL [ $responseJSON; "http://localhost:11434/api/generate"; cURL options: "--header \"Content-Type: application/json\" -- data @$body" ]
[ Select; No dialog ]
Set Field [ OllamaChat::Reply; JSONGetElement ( $responseJSON ; "response" ) ]
```

Note the formatting on the cUrl options.

```plaintext
"--header \"Content-Type: application/json\" -- data @$body"
```

Be sure to use escape quotes `\”` around headers, and regular quotes around the entire string.

### Connecting the UI

Next, add the *Prompt* and *Reply* fields to the layout, and add a button to call the script.

**Now test it out from FileMaker!**

Turn off your wifi and ask it something specific. It’s amazing how much knowledge is packed in that 2GB model!

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1729383438604/c8f236c3-064c-4577-b0a6-9fdbc56d1cc0.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1729384415277/de217568-c0e4-4419-87dd-9b844d59a47b.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1729384418787/5cc38236-7624-4f8b-950d-2430f05b068e.png)

I have a feeling that the Salesforce API answer is a little outdated, but the fact that it can even answer this offline with a 2GB model is impressive!

## Conclusion

Hosting your own LLM is a great alternative to paying for subscription services, and it avoids privacy concerns and internet connection requirements. By using Ollama to host LLMs on the same server as FileMaker Pro, you can easily add AI to any FileMaker solution, even offline!

### What’s Next?

From here, you can try installing other models, or creating vector stores and adding fine-tuning and retrieval augmented generation (RAG). You could even train a model on your company data and gather data insights without any data ever leaving your company network!