---
title: "Talk To Your SpreadSheet:  Apps Script + Cohere AI"
date: 2024-09-06
permalink: "/talk-to-your-spreadsheet-apps-script-cohere-ai/"
layout: "post"
excerpt: "AI can be a huge productivity boost, but it can also become a new bottleneck if it doesn't have existing access to your data. Bouncing back and forth between tabs and pasting sheets data into ChatGPT might solve one problem, but it creates another.
I..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1725586965738/123d3174-4a61-4b04-87af-c80391fec65b.png"
readTime: 5
tags: ["llm", "AI", "Google", "google apps script", "cohereAI", "cohere "]
series: "Google Apps Script"
---

AI can be a huge productivity boost, but it can also become a new bottleneck if it doesn't have existing access to your data. Bouncing back and forth between tabs and pasting sheets data into ChatGPT might solve one problem, but it creates another.

Instead of bouncing between tabs, this guide will show you how to add an AI chat directly to your spreadsheet using an Apps Script Sidebar, and a free API key from [Cohere.com](https://cohere.com/).

**This guide will cover:**

* Integrating with the Cohere API
    
* Creating a Sidebar in Google Sheets
    
* Displaying the API response in the Sidebar
    
* Including Sheet data with the prompt, to get summary data

Let's get started by checking out the Cohere API docs.

## Cohere API /chat Endpoint

Cohere's `/chat` endpoint is easy to use and extremely flexible. Just send a POST request with your message and it responds directly, without having to get an ID back and make a follow up request like many other AI APIs. Yet it can still access websites in realtime and reply with up-to-date information, instead of relying only on the model's training set. You can also choose to ground the responses to only a single website.

To start a new chat, just send a `POST` request with a message property in the body. All other fields are optional.

```bash
curl --request POST \
  --url https://api.cohere.com/v1/chat \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --header "Authorization: bearer $API_KEY" \
  --data '{
    "message": "How can I build a Sidebar in Google Sheets?"
  }'
```

You can create a free account at cohere.com and go to your [Dashboard](https://dashboard.cohere.com/api-keys) to copy the trail API key. This will be rate limited, but it works fine for testing.

## Sending a POST request in Apps Script

Open **Apps Script** from the Sheets **Extension** menu, and update the Code.gs file with the following:

```javascript
function callCohereAPI(apiKey='YOUR_API_KEY', message='hello') {
  const apiUrl = 'https://api.cohere.com/v1/chat';

  const payload = {
    message: 'How can I make a Google Sheets Sidebar?'
    };

  const options = {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify(payload)
  };

  try {
    const response = UrlFetchApp.fetch(apiUrl, options);
    const jsonResponse = JSON.parse(response.getContentText());
    
    const lastReply = jsonResponse.text;
    Logger.log(lastReply)
    return lastReply;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}
```

Insert your API Key in the first line, click **Save**, and then run the function. You should see the AI's response in the Editor Log.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1725583941412/b44bb486-c6dd-471e-a2ba-47c7bdfefbfb.png)

## Creating a Sidebar

Next, we'll add a sidebar to interact with the Cohere AI. So we need an HTML doc to display in the sidebar, and a function to open it.

First add a new HTML file and name it Sidebar. Then paste in the following:

```javascript
<!DOCTYPE html>
<html>
  <head>
    <style>
      body {
        font-family: Arial, sans-serif;
      }
      .input-field {
        margin: 10px 0;
      }
      button {
        margin-top: 10px;
      }
      .result {
        margin-top: 20px;
        font-weight: bold;
        color: #333;
      }
    </style>
  </head>
  <body>
    <h2>Cohere Chat</h2>
    
    <div class="input-field">
      <label for="apiKey">API Key:</label>
      <input type="text" id="apiKey" placeholder="Enter your API key" style="width:100%;" />
    </div>
    
    <div class="input-field">
      <label for="message">Message:</label>
      <textarea id="message" placeholder="Enter your message" style="width:100%; height:100px;"></textarea>
    </div>
    
    <button onclick="sendRequest()">Send</button>
    
    <div class="result" id="result"></div>
    
    <script>
      function sendRequest() {
        var apiKey = document.getElementById('apiKey').value;
        var message = document.getElementById('message').value;
        
        if (!apiKey || !message) {
          document.getElementById('result').innerHTML = "Please provide both API key and message.";
          return;
        }

        google.script.run.withSuccessHandler(function(response) {
          document.getElementById('result').innerHTML = "Reply: " + response;
        }).callCohereAPI(apiKey, message);
      }
    </script>
  </body>
</html>
```

Then add a function to the Code.gs to show the sidebar, and another one to add that function to the sheet menu bar.

```javascript
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('Custom Menu')
    .addItem('Show Cohere Chat', 'showSidebar')
    .addToUi();
}

function showSidebar() {
  var html = HtmlService.createHtmlOutputFromFile('Sidebar')
      .setTitle('Cohere Chat');
  SpreadsheetApp.getUi().showSidebar(html);
}
```

Click Save, then refresh the sheet, and you should see the new menu item to open the sidebar. Then just paste in your API key and try asking a question.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1725584590936/29e623b4-9ae3-450b-9157-0d1a8c38f527.png)

## Talking To Your SpreadSheet

**Now for the fun part!** By sending the sheet data with the message, we can ask questions about it and get summary data, generate or classify text, and ask for extra details to enrich the existing dataset.

Simply update the message to include a stringified version of the sheet data. You can also enable Cohere's Web Search by including it in the 'connectors', allowing it to search the web in realtime.

```javascript
 function callCohereAPI(apiKey='YOUR_API_KEY', message='hello') {
  const apiUrl = 'https://api.cohere.com/v1/chat';
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = SpreadsheetApp.getActiveSheet();
  const data = sh.getDataRange().getValues()
  const payload = {
    message: `${message}, DATA: ${JSON.stringify(data)}`,
    connectors: [
      {
        id: 'web-search'
      }
    ]
  };

  const options = {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Accept': 'application/json',
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify(payload)
  };

  try {
    const response = UrlFetchApp.fetch(apiUrl, options);
    const jsonResponse = JSON.parse(response.getContentText());
    
    // Get only the last system message from the response
    const lastReply = jsonResponse.text;
    Logger.log(lastReply)
    return lastReply;
  } catch (error) {
    return `Error: ${error.message}`;
  }
}
```

Save and refresh the sheet, then reopen the sidebar. You should now be able to *Talk to your spreadsheet* and get summary data and other insights.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1725585287829/9cf65090-0830-47fd-b1d4-76be155c4da7.png)

## What's Next?

From here, you can save the response back to the sheet, update the message to only included the selected row, or send the response in an email. You could also train a model on your data and create a custom chat bot that has more background on your use case besides the sheet data.