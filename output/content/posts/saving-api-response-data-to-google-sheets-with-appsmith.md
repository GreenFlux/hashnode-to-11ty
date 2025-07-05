---
title: "Saving API Response Data to Google Sheets with Appsmith"
date: 2021-07-14
permalink: "/saving-api-response-data-to-google-sheets-with-appsmith/"
layout: "post"
excerpt: "Appsmith recently released a new Google Sheets integration with a huge list of options, including a method to Bulk Insert Rows to an existing sheet.  

☝️ So let's say you want to take the response data from a GET request, transform the data and send..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1626297230856/QBTAcJtqB.png"
readTime: 5
tags: ["APIs", "REST API", "Tutorial", "google sheets", "Google"]
series: "Appsmith"
---

{% raw %}
Appsmith recently released a new [Google Sheets integration](https://docs.appsmith.com/datasource-reference/querying-google-sheets) with a huge list of options, including a method to **Bulk Insert Rows** to an existing sheet.  

![Screen Shot 2021-07-14 at 2.02.45 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626285769728/HdacnH9iA.png)

### ☝️ So let's say you want to take the response data from a GET request, transform the data and send it to Google Sheets:

For this example, I will be using data from the [RandomUser.me](https://www.randomuser.me) API to build on my previous [Appsmith sample app](https://community.appsmith.com/t/sample-app-random-user-api/100) . However, I'm going to try to break down the steps so this post can be applied to saving data from any API to Google Sheets.

### ✅ Project Requirements

* Download multiple records of JSON data from an API
    
* Transform/flatten the data
    
* Add modified records as new rows in Google Sheets

### 👉 Prerequisites

1. Existing [GET request](https://docs.appsmith.com/core-concepts/connecting-to-data-sources/connect-to-apis) is already configured in Appsmith
    
2. Destination spreadsheet is setup with desired column names

**Sample Request**

`GET: https://randomuser.me/api/?seed=foobar&results=50&nat=us`

The response data has several nested fields, but we want to 'flatten' the data and only send certain values to the spreadsheet.

![Screen Shot 2021-07-14 at 2.20.00 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626286804433/ck6PXpTiA.png)

![Screen Shot 2021-07-14 at 2.21.10 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626286876590/66YpvlZGb.png)

### ⚙️ Setup

1. Add a new Google Sheets Data Source and authorize it for your Google account.
    
2. Add a new API and choose the method **Bulk Insert Rows**.
    
3. Copy/paste in the function below

```json
{{
get_users.data.results.map(
  u => {
    return {'name':u.name.first, 'email':u.email, 'id':u.id.value};
  }
)
}}
```

4. **DEPLOY!** 🚀

![Screen Shot 2021-07-14 at 5.46.53 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626299508055/Qp12vVOmt.png)

![Screen Shot 2021-07-14 at 5.53.07 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626299626935/pGzhjxQhi3.png)

The **Bulk Insert Rows** method expects an array of objects, with keys that match the the sheet's column names:

`[{key:value},...]`

And the map() method returns an array. So we can **map!** over the `get_users` data and build our rows.

## That's it! 😁

#### It really is that easy to transform and push data to Google Sheets from an API response!

---

This is just the beginning in a series where I will cover transforming the data in more detail, filtering and sorting the results, and eventually, syncing a Google Sheet with an API endpoint on a timer.

Thanks for reading!
{% endraw %}