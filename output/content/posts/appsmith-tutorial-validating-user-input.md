---
title: "Appsmith Tutorial: Validating User Input"
date: 2021-10-10
permalink: "/appsmith-tutorial-validating-user-input/"
layout: "post"
excerpt: "Hey, Joseph from GreenFlux, LLC here. I'm a full-time freelancer and a HUGE fan of Appsmith ! I've written a few other tutorials for Appsmith before but this one is gonna be a little different:
Instead of an app for a specific use-case like an admin ..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1626377405556/XCHSzYyCp.png"
readTime: 5
tags: ["JavaScript", "Regex", "#hacktoberfest ", "Tutorial", "Developer Tools"]
series: "Appsmith"
---

{% raw %}
Hey, Joseph from @[GreenFlux, LLC](@greenflux) here. I'm a full-time freelancer and a HUGE fan of [Appsmith](https://www.appsmith.com/) ! I've written a few other tutorials for Appsmith before but this one is gonna be a little *different*:

Instead of an app for a *specific use-case* like an admin panel or dashboard, this app is a collection of examples and snippets to help with your *other* apps. This app- as a whole- does **nothing**! 🙃

But it's filled with examples using Javascript and REGEX to serve as a single reference for a bunch of common techniques. **It's a meta-app!**

The idea is to pack a ton of tips and tricks into a single sample app, instead of having them scattered throughout the forums, Discord, help docs, etc. This will be an 'evolving' app, as I continue to add more examples over time. Feel free to post suggestions below if you'd like to see any other features added.

Ok, let's get started!

---

Appsmith Widgets provide a wide range of User Input options, like a **Date Picker**, **Select/Multi-Select**, **Checkbox**, **Switch** or just a plain **Input** widget.

![Screen Shot 2021-07-15 at 3.33.22 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1626377749201/GRnhtTTdQ.png)

These Widgets have various settings to control the user input and ensure it's of the proper format *(Date, Number, Value from List, etc)*.

For more advanced input checking, Javascript and regular expressions can be used inside the properties pane for most widgets. Javascript can also be used to generate the values in a dropdown, filter table data, format text, or dynamically hide inputs.

---

### Select Widget: Generate label/value pairs from static list

The Select Widget's options are controlled using an array of objects with label and value properties.

```json
[
  {
    "label": "JAN",
    "value": "JAN"
  },
  {
    "label": "FEB",
    "value": "FEB"
  },
  {
    "label": "MAR",
    "value": "MAR"
  },...
]
```

Typing this out manually can be a bit tedious for a long list of options. But we can use the `map()` method on an array to return the correct format without all the repetition.

Now, to get an array, we could type out each value wrapped in quotes and separated by commas:

`["JAN","FEB","MAR",...]`

Or, to shorten it even further, we can use a single string and `split()` it!

```json
{{
"JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC".split('|')
  .map(m => ({'label':m,'value':m}))
}}
```

![Screen Shot 2021-10-08 at 5.02.40 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1633727669888/L7Nasn_bt.png)

### DatePicker: Date is within last 30 days

The DatePicker Widget has a setting for MIN and MAX date, where you can type the date, explicitly, *or* click the JS option to enter custom Javascript. But what if you want the MIN or MAX to be relative to *today* or some other date?

We can use the `moment.js` library (included with Appsmith) to generate a new Date that is 30 days before today and use that for the MIN value.

MIN Date = `{{moment().add(-30, 'days')}}`

https://momentjscom.readthedocs.io/en/latest/moment/03-manipulating/01-add/

### Days of the week

Or how about a dropdown for the day of the week, displayed as text but saved as a number:

```json
{{'SUN|MON|TUE|WED|THU|FRI|SAT'.split('|').map((d,i) => ({label:d,value:i}))}}
```

![2021-10-09 17.59.46.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1633817231335/L8totaM4J.gif)

### Range of numbers

Or how about generating a list of numbers, say 0-100, by increments of 10:

```json
{{
[...Array(11)].map(
	(n,i) => ({label:i*10,value:i*10})
)
}}
```

![2021-10-09 16.33.31.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1633811654620/q6UxhEvg4.gif)

https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread\_syntax

### Email Validation

Want to check that the input is a valid email format? Sounds like a job for REGEX!

> Note: This is different from *validating* an email address actually exists and is connected to a real account. But you can do that in Appsmith too! Just check out this tutorial. https://blog.greenflux.us/validating-emails-with-appsmith-and-the-verifalia-api

So, we need a regular expression to check that the user typed in a valid email *format*. This should be easy, right? 😭

```json
(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])
```

Oh REGEX, you mysterious beast. No, that's not my cat sitting on the keyboard. This is just one version of an attempt to capture all allowable email addresses, found here:

> https://www.emailregex.com/

But if you look in the comments, someone points out that it doesn't work for international domains.

It doesn't have to be that complex, though. Let's say you own a company that has 4 locations, and all employees have an email in the format `first.last@company#.com`.

This REGEX is a good start: `[a-z]{2,12}\.[a-z]{4,12}@company[1-4]\.com`

But what if two users have the same name? We may want to add a number after the last name: `[a-z]{2,12}\.[a-z0-9]{4,12}@company[1-4]\.com`

Ok, perfect. Except, it doesn't cover hyphenated last names. And it would allow the last name to be all numbers. And... you get the point. This is a big topic and there's no right answer.

### Input Value Exists in Query Data

Let's say you have a dynamic list of values, like emails from the `get_users` query, and you want to ensure the input value exists in the dataset. For this validation, I'm using the `some()` method which returns true after the *first* match so that it doesn't have to check the entire table.

```json
{{get_users.data.some(u => u.email === Input2.text)}}
```

![Screen Shot 2021-10-08 at 5.38.42 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1633729370687/2mskbjdq3.png)

### Unique Value (Not in data from query)

Here, we can use the `every()` method to make sure every value in the array matches a condition. The expression will return false if any matching value is found, or true, after all values have been checked.

```json
{{get_users.data.every(u => u.name !== Input3.text)}}
```

### Default Value: Random ID

For ID fields, a random HEX string of X-length can be generated with the following snippet:

```json
{{[...Array(8)].map(() => Math.floor(Math.random() * 16).toString(16)).join('')}}
```

### Check input for a specific pattern (X###-#######)

Another job for REGEX!

```json
^[A-Z]\d{3}-\d{7}$
```

This regular expression will match any upper case letter followed by 3 digits, a dash and 7 digits. The `[A-Z]` declares a range of allowed values for the first character. Then the `\d` represents a single digit and the `{#}` indicates how many digits are required.

### Hide input if another input is invalid

Just reference the widget's `isValid` property. This returns a true/false value, so it's already in the right format to insert directly in the Show/Hide JS setting.

![2021-10-08 17.53.34.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1633730035077/WWLjhokHG.gif)

### Generate the options for a select widget from query data

Need a dropdown using values from an existing query? This one is a little tricky if the data has duplicate values.

In this example, I wanted to make a dropdown of the Countries from the `get_users` query. But duplicates must be removed, or the Appsmith editor will throw an error. And the final array should be sorted alphabetically, after removing duplicates.

This could be done with pure Javascript but it's a lot easier with Lodash, which is also included in Appsmith!

https://docs-lodash.com/v4/sort-by/

```json
{{
_.sortBy(_.uniqBy(get_users.data.map((u) => ( 
{label:u.country, value:u.country} 
) ), 'value'), 'value')
}}
```

![Screen Shot 2021-10-08 at 7.00.56 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1633734092893/dPgUNN8wh.png)

Special thanks to @cokoghenun and @Somangshu on Discord for help on this one!

### Filter table data based on SelectedOption

Now that the Select options contain all the Countries from our User table, we can use the selected value to filter the table. However, we need to include a way to show all Countries and some way to handle when no option is selected.

I started by adding a placeholder value to the top of the country list.

```json
{{
[{label:'--country', value:''}].concat(
_.sortBy(_.uniqBy(get_users.data.map((u) => ( 
{label:u.country, value:u.country} 
) ), 'value'), 'value'))
}}
```

Then, updated the Table1 binding to filter() the get\_users data.

```json
{{
get_users.data.filter( 
  u => {return u.country === Select2.selectedOptionValue || Select2.selectedOptionValue === ''}
)
}}
```

The || (OR) operator is used to return true when the selectedOptionValue is blank.

### Display data from the selected row of a table

Table Widgets have a selectedRow property that can be referenced in other widgets. You can even combined multiple values into a single expression to feed into the next widget.

![Screen Shot 2021-10-08 at 6.25.58 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1633731983583/JEyko0wHN.png)

### Dynamically format data based on its value

Javascript can also be used in Appsmith to dynamically control formatting, like text color. To assign a different color to each value, you can define a new object with your desired settings and then lookup the color for each row.

```json
{{ function(){
let colors = {
	'Netherlands':'Blue',
	'Norway':'Green',
	'United Kingdom':'Red',
	'United States':'Purple',
	'Canada':'Orange'
};
return colors[currentRow.country]
}()}}
```

![Screen Shot 2021-10-10 at 10.21.04 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1633876035606/A_uBcfnBv.png)

### Dynamically add color to a number value based on a range

```json
{{( () => { 
	const id = currentRow.id;
	
	if (id < 4)
 { return '#FF0000'}
	
else if (id >=4 && id < 6)
   {return '#FFCC00'} 
		
else if (id >=6 && id < 8)
   {return '#0066FF'}
	
	else if (id >=8 && id < 12)
   {return '#00CC00'}

  })()
}}
```

![Screen Shot 2021-10-10 at 11.01.01 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1633878070093/s7pRqZvg4.png)

---

As you can see, there's a lot you can do with Javascript and REGEX in Appsmith! These examples are mostly limited to formatting and input validation, but you can also use Javascript to run API calls, chain together actions, transform data and more.

I'll be updating this sample with new snippets and examples, so check back for updates. And feel free to send in your own snippets or requests for new examples. I hope you all find this useful. Thanks for reading!

Here's a link to the app:

https://app.appsmith.com/applications/61328586987e5a1cc9ff7511/pages/616023beea18372f051050c9
{% endraw %}