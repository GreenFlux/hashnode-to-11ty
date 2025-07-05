---
title: "Replacing Google Forms with Appsmith"
date: 2021-07-18
permalink: "/replacing-google-forms-with-appsmith/"
layout: "post"
excerpt: "Google Forms is widely used in various integrations and workflows that all start with capturing data and sending it to a Google Sheet.
Whether it's a contact form embedded on your website, a registration form to share on social media, or something mo..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1626617063902/J2Tc1vU86.png"
readTime: 5
tags: ["Google", "google sheets", "devtools", "forms", "Tutorial"]
series: "Appsmith"
---

{% raw %}
**Google Forms is widely used in various integrations and workflows that all start with capturing data and sending it to a Google Sheet.**

Whether it's a contact form embedded on your website, a registration form to share on social media, or something more advanced- the general principle is the same. Give the user some input fields and a suitable UI, capture the response and send the data to a spreadsheet.

From there, all kinds of integrations, automations and workflows are possible. But regardless of the use case, the Google branding is pretty noticeable. Even with a form embedded in an iframe on your own site, the bottom of the form clearly states that it was built with Google Forms.

![Screen Shot 2021-07-18 at 9.52.32 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626616366678/LKymzbGbS.png)

So how do you replace the form with something that has your own branding, without breaking the integrations that rely on Google Sheets as a datasource?

## with Appsmith!

### Add APIs

1. Start a new Appsmith app and add a new API: `Datasources> Create New> Google Sheets > Fetch Rows`
    
2. Use the URL from your existing Responses Sheet that is linked to your Google Form
    
    ![Screen Shot 2021-07-18 at 10.09.51 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626617485038/yRLPr5ArF.png)
    
3. Run the API and verify the response
    
    ![Screen Shot 2021-07-18 at 10.12.22 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626617596660/DWI7VCfN5.png)
    
    ![Screen Shot 2021-07-18 at 10.12.12 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626617598855/SXd62K5Lc.png)
    
4. Now, Copy the API, and change the method to `Insert Row`
    
5. Copy the *Response* from the `get_rows` API into the *Row Object* of the `add_row` API.
    
6. Remove the `RowIndex` *(not needed for Insert row)*
    
7. Add commas after each property in the *Row Object* template *(except the last one)*
    
8. Run the API and verify a new row was added to the sheet

![Screen Shot 2021-07-18 at 10.43.14 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626619417424/I7uah37f2.png)

You should have a new row in added to your sheet, using the hard-coded data we just added to the template. Now, let's add a form to capture the inputs. Then we can come back to the template and bind the inputs.

### Create Form

1. Change [Layout Size](https://docs.appsmith.com/core-concepts/dynamic-ui/application-layout#how-it-works) to Mobile *(smaller for iframe)*
    
2. Add a new Button-Widget to the Page
    
3. Button Settings: `OnClick> Open Modal> New Modal`
    
4. Change Modal type to **Form**
    
5. Add Inputs to Form
    
    ![2021-07-18 11.09.20.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1626620982730/GsibVgO0T.gif)
    
6. Bind Submit button to `add_row` API
    
    ![Screen Shot 2021-07-18 at 11.08.17 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626620929979/L4eXrJPNT.png)
    
7. Update API body template to bind inputs

```json
{
"Timestamp": "{{moment().format('MM/DD/yyyy hh:mm:ss')}}",
"Name":"{{name.text}}",
"Email":"{{email.text}}",
"Comments":"{{comments.text}}"
}
```

8. **DEPLOY!** 🚀

### Ok, now we have a working replacement for our Google Form.

Next, either set your app to [share publicly](https://docs.appsmith.com/core-concepts/access-control#public-apps), or add the users you want to have access to the form.

If your previous integration was embedded in an iframe, you can replace it with the new app using this format:

`<iframe src="https://app.appsmith.com/applications/{{APP_ID}}/pages/{{PAGE_ID}}?embed=true" height="700" width="100%"></iframe>`

> Note the `embed=true` parameter. This removes the Appsmith top bar so you can add your own branding.

[Docs:embed-appsmith-into-existing-application](https://docs.appsmith.com/how-to-guides/embed-appsmith-into-existing-application)

---

Using this guide, you should be able to replace a *Google Form* with an **Appsmith app** and continue adding rows to the same sheet. So any integrations that rely on data in that spreadsheet should continue to work.

However, if you were using an onSubmit() trigger you may have to replace that with a webhook from Appsmith.
{% endraw %}