import * as firebase from 'react-firebase';

// firebase junk 
const API_KEY = process.env.API_KEY

// Your web app's Firebase configuration
var firebaseConfig = {
    apiKey: API_KEY,
    authDomain: "discord-plays.firebaseapp.com",
    databaseURL: "https://discord-plays.firebaseio.com",
    projectId: "discord-plays",
    storageBucket: "discord-plays.appspot.com",
    messagingSenderId: "684539998887",
    appId: "1:684539998887:web:2504f87bf0ff5d238f6182"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

export default firebase;