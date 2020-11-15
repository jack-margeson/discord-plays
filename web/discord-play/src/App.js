import './App.css';
import Logo from './images/title.svg'
import Background from './images/site-background.png'
import { Grid } from '@material-ui/core'
import firebase from 'firebase/app'
import 'firebase/auth'
import 'firebase/firestore'

// Grab firebase variables from /.env.
var API_KEY = process.env.API_KEY;

firebase.initializeApp({
  apiKey: API_KEY,
  authDomain: "discord-plays.firebaseapp.com",
  projectId: "discord-plays"
});

var db = firebase.firestore();
var shown_commands = [];

db.collection('commands').onSnapshot(function(querySnapshot) {
  var commands = [];
  querySnapshot.forEach(function(doc) {
    commands.splice(parseInt(doc.id), 0, doc.data().name+ " " + doc.data().command);
  });

  shown_commands = commands.slice(Math.max(commands.length - 5, 1));
  console.log(shown_commands);
});

const styles = {
  main: {
    backgroundImage: `url(${Background})`
  }
}

function App() {
  return (
    <Grid container style={styles.main} spacing={0} direction="column" alignContent="center" justify="center">
      <Grid
        container
        spacing={0}
        direction="column"
        alignContent="center"
        className="main-container"
      >
        <Grid item xs={12} className="title">
          <Grid container spacing={0} direction="column" alignContent="center" justify="center">
            <img className="logo" src={Logo} alt="DiscordPlays Logo" />
          </Grid>
        </Grid>
        <Grid item xs={12} className="youtube-embed">
          <Grid container spacing={0} direction="column" alignContent="center" justify="center">
            <iframe title="Youtube" className="video" width="560" height="315" src="https://www.youtube.com/embed/L9YKs_pmZMg" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" ></iframe>
          </Grid>
        </Grid>
        <Grid item xs={12} className="discord-embed">
          <Grid container spacing={0} direction="row" alignContent="center" justify="center">
            <Grid item xs={6} className="statistics">
              <Grid container spacing={0} direction="column" alignContent="center" justify="center">
                <div className="statistics-text">
                  <span>Anarchic gaming, now with friends! </span><br></br><br></br><br></br>
                  <span>Discord is a social chat platform for friends and communities to congregate online. With discord-plays, you can play your favorite games together as one, but with a twist: everyone is using the same controller! Work together with everyone to get a high score on your favorite games, or, screw over your friends by making your character jump over and over again.</span><br></br><br></br><br></br>
                  <span>Try it out now by joining our Discord on the right! We hope you have as much fun playing with discord-plays  as we did making it.</span><br></br><br></br><br></br>
                  <span>- Drew, Landon, Jack, and Cameron (the discord-plays team)</span>
                </div>
              </Grid>
            </Grid>
            <Grid item xs={6} className="join-discord">
              <Grid container spacing={0} direction="column" alignContent="center" justify="center">
                <iframe title="Discord" src="https://discord.com/widget?id=776947521166639154&theme=dark" width="350" height="500" allowtransparency="true" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
}

export default App;
