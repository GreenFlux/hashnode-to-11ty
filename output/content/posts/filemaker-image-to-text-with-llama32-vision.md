---
title: "FileMaker Image-to-Text with Llama3.2-vision"
date: 2024-11-09
permalink: "/filemaker-image-to-text-with-llama32-vision/"
layout: "post"
excerpt: "Last week, Meta released the LLama3.2-vision models, adding image recognition to the existing v3.2 text models. GenAI with image-to-text has been out for a while now, but what’s new here is just how optimized and lightweight the models are. The small..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1731169343754/d5bb93ae-77d8-4c82-8c07-3211b2ff8f26.png"
readTime: 5
tags: ["filemaker", "ollama", "genai", "image processing", "claris"]
series: "FileMaker Pro"
---

Last week, Meta released the [LLama3.2-*vision*](https://ollama.com/library/llama3.2-vision) models, adding image recognition to the existing v3.2 text models. GenAI with image-to-text has been out for a while now, but what’s new here is just how optimized and lightweight the models are. The smaller 11b (11 billion parameter) model is only 7.9Gb and can easily run on regular hardware, without the need for an expensive GPU.

In this guide, I’ll be building on a [previous post](https://blog.greenflux.us/local-llms-and-filemaker-pro) about integrating with the original text model using FileMaker Pro and Ollama. Now that the vision model is out, I wanted to update the app to send images from a container field in FileMaker and share a copy of the [finished app](https://github.com/GreenFluxLLC/FileMaker-Experiments/tree/main/OllamaChat).

## Running Llama3.2-vision Locally

Start out by installing the [Ollama desktop app](https://ollama.com/download) and opening it. You should see a llama icon in the menu bar. Then open up the terminal and run:

```bash
ollama run llama3.2-vision
```

You’ll see several files download the first time you run the model. Once the download is finished, the model will begin running and you can chat with it directly from the terminal!

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731167586934/832fd947-fb70-4e97-b7bb-df105ca95cb6.png)

To include an image with a prompt, just drag a file into the terminal and it will add the file path!

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731167934603/19869bb3-8833-46b9-b4f8-9b31c9bb0531.gif)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731168152472/af7b5b97-a68b-440c-b9d9-03c784adc009.png)

## Sending Image Prompts From FileMaker

When the Llama3.2-vision models were released last week, the first thing I did was pull up the FMP chat app I made with the regular text model. Once I had the new model downloaded and running, it only took 2 minutes and a few small changes from the original FMP chat app, to start prompting with images. Since most of the steps are explained in the [original tutorial](https://blog.greenflux.us/local-llms-and-filemaker-pro), I’ll just be sharing the final, updated solution here.

### Updated Script

```bash
Set Variable [ $image; Value:Base64Encode ( OllamaChat::image ) ]
Set Variable [ $body; Value:JSONSetElement ( "{}" ;
["stream" ; "false" ; JSONBoolean ];
["model" ; "llama3.2-vision" ; JSONString ];
["prompt" ; OllamaChat::Prompt ; JSONString ];
["images" ; "[\"" & $image & "\"]" ; JSONArray ]
) ]
// Show Custom Dialog [ Message: $body; Default Button: “OK”, Commit: “Yes”; Button 2: “Cancel”, Commit: “No” ]
Insert from URL [ $responseJSON; "http://localhost:11434/api/generate"; cURL options: "--header \"Content-Type: application/json\" --
data @$body" ]
[ Select; No dialog ]
Set Field [ OllamaChat::Reply; JSONGetElement ( $responseJSON ; "response" ) ]
```

### Updated UI and Database

* Added `OllamaChat::image` *(container field)*

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731168894413/d1a4add9-a5cc-41c8-a7bb-02df58c9f76c.png)

**Link to app**: [FileMaker Experiments &gt; OllamaChat](https://github.com/GreenFluxLLC/FileMaker-Experiments/tree/main/OllamaChat)

## Conclusion

Newer multi-modal LLMs have advanced and been optimized to run on regular hardware, enabling new use cases and integrations, like image-to-text processing in FileMaker Pro. By hosting the model locally with Ollama, you can build AI integrations with image recognition, and avoid the privacy and security issues that come with web based services. This can also be a more cost effective solution, and it runs completely offline.

### What’s Next?

From here, you can work on different prompts for describing images, extracting text, classifying images, or detecting certain types of content.

*Got an idea for a new use case?* **Drop a comment below!**

Also, I’d love to hear from others about how this performs on newer hardware. It takes at least a full minute or two on my laptop. How does it perform on a higher-end desktop with a dedicated GPU and more RAM?