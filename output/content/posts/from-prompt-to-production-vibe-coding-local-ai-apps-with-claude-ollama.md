---
title: "From Prompt to Production: Vibe Coding Local AI Apps with Claude + Ollama"
date: 2025-06-30
permalink: "/from-prompt-to-production-vibe-coding-local-ai-apps-with-claude-ollama/"
layout: "post"
excerpt: "In this guide, I’ll show you how you can build and run your own AI-powered apps that work completely offline, and do it without writing a single line of code. I’ll be using my favorite vibe-coding tool, Claude Code, to build an app that connects to l..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1751125199660/d2ecd9c2-420d-4c60-b26b-59eb25257a56.png"
readTime: 5
tags: ["ollama", "Llama3", "#multimodalai", "llm", "AI", "macOS", "claude.ai", "#anthropic", "Open Source", "vibe coding"]
series: "Artificial Intelligence"
---

In this guide, I’ll show you how you can build and run your own AI-powered apps that work completely offline, and do it without writing a single line of code. I’ll be using my favorite vibe-coding tool, Claude Code, to build an app that connects to local AI models using Ollama.

**This guide will cover:**

* Installing Ollama and running models locally
    
* Installing Claude Code and starting a new project
    
* Building a web app with Claude Code
    
* Dealing with CORS errors when connecting to Ollama
    
* Using multi-modal models with image recognition

To show the multi-modal input (image with prompt), I’ll be building an app for logging machinery inspections, that can analyze an equipment photo and auto-fill the inspection form. But we’ll keep the vibe-coded app simple and focus more on the process, so you can apply this to any AI powered app that you’d like to build and run offline.

## Installing Ollama and running models locally

I’ll be using Mac for this guide, but Ollama also has Windows and Linux installers, and most of this guide should be the same regardless of the OS.

Start out by downloading and installing [Ollama](https://ollama.com/download), then open it up. You’ll notice a new llama icon in the menu bar, with a single option to *Quit Ollama*.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731150387579/b9ce4790-220e-4721-8346-8e4cbdd4d05c.png?auto=compress,format&format=webp&auto=compress,format&format=webp&auto=compress,format&format=webp)

There’s no other GUI— everything else is done from the terminal.

### **Downloading and Prompting Models**

Next, open the terminal and run:

```bash
ollama run llama3.2:1b
```

This will download the smaller, 1 billion parameter Llama3.2 model, then run it and let you begin prompting from the terminal. You’ll see several files download the first time running a model, but after that it should load quickly and be ready to start prompting.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1746880539273/d64ce232-ab23-451d-b481-e1f69624c61e.png?auto=compress,format&format=webp)

Type a prompt and hit **Enter**. You should see a response in the terminal.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751118446059/5670c764-c38d-4ae7-9032-084a8ee05eda.png)

You can also test that the server is running from the browser, by going to [http://localhost:11434/](http://localhost:11434/)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751118556153/9036a000-953f-4d27-86ec-9fa6d065c5b9.png)

Type `/bye` to exit the Ollama chat, and return to the terminal. You can also type `/?` for a list of other commands.

Once you’ve exited Ollama and get back to the regular terminal, you can list the models you have downloaded using:

```bash
ollama list
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751118764946/69ac4dae-bd4f-4ec2-b3d2-eb61a5b22770.png)

Next, download the `llama3.2-vision` model so we can build an app with image recognition. But this time, we don’t want to chat from the terminal, we want to build our own web app to interact with it. So we only want to pull the model, but not run it from the terminal.

```bash
ollama pull llama3.2-vision
```

This will download the model without starting the terminal chat. When the download finishes, close the terminal and exit Ollama from the menu bar. This will ensure Ollama releases the 11343 port before we try starting it in server only mode in the next step.

Next, we’ll start up the ollama server without running a specific model. This way we can access it from the API only, without the terminal chat session going.

```bash
ollama serve
```

This will start up the Ollama server, without a specific model or chat running. Then, you can chat through the API and specify the model in your request.

If you see an error about port 11434 already being in use, make sure you exited Ollama from the Mac menu bar first.

Retest [http://localhost:11434/](http://localhost:11434/) and you should still see the status page. You’ll also notice the server activity logged in the terminal as a `GET` request with a `200` response.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751119493706/36495cc7-bc58-4820-bb88-c776d50aca15.png)

Ok, the Ollama server is running and available by API. Now let’s get Claude Code installed. Be sure to keep this terminal window running for Ollama, and open a new terminal window for the next step.

## Installing Claude Code and starting a new project

Download and install [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview) from the terminal:

```bash
npm install -g @anthropic-ai/claude-code
```

Once you have it installed, create a new folder for the project, and navigate into it.

```bash
mkdir inspection-app && cd inspection-app
```

Now, start up Claude Code:

```bash
claude
```

You’ll see a confirmation screen asking for permission to allow Claude to access this folder.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751120106569/cf4d2ff6-17b3-4f90-97e7-44a6a977945b.png)

Approve it, and then you’ll be greeted with a prompt. From here, you can begin chatting with Claude and tell it what to build.

## Building a web app with Claude Code

Paste in the following prompt, or try with your own app idea. Be sure to keep that first line to tell Claude that Ollama is running with the llama3.2-vision model available.

```plaintext
Ollama is running locally with llama3.2-vision. 
Build a simple client-side web app for machinery inspections with photo upload to local storage. 
Use Ollama to examine the image and fill out the inspection. 
```

Hit **Enter**, and you’ll see Claude start chugging away. Claude will know how to integrate with Ollama’s API. But if you’re curious about the details, here’s the [docs](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-request-streaming).

After some planning, you should get prompted to allow Claude to create a new file in the project folder. You can approve it once, or *always approve* for the rest of the session.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751120480910/6406436a-a46a-40fb-ad17-98b360f96a57.png)

Give it a few more minutes to finish writing the JavaScript and CSS, and then you should have a basic web app ready to test out.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751120622748/1e21bdf6-3f3e-433b-aeec-b7cb3de93ca4.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751120739195/74843249-54c0-4da1-a1d9-5807cb532de6.png)

*Not bad!* Time to test it out. Try uploading an image and analyzing it.

## Dealing with CORS errors when connecting to Ollama

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751120844300/5708f800-f819-4d08-8eea-6c20629d90ec.png)

Oh, our first error. Ok, take a look at the browser console.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751120906134/a6de0a2b-fef2-4724-87a9-c549cca49397.png)

***CORS!*** 🤬

The browser is blocking our web app from connecting to APIs on local host because the server (Ollama) is not accepting cross origin requests.

> **Note**: CORS is an issue because our app is just a simple HTML file with everything running client-side. If we prompted Claude Code to build a Node.js or Python server for the app, then CORS wouldn’t be a problem as long as the API requests run from the server-side to Ollama.

Go back to the terminal that has Ollama running and hit `control+c`, or close it and open a new terminal. Then restart Ollama with a wildcard to allow all origins.

```bash
OLLAMA_ORIGINS="*" ollama serve
```

Clear out the console errors, and try again. This time, test it out with the internet off, and Ollama should still be able to generate a response. Just remember to turn it back on before asking Claude to make any edits to the app.

You should now be able to use Ollama and the Llama3.2-vision model to analyze images and auto-fill the form.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1751121437162/25dbc674-f58e-4719-a02e-620e61d029fb.png)

> **Note**: Ollama may take several minutes to respond, depending on your hardware. I’m running a ~4 year old Macbook Pro M1 with 16GB of RAM, and it takes about 2-3 minutes. Desktops with a decent video card will have much better response times.

**Look at that!** The vibe-coded app actually worked on the first prompt, once we had Ollama running with CORS enabled. From here, you can continue to prompt with Claude to add features and build your own custom, AI powered app that works completely offline with no internet!

## Other Thoughts

There’s a lot more I could say here about vibe-coding, and techniques to plan out your app before prompting. But I wanted to keep this tutorial about connecting to Ollama with a local web app and dealing with CORS errors. For more info on vibe-coding techniques, check out this [best practices](https://www.anthropic.com/engineering/claude-code-best-practices) guide from Anthropic.

## Conclusion

Newer language models have become more efficient and can now run on regular hardware using Ollama, enabling new use cases in environments where AI was previously not an option. Other AI tools like Claude Code can be used to build apps that integrate with Ollama, without writing a single line of code. This enables non-developers to build AI powered applications that can run on their local network, with no outside internet, and even use more advanced features like image recognition.