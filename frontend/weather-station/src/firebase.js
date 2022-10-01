// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getFirestore } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBQFRjgAvMi0dZrpJSHz1S76JMTTnJfzUk",
  authDomain: "weather-stations-w1.firebaseapp.com",
  projectId: "weather-stations-w1",
  storageBucket: "weather-stations-w1.appspot.com",
  messagingSenderId: "620216359571",
  appId: "1:620216359571:web:80c2772dbf41b1d8bf8b66",
  measurementId: "G-GNGN1Y1X2X"
};

// Initialize Firebase
export const app = initializeApp(firebaseConfig);
export const analytics = getAnalytics(app);
export const db = getFirestore(app);
