---
title: "Save files to Google Drive by POST-ing the URL to a web app"
date: 2023-06-09
permalink: "/save-files-to-google-drive-by-post-ing-the-url-to-a-web-app/"
layout: "post"
excerpt: "I just found an old script I wrote that others might find useful, so I wanted to share. This script saves a file to Google Drive when you POST its URL to the webapp, using this format:
{
  'key': 'APIKEY',
  'fileUrl': 'https://upload.wikimedia.org/w..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1686327110546/5d109736-bf60-4079-860c-601a332f6452.png"
readTime: 5
tags: ["google apps script", "APIs", "Google Drive", "JavaScript"]
---

I just found an old script I wrote that others might find useful, so I wanted to share. This script saves a file to Google Drive when you POST its URL to the webapp, using this format:

```javascript
{
  'key': 'APIKEY',
  'fileUrl': 'https://upload.wikimedia.org/wikipedia/commons/0/07/Reddit_icon.svg',
  'folderId': 'FOLDER_ID'
}
```

The script checks the POST body for the API key, then saves the file to the specified folder in Google Drive.

Just publish as a web app, and set the permissions to:  
\- *Execute as:* ***ME***  
\- *Who has access:* ***ANYONE***

```javascript
const key = 'APIKEY'; // custom string to check in request body
const defaultFolder = 'FOLDER_ID_FROM_URL'; // folder to use if no id is given
const defaultUrl = 'https://upload.wikimedia.org/wikipedia/commons/0/07/Reddit_icon.svg';

function doPost(e) {
  let returnedUrl = '';
  let request = JSON.parse(e.postData.contents);
  if (request.key == key && 'fileUrl' in request) {
    returnedUrl = getFileByUrl(request.fileUrl, request.folderId);
  }
  return ContentService.createTextOutput(returnedUrl)
}

function getFileByUrl(url = defaultUrl, folderId = defaultFolder) { 
  // Download file from url and save to GDrive folder with fileName
  const fileData = UrlFetchApp.fetch(url);
  const folder = DriveApp.getFolderById(folderId);
  const fileName = url.split('/').pop(); 
  // string after last forwardslash: url/folder/filename.type
  const newFileUrl = folder.createFile(fileData).setName(fileName).getUrl();
  Logger.log(newFileUrl);
  return newFileUrl;
}
```

I've used this on several jobs to send files from other platforms to Google Drive. Hope someone finds this helpful!