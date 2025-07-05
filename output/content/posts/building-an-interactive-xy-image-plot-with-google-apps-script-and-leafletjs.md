---
title: "Building an Interactive XY Image Plot with Google Apps Script and Leaflet.js"
date: 2024-09-03
permalink: "/building-an-interactive-xy-image-plot-with-google-apps-script-and-leafletjs/"
layout: "post"
excerpt: "Google Maps has a ton of features for plotting points on a map, but what if you want to plot points on an image? These XY Image Plot maps are commonly used for floor maps, job site inspections, and even games.
In this guide, I'll show you how to crea..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1725394906396/98552e90-8fed-45f0-85a3-c75163245a8a.png"
readTime: 5
tags: ["google apps script", "leaflet", "Mapping", "google sheets", "JavaScript"]
series: "Google Apps Script"
---

Google Maps has a ton of features for plotting points on a map, but what if you want to plot points *on an image*? These XY Image Plot maps are commonly used for floor maps, job site inspections, and even games.

In this guide, I'll show you how to create an interactive map with draggable points using Leaflet.js and Google Apps Script. We'll cover everything from setting up the map to integrating data from Google Sheets, and deploying it as a web app.

**This guide will cover:**

* Setting up Leaflet.js in a Google Apps Script HTML Service
    
* Displaying Markers using data from Google Sheets
    
* Updating Sheets row when a Marker is moved
    
* Creating new Markers from the map and saving to Sheets
    
* Deleting a marker from the web app

### **Setting up Leaflet.js in a Google Apps Script HTML Service**

[Leaflet.js](https://leafletjs.com/) is one of the most popular open-source mapping libraries. It's light-weight, easy to use, and had great documentation. They support a ton of different map types, including "[CRS.Simple](https://leafletjs.com/examples/crs-simple/crs-simple.html)", or Coordinate Reference System, which allows you to supply a background image.

### Google Sheets Set Up

Start out by creating a sheet named `map_pin` with the following structure:

| id | title | x | y |
| --- | --- | --- | --- |
| 1 | test1 | 10 | 30 |
| 2 | test2 | 50 | 80 |

Then open Apps Script from the Extensions menu.

### Creating HTML File

First, we'll start with the basic example from the Leaflet docs, just to get the library working. You can see the full example in their quick start guide, [here](https://leafletjs.com/examples/quick-start/).

Add a new HTML File named Index, and set the content to:

```xml
<!DOCTYPE html>
<html>
<head>
  <title>Quick Start - Leaflet</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
  <style>
    #map {
      height: 400px;
    }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
  <script>
    var map = L.map('map').setView([40.73, -73.99], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap'
    }).addTo(map);

    var marker = L.marker([40.73, -73.99]).addTo(map)
      .bindPopup('Test Popup Message')
      .openPopup();
  </script>
</body>
</html>
```

Then update the Code.gs file with:

```javascript
function doGet() {
  const html = HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Map with Draggable Points')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
  return html;
}
```

Save, and then click Deploy, and publish as a web app. Then open the link for the new deployment and you should see Leaflet.js displaying a map on New York.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1725276194580/de10090c-7a53-4943-b96c-1792da69b88a.png)

Ok, that's the regular map example using Leaflet. Now on to the CRS.Simple map type, which allows supplying a background image.

Update the HTML with this example from the Leaflet Tutorials.

```xml
<!DOCTYPE html>
<html>
<head>
  <title>CRS Simple Example - Leaflet</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css" />
  <style>
    #map {
      height: 400px;
      width: 600px;
    }
    body {
      margin: 0;
      padding: 0;
    }
  </style>
</head>
<body>
  <div id="map"></div>

  <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
  <script>
    // Set up the map with a simple CRS (no geographic projection)
    var map = L.map('map', {
      crs: L.CRS.Simple,
      minZoom: -1,
      maxZoom: 4
    });

    // Define the dimensions of the image
    var bounds = [[0, 0], [1000, 1000]];
    var image = L.imageOverlay('https://leafletjs.com/examples/crs-simple/uqm_map_full.png', bounds).addTo(map);

    // Set the initial view of the map to show the whole image
    map.fitBounds(bounds);

    // Optional: Add a marker or other elements to the map
    var marker = L.marker([500, 500]).addTo(map)
      .bindPopup('Center of the image')
      .openPopup();
  </script>
</body>
</html>
```

Here we are supplying an image of 1000 x 1000 pixels, then setting the center marker at `500, 500`.

Click **Save**, then **Deploy&gt;Test Deployments**, to see the new map type. You should now have a map with a background image and a marker plotted in the center.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1725281356836/23b771ed-936b-404f-a102-d05e60808aaf.png)

### **Initializing a Map with Data from Google Sheets**

Next, we'll use data from the sheet to populate a set of markers on the map.

First, add a function to the Code.gs file to get the marker locations:

```javascript
function getPinData(){
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName('map_pin');
  const data = sh.getDataRange().getValues();
  const json = arrayToJSON(data);
  //Logger.log(json);
  return json
}

function arrayToJSON(data=getPinData()){
  const headers = data[0];
  const rows = data.slice(1);
  let jsonData = [];
  for(row of rows){
    const obj = {};
    headers.forEach((h,i)=>obj[h] = row[i]);
    jsonData.push(obj)
  }
  //Logger.log(jsonData)
  return jsonData
}
```

Here I'm returning the pins as JSON so they're easier to work with in the HTML in the next section.

Now add a function to the HTML to loop over this JSON and create the map pins after the map has loaded.

```javascript
// Add map pins from sheet data
    google.script.run.withSuccessHandler(addMarkers).getPinData();

    function addMarkers(mapPinData) {
      mapPinData.forEach(pin => {
        const marker = L.marker([pin.x, pin.y], {
          draggable: true
        }).addTo(map);

        marker.bindPopup(`<b>${pin.title}`).openPopup();

        marker.on('dragend', function(e) {
          const latLng = e.target.getLatLng();
          console.log(`Marker ${pin.title} moved to: ${latLng.lat}, ${latLng.lng}`);
        });
      });
    } 
```

Save, and then open the test deployment. You should now have markers generated from your sheet data!

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1725389885086/b435fccc-a6a1-4c59-8e18-acdd52987d56.png)

Each pin has a popup with the title from that row. The pins are draggable at this point, but we still need a function to save the new position.

## Saving Marker Position When Dragged

To save the new position, we need two functions: one in the HTML to capture the event on the client side, and one to save the new position on the server side, in the Code.gs file.

Update the HTML with:

```javascript
    function addMarkers(mapPinData) {
      mapPinData.forEach(pin => {
        const { id, title, x, y } = pin;
        const marker = L.marker([x, y], {
          draggable: true
        }).addTo(map);

        marker.bindPopup(`<b>${title}</b>`).openPopup();

        marker.on('dragend', function(e) {
          const latLng = e.target.getLatLng();
          console.log(`Marker ${title} moved to: ${latLng.lat}, ${latLng.lng}`);
          saveMarkerPosition({ id, title, lat: latLng.lat, lng: latLng.lng });
        });
      });
    }

    function saveMarkerPosition({ id, title, lat, lng }) {
      google.script.run.saveMarkerPosition({ id, title, lat, lng });
    }
```

And then add a function to the Code.gs file to save the location:

```javascript
function saveMarkerPosition({ id, lat, lng }) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName('map_pin');
  const data = sh.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === id) {  // ID column (index 0)
      sh.getRange(i + 1, 3).setValue(lat);  // latitude column 
      sh.getRange(i + 1, 4).setValue(lng);  // longitude column 
      break;
    }
  }
}
```

Save, and refresh the test deployment. You should now see the sheet update when a marker is dragged!

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1725391537794/72d5c1fb-657c-442e-8af3-a7b2b57ba0cb.gif)

## Adding New Points

We can now move the existing points, but what about adding new ones? Again, we'll need two functions, one in the HTML, and one in the Code.gs file.

First, add a function to the HTML to open a prompt when the user clicks an empty spot on the map, and pass the value to a server function.

```javascript
    // Function to add a new pin
    map.on('click', function(e) {
      const latLng = e.latlng;
      const title = prompt('Enter a title for the new pin:');
      if (title) {
        google.script.run.withSuccessHandler(function(id) {
          addNewMarker({ id, title, lat: latLng.lat, lng: latLng.lng });
        }).addNewPin({ title, lat: latLng.lat, lng: latLng.lng });
      }
    });

    function addNewMarker({ id, title, lat, lng }) {
      const marker = L.marker([lat, lng], {
        draggable: true
      }).addTo(map);

      marker.bindPopup(`<b>${title}</b>`).openPopup();

      marker.on('dragend', function(e) {
        const latLng = e.target.getLatLng();
        saveMarkerPosition({ id, title, lat: latLng.lat, lng: latLng.lng });
      });
    }
```

Then add the function to the Code.gs to save the new row.

```javascript
function addNewPin({ title, lat, lng }) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName('map_pin');
  
  // Check if there are any rows present, if not initialize ID
  const lastRow = sh.getLastRow();
  let newId = 1;
  
  if (lastRow > 0) {
    const lastId = sh.getRange(lastRow, 1).getValue(); 
    newId = lastId + 1;
  }

  sh.appendRow([newId, title, lat, lng]);

  return newId;  
}
```

Save once more and refresh the test deployment. Now when you click an empty spot, you can enter a title and save a new marker!

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1725393299701/f74f0782-a908-443a-9a39-89d6708a99cb.png)

## Deleting A Marker

Lastly, we should add a way to delete markers, giving us a full CRUD app in map view.

Update the add marker function to give the popup a delete button:

```javascript

      const popupContent = `<b>${title}</b><br><button onclick="deleteMarker(${id})">Delete Marker</button>`;
      marker.bindPopup(popupContent).openPopup();
```

And then add a function for deleting from the client side:

```javascript
// Function to delete a marker
  function deleteMarker(id) {
    const confirmed = confirm('Are you sure you want to delete this marker?');
    if (confirmed) {
      google.script.run.withSuccessHandler(() => {
        // Refresh the markers after deletion
        google.script.run.withSuccessHandler(addMarkers).getPinData();
      }).deleteMarker(id);
    }
  }
```

Then add the matching function to the Code.gs file:

```javascript
function deleteMarker(id) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sh = ss.getSheetByName('map_pin');
  const data = sh.getDataRange().getValues();

  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === id) {  // ID column (index 0)
      sh.deleteRow(i + 1);  // Delete the row
      break;
    }
  }
}
```

## What's Next?

There's a ton more you could do from here, like adding other data points to each marker, dynamic background images, or other click and drag interactions. You could even make a game! Got an idea for a use case? Drop a comment below!