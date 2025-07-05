---
title: "Creating a Delivery App in Appsmith!"
date: 2021-10-23
permalink: "/creating-a-delivery-app-in-appsmith/"
layout: "post"
excerpt: "Hello again, Joseph from GreenFlux, LLC here with another Appsmith tutorial; I'm submitting this one for Appsmith's Hacktoberfest . Today I will be integrating with the Google Maps Embed API to plot directions for a delivery route, and then send that..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1635014605960/3Q7mzGEGk.png"
readTime: 5
tags: ["#hacktoberfest ", "Tutorial", "devtools", "google maps", "APIs"]
series: "Appsmith"
---

{% raw %}
Hello again, Joseph from @[GreenFlux, LLC](@greenflux) here with another Appsmith tutorial; I'm submitting this one for Appsmith's [Hacktoberfest](https://www.appsmith.com/blog/all-you-need-to-know-about-the-appsmith-hacktoberfest-2021) . Today I will be integrating with the Google Maps Embed API to plot directions for a delivery route, and then send that route to drivers.

Appsmith's [map widget](https://docs.appsmith.com/setup/instance-configuration/google-maps) is great for plotting a single location, or even multiple points at once on a single map. But what if you want to plot *directions* between two points? The map widget doesn't have any options for displaying directions, so maybe an iframe will work!

At first I tried just running Google Maps inside an iframe, but unfortunately, Google blocks maps from loading in an iframe.

![Screen Shot 2021-10-23 at 1.03.20 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1635008608278/Yy1j1ss2W.png)

It turns out, if you want to run Google Maps in an iframe, you have to use the Maps Embed API.

## Enabling the Maps Embed API

Most Google APIs have fees involved, which means you have to set up a billing before you can start using the API, but the Google Maps Embed API is free to use! So all you have to do is set up a new project, enable the API and create a new API key.

Head on over to the quick start guide for detailed instructions on enabling the API. https://developers.google.com/maps/documentation/embed/map-generator

Ok, now that you've got your Maps Embed API key...

## Let's build a delivery app! 🚙

This guide assumes you're already familiar with a few basics in Appsmith, like adding data sources and connecting an API response to a table widget. If this is new to you, check out a few of my previous tutorials for more info on getting started.

https://blog.greenflux.us/saving-api-response-data-to-google-sheets-with-appsmith

https://www.appsmith.com/blog/building-a-shopify-admin-panel-a-step-by-step-guide

I'm using Google Sheets for storing the list of delivery drivers, and Shopify for receiving orders. However, this guide could easily be applied to other data sources. So go ahead and connect whatever sources you're using for drivers and orders, and add two table widgets, connected to your `get_orders` and `get_drivers` queries.

![Screen Shot 2021-10-23 at 12.10.13 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1635005420049/WsqdsZS4o.png)

To keep things simple, I'll be using the `latitude, longitude` format for both the origin and destination in our API request. Although it is possible to search for directions by street address, it's best to send a separate request to look up the `place_id` first, and then use that `id` instead of the lat-long value. Fortunately, Shopify stores the lat-long format along with the street address.

## Create `Origin` and `Destination` Input Widgets

Before we get to the map iframe, let's set up a few input widgets to store the `latitude, longitude` of the `selectedRow` from both table widgets. This will make it a little easier to reference the one field we need from each table in our API request.

`Origin`

```json
{{tbl_drivers.selectedRow.location}}
```

`Destination`

```json
{{tbl_orders.selectedRow.billing_address.latitude + "," + tbl_orders.selectedRow.billing_address.longitude}}
```

![2021-10-23 12.19.11.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1635005985071/4ToS9DIo5.gif)

Next, add an iframe widget and set the URL to:

```json
https://www.google.com/maps/embed/v1/directions?origin={{origin.text}}&destination={{destination.text}}&key=YOUR_API_KEY
```

Deploy the app, and test by selecting different drivers and orders.

![2021-10-23 12.23.59.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1635006289173/bXDS2J7MA.gif)

Awesome! Now we just need a way to send these directions to a delivery driver. This will depend on your specific use-case and how you want to contact each driver. Appsmith doesn't have direct support for sending emails or text messages, but either one could be accomplished with a 3rd party API.

Here's one example of sending emails using reply.io:

https://www.appsmith.com/blog/connecting-mixpanel-reply-io-and-activecampaign-using-appsmith-to-engage-with-your-users

Regardless of how you choose to send the directions, the body of that request is what's important. If you try opening the embed link directly in the browser, you'll end up getting an error that says the API can only be used in an iframe. Instead, we could use the Directions API, but that one isn't completely free. There is a free quota, but you have to enable billing to cover if you go over the free limit.

https://developers.google.com/maps/documentation/directions/quickstart

**So how can we send directions to our drivers without using a paid API?**

Well, at first we were forced to use the Embed API because the map wouldn't load in an iframe. But if we're sending the directions to a phone or email, we can just send the driver a direct link to the Google Maps site now.

The URL format is a little different, but we can still use the same `origin` and `destination` widgets to pass in the lat-long values.

```json
https://www.google.com/maps/dir/?api=1&origin={{origin.text}}&destination={{destination.text}}&travelmode=driving
```

This link will show the same directions as our embed version, but it will work outside of an iframe only, while the Embed API only works *inside* an iframe. So you can text or email the link directly to your drivers using the same `selectedRow`s from the orders and drivers table to determine the locations.

Another option besides text/email is to send a webhook to a Slack Channel , Discord, Telegram, etc. This way your drivers can have an installed app that will notify them of the new message.

---

So the big thing to keep in mind is that the regular Google Maps site *won't* work in an iframe, but the Embed API is free and will work in iframes *only*. Thanks for reading and happy Appsmithing!
{% endraw %}