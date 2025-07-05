---
title: "Becoming the Art: AI Powered Selfies with FLUX1 and Replicate.com"
date: 2024-12-29
permalink: "/becoming-the-art-ai-powered-selfies-with-flux1-and-replicatecom/"
layout: "post"
excerpt: "AI image generation has been around for a while now and become fairly accessible. You can ask ChatGPT or MidJourney to draw anything you can imagine, and they can create some pretty impressive results. But try getting it to draw a picture with your f..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1735491028325/408e37ef-be91-48b2-98cf-8f0d383f585f.png"
readTime: 5
tags: ["AI", "generative ai", "Artificial Intelligence", "Dall-e2", "image generation API", "LLM\u0027s "]
---

AI image generation has been around for a while now and become fairly accessible. You can ask ChatGPT or MidJourney to draw anything you can imagine, and they can create some pretty impressive results. But try getting it to draw a picture with your face or likeness, and suddenly the results aren’t so impressive. ChatGPT will let you upload a photo as an example, but the output image will only have a few similar characteristics at best. To get good, repeatable results, you have to fine-tune the model on a training set of images first.

In this guide, I’ll show you how to train a vision model on your likeness, and start generating amazing hi-resolution images that actually look like you. I’ll be using the [flux-dev-lora-trainer](https://replicate.com/ostris/flux-dev-lora-trainer/train) model, which is based on the FLUX.1 model from Black Forest Labs. For this guide, I’ll be running the training job and model using Replicate.com, but you could run the same model locally if you have sufficient hardware.

But before we get into the details, let’s check out a few of the results! Here are a few samples that I made after training the model on only ten images of me.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735490924979/349197b6-b045-48f6-9fb5-7ef2173c47af.png)

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735490949822/d09c537e-9e24-4fa7-9e5c-5c93ec0cefc7.png)

Not bad for only 10 training images and a 20 minute training job! The images could be even better with more training data and higher settings for the various generation options.

**Alright, let’s get to it!**

**Note**: Using Replicate.com to host the model does require adding a credit card. You can set a max billing amount to avoid any surprises. I am in no way affiliated with Replicate.com, and not using any referral links.

## Creating a Replicate.com Account

Start out by signing up for [Replicate.com](https://replicate.com/) and adding a payment method. You can set a spend limit while you’re here, and Replicate will stop running your models when you hit the limit.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735490477706/11499289-2f40-4f02-b221-8d084a94d52c.png)

You’ll get an initial charge of $1.00 to verify the card, then a notification if/when you hit your spending limit. After initially training my model and several hours of prompting, I’m only at $7 USD, and very happy with the results!

## Prepare the Training Dataset

Next, you’ll want to prepare at least 10 images to fine-tune the model. Be sure to crop out any other faces, and avoid images with writing. I found that text from clothing can appear in the generated images and look out of place, so ideally you should use pictures with no writing.

Once you have your 10+ images cropped, compress them into a zip file to prepare for upload to the model. Do not add the images to a folder first, just zip all 10+ into a single zip file.

## Training the Model

Next, we’ll add the model to our account and set up a training job. Start out by going to the search bar in Replicate.com and type: `ostris`

Then select the **ostris/flux-dev-lora-trainer** model.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735491688078/c41dd352-c0b6-434b-b132-fcbbf6b8163b.png)

Next, scroll down to the **Form** section.

In the **Destination** field, select **\+ create new model**, then give it a name. Be sure to set the model to private unless you want others to use it.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735491929637/3acf5a62-70ef-4ee2-b0a4-f36531b9976e.png)

Then add your zip file to the `input_images` field.

Next, scroll down and set the `trigger_word` to your name, or other keyword. This will be used when prompting to tell the model to generate an image of you.

### Other Settings

You may also want to adjust the number of `steps` and `lora_rank` based on your desired results. I kept the default 1000 steps but increased the lora\_rank to 32 for my test, and the results were fairly good quality without costing too much to train.

Lastly, scroll down and click **Create Training**, to start the training job. Then grab a cup of coffee while the job finishes. ☕️

In my case, the job took about 20 minutes. Yours may vary based on the number of images and settings used.

## Generating Images

Once the training job is complete, you can begin prompting by going to the [Models](https://replicate.com/models) tab in your Dashboard and selecting the new model. In the prompt field, be sure to use the `trigger_word` to add yourself to the generated image.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735493222035/44dfdce8-059a-465b-a730-e32259ccdd7e.png)

You can also adjust settings for the aspect ratio, size, and a ton of different options that affect the image style and quality. Try out the same prompt with different settings to see what kind of results you get. The `guideance_scale` setting can yield some particularly odd results when adjusted from the default value of 3.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1735494093702/24a47908-40db-4f97-bc74-f9e0e9278b04.png)

## Conclusion

Training your own vision model would have been impossible for the average user just a few years ago. But now with hosted services like replicate.com, anyone can train their own model in minutes and start generating hi-resolution AI images based on their own likeness.