---
title: "Building an AI-Powered Discord Bot with Railway and Pinecone"
date: 2025-06-01
permalink: "/building-an-ai-powered-discord-bot-with-railway-and-pinecone/"
layout: "post"
excerpt: "Discord may be known for gaming, but it’s also widely used as a community and support forum for tech companies. Regardless of the use though, pretty much ever server has to deal with spam and scammers at some point. Discord has a few simple tools bui..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1748768084103/1ac03d56-8fc6-454c-9fe7-5e6ba0ba242a.png"
readTime: 5
tags: ["Python", "discord", "Pinecone", "AI Assistants ", "GitHub", "railway", "llm", "bot"]
series: "Artificial Intelligence"
---

Discord may be known for gaming, but it’s also widely used as a community and support forum for tech companies. Regardless of the use though, pretty much ever server has to deal with spam and scammers at some point. Discord has a few simple tools built-in to help combat this, but they don’t catch everything.

You can try to catch everything yourself, or maybe elevate some community members to moderators, but someone has to be online to see and remove the offending posts quickly. This is a perfect job for a Discord bot.

In this guide, I’ll show you how to build an AI-powered Discord bot using a Python script running in [Railway](https://railway.com/), and a [Pinecone](https://www.pinecone.io/) Assistant.

**This guide will cover:**

* Creating a Discord bot and installing it to a server
    
* Running the bot from a Python script in Railway
    
* Creating a Pinecone Assistant
    
* Integrating the Discord bot with Pinecone

Let’s get started!

## Creating a Discord bot

Start out by going to the [Discord Applications](https://discord.com/developers/applications) page click **New Application**. Give it a name, agree to the terms, and click **Create**. This will take you to the app’s setting page.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748719198636/cb6ed2d3-c095-42fa-8075-46829ffb385d.png)

Go to the **Bot** section on the left sidebar, and then scroll down to **Privileged Gateway Intents**.

* enable SERVER MEMBERS INTENT
    
* enable MESSAGE CONTENT INTENT

Scroll down to Bot Permissions and enable:

✅ View Channels  
✅ Send Messages  
✅ Manage Messages (required to delete messages)  
✅ Read Message History

Be sure to click **SAVE** before installing the bot in the next step!

## Installing the bot to a server

Ok, the bot is created and the permissions are set, but we haven’t added the bot to a server yet. Next, go to the **OAuth2** tab.

Scroll down to the **Scopes** section and enable the `bot` scope. Then, under Bot Permissions, enable:

* Send Messages
    
* Send Messages in Threads
    
* Read Message History
    
* View Channels

But wait, didn’t we just turn on those same settings in the Bot section? Kind of… In the Bot section, you’re setting the max settings this Discord app should ever have, no matter where it’s installed. Then, in the OAuth2 section, you are selecting the permissions for a single install of the bot on a specific server. You can request up-to the same permissions as the Bot tab, but not more.

Scroll to the bottom and copy the GENERATED URL. This URL contains a `permissions=#` parameter, where the number is a unique integer representing the exact combination of permissions you’ve selected.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748719849255/bfcf5a07-fa84-4aad-a349-4b737967d9a6.png)

Open the URL and you should be prompted to install the bot to a server. Select your server, and authorize the bot.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748719903711/45e58b9d-9a61-4ad5-a034-ab53ab74b655.png)

Alright, the bot has been added to the server. You should see a welcome message in the server chat.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748720026643/b3132490-6620-46c1-8ab5-8822f023fc0c.png)

At this point, the bot has permissions to begin posting in the channel. But we don’t actually have a bot running anywhere. We need to set up a server where the bot can run and listen for messages to reply to.

## Running the bot from a Python script in Railway

Up to this point, I’ve used ‘bot’ to refer to the application we created in Discord, and the settings and permissions that go with it. But that’s just part of the solution. It’s more like an account or identity for the bot, not the bot itself. The logic and actions come from running custom code to interact the bot account and the server where the bot is installed.

For this guide, I’ll be using Railway to run a Python script to act as our bot. Railway offers a free *trial* with no credit card required. There are some free alternatives, but they require work-arounds to keep the bot awake and online. If you prefer a completely free service, try Replit’s free tier and search ‘Discord bot keep alive’ for a workaround to keep the bot from going to sleep.

### Bot GitHub Repo

Start out by creating a GitHub repo for the project. You can make it private if you want. Add the three files below:

**runtime.txt**

```plaintext
python-3.11.8
```

**requirements.txt**

```plaintext
discord.py==2.3.2
pinecone
```

**main.py**

```python
import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if bot.user in message.mentions:
        await message.reply("Hello from Discord-bot!")  # ⬅️ reply to original message

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
```

This will start up the bot and log it into any server where it has been installed (using the generated link), then run the `on_message()` function whenever a message is posted. The function then checks to see if the bot was mentioned, and if so, replies ‘Hello from Discord-bot!’.

Once you have these 3 files saved to a new repo, head over to the [account page](https://railway.com/account) in Railway and connect GitHub, then select your repo. If you’ve already connected GitHub for a different repo, click the **Edit Scopes** button to add a new repo.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748724322960/8467ab33-59e6-4737-8927-8c95d9799696.png)

Then create a [new project](https://railway.com/new) and select the repo as the source. You should see the new project open up, and the server automatically building and deploying. Give it a few minutes to finish. You’ll eventually see a green status saying the deployment was successful, followed by a red status saying the server crashed.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748724568004/0d50bc98-e1fd-468d-b9f3-2c2d8a3ab2cf.png)

This is because the server is missing the Discord bot token in the environment variables. Head back to the Discord App’s setting page and go to the Bot section. Click **Reset Token** to generate a new token.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748724836235/c0d65d6c-1367-4edd-8e17-57e705adc62f.png)

Then add the token as a new variable in Railway, with the key `DISCORD_TOKEN`.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748724839858/3d76bfdc-e0fd-4a11-a75a-577ce609497d.png)

Lastly, click **Deploy** to apply the changes.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748724900520/a9e8da40-b1be-484d-a673-39da95f04a95.png)

The server should automatically rebuild and deploy. Once the status shows it’s running, click to view the logs. You should see the log entry showing the bot logging into the server.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748725368805/81cdf142-3bfc-4b67-844d-2e4cd8f627af.png)

Ok, the bot is running and logged into the server. Now go to the Discord server, and mention the bot in a new message.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748725430152/6bcee778-121c-4b9a-bbd2-6d4fcb1ea449.png)

Awesome! The bot is listening to messages, and responding when mentioned. But the response is hard-coded. To get a real reply, we need to send the message to an LLM and generate a response, then send that back to Discord.

## Creating a Pinecone Assistant

Next, create a free [Pinecone account](https://www.pinecone.io/) and go to the Dashboard. Then create a new assistant.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748725730553/297dfc36-6631-44f0-a4c5-6f9b81557918.png)

Give it a name and click **Create assistant**.

Next, the assistant needs at least one file to reference. Pinecone’s Assistant’s are made for performing RAG (Retrieval-Augmented Generation), and the chat won’t work until you’ve added at least one file. This can be anything you want the bot to reference to help answer questions, like software documentation, example responses, or other instructions.

In my case, I added a text file with some common questions and responses, and a list of banned topics.

**instructions.txt**

```plaintext
# Common questions and responses
- User asks about contributing to Appsmith
- - Thank them for their interest. Direct them to: https://github.com/appsmithorg/appsmith/blob/release/CONTRIBUTING.md

- Any question about licensing, pricing, business/enterprise features
- - Direct them to sales@appsmith.com

# Banned Topics
Use this list of banned topics to identify messages that should be flagged for removal. 

- Invitations to cyrpto discords, or anything crypto related that doesn't involve an Appsmith app building question. 
- Posting a full CV or resume. It's ok to introduce yourself and mention some skills, but don't advertize your services here. 
- anything NSFW related. It's ok to use a bad word or two, but no NSFW topics.
```

There’s also the Assistant Instructions field where you can add more instructions for how the assistant should respond. Enter a description of the bot and it’s purpose.

```plaintext
You are an assistant that responds to users on Discord. Read their message and reply as a helpful Discord bot. Your job is to supplement the main Appsmith Discord support bot, by monitoring the other channels outside of actual product support. 

Users sometimes mistakenly ask support questions in the wrong channel. Direct them to post in #support for Appsmith support questions. 

If any of the banned topics are mentioned, respond only with: 
This message should be deleted.
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748769490614/e49d4659-aa04-4852-8146-da56dd01a366.png)

Next, go to the **API Keys** tab and create a new API key. Then add it as a new variable in Railway with the key `PINECONE_API_KEY`. Click **Deploy**.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748726516283/2f1ac27a-025d-4f58-bc7a-16fd9653e92a.png)

## Integrating the Discord bot with Pinecone

Alright, we have a bot that can listen for mentions and respond with a hard-coded reply. And now we have a Pinecone assistant that can generate real replies. Now we need a script to tie it all together.

For my use case, I have a few banned topics, where I want to delete the message instead of replying. This means ALL messages need to be sent to the assistant, even if the bot isn’t mentioned. The assistant will look for banned topics first, and reply that the message should be deleted. Then, only if the bot was mentioned (and the topic isn’t banned), it will reply to that thread.

You don’t want to have to mention the bot every time though, if you’re in a thread where it has already replied. So I’ve added some logic to only require the mention once, then the bot continues to reply on that thread.

Here’s the resulting script:

```python
import os
import discord
from discord.ext import commands
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Pinecone Assistant setup
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
assistant = pc.assistant.Assistant(assistant_name="railway-discord-bot")

# Track channels (including threads) where the bot was mentioned
active_channels = set()

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    channel_id = message.channel.id
    mentioned = bot.user in message.mentions
    is_thread = isinstance(message.channel, discord.Thread)

    # Track channels where bot was mentioned for future replies
    if mentioned:
        active_channels.add(channel_id)

    # Always send every message to Pinecone
    query = message.clean_content.replace(f"@{bot.user.name}", "").strip()

    try:
        msg = Message(content=query or "[empty]")
        response = assistant.chat(messages=[msg])
        content = response["message"]["content"]

        # Always check for deletion
        if content.strip() == "This message should be deleted.":
            await message.delete()
            return

        # Only reply if mentioned or in active channel
        if mentioned or channel_id in active_channels:
            await message.reply(content[:2000])

    except Exception as e:
        if mentioned or channel_id in active_channels:
            await message.reply(f"❌ Error: {e}")

    await bot.process_commands(message)

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
```

Update the repo with the new `main.py` file, and the server should redeploy automatically.

Once the server is running again, send a new test message and mention the bot.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748727160524/06731735-2b82-42ea-9f89-64f6c4a81a9a.png)

Ok, the assistant is replying now. Let’s test one of those banned topics.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748727262761/aa774e63-cd5b-4636-b57f-c374a71c94a0.gif)

Awesome! The Pinecone assistant recognized the banned topic and responded with the trigger phrase to mark it for deletion. Then the Python code deleted the message almost instantly!

## Conclusion

Setting up a Discord bot is a great way to moderate a server and assist members with common questions. You can adjust the assistant instructions and knowledge sources to create bots for customer support, or just use them to scan for and remove banned content. The [Discord.py](https://discordpy.readthedocs.io/en/stable/) library makes it easy to set up with only a few lines of code, which can be hosted on Railway, [Replit](https://replit.com/), [AWS Lambda](https://aws.amazon.com/lambda/), or any other Python hosting platform.