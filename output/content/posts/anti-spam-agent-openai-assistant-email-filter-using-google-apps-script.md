---
title: "Anti-Spam Agent: OpenAI Assistant Email Filter Using Google Apps Script"
date: 2025-02-08
permalink: "/anti-spam-agent-openai-assistant-email-filter-using-google-apps-script/"
layout: "post"
excerpt: "I get a LOT of spam email that make it passed Google’s spam detection, and I’m constantly marking emails as spam and blocking senders. It’s a never-ending battle. Most of them end with something like
“if this isn’t for you, just reply STOP”.“P.S. Not..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1739023382667/509f43ca-6a3c-4629-8f9d-afafa28d7a56.png"
readTime: 5
tags: ["google apps script", "openai", "agentic AI", "spam", "gmail", "REST API", "JavaScript"]
series: "Google Apps Script"
---

I get a LOT of spam email that make it passed Google’s spam detection, and I’m constantly marking emails as spam and blocking senders. It’s a never-ending battle. Most of them end with something like

*“if this isn’t for you, just reply STOP”.  
“P.S. Not the right fit? Just reply “no,” and I’ll take you off my list.”  
“Not relevant? Just reply 'all good' and I'll stop messaging :)”*

![No, I Don't Think I Will | Know Your Meme](https://i.kym-cdn.com/photos/images/newsfeed/001/535/091/d97.jpg)

These spammers just want your help warming up their email account so they can send more spam. By replying, you’re just boosting their sender reputation, and helping them get passed more spam filters and land in more inboxes.

Every time I mark a message as spam, I think of how much time I’ve spent so far, and how I could have automated this 10 times by now. It sounds like the perfect job for AI, but how do you go about implementing it? And more importantly, automating it?

## Google Apps Script + OpenAI Assistant with Structured Outputs

Cloud-hosted Large Language Model APIs like OpenAI Assistants are a great solution for processing unstructured data like emails. And the Structured Output feature ensures the LLM response conforms to a specific JSON structure, making it ideal for passing to regular JavaScript functions in Google Apps Script.

*In this guide, I’ll show how you can use* ***Google Apps Script + OpenAI Assistants*** *to:*

* Create an OpenAI Assistant for scoring emails as spam on multiple metrics
    
* Scan for unread emails in Apps Script
    
* Skip emails from your contacts or coworkers
    
* Skip threads you started, or threads you’ve already replied on
    
* Send possible spam emails to the OpenAI Assistant to be scored
    
* Move offending emails to spam
    
* Run the script on a timer

## Creating an OpenAI Assistant

Start out by creating a new assistant from the [OpenAI dashboard](https://platform.openai.com/assistants), and entering instructions that describe the specific type of spam emails that tend to make it to your inbox. Here’s the instructions I’m using, but this should only be used as a starting point. Modify the instructions to describe the type of messages you’re trying to block.

```markdown
Your job is to scan emails and score them on various metrics to determine if they are a specific type of spam. The prompt will be a JSON object with senderDomain, senderName, subject, and body. Use these to generate the JSON spam scores. 
Score the email as described below, and reply with nothing but the scores. 

You should return a structured JSON output with multiple scores, describing how spammy different aspects of the email are, in the following categories. When these conditions are fully met, the score should be 1.0 for that section. 

# Sender
- Domain is not a private email provider like Gmail, Outlook, etc
- Name is a private person (not general company address like info@, support@, etc)
# Subject
- Selling a product/service
- Mentions funding or startups
 -Mentions me by name (Joseph Petty)
# Intro
 -Mentioning the receiver is a founder, or employee of Appsmith
 -A question about a business problem or solution
# Body
 -Plain text, no image and minimal or no bold/italics formatting
 -Offering a business solution or asking about a problem
# Unsubscribe
 -No link provided to unsubscribe 
 -No mention of how to unsubscribe at all 
# Closing
Says to email back to unsubscribe, usually with something like:
- If you’d like to unsubscribe, just reply ‘no thanks’
 -If this isn’t relevant, reply with unsubscribe
 -Reply with "stop" and I'll stop emailing you
 -P.S. Not the right fit? Just reply “no,” and I’ll take you off my list.
 -Not relevant? Just reply 'all good' and I'll stop messaging :)

For each section, return a number (0-1) for how spammy that aspect of the email is, based on these cold email approaches. Then return a final isSpam score (0-1) based on the weighted average of all other scores. Double the weight for the closing if they ask for a reply email in order to unsubscribe. 
```

## Structured Outputs with JSONSchema

Next, define a JSONSchema to ensure the model always replies with valid JSON that will work with the code in Apps Script.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1739023904349/5b8f4bd6-e687-4094-95db-53328f37e9a2.png)

Select `json_schema` for the **response\_format**, then paste is this schema:

```javascript
{
  "name": "email_spam_scoring",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "scores": {
        "type": "object",
        "properties": {
          "sender": {
            "type": "object",
            "properties": {
              "domain_private": {
                "type": "number",
                "description": "Score indicating whether the domain is a private email provider."
              },
              "name_personal": {
                "type": "number",
                "description": "Score indicating whether the sender's name represents a private person."
              }
            },
            "required": [
              "domain_private",
              "name_personal"
            ],
            "additionalProperties": false
          },
          "subject": {
            "type": "object",
            "properties": {
              "selling_product": {
                "type": "number",
                "description": "Score indicating whether the subject references selling a product/service."
              },
              "funding_startups": {
                "type": "number",
                "description": "Score indicating whether the subject mentions funding or startups."
              },
              "mentions_name": {
                "type": "number",
                "description": "Score indicating whether the subject mentions the recipient's name."
              }
            },
            "required": [
              "selling_product",
              "funding_startups",
              "mentions_name"
            ],
            "additionalProperties": false
          },
          "intro": {
            "type": "object",
            "properties": {
              "mentions_founder": {
                "type": "number",
                "description": "Score indicating whether the intro mentions the receiver is a founder or employee."
              },
              "business_question": {
                "type": "number",
                "description": "Score indicating whether the intro contains a business problem or solution question."
              }
            },
            "required": [
              "mentions_founder",
              "business_question"
            ],
            "additionalProperties": false
          },
          "body": {
            "type": "object",
            "properties": {
              "plain_text": {
                "type": "number",
                "description": "Score indicating whether the body is plain text with minimal formatting."
              },
              "business_solution": {
                "type": "number",
                "description": "Score indicating whether the body offers a business solution or asks about a problem."
              }
            },
            "required": [
              "plain_text",
              "business_solution"
            ],
            "additionalProperties": false
          },
          "unsubscribe": {
            "type": "object",
            "properties": {
              "no_link": {
                "type": "number",
                "description": "Score indicating whether there is no link provided to unsubscribe."
              },
              "no_mention": {
                "type": "number",
                "description": "Score indicating if there's no mention of how to unsubscribe."
              }
            },
            "required": [
              "no_link",
              "no_mention"
            ],
            "additionalProperties": false
          },
          "closing": {
            "type": "object",
            "properties": {
              "email_reply_unsubscribe": {
                "type": "number",
                "description": "Score indicating whether the closing contains instructions to email back to unsubscribe."
              }
            },
            "required": [
              "email_reply_unsubscribe"
            ],
            "additionalProperties": false
          }
        },
        "required": [
          "sender",
          "subject",
          "intro",
          "body",
          "unsubscribe",
          "closing"
        ],
        "additionalProperties": false
      },
      "isSpam": {
        "type": "number",
        "description": "Final score indicating how spammy the email is."
      }
    },
    "required": [
      "scores",
      "isSpam"
    ],
    "additionalProperties": false
  }
}
```

You can also click the **Generate** tab, and describe the schema, and OpenAI will generate it. I generated this one by pasting in the Assistant’s instructions, then modifying a few values.

Next, go to the API section of the dashboard and create a new key. Then keep this page open to copy the key, while you create a new Apps Script.

## Processing Emails and Contacts in Apps Script

Before we get to integrating with AI, let’s set up a basic script to loop through unread emails from the inbox and see if they are in our existing contacts, from a co-worker, or from a thread we have already replied to. This way we scan skip these emails and avoid calling the OpenAI API on every email.

Start out by creating a [new script](https://script.new), the go to the services section and enable the **Gmail API** and the **People API**. Then name the script, and paste in the code below:

```javascript
const MY_EMAIL = 'YOUR_WORK_EMAIL';

function isContactOrCoworker(email = 'EMAIL_TO_TEST') {
  if (!email) return false;
  if (MY_EMAIL.endsWith('@' + email.split('@')[1]) && email !== MY_EMAIL) {
    Logger.log('Found coworker');
    return true;
  }
  const results = (
    People.People.searchContacts({ query: email, readMask: 'emailAddresses' }).results || []
  ).concat(
    People.OtherContacts.search({ query: email, readMask: 'emailAddresses' }).results || []
  );
  Logger.log(`isContactOrCoworker() found ${results.length} matches for ${email}`);
  return !!results.length;
}
```

Update the script with your email, and an email to test. Save the script, and click **Run**.

You should be prompted to approve access to your email and contacts on the first run. This function will return `true` if the input email is a coworker (same domain), or is in your main Google Contacts, or Other Contacts. Test out a few different emails, using addresses from your contacts, coworker’s addresses, and a then a potential spam sender that isn’t a coworker or contact.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1739018298617/4c5b53ec-eb7f-4180-a6e5-d7d56651e8e0.png)

## Scan for unread emails in Apps Script

Next, we can loop over unread emails in the inbox, and run this function on each one to see if it should be checked for spam. Additionally, each thread will be checked to see if `MY_EMAIL` is the sender on any of the thread’s messages, skipping threads that I started or already replied on.

```javascript
function checkSpamEmails() {

  // Fetch unread Gmail threads
  const gmailThreads = GmailApp.search('in:inbox is:unread');
  Logger.log(`Found ${gmailThreads.length} unread thread(s).`);
  
  gmailThreads.forEach((gmailThread, threadIndex) => {
    Logger.log(`---> Gmail Thread #${threadIndex + 1}: "${gmailThread.getFirstMessageSubject()}"`)
    
    // Skip if already replied, or if I started the thread
    const allThreadEmailAddresses = gmailThread.getMessages()
    .map(msg => msg.getFrom().match(/(?<=<).*?(?=>)/)[0]);
    Logger.log(allThreadEmailAddresses);

    if(allThreadEmailAddresses.includes(MY_EMAIL)){
      Logger.log('Skipping thread. Already replied, or I started the thread.');
      return 
    };

    // Skip if any email on thread is coworker or contact
    const anyEmailIsCoworkerOrContact = allThreadEmailAddresses.find(e=>isContactOrCoworker(e))
    if(anyEmailIsCoworkerOrContact){
      Logger.log('At least one email is coworker or contact. Skipping thread.')
      return
    }
    // Email is not from contact/coworker, I haven't replied, and didn't start thread
    Logger.log(`Potential Spam found. Checking: ${gmailThread.getFirstMessageSubject()}`)
    // Check first message using OpenAI Assistant
    
  });
}
```

Save the script again, and this time run the `checkSpamEmails()` function. You should get another prompt to approve the new permissions for reading emails. Then go through your spam, and mark a few as unread and *not spam* to move them to the inbox. Run the function again and you should see the list of emails being processed.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1739018668905/92c91293-cabf-4c43-8095-20763abeefe1.png)

## Checking emails with OpenAI Assistant

Next, we’ll write a separate function that sends a message to our assistant with the email to be scanned, and returns the spam score, in the structured JSON format that we defined earlier. First, we’ll just hard code some values to test a single email. Then that function can be called in the forEach loop of the `checkSpamEmails()` function.

Start out by adding a few more variables to the top of the script.

```javascript
const SPAM_THRESHOLD = 0.7;
const ASSISTANT_ID = 'YOUR_ASSISTANT_ID';
const API_KEY = 'YOUR_OPENAI_API_KEY';
```

The spam threshold is the value we will use to trigger marking the email as spam, as scored by the assistant. This will let you tweak the ‘spammy-ness’ level of the filter, and avoid false positives that could mark an important email as spam.

Then add a new function to call the OpenAI Assistant, using the ‘[Create Thread and Run](https://platform.openai.com/docs/api-reference/runs/createThreadAndRun)’ method. This starts a new thread, adds the first message, and runs the thread, in one API.

```javascript

const mockPrompt = {
        senderDomain: 'spammer.com',
        senderName: 'Spammer',
        subject: 'Try our new AI Powered Coffee Maker! ',
        body: 'if this isn’t for you, just reply STOP'
      };

function createRun(promptData=mockPrompt) {
  try {
    Logger.log('Creating run for spam check...');
    const requestBody = {
      assistant_id: ASSISTANT_ID,
      thread: {
        messages: [
          {
            role: 'user',
            content: JSON.stringify(promptData)
          }
        ]
      }
    };

    const response = UrlFetchApp.fetch('https://api.openai.com/v1/threads/runs', {
      method: 'post',
      contentType: 'application/json',
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'OpenAI-Beta': 'assistants=v2'
      },
      payload: JSON.stringify(requestBody),
      muteHttpExceptions: true
    });

    const data = JSON.parse(response.getContentText());
    Logger.log('Create run response: ' + JSON.stringify(data));

    return {
      runId: data.id || null,          // e.g. "run_abc123"
      threadId: data.thread_id || null // e.g. "thread_abc123"
    };
  } catch (err) {
    Logger.log('Error while creating run: ' + err);
    return { runId: null, threadId: null };
  }
}
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1739020319786/e1e7aade-78ca-46b4-90c6-b04c868ca5f9.png)

Notice the `thread_id` in the reply. This is an async operation that takes several seconds to complete. So a second API must be called to get the reply message from the LLM, using the `thread_id`. Copy the ID from this response to use as a test in the next section. Then add a new function to `fetchAssistantMessage()`

```javascript
function fetchAssistantMessage(openAiThreadId='THREAD_ID') {
  Logger.log('Fetching final assistant message for OpenAI thread: ' + openAiThreadId);

  const getMessagesUrl = `https://api.openai.com/v1/threads/${openAiThreadId}/messages`;
  const response = UrlFetchApp.fetch(getMessagesUrl, {
    method: 'get',
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      'OpenAI-Beta': 'assistants=v2'
    },
    muteHttpExceptions: true
  });

  const data = JSON.parse(response.getContentText());
  Logger.log('Thread messages response: ' + JSON.stringify(data));

  const messages = data.data || data.messages || [];

  // Find the last assistant message that has content
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i];
    if (msg.role === 'assistant' && msg.content && msg.content.length > 0) {
      // Concatenate .text.value parts into a single string
      let combinedText = '';
      for (const segment of msg.content) {
        if (segment.type === 'text' && segment.text && segment.text.value) {
          combinedText += segment.text.value;
        }
      }
      Logger.log('Assistant raw text: ' + combinedText);
      return combinedText; // Return the raw string
    }
  }
  return null;
}
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1739020797414/f1740697-56cc-4c53-a8bf-abd9b8ac59cb.png)

## Checking Messages On Async Loop

If you check for messages too soon, the LLM won’t be done replying yet. You can hard-code a longer wait period, but that isn’t a great user experience. Instead, it’s best to check on a loop, and exit the loop once the reply is complete. So we’ll use a wrapper function that creates a run, then checks for messages every few seconds until the LLM has finished responding.

```javascript
function createRunAndWaitForReply(promptData = mockPrompt) {
  // Initiate a run
  const { runId, threadId } = createRun(promptData);
  if (!runId || !threadId) {
    Logger.log('Could not create run.');
    return null;
  }

  // Poll for a final assistant message
  const maxAttempts = 10;
  const waitMs = 3000; // 3 seconds
  let assistantText = null;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    Utilities.sleep(waitMs);
    assistantText = fetchAssistantMessage(threadId);
    if (assistantText) {
      Logger.log(`Assistant replied on attempt #${attempt}: ${assistantText}`);
      return assistantText;
    }
    Logger.log(`No assistant reply yet. Attempt #${attempt} of ${maxAttempts}...`);
  }

  Logger.log('No assistant reply within max attempts.');
  return null;
}
```

Finally, this wrapper function can be called in the checkSpamEmail loop, on the emails that were not skipped due to being a contact, coworker, etc. Update the checkSpamEmail() function with:

```javascript
function checkSpamEmails() {
  // Fetch unread Gmail threads
  const gmailThreads = GmailApp.search('in:inbox is:unread');
  Logger.log(`Found ${gmailThreads.length} unread thread(s).`);
  
  gmailThreads.forEach((gmailThread, threadIndex) => {
    Logger.log(`---> Gmail Thread #${threadIndex + 1}: "${gmailThread.getFirstMessageSubject()}"`);
    
    // Extract all sender email addresses in the thread
    const allThreadEmailAddresses = gmailThread.getMessages()
      .map(msg => {
        const match = msg.getFrom().match(/(?<=<).*?(?=>)/);
        return match ? match[0] : null;
      })
      .filter(Boolean);
    Logger.log(allThreadEmailAddresses);

    // Skip if I am among the senders
    if (allThreadEmailAddresses.includes(MY_EMAIL)) {
      Logger.log('Skipping thread. Already replied or I started the thread.');
      return;
    }

    // Skip if any sender is a coworker or contact
    if (allThreadEmailAddresses.some(e => isContactOrCoworker(e))) {
      Logger.log('At least one email is coworker or contact. Skipping thread.');
      return;
    }

    // Not a contact/coworker, and I haven't replied
    Logger.log(`Potential Spam found. Checking: ${gmailThread.getFirstMessageSubject()}`);

    // Build the prompt from the first message
    const firstMessage = gmailThread.getMessages()[0];
    const fromEmail = allThreadEmailAddresses[0];
    const senderDomain = fromEmail.split('@')[1] || '';
    const senderName = fromEmail.split('@')[0] || '';
    const subject = gmailThread.getFirstMessageSubject();
    const body = firstMessage.getPlainBody().slice(0, 1000); // Example snippet

    const promptData = {
      senderDomain,
      senderName,
      subject,
      body,
    };

    // Create a run and wait for the assistant’s reply
    const assistantReply = createRunAndWaitForReply(promptData);
    if (!assistantReply) {
      Logger.log('No reply from assistant within the timeout.');
      return;
    }

    Logger.log(`Assistant response:\n${assistantReply}`);

    // Example: parse the assistant's JSON content (e.g. {"isSpam":true,"score":0.95,"reason":"..."})
    // Adjust the parsing logic to fit your assistant's actual output format
    try {
      const spamData = JSON.parse(assistantReply);
      if (!!spamData.isSpam && spamData.isSpam >= SPAM_THRESHOLD) {
        gmailThread.moveToSpam();
        Logger.log('Thread moved to spam.');
      } else {
        Logger.log('Assistant indicates not spam or below threshold.');
      }
    } catch (parseErr) {
      Logger.log('Error parsing assistant response as JSON:', parseErr);
    }
  });
}
```

Now go through your spam messages and move a few more into the inbox. Make sure to mark them as 'not spam’, and unread.

Run the script again, and hopefully you’ll see a few that get moved back to spam. If not, try adjusting the assistant’s instructions to better target the type of spam you’re receiving, and/or increase the threshold variable.

## Run the script on a timer

Once everything is working, you can set this script to run on a timer, and automatically move messages to spam when they make it passed Gmail’s spam filter.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1739024406766/5cf77574-1c1a-4b9e-a26a-4c114126d2ff.png)

## Limitations

Depending on how many spam emails you get, you may start to run into usage limits, or quotas, on the Google APIs for Gmail and People (contacts). Once you start to hit those limits, you’ll have to migrate to using the REST API, which requires creating a project in Google and adding your credit card. At that point, you’ll have to write a LOT more code to handle constructing all the API calls, error checking, etc. So it makes more sense to switch platforms at this point, and using something like Appsmith to manage all the APIs and async JavaScript. But for lower volume, personal use, Apps Script works great and is free!

## Conclusion

Gmail’s built-in spam detection tends to miss a lot of emails that should be marked as spam. Using Google Apps Script and an OpenAI Assistant, you can score emails on various metrics and set a threshold to trigger sending emails to spam automatically. This free alternative to using Google’s REST API works well for small projects, but it has usage limits. For a more robust solution, consider using the REST API and another platform handle the logic.

## Full Script

```javascript
const MY_EMAIL = 'joseph@appsmith.com';
const SPAM_THRESHOLD = 0.7;
const ASSISTANT_ID = 'ASSISTANT_ID';
const API_KEY = 'API_KEY';

function isContactOrCoworker(email = 'TEST@SPAM.COM') {
  if (!email) return false;
  if (MY_EMAIL.endsWith('@' + email.split('@')[1]) && email !== MY_EMAIL) {
    Logger.log('Found coworker');
    return true;
  }
  const results = (
    People.People.searchContacts({ query: email, readMask: 'emailAddresses' }).results || []
  ).concat(
    People.OtherContacts.search({ query: email, readMask: 'emailAddresses' }).results || []
  );
  Logger.log(`isContactOrCoworker() found ${results.length} matches for ${email}`);
  return !!results.length;
}

function checkSpamEmails() {
  // Fetch unread Gmail threads
  const gmailThreads = GmailApp.search('in:inbox is:unread');
  Logger.log(`Found ${gmailThreads.length} unread thread(s).`);
  
  gmailThreads.forEach((gmailThread, threadIndex) => {
    Logger.log(`---> Gmail Thread #${threadIndex + 1}: "${gmailThread.getFirstMessageSubject()}"`);
    
    // Extract all sender email addresses in the thread
    const allThreadEmailAddresses = gmailThread.getMessages()
      .map(msg => {
        const match = msg.getFrom().match(/(?<=<).*?(?=>)/);
        return match ? match[0] : null;
      })
      .filter(Boolean);
    Logger.log(allThreadEmailAddresses);

    // Skip if I am among the senders
    if (allThreadEmailAddresses.includes(MY_EMAIL)) {
      Logger.log('Skipping thread. Already replied or I started the thread.');
      return;
    }

    // Skip if any sender is a coworker or contact
    if (allThreadEmailAddresses.some(e => isContactOrCoworker(e))) {
      Logger.log('At least one email is coworker or contact. Skipping thread.');
      return;
    }

    // Not a contact/coworker, and I haven't replied
    Logger.log(`Potential Spam found. Checking: ${gmailThread.getFirstMessageSubject()}`);

    // Build the prompt from the first message
    const firstMessage = gmailThread.getMessages()[0];
    const fromEmail = allThreadEmailAddresses[0];
    const senderDomain = fromEmail.split('@')[1] || '';
    const senderName = fromEmail.split('@')[0] || '';
    const subject = gmailThread.getFirstMessageSubject();
    const body = firstMessage.getPlainBody().slice(0, 1000); // Example snippet

    const promptData = {
      senderDomain,
      senderName,
      subject,
      body,
    };

    // Create a run and wait for the assistant’s reply
    const assistantReply = createRunAndWaitForReply(promptData);
    if (!assistantReply) {
      Logger.log('No reply from assistant within the timeout.');
      return;
    }

    Logger.log(`Assistant response:\n${assistantReply}`);

    // Example: parse the assistant's JSON content (e.g. {"isSpam":true,"score":0.95,"reason":"..."})
    // Adjust the parsing logic to fit your assistant's actual output format
    try {
      const spamData = JSON.parse(assistantReply);
      if (!!spamData.isSpam && spamData.isSpam >= SPAM_THRESHOLD) {
        gmailThread.moveToSpam();
        Logger.log('Thread moved to spam.');
      } else {
        Logger.log('Assistant indicates not spam or below threshold.');
      }
    } catch (parseErr) {
      Logger.log('Error parsing assistant response as JSON:', parseErr);
    }
  });
}

const mockPrompt = {
        senderDomain: 'spammer.com',
        senderName: 'Spammer',
        subject: 'Try our new AI Powered Coffee Maker! ',
        body: 'if this isn’t for you, just reply STOP'
      };

function createRun(promptData=mockPrompt) {
  try {
    Logger.log('Creating run for spam check...');
    const requestBody = {
      assistant_id: ASSISTANT_ID,
      thread: {
        messages: [
          {
            role: 'user',
            content: JSON.stringify(promptData)
          }
        ]
      }
    };

    const response = UrlFetchApp.fetch('https://api.openai.com/v1/threads/runs', {
      method: 'post',
      contentType: 'application/json',
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        'OpenAI-Beta': 'assistants=v2'
      },
      payload: JSON.stringify(requestBody),
      muteHttpExceptions: true
    });

    const data = JSON.parse(response.getContentText());
    Logger.log('Create run response: ' + JSON.stringify(data));

    return {
      runId: data.id || null,          // e.g. "run_abc123"
      threadId: data.thread_id || null // e.g. "thread_abc123"
    };
  } catch (err) {
    Logger.log('Error while creating run: ' + err);
    return { runId: null, threadId: null };
  }
}

function fetchAssistantMessage(openAiThreadId='thread_jTg2nGhtBvju7nYrSdhHrPDh') {
  Logger.log('Fetching final assistant message for OpenAI thread: ' + openAiThreadId);

  const getMessagesUrl = `https://api.openai.com/v1/threads/${openAiThreadId}/messages`;
  const response = UrlFetchApp.fetch(getMessagesUrl, {
    method: 'get',
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      'OpenAI-Beta': 'assistants=v2'
    },
    muteHttpExceptions: true
  });

  const data = JSON.parse(response.getContentText());
  Logger.log('Thread messages response: ' + JSON.stringify(data));

  const messages = data.data || data.messages || [];

  // Find the last assistant message that has content
  for (let i = messages.length - 1; i >= 0; i--) {
    const msg = messages[i];
    if (msg.role === 'assistant' && msg.content && msg.content.length > 0) {
      // Concatenate .text.value parts into a single string
      let combinedText = '';
      for (const segment of msg.content) {
        if (segment.type === 'text' && segment.text && segment.text.value) {
          combinedText += segment.text.value;
        }
      }
      Logger.log('Assistant raw text: ' + combinedText);
      return combinedText; // Return the raw string
    }
  }
  return null;
}

function createRunAndWaitForReply(promptData = mockPrompt) {
  // Initiate a run
  const { runId, threadId } = createRun(promptData);
  if (!runId || !threadId) {
    Logger.log('Could not create run.');
    return null;
  }

  // Poll for a final assistant message
  const maxAttempts = 10;
  const waitMs = 3000; // 3 seconds
  let assistantText = null;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    Utilities.sleep(waitMs);
    assistantText = fetchAssistantMessage(threadId);
    if (assistantText) {
      Logger.log(`Assistant replied on attempt #${attempt}: ${assistantText}`);
      return assistantText;
    }
    Logger.log(`No assistant reply yet. Attempt #${attempt} of ${maxAttempts}...`);
  }

  Logger.log('No assistant reply within max attempts.');
  return null;
}
```