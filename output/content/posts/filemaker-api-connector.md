---
title: "FileMaker API Connector"
date: 2023-06-09
permalink: "/filemaker-api-connector/"
layout: "post"
excerpt: "Hey, I'm Joseph, I'm an engineer at Appsmith, and a long-time FileMaker Pro developer and consultant. I freelanced in FileMaker Pro for years, integrating APIs like Shopify, BigCommerce, eBay and other services, using FileMaker's insert from URL scri..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1661080486105/dnw6KBVrm.png"
readTime: 5
tags: ["filemaker", "appsmith", "curl", "REST API"]
series: "FileMaker Pro"
---

Hey, I'm Joseph, I'm an engineer at [Appsmith](https://www.appsmith.com/), and a long-time FileMaker Pro developer and consultant. I freelanced in FileMaker Pro for years, integrating APIs like Shopify, BigCommerce, eBay and other services, using FileMaker's `insert from URL` script step, curl requests, and roughly a terabyte of `\"escaped quotes\"`. 😖

FileMaker is a powerful low-code platform that can build some pretty amazing apps, but the developer experience isn’t always as… *let’s just say* — modern. And while curl requests still have their uses, these days, I’d much rather use a *Postman-like interface* for making API calls. **So I built one!** And I wanted to share it with the FileMaker community.

[This app](https://app.appsmith.com/app/filemaker-api-connector/fmp-to-api-6304e44ab189ad45f609d8bb?utm_source=reddit&utm_medium=filemaker-reddit&utm_content=appsmith_apps&utm_campaign=devrel&utm_term=filemaker-appsmith-app), built on Appsmith, provides a starting point for connecting your FileMaker data to almost any API or Database using one of Appsmith’s many [integrations](https://www.appsmith.com/integration?utm_source=reddit&utm_medium=filemaker-reddit&utm_content=appsmith_apps&utm_campaign=devrel&utm_term=integration)**,** and a Postman-like API builder.

![r/filemaker - FileMaker API Connector: A free and open-source starter solution for integrating FileMaker with any API or database](https://preview.redd.it/p2q3dx4kpxj91.png?width=2254&format=png&auto=webp&v=enabled&s=d04cd5f045adef240418f3090ac95e90c470d7b0)

![Screen Shot 2022-08-16 at 2.24.58 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1660674420036/L5e62_R51.png)

> **Appsmith is** [open-source](https://github.com/appsmithorg/appsmith) **and can be self-hosted, or hosted for** [free](https://www.appsmith.com/pricing?utm_source=reddit&utm_medium=filemaker-reddit&utm_content=appsmith_apps&utm_campaign=devrel&utm_term=pricing) **on our cloud platform**

## Getting started

The app handles the FileMaker login flow and query building, using a UI to select fields and enter search terms without coding—just like a *Find Request* in FileMaker. It generates the actual JSON query object for you and runs the API request, returning any matching records.

To get started, click the [Fork App](https://app.appsmith.com/app/filemaker-api-connector/fmp-to-api-6304e44ab189ad45f609d8bb?utm_source=reddit&utm_medium=filemaker-reddit&utm_content=appsmith_apps&utm_campaign=devrel&utm_term=filemaker-appsmith-app) button in the top right to copy the app to your Appsmith account. Then, follow the instructions in the app to connect to your FileMaker server.

![Screen Shot 2022-08-16 at 2.35.31 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1660674980756/8e6TVeUZU.png)

Click the **Test Connection** button to verify if the API is working, and then close the setup window.

Enter the layout name you want to query, and the app will pull in the table name, field names, and total record count. This populates the Select widgets in the query builder so you can easily build complex `AND`/`OR` queries with multiple conditions.

Click **FIND** to run the query and the table should populate with the first 100 records from your FileMaker database. This query builder uses Appsmith's [**JSON Form widget**](https://docs.appsmith.com/reference/widgets/json-form?utm_source=reddit&utm_medium=filemaker-reddit&utm_content=appsmith_apps&utm_campaign=devrel&utm_term=docs), which dynamically generates a form from a JSON object.

Next, try entering a few search terms using the query builder, and set a **Query Type**: `AND` or `OR`. See how the query-body preview updates and the JSON structure changes? Awesome! Now let's check out the API requests.

![2022-08-16 19.52.22.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1660693979810/ic59SZNkS.gif)

## GET or POST

The FileMaker API uses a `GET` method to retrieve records from a layout if no specific filter is used. However, to perform a *find request*, a `POST` method is used to send the query conditions in the `POST` body.

> The search works the same as FileMaker's native *find requests*, using the [same operators](https://support.claris.com/s/article/Refining-find-requests-in-FileMaker-Pro-using-find-operators-1503693059311?language=en_US) for wildcards `*`, exact matches `==`, and others.

`AND` requests group the conditions as multiple properties of the same object:

```js
{
  "query": [
    {
      "address_state": "FL",
      "first_name": "J*"
    }
  ]
}
```

`OR` requests separate each condition into a separate object:

```js
{
  "query": [
    {
      "address_state": "FL"
    },
    {
      "first_name": "J*"
    }
  ]
}
```

# Pagination

Feel free to skip to the next section if your table has &lt;=100 records. Still here? Ok, well it sounds like you might need to paginate your data. **But do you?** 🤨

If possible, try to request only the records needed client-side and limit the results to less than 100 records, the limit per request for the FileMaker API. If you really need more than 100 records pulled, check out this [**guide**](https://docs.appsmith.com/core-concepts/data-access-and-binding/displaying-data-read/display-data-tables#pagination) on pagination.

# Low-code: Integrate with another database or API

There's a lot you can do without coding in Appsmith, but you can do even more with JavaScript, like controlling widgets’ behaviors and appearances, transforming data, or chaining together multiple actions. This app was built using a few JavaScript nuggets to make the query builder, but it can easily be extended to send data to another API or database without additional coding.

Just add a new column to the table widget and set the type to *Button*. Then add a new API or database query to send data from the current row to another system.

![add API.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1660917739089/GBE7XIxJ_.gif)

# Building the query body with JavaScript

The JSONForm widget supports Array and Object type fields, and allows the user to add additional objects—sets of fields and values—to an array. In this case, you are adding new query objects with inputs for the `field_name` and `search_term`. The data can be accessed inside the JSONForm widget by referencing `JSONForm1.formData`.

```javascript
{
  "query": [
    {
      "field_name": "address_state",
      "search_term": "FL"
    },
    {
      "field_name": "first_name",
      "search_term": "J*"
    }
  ],
  "query_type": "AND"
}
```

Then, this data is transformed using a `map()` function, or `forEach()` function, depending on the **query\_type** (`AND` or `OR`).

```javascript
	buildQuery: () => {
		if(!JSONForm1.formData?.query){return ''}
		let queryBody = {query:[{}]};
		let conditions = JSONForm1.formData.query;
		let queryType = JSONForm1.formData.query_type;
		if(queryType == 'OR'){
			let body = conditions.map(c => ({[c.field_name]:c.search_term})); 
			queryBody['query'] = body;
		}else{
			conditions.forEach(c => queryBody['query'][0][c.field_name] = c.search_term)
		};
		return queryBody
	}
```

# Server credentials and security

For easy setup and demo, this public Appsmith app was built using a client-side form to input the FileMaker API credentials as an *app user*. Appsmith also offer a secure datasource feature that saves the credentials on your Appsmith server as an *admin*, without exposing them to the *user*. Check out our [**Authenticated API**](https://docs.appsmith.com/core-concepts/connecting-to-data-sources/authentication#create-authenticated-api) docs for more info.

# Final thoughts

I started this app as a fun experiment to learn the FileMaker API and query structure, but it quickly evolved into the perfect starting point to connect FileMaker to any API or database. Hope this helps you get started on your own integrations!

I would love to hear back from you on your experience using the app, or if you would like to collaborate on adding additional features. I may even open-source this app as its own project if others are interested in contributing.