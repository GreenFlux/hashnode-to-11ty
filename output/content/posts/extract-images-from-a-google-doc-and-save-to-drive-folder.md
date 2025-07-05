---
title: "Extract Images from a Google Doc and Save to Drive Folder"
date: 2023-06-10
permalink: "/extract-images-from-a-google-doc-and-save-to-drive-folder/"
layout: "post"
excerpt: "Recently, I needed to export all the images from a Google Doc and upload them to another service. Seems like a simple job, right? You would think... but not so much.
Google Docs blocks the standard right-click context menu and replaces it with a cust..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1686404452524/69a630a7-b563-4211-a4c2-2b9718ade691.png"
readTime: 5
tags: ["google apps script", "Google Drive", "Google Docs"]
series: "Google Apps Script"
---

Recently, I needed to export all the images from a Google Doc and upload them to another service. Seems like a simple job, right? You would think... but not so much.

Google Docs blocks the standard *right-click* context menu and replaces it with a custom menu, so there's no `right-click > save image as` option.

There is an option to **Save to Keep**, and once saved, then you can right-click and `save image as`. But I had over 20 images to export, so I wanted to find a way to scrape the images all at once.

Realistically, it would have taken only 5-10 minutes of work. But that time would have felt like an eternity. Clicking in circles like a mindless robot.

No, I don't have time for such mindless tasks. I'd much rather spend 1.5 hours writing a script to do this one task that I'll probably never have to do again. But if I do, I'll have a script for it!

---

**This function takes the source Doc, loops through all images, and saves them to a Drive folder.**

You can specify a destination folder ID, or leave the second parameter blank and it will create a new *images* folder in the same folder as the source Doc (naming the images after the source doc + #).

```javascript
function getDocImages(sourceId, destinationId) {
  const sourceName = DriveApp.getFileById(sourceId).getName();
  const allImages  = DocumentApp.openById(sourceId).getBody().getImages();

  if(!destinationId){
    const parentId = DriveApp.getFileById(sourceId).getParents().next().getId();
    destinationId  = DriveApp.getFolderById(parentId).createFolder('images').getId()
    };

  const saveTo = DriveApp.getFolderById(destinationId) ;

  allImages.forEach( (i, idx) => saveTo.createFile(i.getAs('image/png').setName( `${sourceName}_${idx + 1}` )) )

}
```

I'll probably never need to do this again, but if anyone else does, I hope this helps.