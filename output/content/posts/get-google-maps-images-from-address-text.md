---
title: "GET Google Maps Images from Address Text"
date: 2021-07-17
permalink: "/get-google-maps-images-from-address-text/"
layout: "post"
excerpt: "Today I will be integrating with Google's Static Maps API and using Appsmith to retrieve a map image, given a text-string street address.
There's a bit of setup involved if you've never used the Google Cloud Platform before. You'll have to accept the..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1626536051582/IdmkSJI5M.png"
readTime: 5
tags: ["Google", "google maps", "APIs", "REST API", "Tutorial"]
series: "Appsmith"
---

{% raw %}
### Today I will be integrating with Google's Static Maps API and using Appsmith to retrieve a map image, given a text-string street address.

There's a bit of setup involved if you've never used the Google Cloud Platform before. You'll have to accept the terms and set up billing, but you can also get a free trial if haven't used it yet.

Google's own guides on enabling the API and creating a project are great, so I'm just going to link them here and skip to the fun stuff.

## 📍 Enable the Static Maps API

* [Create a New Project](https://console.cloud.google.com/projectcreate)
    
* Enable the [Static Maps API](https://developers.google.com/maps/gmp-get-started)
    
* [Create Credentials](https://developers.google.com/workspace/guides/create-credentials)

# ⚙️ Appsmith Setup

* Add new Datasource: Create New&gt; API &gt; GET

**Parameters:**

```json
{
  sensor: false,
  center: {{address.text.replace(/\W/g,'+')}},
  key: 'YOUR_API_KEY',
  size: '512x512'
}
```

* Add new Widgets

| Type | Name | Value/ Settings |
| --- | --- | --- |
| **Input** | address | **OnTextChange:** `{{function({if(live.isSwitchedOn{addressToImage.run()}}()}}` |
| **Switch** | live | **Default:** Off |
| **Button** | submit | **Run a Query:** addressToImage |
| **Image** | image | `{{addressToImage.data}}` |

![2021-07-17 12.58.04.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626541152459/nlgE1ESp_T.gif)

# DEPLOY! 🚀

![2021-07-17 11.27.42.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626535698182/czJdCEVsP.gif)

# WARNING! ☠️⚠️

### I don't recommend using the live search in a public app or anything with a lot of users.

It's just a fun experiment to see the image update in real time as you type. But it'll definitely rack up some charges quick if you're not careful.

---

## Thanks for reading! This was a fun one 🤓

Here's the entire app definition for anyone that wants to skip the build and just import the app.

```json
{"exportedApplication":{"userPermissions":["manage:applications","canComment:applications","export:applications","read:applications","publish:applications","makePublic:applications"],"name":"Map Image Extractor","isPublic":false,"appIsExample":false,"unreadCommentThreads":0,"color":"#A8D76C","icon":"location","appLayout":{"type":"DESKTOP"},"new":true},"datasourceList":[],"pageList":[{"userPermissions":["read:pages","manage:pages"],"unpublishedPage":{"name":"Page1","layouts":[{"id":"60f2b0955686e31913efe828","userPermissions":[],"dsl":{"widgetName":"MainContainer","backgroundColor":"none","rightColumn":1280,"snapColumns":64,"detachFromLayout":true,"widgetId":"0","topRow":0,"bottomRow":880,"containerStyle":"none","snapRows":125,"parentRowSpace":1,"type":"CANVAS_WIDGET","canExtend":true,"version":27,"minHeight":890,"parentColumnSpace":1,"dynamicTriggerPathList":[],"dynamicBindingPathList":[],"leftColumn":0,"children":[{"backgroundColor":"#FFFFFF","widgetName":"Container1","rightColumn":36,"widgetId":"s9pgimssky","containerStyle":"card","topRow":1,"bottomRow":59,"parentRowSpace":10,"isVisible":true,"type":"CONTAINER_WIDGET","version":1,"parentId":"0","isLoading":false,"parentColumnSpace":19.8125,"leftColumn":0,"children":[{"widgetName":"Canvas1","rightColumn":634,"detachFromLayout":true,"widgetId":"mv8rqf5log","containerStyle":"none","topRow":0,"bottomRow":400,"parentRowSpace":1,"isVisible":true,"canExtend":false,"type":"CANVAS_WIDGET","version":1,"parentId":"s9pgimssky","minHeight":580,"isLoading":false,"parentColumnSpace":1,"dynamicTriggerPathList":[],"leftColumn":0,"dynamicBindingPathList":[],"children":[{"image":"{{addressToImage.data}}","widgetName":"image","rightColumn":52,"objectFit":"cover","widgetId":"si6a53w6f1","topRow":10,"bottomRow":46,"parentRowSpace":10,"isVisible":true,"type":"IMAGE_WIDGET","version":1,"parentId":"mv8rqf5log","isLoading":false,"maxZoomLevel":1,"enableDownload":false,"parentColumnSpace":18.409375,"dynamicTriggerPathList":[],"imageShape":"RECTANGLE","leftColumn":0,"dynamicBindingPathList":[{"key":"defaultImage"},{"key":"image"}],"enableRotation":false,"defaultImage":"{{addressToImage.data}}"},{"widgetName":"address","dynamicPropertyPathList":[{"key":"onTextChanged"}],"onSubmit":"","topRow":4,"bottomRow":8,"parentRowSpace":10,"type":"INPUT_WIDGET","parentColumnSpace":19.8125,"dynamicTriggerPathList":[{"key":"onTextChanged"},{"key":"onSubmit"}],"resetOnSubmit":false,"leftColumn":0,"dynamicBindingPathList":[],"inputType":"TEXT","placeholderText":"address","isDisabled":false,"isRequired":false,"onTextChanged":" {{function(){\nif(live.isSwitchedOn){addressToImage.run()}\n}()}}","rightColumn":36,"widgetId":"1ovbcudtlz","isVisible":true,"label":"","version":1,"parentId":"mv8rqf5log","isLoading":false,"defaultText":""},{"widgetName":"live","rightColumn":52,"widgetId":"860098p531","topRow":0,"bottomRow":4,"parentRowSpace":10,"isVisible":true,"label":"live search","type":"SWITCH_WIDGET","defaultSwitchState":true,"version":1,"alignWidget":"LEFT","parentId":"mv8rqf5log","isLoading":false,"parentColumnSpace":19.8125,"dynamicTriggerPathList":[],"leftColumn":38,"dynamicBindingPathList":[],"isDisabled":false},{"widgetName":"submit","rightColumn":52,"onClick":"{{addressToImage.run()}}","isDefaultClickDisabled":true,"widgetId":"1jslvl8hbw","buttonStyle":"PRIMARY_BUTTON","topRow":4,"bottomRow":8,"recaptchaV2":false,"parentRowSpace":10,"isVisible":true,"type":"BUTTON_WIDGET","version":1,"parentId":"mv8rqf5log","isLoading":false,"parentColumnSpace":19.8125,"dynamicTriggerPathList":[{"key":"onClick"}],"leftColumn":38,"dynamicBindingPathList":[],"text":"Submit","isDisabled":false},{"widgetName":"Text1","rightColumn":36,"textAlign":"LEFT","widgetId":"muibkh17ic","topRow":0,"bottomRow":4,"parentRowSpace":10,"isVisible":true,"fontStyle":"BOLD","type":"TEXT_WIDGET","textColor":"#231F20","version":1,"parentId":"mv8rqf5log","isLoading":false,"parentColumnSpace":19.5,"dynamicTriggerPathList":[],"leftColumn":0,"dynamicBindingPathList":[],"fontSize":"PARAGRAPH","text":"Google - Static Maps API"}]}]}]},"layoutOnLoadActions":[[{"id":"60f2b0ac5686e31913efe82a","name":"addressToImage","pluginType":"API","jsonPathKeys":["address.text.replace(/\\W/g,'+')"],"timeoutInMillisecond":10000}]],"new":false}],"userPermissions":[]},"publishedPage":{"name":"Page1","layouts":[{"id":"60f2b0955686e31913efe828","userPermissions":[],"dsl":{"widgetName":"MainContainer","backgroundColor":"none","rightColumn":1280,"snapColumns":64,"detachFromLayout":true,"widgetId":"0","topRow":0,"bottomRow":880,"containerStyle":"none","snapRows":125,"parentRowSpace":1,"type":"CANVAS_WIDGET","canExtend":true,"version":27,"minHeight":890,"parentColumnSpace":1,"dynamicTriggerPathList":[],"dynamicBindingPathList":[],"leftColumn":0,"children":[{"backgroundColor":"#FFFFFF","widgetName":"Container1","rightColumn":36,"widgetId":"s9pgimssky","containerStyle":"card","topRow":1,"bottomRow":59,"parentRowSpace":10,"isVisible":true,"type":"CONTAINER_WIDGET","version":1,"parentId":"0","isLoading":false,"parentColumnSpace":19.8125,"leftColumn":0,"children":[{"widgetName":"Canvas1","rightColumn":634,"detachFromLayout":true,"widgetId":"mv8rqf5log","containerStyle":"none","topRow":0,"bottomRow":400,"parentRowSpace":1,"isVisible":true,"canExtend":false,"type":"CANVAS_WIDGET","version":1,"parentId":"s9pgimssky","minHeight":580,"isLoading":false,"parentColumnSpace":1,"dynamicTriggerPathList":[],"leftColumn":0,"dynamicBindingPathList":[],"children":[{"image":"{{addressToImage.data}}","widgetName":"image","rightColumn":52,"objectFit":"cover","widgetId":"si6a53w6f1","topRow":10,"bottomRow":46,"parentRowSpace":10,"isVisible":true,"type":"IMAGE_WIDGET","version":1,"parentId":"mv8rqf5log","isLoading":false,"maxZoomLevel":1,"enableDownload":false,"parentColumnSpace":18.409375,"dynamicTriggerPathList":[],"imageShape":"RECTANGLE","leftColumn":0,"dynamicBindingPathList":[{"key":"defaultImage"},{"key":"image"}],"enableRotation":false,"defaultImage":"{{addressToImage.data}}"},{"widgetName":"address","dynamicPropertyPathList":[{"key":"onTextChanged"}],"onSubmit":"","topRow":4,"bottomRow":8,"parentRowSpace":10,"type":"INPUT_WIDGET","parentColumnSpace":19.8125,"dynamicTriggerPathList":[{"key":"onTextChanged"},{"key":"onSubmit"}],"resetOnSubmit":false,"leftColumn":0,"dynamicBindingPathList":[],"inputType":"TEXT","placeholderText":"address","isDisabled":false,"isRequired":false,"onTextChanged":" {{function(){\nif(live.isSwitchedOn){addressToImage.run()}\n}()}}","rightColumn":36,"widgetId":"1ovbcudtlz","isVisible":true,"label":"","version":1,"parentId":"mv8rqf5log","isLoading":false,"defaultText":""},{"widgetName":"live","rightColumn":52,"widgetId":"860098p531","topRow":0,"bottomRow":4,"parentRowSpace":10,"isVisible":true,"label":"live search","type":"SWITCH_WIDGET","defaultSwitchState":true,"version":1,"alignWidget":"LEFT","parentId":"mv8rqf5log","isLoading":false,"parentColumnSpace":19.8125,"dynamicTriggerPathList":[],"leftColumn":38,"dynamicBindingPathList":[],"isDisabled":false},{"widgetName":"submit","rightColumn":52,"onClick":"{{addressToImage.run()}}","isDefaultClickDisabled":true,"widgetId":"1jslvl8hbw","buttonStyle":"PRIMARY_BUTTON","topRow":4,"bottomRow":8,"recaptchaV2":false,"parentRowSpace":10,"isVisible":true,"type":"BUTTON_WIDGET","version":1,"parentId":"mv8rqf5log","isLoading":false,"parentColumnSpace":19.8125,"dynamicTriggerPathList":[{"key":"onClick"}],"leftColumn":38,"dynamicBindingPathList":[],"text":"Submit","isDisabled":false},{"widgetName":"Text1","rightColumn":36,"textAlign":"LEFT","widgetId":"muibkh17ic","topRow":0,"bottomRow":4,"parentRowSpace":10,"isVisible":true,"fontStyle":"BOLD","type":"TEXT_WIDGET","textColor":"#231F20","version":1,"parentId":"mv8rqf5log","isLoading":false,"parentColumnSpace":19.5,"dynamicTriggerPathList":[],"leftColumn":0,"dynamicBindingPathList":[],"fontSize":"PARAGRAPH","text":"Google - Static Maps API"}]}]}]},"layoutOnLoadActions":[[{"id":"60f2b0ac5686e31913efe82a","name":"addressToImage","pluginType":"API","jsonPathKeys":["address.text.replace(/\\W/g,'+')"],"timeoutInMillisecond":10000}]],"new":false}],"userPermissions":[]},"new":true}],"publishedDefaultPageName":"Page1","unpublishedDefaultPageName":"Page1","actionList":[{"id":"60f2b0ac5686e31913efe82a","userPermissions":["read:actions","execute:actions","manage:actions"],"pluginType":"API","pluginId":"restapi-plugin","unpublishedAction":{"name":"addressToImage","datasource":{"userPermissions":[],"name":"DEFAULT_REST_DATASOURCE","pluginId":"restapi-plugin","datasourceConfiguration":{"url":"https://maps.google.com"},"invalids":[],"isValid":true,"new":true},"pageId":"Page1","actionConfiguration":{"timeoutInMillisecond":10000,"paginationType":"NONE","path":"/maps/api/staticmap","headers":[{"key":"","value":""},{"key":"","value":""}],"encodeParamsToggle":true,"queryParameters":[{"key":"sensor","value":"false"},{"key":"center","value":"{{address.text.replace(/\\W/g,'+')}}"},{"key":"key","value":"YOUR_API_KEY"},{"key":"size","value":"512x512"}],"body":"","httpMethod":"GET","pluginSpecifiedTemplates":[{"value":true}]},"executeOnLoad":true,"dynamicBindingPathList":[{"key":"queryParameters[1].value"}],"isValid":true,"invalids":[],"jsonPathKeys":["address.text.replace(/\\W/g,'+')"],"confirmBeforeExecute":false,"userPermissions":[]},"publishedAction":{"name":"addressToImage","datasource":{"userPermissions":[],"name":"DEFAULT_REST_DATASOURCE","pluginId":"restapi-plugin","datasourceConfiguration":{"url":"https://maps.google.com"},"invalids":[],"isValid":true,"new":true},"pageId":"Page1","actionConfiguration":{"timeoutInMillisecond":10000,"paginationType":"NONE","path":"/maps/api/staticmap","headers":[{"key":"","value":""},{"key":"","value":""}],"encodeParamsToggle":true,"queryParameters":[{"key":"sensor","value":"false"},{"key":"center","value":"{{address.text.replace(/\\W/g,'+')}}"},{"key":"key","value":"YOUR_API_KEY"},{"key":"size","value":"512x512"}],"body":"","httpMethod":"GET","pluginSpecifiedTemplates":[{"value":true}]},"executeOnLoad":true,"dynamicBindingPathList":[{"key":"queryParameters[1].value"}],"isValid":true,"invalids":[],"jsonPathKeys":["address.text.replace(/\\W/g,'+')"],"confirmBeforeExecute":false,"userPermissions":[]},"new":false}],"decryptedFields":{},"publishedLayoutmongoEscapedWidgets":{},"unpublishedLayoutmongoEscapedWidgets":{}}
```
{% endraw %}