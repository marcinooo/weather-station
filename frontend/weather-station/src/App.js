import  { useState, useEffect } from 'react';
import Container from 'react-bootstrap/Container';
import 'bootstrap/dist/css/bootstrap.min.css';

import Header from './components/Header';
import TemperatureChart from './components/TemperatureChart';
import { db } from './firebase';
import { collection, getDocs } from "firebase/firestore"; 
import './App.css';


function App() {

  const [temperatureData, temperatureDataSet] = useState([]);

  useEffect(() => {
    async function  getTemperatureData() {
      const querySnapshot = await getDocs(collection(db, "weather"));
      const chartData = [];
      querySnapshot.forEach((doc) => {
        const docData = doc.data();
        console.log(`${doc.id} => ${docData}`);
        const dataObj = docData.date.toDate();
        const date = `${dataObj.getHours()}:${dataObj.getMinutes()}`;
        chartData.push({date: date, temperature: docData.temperature});
        console.log(date);
        temperatureDataSet(chartData);
      });
    };

    getTemperatureData();
  }, []);
  
  return (
    <Container className="mainContainer">
      <Header/>
      <hr/>
      <TemperatureChart data={temperatureData}/>
    </Container>
  );
}

export default App;
