const functions = require("firebase-functions");
const admin = require("firebase-admin");
const cors = require("cors")({origin: true});
const express = require("express");

admin.initializeApp();

const app = express();
const db = admin.firestore();
const weatherCollection = "weather-points";

app.use(cors);

app.get("/api/status", async (req, res) => {
  const date = new Date();
  res.json({status: "backend is working", date: date.toString()});
});

app.post("/api/weather", async (req, res) => {
  console.log("1");
  try {
    const weatherData = {
      humidity: {
        value: req.body["humidity"],
        unit: "%",
      },
      temperature: {
        value: req.body["temperature"],
        unit: "°C",
      },
      wind: {
        value: req.body["wind"],
        unit: "m/s",
      },
      date: new Date(),
    };
    console.log("2");
    const newDoc = await db.collection(weatherCollection).add(weatherData);
    console.log("3");
    res.status(201).json({status: `New weather data ${newDoc.id}`});
    console.log("4");
  } catch (err) {
    res.status(400).json({error:
      "Weather data should cointain humidity, temperature and wind fields."});
    console.log("5");
  }
});

exports.app = functions.https.onRequest(app);
