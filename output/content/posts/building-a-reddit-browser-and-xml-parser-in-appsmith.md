---
title: "Building a Reddit Browser (and XML Parser) in Appsmith"
date: 2021-07-21
permalink: "/building-a-reddit-browser-and-xml-parser-in-appsmith/"
layout: "post"
excerpt: "Did you know you can turn almost any sub-Reddit into an RSS feed by adding .RSS to the url?!

RSS? Ok, by why is this useful? 🤨
Because it's basically an API to GET the recent posts, in XML format, without all the setup of enabling the API!!

And wi..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1626825294574/ePvyhIJeB.png"
readTime: 5
tags: ["xml", "rss", "Devops", "Tutorial", "7daystreak"]
series: "Appsmith"
---

{% raw %}
## Did you know you can turn almost any sub-Reddit into an RSS feed by adding `.RSS` to the url?!

![shocked](https://media.giphy.com/media/SJX3gbZ2dbaEhU92Pu/giphy.gif)

### RSS? Ok, by why is this useful? 🤨

**Because it's basically an API to GET the recent posts, in XML format, without all the setup of enabling the API!!**

![Screen Shot 2021-07-20 at 7.33.48 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626824033656/ESM_NzLBZ.png)

And with a little data transformation using Appsmith, the raw XML can easily be turned into an array of JSON objects to build a feed viewer. From there, all kinds of other integrations could be built, passing data from the selected feed to the next function. 

**For this tutorial, I'll be parsing data from www.Reddit.com using the `.RSS` url, but this method could be applied for viewing any XML data source.** 

## ⚙️ Setup

### Create a new Appsmith app and add the following Widgets:
![2021-07-20 19.36.18.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626824203045/yf44xZTMB.gif)

|Name|Type|
|---|---|
|subreddit|Input/Text|
|results|Table|
|update|Button|
|preview|Iframe|

1. Add a new Datasource>APIs>Create New: `Name: getXML`
```GET: https://www.reddit.com/r/{{subreddit.text}}/.rss```
2. Enter a sub-reddit name in the subreddit Input Widget
3. Run `getXML`

Now that the API response is populated, the auto-complete will help us navigate the results and bind the correct property of the response to a the `results` table Widget. 
4. Bind the `results` Table-Widget to the `getXML` API
```{{xmlParser.parse(getXML.data).feed.entry}}```
![Screen Shot 2021-07-20 at 7.40.32 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626824450373/xM8sm89p-.png)
5. Bind the `preview` Iframe-Widget to the 3rd link in the `content` property of the "currentRow"
![Screen Shot 2021-07-20 at 7.47.44 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626824961173/vzkx864ZR.png)
6. **DEPLOY!** 🚀

![2021-07-20 19.49.59.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626825036971/-B-YEaa9v.gif)

___
{{results.selectedRow.content.split(`'&quot;'`)[3]}}

This line 'splits' the  `content` property of the `getXML` API results by the `&quote;` pattern, and creates and array from the results. The 4rd value in this list is the one we want for the preview, but the list is zero-based. So [3] gets the 4th item from the array. 

![2021-07-20 20.18.28.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626826737197/772LDjml7.gif)
___
Thanks for reading! Even though RSS isn't as popular these days for personal use, there are still TONS of uses for no-code solutions! Here are a few resources to help inspire your own integration:

https://rss.app/

https://rss2json.com/

https://www.listennotes.com/rss-viewer/

https://www.google.com/alerts

{% endraw %}