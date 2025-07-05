---
title: "ChatFMP: FileMaker Pro Starter Template For Integrating OpenAI Assistants"
date: 2024-08-03
permalink: "/chatfmp-filemaker-pro-starter-template-for-integrating-openai-assistants/"
layout: "post"
excerpt: "OpenAI’s Assistants allow developers to add a ChatGPT-like AI chat to other apps and websites. I’ve been using the Assistant API quite a bit lately in Appsmith, and I wanted to see if I could build the same type of integration in my original go-to lo..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1722705439158/66335c9f-18da-406c-9487-a0b60471b588.png"
readTime: 5
tags: ["claris", "filemaker", "openai", "chatgpt", "AI Assistants "]
series: "FileMaker Pro"
---

OpenAI’s Assistants allow developers to add a ChatGPT-like AI chat to other apps and websites. I’ve been using the Assistant API quite a bit lately in Appsmith, and I wanted to see if I could build the same type of integration in my original go-to low-code platform, FileMaker Pro.

It turned out to be fairly easy, aside from the usual struggles with curl requests and escape quotes in FileMaker. Now that I have it working, I wanted to share the app as a resource for other FileMaker devs, and write up a quick tutorial. 

**This guide will cover:**

* Create an OpenAI Assistant
    
* Create an OpenAI API key
    
* Integrate FileMaker Pro with the Assistant API

**Note:** *Using the OpenAI API requires a paid plan.* 

## Creating the Assistant

Start out by going to your [OpenAI Dashboard](https://platform.openai.com/assistants), and creating a new Assistant. You can enter *Instructions* to describe how the Assistant should reply, upload files, and adjust other options as needed for your use case. The Instructions and Files you add here will be used in every conversation (called `threads` in the API) with the Assistant .

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1722702606274/654c869e-ac57-4710-81eb-e2fc7e7a4339.png)

**Examples**

| Use Case | Prompt | File |
| --- | --- | --- |
| Employee HR Assistant | answer employee questions based on our company policies in the file provided | employee handbook |
| Support Assistant | draft a reply to the support request based on the support docs in the file provided | support docs |
| Contract Assistant | draft a contract between the two parties | example contracts |

Finish setting up your Assistant and enter a name. Note the `assistant_id` under the name field. This will be needed in a few steps.

## Connect Your Assistant To FMP

### Creating an API Key

Next, go to the **API Keys** section of the OpenAI dashboard and click **create new secret key**. Give it a name, and then click **create secret key.** Then copy the key.

**Note**: You won't be able to see this value again, so keep this window open for the next step!

### Connect Your Assistant To FMP

Now, open the ChatFMP app and go to the script editor.

**You can copy the app from here:**

[https://github.com/GreenFluxLLC/ChatFMP](https://github.com/GreenFluxLLC/ChatFMP)

Update the `Create Thread` script with your `API key` and `assistant_id`.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1722701657670/9c694e2e-d4b2-4221-aba1-dee9f7e10651.png)

**That's It!** Your app should now be connected to your own custom AI Assistant.

## Using the App

Enter Layout mode and create a new record. Then type your prompt, and hit enter. It takes a few seconds for the AI to analyze the request and write a response, so the `Add Message` script will run on a loop, checking for a reply every 1.3 seconds.

You can name the thread, and save the conversation to come back to later. Each record will store a different `thread_id` so you can switch between conversations and continue the thread at any time.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1722701780766/762e33a7-97b6-4b60-a637-c8d364f6bd54.png)

## How It Works

### Assistant API

In order to 'talk' to your custom AI Assistant, there are [4 API's involved](https://platform.openai.com/docs/api-reference/threads), which run in the following order:

1. **Create Thread**: Returns a `thread_id`, used in subsequent API's.
    
2. **Add Message**: Adds the user message (prompt) to the thread.
    
3. **Create Run**: Runs the thread with the specified Assistant.
    
4. **List Messages**: Gets the messages from a thread.

List Messages returns an array of all the messages in the thread, with the most recent one first. If you run List Messages too early after adding your prompt, the last message will still be yours because the AI hasn't replied yet. So the script handles checking on a loop until the AI has responded.

### FileMaker Scripts

Both scripts use the *Insert From URL* script step to send a curl request to the Assistant API, and they have the same headers. So I wrote a custom function to construct the curl options.

```javascript
Let (
    [
        // Ensure the method is in uppercase and defaults to POST if empty
        requestMethod = If ( IsEmpty ( method ); "POST"; Upper ( method ) );
        // Format headers: each header is prefixed with "--header " and enclosed in quotes
        formattedHeaders = If (
            not IsEmpty ( headers );
            Substitute (
                headers;
                "¶";
                Quote ( "\" --header " )
            );
            ""
        );
        // Prepare headers with initial "--header" prefix
        formattedHeaders = If (
            not IsEmpty ( formattedHeaders );
            "--header \"" & formattedHeaders & "\"";
            ""
        );
        // Format body: add "--data" only if body is not empty and method requires it
        formattedBody = If (
            not IsEmpty ( body ) and requestMethod ≠ "GET";
            "--data " & Quote( body );
            ""
        );
        // Construct the full cURL command
        curlCommand = "-X " & requestMethod & " " & formattedHeaders & " " & formattedBody
    ];
    curlCommand
)
```

This makes it easy to construct the curl options in the four different APIs.

**Example Usage**

```javascript
curl ( 
  "POST" ; 

  $$headers ; 

 "" //no body

)
```

...which returns:

```bash
-X POST --header "OpenAI-Beta: assistants=v2"\" --header "Authorization: Bearer sk-proj-XYZ" 
```

**Create Thread**

This script runs *onRecordLoad* and checks to see if there is already a `thread_id`. If not, it creates a new thread and saves the ID.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1722701657670/9c694e2e-d4b2-4221-aba1-dee9f7e10651.png)

**Add Message**

This script adds your prompt as a new message to the thread, then runs the thread with your Assistant. It then loops every 1.3 seconds, checking the response from List Messages.

Once the assistant has replied, the script exits the loop, saves the response, and then clears your prompt so you can continue the conversation and enter a new message on the same thread.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1722702320370/dca63e9d-4eb4-4a43-96e8-94dd33d53ba2.png)

To keep this template simple, I'm only displaying the AI's last response, and not the full message history. However, the data is there in the response if you want to extend the UI to display it.

## Conclusion

The OpenAI Assistant API makes it easy to enhance other apps and websites with AI features. Using FileMaker's Insert From URL script step, you can integrate a live AI chat into any solution with just a few simple scripts. Just copy the scripts and add your API key and `assistant_id` to get started.

**Thanks for reading!** I hope this helps others get started with the OpenAI API in FileMaker. If you're looking for other ways to integrate FileMaker Pro with APIs without dealing with FileMaker curl requests, check out the [Postman-type interface](https://community.appsmith.com/content/blog/filemaker-api-connector-free-and-open-source-starter-solution-integrating-filemaker) I made for the FileMaker Data API.