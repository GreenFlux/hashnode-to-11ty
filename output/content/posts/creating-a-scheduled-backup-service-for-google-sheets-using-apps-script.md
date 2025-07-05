---
title: "Creating a Scheduled Backup Service for Google Sheets using Apps Script."
date: 2021-07-09
permalink: "/creating-a-scheduled-backup-service-for-google-sheets-using-apps-script/"
layout: "post"
excerpt: "Apps Script is a powerful tool for automating routine tasks with Google Sheets, Docs, Gmail, and other Google services. On a recent job, I needed to create a daily backup of a Google Sheet for a client, and I was looking for a simple, reusable soluti..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1625584039639/esE1Zsh89.png"
readTime: 5
tags: ["google sheets", "JavaScript", "Tutorial", "Google"]
series: "Google Apps Script"
---

Apps Script is a powerful tool for automating routine tasks with Google Sheets, Docs, Gmail, and other Google services. On a recent job, I needed to create a daily backup of a Google Sheet for a client, and I was looking for a simple, reusable solution.

This sounded like a perfect job for Apps Script! Here's what I came up with. Jump to the end to see the final script.

#### 🧐 This post will cover

* Writing a basic [Apps Script](https://developers.google.com/apps-script/overview) function
    
* Using [SpreadsheetApp](https://developers.google.com/apps-script/reference/spreadsheet/spreadsheet-app) & [DriveApp](https://developers.google.com/apps-script/reference/drive/drive-app) Classes
    
* Creating a time-driven [Trigger](https://developers.google.com/apps-script/guides/triggers/installable) to run the function

#### 👉 Project Requirements

1. Backup multiple sheets on a schedule
    
2. Different backup destinations for each sheet
    
3. Read/write between different Google accounts

#### ⚙️ Setup

I started out with a new sheet, and added columns for the source sheet Id, destination folder Id, and a link to the latest backup file.

![Screen Shot 2021-07-09 at 8.08.18 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625832710063/5qXaLmxMN.png)

And created a new script: `Tools>Script Editor`

![Screen Shot 2021-07-09 at 8.13.18 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625832942981/hlKWVKJlY.png)

Next, I loaded up the list of source sheet Ids into an array so I could loop through them for backing up:

![Screen Shot 2021-07-09 at 8.18.58 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625833143982/TTmL4KKA5.png)

> 📌 NOTE: `getLastRow() - 1` is used to offset the the header row.

#### Now, what should I name the backup file?🤔

Well, I wanted the original sheet name included, and a timestamp to make each name unique.

Something like this: `const backupName = sourceName +'_BAK' + dateTimeStr`

So to get a string with the current timestamp, I used [Utilities.formatDate()](https://developers.google.com/apps-script/reference/utilities/utilities#formatdatedate,-timezone,-format) .

```json
const dateTimeStr = Utilities.formatDate(new Date(),'GMT-4','yyyyMMdd_HHmmss');
const backupName = sourceName +'_BAK' + dateTimeStr
```

Now the `backupName` can be used in the next step, which creates the actual backup file.

```json
// COPY EACH SOURCE SHEET TO DESTINATION FOLDER
  sourceIds.forEach((sourceId, index) => {
    const source = SpreadsheetApp.openById(sourceId);
    const sourceName = source.getName();
    const dateTimeStr = Utilities.formatDate(new Date(),'GMT-4','yyyyMMdd_HHmmss');
    const backupName = sourceName +'_BAK' + dateTimeStr;
    const backupId = source.copy(backupName).getId();  // File created in My Drive by default
    const destinationId = sh.getRange(index + 2, destinationIdCol).getValue();  // Folder Id for destination sheet
    const destination = DriveApp.getFolderById(destinationId);
    DriveApp.getFileById(backupId).moveTo(destination);
```

> 📌 NOTE: Here the offset is `-2` because the `index` of the forEach() loop is zero-based. So to match the loop index with the correct row number (one-based), the offsets are combined.

For the last step, I wanted to save a link to the sheet for the latest backup file. Saving the link text was pretty easy, but that only shows the Id, and not the name. `https://docs.google.com/spreadsheets/d/{SPREADSHEET_ID}/edit#gid=0`

So to get the new filename as the link text, the cell value has to be a hyperlink. I tried the normal setValue() method but this doesn't work with hyperlinks. They have to be created using the [newRichTextValue()](https://developers.google.com/apps-script/reference/spreadsheet/spreadsheet-app#newrichtextvalue) method.

![Screen Shot 2021-07-09 at 8.50.12 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625835019072/7YGgZUVn4.png)

#### Lastly, to set the script on a timer

`Triggers (Left sidebar in script editor) > Add Trigger`

![Screen Shot 2021-07-09 at 9.02.13 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625835739110/K4D8R4nzv.png)

Now all sheets will be backed up daily to their specified folder. This even works across Google accounts! All you need is READ access to the source sheet, and WRITE access to the destination folder.

![Screen Shot 2021-07-09 at 9.04.35 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1625836066096/iTGa6Jpp5.png)

### FINISHED SCRIPT

```json
function backupSheets() {
  // CONFIGURE FOR GSHEET
  const spreadsheetId     = '{SPREADSHEET_ID}'  //  list of sheet/folder Ids
  const sheetName         = 'sheetlist' // sheet with the list of Ids
  const sourceIdCol       = 1;  // source spreadsheet Id
  const destinationIdCol  = 2;  // destination folder Id
  const newFileURLCol     = 3;  // link to new file [OUTPUT TO SHEET]
  
  // LOAD SOURCE SHEET IDS FOR BACKUP
  const ss = SpreadsheetApp.openById(spreadsheetId); 
  const sh = ss.getSheetByName(sheetName);
  const lastRow   = sh.getLastRow();
  const sourceIds = sh.getRange(2, sourceIdCol, lastRow - 1, 1).getValues(); // Array of Ids for source sheets

  // COPY EACH SOURCE SHEET TO DESTINATION FOLDER
  sourceIds.forEach((sourceId, index) => {
    const source        = SpreadsheetApp.openById(sourceId);
    const sourceName    = source.getName();
    const dateTimeStr   = Utilities.formatDate(new Date(),'GMT-4','yyyyMMdd_HHmmss');
    const backupName    = sourceName +'_BAK' + dateTimeStr;
    const backupId      = source.copy(backupName).getId();  // File created in My Drive by default
    const destinationId = sh.getRange(index + 2, destinationIdCol).getValue();  // Folder Id for destination sheet
    const destination   = DriveApp.getFolderById(destinationId);
    DriveApp.getFileById(backupId).moveTo(destination);

    // SAVE NEW FILE LINK TO SHEET
    const backupURL = 'https://docs.google.com/spreadsheets/d/' + backupId +'/edit#gid=0';
    const hyperlink = SpreadsheetApp.newRichTextValue().setText(backupName).setLinkUrl(backupURL).build();
    sh.getRange(index + 2,newFileURLCol).setRichTextValue(hyperlink);    // link to last backup file
  });
}
```