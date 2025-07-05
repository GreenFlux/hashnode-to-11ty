---
title: "Saving Files to Google Drive by POST-ing the Url to a Web App"
date: 2021-07-25
permalink: "/saving-files-to-google-drive-by-post-ing-the-url-to-a-web-app/"
layout: "post"
excerpt: "In this tutorial, I'll be writing a general purpose Apps Script Web App to save a cloud-hosted file to Google Drive as a new file, when the original file url is POST-ed to the script's web app endpoint.
function getFileByUrl(url , folderId){
  // Dow..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1627213302520/-IEe36ZNq.png"
readTime: 5
tags: ["Google", "google cloud", "JavaScript", "Tutorial", "APIs"]
series: "Google Apps Script"
---

In this tutorial, I'll be writing a general purpose Apps Script [Web App](https://developers.google.com/apps-script/guides/web) to save a cloud-hosted file to Google Drive as a new file, when the original file url is POST-ed to the script's web app endpoint.

```json
function getFileByUrl(url , folderId){
  // Download file from Url and save to specified folder
  return newFileUrl
  ...
}
```

The script will be published as a web app so that POST requests can be sent from other apps/services, allowing integrations with any REST API.

```json
function doPost(e) {
  // POST Request Received, containing fileUrl and folderId
  ...
      returnedUrl = getFileByUrl(fileUrl, folderId);

  return ContentService.createTextOutput(returnedUrl)
}
```

## Use Cases

* Copy images/files from 3rd party app or API
    
* Loop through a spreadsheet of file urls
    
* Scrape image/file urls from a web page

### DoPost() - Requirements for web apps:

> A script can be published as a web app if it meets these requirements:
> 
> It contains a doGet(e) or doPost(e) function.
> 
> The function returns an HTML service HtmlOutput object or a Content service TextOutput object.

1. Start with a basic doPost() function that returns a url.

```json
function doPost(e) {
  let returnedUrl = 'https://indico.cern.ch/event/853710/contributions/3708132/attachments/1985053/3307323/Armina_Abramyan_JS_for_Science.pdf';

  return ContentService.createTextOutput(returnedUrl)
}
```

2. Name, save and then publish as a web app: `Execute as: *Me*, Who has access: *Anyone*`
    
3. Send a test POST to the new published URL
    
    ![Screen Shot 2021-07-25 at 9.00.00 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1627218007410/aFH2zDUV4z.png)

Ok, the doPost() responds to our POST request and returns a file url. Now let's create a function that GETs a file from a url and saves it to Google Drive.

```json
function getFileByUrl(url, folderId){
  // Download file from url and save to GDrive folder with fileName

  const fileData = UrlFetchApp.fetch(url);
  const folder = DriveApp.getFolderById(folderId);
  const fileName = url.split('/').pop(); // last value = file name in last folder, url/folder/filename.type
  const newFileUrl = folder.createFile(fileData).setName(fileName).getUrl();
  Logger.log(newFileUrl);
  return newFileUrl;

}
```

> `const fileName = url.split('/').pop();`

The split() method creates an array of strings from the url, with the last value being the text after the last forward slash. https://indico.cern.ch/event/853710/contributions/3708132/attachments/1985053/3307323/`Armina_Abramyan_JS_for_Science.pdf` And the pop() array method returns the last value, to be used as the new file name!

Now the getFileByUrl() function can be inserted into the doPost().

```json
function doPost(e) {

  const fileUrl = 'https://www.evl.uic.edu/luc/bvis546/Essential_Javascript_--_A_Javascript_Tutorial.pdf';
  const folderId = '{FOLDER_ID}';
  returnedUrl = getFileByUrl(fileUrl, folderId);
  return ContentService.createTextOutput(returnedUrl)
}
```

PUBLISH and Retest.

![Screen Shot 2021-07-25 at 9.18.40 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1627219153918/scNWuDaZ9.png)

![image.png](https://media.giphy.com/media/xT5LMHxhOfscxPfIfm/giphy.gif)

SUCCESS! The script created a new copy of the file in Google Drive!

![Screen Shot 2021-07-25 at 9.22.48 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1627219372636/qLAdeGq7F.png)

Finally, to dynamically pass the url and folderId, and an API key as a security check:

```json
function doPost(e) {
  let returnedUrl = '';

  if(e.parameter.key == key && 'fileUrl' in e.parameter){
    const fileUrl = decodeURI(e.parameter.fileUrl);
    const folderId = decodeURI(e.parameter.folderId);
    returnedUrl = getFileByUrl(fileUrl, folderId);
  }
  return ContentService.createTextOutput(returnedUrl)
}
```

Now we can POST to the web app using the following url parameters:

```json
{
  key: 'API_KEY',
  fileUrl: 'FULL_URL_TO_FILE',
  folderId: 'ID_OF_DRIVE_FOLDER'
}
```

![Screen Shot 2021-07-25 at 9.34.34 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1627220175285/_iJ2aDnOa.png)

## Here's the finished script:

```json
const key = 'APIKEY';  // custom string to check before returning contacts
const defaultFolder = 'OPTIONAL_FOLDER_ID'; // folder to use if no id is given
const defaultUrl = 'https://www.acquisition.gov/sites/default/files/current/dfars/pdf/DFARS.pdf';

function doPost(e) {
  let responseBody = {'requestEvent':e};
  let returnedUrl = '';

  if(e.parameter.key == key && 'fileUrl' in e.parameter){
    const fileUrl = decodeURI(e.parameter.fileUrl);
    const folderId = decodeURI(e.parameter.folderId);
    returnedUrl = getFileByUrl(fileUrl, folderId);
  }
  return ContentService.createTextOutput(returnedUrl)
}

function getFileByUrl(url = defaultUrl, folderId = defaultFolder){
  // Download file from url and save to GDrive folder with fileName

  const fileData = UrlFetchApp.fetch(url);
  const folder = DriveApp.getFolderById(folderId);
  const fileName = url.split('/').pop(); // last value = file name in last folder, url/folder/filename.type
  const newFileUrl = folder.createFile(fileData).setName(fileName).getUrl();
  Logger.log(newFileUrl);
  return newFileUrl;

}
```

---

#### Thanks for reading!

Comment below with any questions or ideas for other use cases.