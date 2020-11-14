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
console.log(db.collection('commands'));

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
            <iframe className="video" width="560" height="315" src="https://www.youtube.com/embed/NBFuzr_GnqQ" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          </Grid>
        </Grid>
        <Grid item xs={12} className="discord-embed">
          <Grid container spacing={0} direction="row" alignContent="center" justify="center">
            <Grid item xs={6} className="statistics">
              <Grid container spacing={0} direction="column" alignContent="center" justify="center">
                <div className="statistics-text">
                  <span>only 25% of you are subscribed please like and subscribe to pboco pbot on youutbe </span>
                </div>
              </Grid>
            </Grid>
            <Grid item xs={6} className="join-discord">
              <Grid container spacing={0} direction="column" alignContent="center" justify="center">
                <iframe src="https://discord.com/widget?id=776947521166639154&theme=dark" width="350" height="500" allowtransparency="true" frameborder="0" sandbox="allow-popups allow-popups-to-escape-sandbox allow-same-origin allow-scripts"></iframe>
              </Grid>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Grid>
  );
}

export default App;
