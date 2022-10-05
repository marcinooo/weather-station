import  { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import 'bootstrap/dist/css/bootstrap.min.css';

import Header from './components/Header';
import TemperatureChart from './components/TemperatureChart';
import HumidityChart from './components/HumidityChart';
import WindChart from './components/WindChart';
import StationInfoBox from './components/StationInfoBox';
import { db } from './firebase';
import { collection, getDocs, query, orderBy, limit } from "firebase/firestore"; 
import './App.css';


function App() {

  const [stationData, stationDataSet] = useState({});
  const [temperatureData, temperatureDataSet] = useState([]);
  const [humidityData, humidityDataSet] = useState([]);
  const [windData, windDataSet] = useState([]);

  useEffect(() => {
    async function  getTemperatureData() {
      const q = query(collection(db, "weather-points"), orderBy("date"), limit(24));
      const querySnapshot = await getDocs(q);

      const chartTemeperatureData = [];
      const chartHumidityData = [];
      const chartWindData = [];
      querySnapshot.forEach((doc) => {
        const docData = doc.data();
        const dateOfData = docData.date.toDate();
        const hours = `${dateOfData.getHours()}:${dateOfData.getMinutes()}`;
        chartTemeperatureData.push({date: hours, temperature: docData.temperature.value});
        chartHumidityData.push({date: hours, humidity: docData.humidity.value});
        chartWindData.push({date: hours, wind: docData.wind.value});
      });
      temperatureDataSet(chartTemeperatureData);
      humidityDataSet(chartHumidityData);
      windDataSet(chartWindData);

      const lastWeatherPoint = querySnapshot.docs[querySnapshot.docs.length-1].data();
      const stationInfoBoxData = {
        lastWeaterPointDate: lastWeatherPoint.date.toDate().toString(),
      };
      stationDataSet(stationInfoBoxData);
    };

    getTemperatureData();
  }, []);
  
  return (
    <Container className="mainContainer">
      <Header/>
      <StationInfoBox data={stationData}/>
      <hr/>
      <TemperatureChart data={temperatureData}/>
      <HumidityChart data={humidityData}/>
      <WindChart data={windData}/>
    </Container>
  );
}

export default App;
