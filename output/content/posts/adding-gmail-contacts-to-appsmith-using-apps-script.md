---
title: "Adding Gmail Contacts to Appsmith using Apps Script"
date: 2021-07-13
permalink: "/adding-gmail-contacts-to-appsmith-using-apps-script/"
layout: "post"
excerpt: "I've been having a lot of fun building with Appsmith lately and wanted to do something with Google Contacts.
It's easy to connect to a new API from Appsmith, but it's not so easy to enable the Google Contacts API for first time users. It takes a bit ..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1626120023386/7E3ShXxC2i.png"
readTime: 5
tags: ["JavaScript", "Google", "APIs", "REST API", "Tutorial"]
series: "Google Apps Script"
---

{% raw %}
#### I've been having a lot of fun building with Appsmith lately and wanted to do something with Google Contacts.

It's easy to connect to a new API from Appsmith, but it's not so easy to enable the Google Contacts API for first time users. It takes a bit of setup in the Google Cloud Console before you can start using the API. You have to set up billing, create a project, add credentials, define the scope, etc. But most of the same data can be accessed using Apps Script, and without all the setup work to enable the API.

### 📐 Project Requirements

* Create endpoint for GET requests to retrieve all Contacts by 'label'
    
* Option to retrieve full list of all labels, to populate dropdown in Appsmith
    
* Security check so web app does not respond to all requests

### 📗 Topics Covered

* Publishing a script as a [web app](https://developers.google.com/apps-script/guides/web#request_parameters)
    
* Passing URL parameters to the web app
    
* Using [ContactsApp](https://developers.google.com/apps-script/reference/contacts/contacts-app) to retrieve contacts & labels

### 📌 A Note on Terminology

Google uses the term `Label` throughout the Gmail UI to refer to email categories.

**But on the Apps Script and API side, they are referred to as** `Groups`!

In an effort to maintain an equal level of confusion in this post, I'll also be using `Label` to refer to the frontend (user input) and using `Groups` when referencing the data returned from the ContactsApp. 🙃

## ⚙️ Setup Guide

#### SCRIPT: Deploy as Web App

1. Create a [new Apps Script project](https://www.script.new) and paste in the script below.
    
2. Replace the `APIKEY` with a custom value, then SAVE.
    
3. Deploy&gt; New Deployment&gt; Select Type&gt; WEB APP
    
4. Execute As: ME, Who has access: ANYONE
    
5. DEPLOY and copy the new URL for the web app.

![Screen Shot 2021-07-13 at 6.26.52 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626172021727/2622fVNQK.png)

#### Appsmith: Add Contacts Web App as API

1. Create a new app, and add a new API using the web app URL.
    
2. Add parameters: `key={APIKEY}` and `labels` -with no value *(to return the list of labels)*
    
    ![Screen Shot 2021-07-13 at 6.35.21 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626172547449/c3WTGGaoI.png)
    
3. Add a Select-widget and set the Options to `{{get_labels.data.groups}}`
    
    ![Screen Shot 2021-07-13 at 11.28.31 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626190164946/JA3RR6BB9.png)
    
4. Copy the get\_labels API, rename `get_contacts`
    
5. Update parameters: Change label**s** to `label`\= `{{Select1.selectedOptionValue}}`
    
    ![Screen Shot 2021-07-13 at 6.28.00 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626172089788/uKzOBveyJ.png)
    
6. Add a Table-widget and set the Data as `{{get_contacts.data.contacts}}`
    
    ![Screen Shot 2021-07-13 at 6.21.46 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626172412376/_NUb_Wd15.png)
    
7. DEPLOY

![2021-07-13 06.24.35.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626172426482/AdkX0UoZq.gif)

### AWESOME! Now all Gmail Contacts can be pulled into Appsmith by Label. 🤓

### 💾 Script

```json
const key = 'APIKEY';  // custom string to check before returning contacts

function doGet(e) {
  let responseBody = {'requestEvent':e};
  
  if('label' in e.parameter && e.parameter.key == key){
    const label = e.parameter.label;
    const foundContacts = getContacts(label);
    responseBody['contacts'] = foundContacts;
    
  }else if('labels' in e.parameter && e.parameter.key == key){
    const foundGroups = getLabels();
    responseBody['groups'] = foundGroups;

  }

  return ContentService.createTextOutput(JSON.stringify(responseBody))
  .setMimeType(ContentService.MimeType.JSON)
}

function getContacts(label) {
  const contactGroup = ContactsApp.getContactGroup(label); 
  const contactsArr = ContactsApp.getContactsByGroup(contactGroup);
  
  const contacts = contactsArr.map(function(c) {
    let cObj = {};
    cObj['name'] = c.getFullName();
    cObj['phone'] = c.getMobilePhone();
    cObj['email'] = c.getEmailAddresses()[0];
    return cObj
  });
  
  Logger.log(JSON.stringify(contacts));
  return contacts
}

function getLabels(){
  const groups = ContactsApp.getContactGroups();
  let groupsArr = groups.map((group, index) => {
                             return {'label':group.getName(),'value':group.getName()}
}

);

Logger.log(groupsArr);
return groupsArr
}
```
{% endraw %}