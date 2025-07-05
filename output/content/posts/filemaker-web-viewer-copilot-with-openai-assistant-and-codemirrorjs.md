---
title: "FileMaker Web Viewer Copilot with OpenAI Assistant and CodeMirror.js"
date: 2025-03-10
permalink: "/filemaker-web-viewer-copilot-with-openai-assistant-and-codemirrorjs/"
layout: "post"
excerpt: "Web viewers in FileMaker Pro are a great way to extend the platform and create new UI components that would otherwise be impossible. The results can be extremely powerful, but working with web viewers and writing the code in FileMaker Pro can be a hu..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1741626218253/1869ad39-c19a-4f52-ba2d-2be50cab59b3.png"
readTime: 5
tags: ["filemaker", "claris", "openai", "AI Assistants ", "AI Code Generator"]
series: "FileMaker Pro"
---

Web viewers in FileMaker Pro are a great way to extend the platform and create new UI components that would otherwise be impossible. The results can be extremely powerful, but working with web viewers and writing the code in FileMaker Pro can be a huge pain, due to the lack of a proper code editor with formatting and syntax highlighting. That’s what led me to build this [CodeMirror Web Viewer app](https://blog.greenflux.us/why-i-built-a-code-editor-inside-filemaker-pro) last year, to simplify the process of writing and testing web viewer code. This app makes developing new web viewers much easier, by eliminating the need to copy/paste code into a separate code editor. However, I still found myself copy/pasting code in chatGPT for more advanced solutions.

So I decided to take this a step further, and integrate the [CodeMirror app](https://blog.greenflux.us/why-i-built-a-code-editor-inside-filemaker-pro) with the [ChatFMP app](https://blog.greenflux.us/chatfmp-filemaker-pro-starter-template-for-integrating-openai-assistants) I made for integrating with an OpenAI Assistant. This enables you to describe the web viewer you want in plain English, and the assistant will return the code and generate a new UI component with a single prompt.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741547865130/ab132a25-08c7-410d-8193-d010d8cd5919.gif)

In this guide, I’ll show how to integrate an OpenAI Assistant to FileMaker Pro to write HTML, and display the results in a web viewer. I’ll be skipping over some of the details from the original CodeMirror and ChatFMP apps, and focusing more on how the two have been integrated together. See the original tutorials for more details on building this from scratch, or just copy the finished app from the [GitHub Repo](https://github.com/GreenFluxLLC/FileMaker-Experiments).

**This Guide will cover:**

* Creating an OpenAI Assistant to write HTML for FMP web viewers
    
* Chatting with the Assistant from FileMaker Pro
    
* Displaying the HTML from the assistant in a web viewer
    
* Inserting data from FMP records into the new UI component

*Let’s Get Started!*

## Creating an OpenAI Assistant

Start out by creating a new assistant from the [OpenAI Dashboard](https://platform.openai.com/assistants).

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741622288594/25f88dec-d3df-4a73-9f8a-53fa35bac4e5.png)

Note the Assistant ID under the name. You’ll need to copy this in a few steps.

Name the assistant, and enter the following **System instructions**:

```plaintext
Your job is to write HTML docs to create UI components in a FileMaker web viewer, similar to an iframe. 
Use client side JS libraries when appropriate, and generate all code in a single HTML doc with style and script tags. 
Do not respond with any text before or after the HTML code. DO NOT wrap the code in back ticks "```html". Return only the HTML. 
```

I’ve found that asking it to return only the HTML makes it easier to parse the response, and it is consistent in following these instructions. However, it still likes to wrap the code in backticks ` ``` `, and it tends to do so even when you ask it not to, depending on the model. So we’ll have to handle that in FMP when parsing the response.

For the model, I would suggest trying `o3-mini` or `gpt-4o` first, but you should experiment with different models and see what works best for your use case.

Next, head over to the [API Keys](https://platform.openai.com/api-keys) section and create a new key.

Then keep the dashboard open so we can copy the key and assistant ID in the next section.

## Chatting with the Assistant

For this new Web Viewer Copilot app, I decided to build on top of a copy of the CodeMirror app because it already had most of the functionality I needed. If you want to follow along building on top of the same app, you can copy it from the repo, [here](https://github.com/GreenFluxLLC/FileMaker-Experiments/tree/main/CodeMirror). I’ll also be importing a custom function and scripts from the ChatFMP app ([repo](https://github.com/GreenFluxLLC/FileMaker-Experiments/tree/main/ChatFMP)).

Start out by opening the CodeMirror app and add 3 new text fields to the CodeMirror table: `thread_id`, `prompt`, and `response`.

Then, make sure you have the ChatFMP saved somewhere locally so you can import from it.

Go to `File>Manage>Custom Functions`, and click **Import**. Then select the ChatFMP app, and import the `curl` function.

This is used in a few of the scripts we’ll be importing, so be sure to import the custom function first! Otherwise, you’ll see the code in the scripts commented out `/*…*/` and you’ll have to manually correct all of the bad references.

The function is similar to using fetch in JavaScript, and simplifies the formatting for curl requests.

Next, go to `Scripts>Import`, and select the ChatFMP app. Import the `Create Thread` and `Add Message` scripts.

The *Create Thread* script will start a new thread and save the ID, so that each record in the CodeMirror table can be its own conversation with the assistant, and a different web viewer code. And the *Add Message* script sends the value from the prompt field to the assistant, then saves the reply in the response field.

In the ChatFMP scripts, the main table is called ChatFMP, but in this new app we’re working in the CodeMirror table. So there are a few places where the table reference needs updated before the scripts will work. Update all the table references, and the scripts should be ready to work in the new app.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741623373031/4e105eb2-39ac-440b-8ca8-a2c236422f78.png)

Next, update the *Create Thread* script to add your `assistant_id` and `API key`.

Then add the **prompt** field to the UI, and add a script trigger to run the *Add Message* script when the field is saved.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741623559621/13655a44-d6df-4b13-b35a-cf69ff253ca8.png)

## Displaying the response in a web viewer

Next, we’ll update the *Add Message* script to perform a few more actions once the response is received. Instead of displaying it directly, we want to remove the backticks ` ``` ` and save the HTML to the `doc` field. This is the field that the web viewer on the right uses as its source.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741623795818/19ba76c1-b9c6-4e69-bb1c-9ca48fcb1b9e.png)

Here you can see the last few lines I added to parse the response and update the UI. To remove the backticks and html wrapper, use `Substitute()` on the `$last_message` variable.

```plaintext
Substitute ( $last_message ; 

  [ "```html
" ; "" ];
  [ "```" ; "" ]

 )
```

I had some issues getting the web viewer to refresh when the doc field was updated, so I’ve added a few extra steps to ensure it’s displaying the most recent value.

## Testing Out the Copilot

**Time to test it out!** Try entering a prompt and see what kind of UI components you can build.

*Here are a few examples:*

**PROMPT**: Calendar with week view, and mock data for 2nd week of March, 2025, using fullcalendar.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741624540797/866d5d9d-6bb5-4305-8cba-46f4908151d4.png)

**PROMPT**: Sankey chart for budget of a software company, using echarts

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741624393442/2d01c50f-139d-41db-85eb-d24658d46364.png)

**PROMPT**: radar map of support tickets using echarts

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741624499829/4a9ca919-5a75-43ab-be19-f326e71fcf0b.png)

**PROMPT**: organizational chart for manufacturing company, using the orgchart library

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1741624815352/47e2c6e6-dc1f-4020-a31a-1acc061f2309.png)

All of these examples worked on the first try, except this last one. The code generated was using a bad link, so the script didn’t import. I found an updated link to a working CDN and provided it to the assistant, and it was able to generate a working org chart.

Since each record is its own thread, you can ask for follow-up changes without having to re-enter the first prompt. The assistant will maintain context and message history, so you can ask for adjustments and iterate on the code.

## Inserting data from FMP records

Ok, you’ve generated the perfect new UI component and now you want to tie in your data. This is where things get a little tricky, because every JavaScript library is going to have a different format for the data, and other parts of the code may have to be updated to reference the field names in your data. Some libraries like eCharts may just need an array of numbers inserted with `Substitute()`, and the rest can be hard-coded. Others, like this OrgChart library require a complex nested JSON structure.

Then there’s the structure of your input data. Are you wanting to display a single record, a list of related records, summary data?

There’s no straightforward answer here. It all depends on the shape of your data, and the format expected by the library. I would recommend using a combination of `Let`, `ExecuteSQL`, and FileMaker’s JSON functions to return a value as close as possible to the input data used in the HTML. Then use Substitute() to insert this into the Doc field. You can leave a placeholder in the HTML like `FMP_DATA`, and then replace it with your data.

If you’re not able to construct the proper data structure using FMP functions, get as close as you can, then provide a sample of the data with your prompt. The assistant should be able to modify the code to accept your input data and transform it with JavaScript as needed, in order to be compatible with the particular JavaScript libraries used in your web viewer code.

## Conclusion

Web Viewers in FileMaker are a flexible tool to solve a wide range of problems, but they come with their own set of challenges. Many of the formatting and validation issues can be solved using CodeMirror in a web viewer, but this still requires writing a lot of code manually. By integrating with an OpenAI Assistant, you can build a Web Viewer Copilot that writes code for you, generating new web viewers with a simple text prompt.

### Inspiration

I was inspired to write this tutorial after using the new Custom Widget Copilot in Appsmith. This native AI integration provides the same functionality out of the box, without having to create your own assistant and integrate it to the platform.

**Check it out in action!** [https://youtu.be/zBKeJf7a7dM](https://youtu.be/zBKeJf7a7dM)

![](https://i9.ytimg.com/vi_webp/zBKeJf7a7dM/maxresdefault.webp?v=678481c7&sqp=CJC1vL4G&rs=AOn4CLDf_pCA6d7To76hts-9oi7i1Fm2dA)