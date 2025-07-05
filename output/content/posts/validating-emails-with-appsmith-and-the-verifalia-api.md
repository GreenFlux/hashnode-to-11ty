---
title: "Validating Emails with Appsmith & the Verifalia API"
date: 2021-07-16
permalink: "/validating-emails-with-appsmith-and-the-verifalia-api/"
layout: "post"
excerpt: "Verifalia is an email validation service with an API and a free plan that can be used to verify up to 25 emails per day (or more with the paid plans).
Send in one or more email addresses, and Verifalia will generate a report with all kinds of data ab..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1626452045811/rWcDbt9TK.png"
readTime: 5
tags: ["REST API", "email marketing", "integration", "Tutorial", "Devops"]
series: "Appsmith"
---

{% raw %}
### [Verifalia](https://verifalia.com/) is an email validation service with an API and a free plan that can be used to verify up to 25 emails per day *(or more with the paid plans)*.

Send in one or more email addresses, and Verifalia will generate a report with all kinds of data about each address.

![Screen Shot 2021-07-16 at 1.55.58 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626458178143/csFjRRjFP.png)

Now, let's build our own email validation tool using Appsmith for the UI to integrate with the Verifalia API.

## 👉 Goals

* Create new APIs in Appsmith to verify email addresses
    
* Build UI to submit verifications and view results
    
* Store results for each request in Google Sheets *(future post)*

## ⚙️ Build Process

### Get Bearer Token

Start by adding Input Widgets for `api_email` and `api_pw`, and a button to run the `POST: Bearer_Request`.

![2021-07-16 14.22.46.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626459947452/Pawu_j3f4.gif)

Then add a new API:

`POST: https://api.verifalia.com/v2.2/auth/tokens`

`Headers: {content-type:'application/json'}`

`Body: {username: 'EMAIL_ADDRESS', password: 'password'}`

![2021-07-16 14.19.36.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626460151335/L3P68aoxJ.gif)

Next, set Button1 to run the `Bearer_Request` query, and save the response to the user's local store (appsmith.store.token).

![Screen Shot 2021-07-16 at 2.52.47 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626461572817/DIEMLUvnu.png)

Deploy, and test to make sure the POST response includes an accessToken. If there is no error alert then you should be good to go. But you can also display the accessToken on the UI just to verify.

![Screen Shot 2021-07-16 at 2.51.59 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626461525502/XHc4WBZht.png)

### Send Email Validation Request

Now that we have an accessToken, we can use that in our header to make a POST request and send an email address to be verified.

Add New API:

`POST: https://api.verifalia.com/v2.2/email-validations`

```json
Headers: {content-type:'application/json', Authorization: Bearer {{Bearer_Request.data.accessToken}} }
```

```json
Body: {
    entries: [
        { inputData: 'test@email.com' }
    ]
}
```

![2021-07-16 14.54.04.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626461673372/CR9pIyj7r.gif)

Run the new `POST: submit_job` and you should get back a response with an 'id' for the job. The request takes some time to process, so the API doesn't return the results in the same call. Instead, you have to get the 'id' and then do a followup GET request to check the status.

![Screen Shot 2021-07-16 at 3.29.43 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626463836594/6Q-9STGdn.png)

### Check Job Status

Add a new API: `check_job`

`GET: https://api.verifalia.com/v2.2/email-validations/{{submit_job.data.overview.id}}`

```json
Headers: {content-type:'application/json', Authorization: Bearer {{Bearer_Request.data.accessToken}} }
```

![Screen Shot 2021-07-16 at 3.00.19 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626462024604/9kiNkd9b4.png)

Run the `GET: check_job` API and you should get back a report like this:

![Screen Shot 2021-07-16 at 3.02.49 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626462234670/V-58X-QRY.png)

## Viewing Results on the UI

Now let's add a Table Widget to display the results. `{{check_job.data.entries.data}}`

![Screen Shot 2021-07-16 at 3.05.17 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626462367831/RW4_RrQOJ.png)

Next, we can add an Input Widget to pass a new email, and a button to send another request.

![2021-07-16 15.09.46.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626462634187/GP1O1me4J.gif)

And finally, a button to check the job status.

![2021-07-16 15.24.11.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626463479531/HgFtx-JHF.gif)

---

Ok, the UI could use some work, but we have a functional system for checking an emails now!

I hope this helps others figure out the authentication and formatting for using the Verifalia API. Please post below if you have any questions setting up your own email validation system in Appsmith.

Thanks for reading!
{% endraw %}