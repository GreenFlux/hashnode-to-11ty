---
title: "So you want to send JSON to a Google Apps Script Web App..."
date: 2025-04-26
permalink: "/so-you-want-to-send-json-to-a-google-apps-script-web-app/"
layout: "post"
excerpt: "Google Apps Scripts is incredible for a free product. There are so many things you can automate using script triggers and Google Sheets, Gmail, Docs, Calendar, and the rest of the Google ecosystem. You can also trigger Apps Script to run from an inco..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1745669824529/32a1e81b-6dae-4700-9216-ec2a44de91b1.png"
readTime: 5
tags: ["google apps script", "google sheets", "JavaScript", "fetch", "CORS", "http", "REST API", "json", "automation"]
series: "Google Apps Script"
---

Google Apps Scripts is incredible for a free product. There are so many things you can automate using script triggers and Google Sheets, Gmail, Docs, Calendar, and the rest of the Google ecosystem. You can also trigger Apps Script to run from an incoming webhook, and even send data with the request to save to Google Sheets, or send a new email. But there are some serious limitations in the webhook triggers that make integrating other systems harder, and difficult to troubleshoot.

Let’s say you want to post a JSON object to an Apps Script web app and parse the data to use in an email. There are two main issues you are likely to run into.

## **Issue #1: Redirects and Method Change**

Apps Script `/exec` endpoints don’t return your doPost/doGet script response directly. They return a `302 Found` with a URL to the actual script, when POST’ing to the deployment URL. This new endpoint expects a GET request, so following the redirect with the same POST method throws a `405 Method not allowed`.

If you test from Postman, you probably won’t notice any issues because Postman follows the 302 and switches the method from POST to GET by default. But turn off the `automatically follow redirects` option in settings, and you’ll receive a **302 Moved Temporarily** error.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745627543943/340ac521-70f2-4a62-ac6e-b41884ebb77c.png)

Postman, and most browsers follow the redirect by default, but as the Postman error points out, this is contradictory to the RFC 1945 standard, and many other platforms enforce the standard. This means those platforms keep the original POST method, and fail to *GET* the redirect URL.

In cUrl, you can follow redirects and switch methods using the `—location` or `-L` flag, which is off by default, so POSTs to Apps Script will fail unless you enable the flag.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745666909352/e5e2488c-d6be-4393-9122-4a8dc4b40a70.png)

If you’re trying to trigger an Apps Script web app from another platform like subscribing to an event in Shopify, or an automation in Make/n8n, you may see the `405 method not allowed` error because the platform is just following the RFC standard, and *not* switching the method to GET. But if you can’t control this behavior from that platform then you may be out of luck.

However, if the platform supports running your own custom JavaScript code with `fetch()`, you can easily work around this because fetch follows redirects by default, like Postman. I came across this issue recently with Appsmith’s REST API integration, but fortunately it was easy to work around since you can run your own JavaScript in Appsmith.

Fetch should follow the redirect automatically, but you can also specify it explicitly in the request:

```javascript
fetch(URL, {
      redirect: "follow",
      method: "POST",
      body: JSON.stringify(DATA),
      headers: {
        "Content-Type": "text/plain;charset=utf-8",
      },
    })
```

Ok, so following the redirect should solve the `405 Method not allowed` error, right? *Right?!*

![Fail Star Trek The Next Generation GIF by MOODMAN](https://media0.giphy.com/media/RKMm7X3HGKZMuoZlMF/200.gif?cid=ecf05e47xigk4gtb18i0aex9csbjwc13wf1n6l4ift1z3784&ep=v1_gifs_search&rid=200.gif&ct=g)

## **Issue #2: Preflight Options not supported in Apps Script**

HTTP methods sometimes use a preflight request to check the receiving server, and ensure it supports the method and content-type being sent. If the server supports these options, it will respond to the preflight request, and then the main request will run.

This preflight request runs whenever the client is not in the *CORS-safelisted* header, or if the content-type is anything besides `application/x-www-form-urlencoded`, `multipart/form-data`, or `text/plain`.

When you send a POST request with `application/json`, this triggers a preflight request to ensure the server supports this method and content-type. But Apps Script only exposes `doPost` and `doGet` methods, and does not provide a `doOptions` method to handle other content-types. So Apps Script can’t respond to the preflight request, and returns a `405 Method Not Allowed`, just like issue #1!

Structuring the body as plain text and stringifying the JSON allows the preflight test to be skipped, so you can send the data directly. So you can send the body as plain-text, url-encoded, or multipart/form-data, and avoid the preflight request. But sending as JSON will fail with a `405 method not allowed`, even if you follow the redirect to avoid the first issue.

## Two Errors, One Code

This is a tough one to figure out because there are two different causes for the same error. Fix one, and you think it didn’t work because you still get a 405 error. So you change it back, and fix the other. Same error.

Best practices for troubleshooting would have you only change one variable at a time. But in this case I had to dig deeper (burn more ChatGPT tokens) and look through the browser console and Postman logs to figure it out.

## Closing Thoughts

I ran into this error over a year ago and couldn’t figure it out so I eventually gave up because it was just a hobby project I was working on. But a member from the Appsmith community recently asked about the same issue and I decided to take a closer look.

It would have been much easier to troubleshoot if there were different error codes for each problem, but I eventually figured it out, and now I have a whole bunch of new Apps Scripts project in mind. Posting data to the body is more secure, and avoids the character limits and encoding of URL parameters. This opens up a lot of new possibilities for integrating Google with other platforms, without relying on a paid service.