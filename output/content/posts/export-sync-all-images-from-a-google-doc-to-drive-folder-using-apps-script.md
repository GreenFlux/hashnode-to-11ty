---
title: "Export & Sync All Images from a Google Doc to Drive Folder using Apps Script"
date: 2025-02-03
permalink: "/export-sync-all-images-from-a-google-doc-to-drive-folder-using-apps-script/"
layout: "post"
excerpt: "Adding images to a Google Doc is no problem, but getting them back out can be a pain. I’ve written about this before with Five Ways to Extract All Images From a Google Doc, and more recently, with this method using Python in Google Colab. However, al..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1738348625546/f6f9e069-e701-4410-84f8-1a5911af3de9.png"
readTime: 5
tags: ["google apps script", "Google", "JavaScript", "Google Docs", "Google Drive", "Low Code"]
series: "Google Apps Script"
---

Adding images to a Google Doc is no problem, but getting them back out can be a pain. I’ve written about this before with [Five Ways to Extract All Images From a Google Doc](https://community.appsmith.com/content/guide/five-ways-extract-all-images-google-doc), and more recently, with [this](https://blog.greenflux.us/extracting-all-images-from-a-google-doc-using-python) method using Python in Google Colab. However, all of those previous methods assumed you are working with a single folder or doc, and didn’t account for existing backup images from a previous run. Not ideal for running on a timer.

In this post, I’m sharing an updated version of the original Apps Script solution from the ‘Five Ways’ post, and adding some logic to handle running it on a timer. Here’s what all the script does:

* Scan for all Google Docs within a folder, and optionally scan subfolders
    
* Filter the list for all docs updated within the last 5 minutes
    
* Loop through each doc, and save images to a folder with matching name
    
* Skip existing images that have already been extracted
    
* Remove backup of images that have been removed from the doc
    
* Rename the backup folder if the doc name changes

With these changes, the script can be run on a timer, and automatically keep a folder of images synced with each source doc.

## Creating the Script

Start out by creating a new Apps Script by going to [script.new](https://script.new), or from the [Apps Script Projects](https://script.google.com/home) page. Name the script, then paste in this code:

```javascript
function extractImagesFromDocs() {
  // Configurable variables
  const ROOT_FOLDER_ID = 'YOUR_FOLDER_ID'; // Set the main folder ID
  const CHECK_SUBFOLDERS = false; // Set to true to include subfolders
  const TIME_THRESHOLD = 5 * 60 * 1000; // Last modified threshold (5 minutes)

  Logger.log("Starting extractImagesFromDocs...");
  
  const docs = getRecentDocs(ROOT_FOLDER_ID, CHECK_SUBFOLDERS, TIME_THRESHOLD);
  Logger.log(`Found ${docs.length} recent Google Docs.`);

  docs.forEach(processDocument);
}

/**
 * Get all recently modified Google Docs from a folder (and optionally subfolders)
 */
function getRecentDocs(folderId, includeSubfolders, timeThreshold) {
  const rootFolder = DriveApp.getFolderById(folderId);
  const docs = [];
  const now = Date.now();

  function scanFolder(folder) {
    Logger.log(`Scanning folder: ${folder.getName()}`);
    const files = folder.getFilesByType(MimeType.GOOGLE_DOCS);

    while (files.hasNext()) {
      const file = files.next();
      Logger.log(`Checking file: ${file.getName()} (Last updated: ${file.getLastUpdated()})`);
      
      if (now - file.getLastUpdated().getTime() <= timeThreshold) {
        Logger.log(`File selected: ${file.getName()} (ID: ${file.getId()})`);
        docs.push(file);
      }
    }

    if (includeSubfolders) {
      const subfolders = folder.getFolders();
      while (subfolders.hasNext()) {
        scanFolder(subfolders.next());
      }
    }
  }

  scanFolder(rootFolder);
  return docs;
}

/**
 * Process a Google Document: extract images and sync them with Drive
 */
function processDocument(file) {
  const docId = file.getId();
  const docName = file.getName();
  const parentFolder = file.getParents().next();

  Logger.log(`Processing document: ${docName} (ID: ${docId})`);

  // Ensure the folder is correctly named (rename if necessary)
  const folderName = `${docName}_${docId}`;
  let imageFolder = findFolderByDocId(parentFolder, docId);

  if (imageFolder) {
    if (imageFolder.getName() !== folderName) {
      Logger.log(`Renaming folder: ${imageFolder.getName()} → ${folderName}`);
      imageFolder.setName(folderName);
    }
  } else {
    Logger.log(`Creating new folder for document: ${folderName}`);
    imageFolder = parentFolder.createFolder(folderName);
  }

  const existingImages = getExistingImages(imageFolder);
  const docImages = DocumentApp.openById(docId).getBody().getImages();
  const newImageNames = new Set();

  Logger.log(`Found ${docImages.length} images in document: ${docName}`);

  // Extract and save new images
  docImages.forEach((img, idx) => {
    const imgName = `${docName}_${idx + 1}.png`;
    newImageNames.add(imgName);
    
    if (!existingImages.has(imgName)) {
      Logger.log(`Saving new image: ${imgName}`);
      imageFolder.createFile(img.getAs('image/png').setName(imgName));
    } else {
      Logger.log(`Skipping existing image: ${imgName}`);
    }
  });

  // Remove images that no longer exist in the document
  existingImages.forEach((fileId, name) => {
    if (!newImageNames.has(name)) {
      Logger.log(`Deleting removed image: ${name}`);
      DriveApp.getFileById(fileId).setTrashed(true);
    }
  });

  Logger.log(`Processing complete for document: ${docName}`);
}

/**
 * Find an existing folder based on the document ID in its name
 */
function findFolderByDocId(parentFolder, docId) {
  Logger.log(`Searching for folder with doc ID: ${docId}`);
  const folders = parentFolder.getFolders();
  
  while (folders.hasNext()) {
    const folder = folders.next();
    if (folder.getName().endsWith(`_${docId}`)) {
      Logger.log(`Found matching folder: ${folder.getName()}`);
      return folder;
    }
  }

  Logger.log(`No matching folder found for doc ID: ${docId}`);
  return null;
}

/**
 * Get a list of existing images in a folder
 */
function getExistingImages(folder) {
  const images = new Map();
  const files = folder.getFiles();

  Logger.log(`Checking existing images in folder: ${folder.getName()}`);

  while (files.hasNext()) {
    const file = files.next();
    if (file.getMimeType().startsWith('image/')) {
      images.set(file.getName(), file.getId());
      Logger.log(`Found existing image: ${file.getName()}`);
    }
  }

  return images;
}
```

Add your folder ID to the top of the script, and optionally enable the subfolder scanning. Then make sure you have a Google Doc in that folder, ready to test.

Save the script, and then run the `extractImagesFromDocs()` function. You should be prompted to approve the script permissions on the first run.

## Running the Script on a Timer

Next, create a new timer for the script and set it to run every 5 minutes, or every minute if you want the images quicker. Just make sure the timer duration is less than or equal to the time filter in the script.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1738347232162/35d91547-550a-4c95-ade5-8f0043580b4f.png)

## Testing the Script

Now try adding a few images to one of the Google Docs in your source folder. Then either wait for timer, or run the script manually. You should see a new folder in the same directory as the doc, with all of the images backed up.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1738347436492/7bef7ce1-81f6-422d-bc0c-de44da748b1a.png)

Try adding a few more images to the doc, and remove one of the originals. When the script runs again, it will add the new images and delete any that were removed from the doc. You can also rename the doc and the folder name will change to match. The source doc’s ID is in the folder name to help find it and keep it in sync when the doc name changes.

## What’s Next?

I thought about adding logic to cover more edge cases, like deleting the whole folder if the doc is deleted, or moving the image folder if the the source doc is moved. There’s a lot more that could be added, but I decided to stop here and just focus on the image extraction.

## Conclusion

Apps Script is a great tool for automating work tasks in Google Docs. This script can aid teams that draft content in Google Docs, and need to extract the images later. By adding conditional logic, the script can be set up to run on a timer and skip docs that have already been processed. This makes the script more performant and helps avoid hitting usage quotas.

*How are you using Apps Script in your daily work?* If you’re looking for more low code content, or want to share your own, join us on Daily.dev in the [Low Code Devs](https://dly.to/SGjNAKXF8ru) Squad!