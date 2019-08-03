
import React,{ Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Profile from './components/profile';
import Nav from './components/nav';
import LoginForm from './components/Login';
import SignupForm from './components/register';
import './App.css';
import {GoogleLogin, GoogleLogout} from 'react-google-login';


class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      displayed_form: '',
      logged_in: localStorage.getItem('token') ? true : false,
      username: '',
    };
    this.google_sign = this.google_sign.bind(this);
  }

  componentDidMount() {
    if (this.state.logged_in) {
      fetch('http://127.0.0.1:8000/IMGSched/current_user/', {
        headers: {
             'Authorization': `JWT ${window.localStorage.getItem('token')}`  
      }
      })
        .then(res => res.json())
        .then(json => {
          this.setState({ username: json.username, is_staff: json.is_staff });
        });
    }
  }

  handle_login = (event, data) => {
    event.preventDefault();
    fetch('http://127.0.0.1:8000/IMGSched/token-auth/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    }).then((response) => response.json())
      .then(json => {
        window.localStorage.setItem('token', json.token);
        window.location.reload();
        this.setState({
          displayed_form: '',
          username: json.username,
          logged_in: true,
        });
      }); 
  };

  handle_signup = (e, data) => {
    e.preventDefault();
    fetch('http://127.0.0.1:8000/IMGSched/userlist/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(res => res.json())
      .then(json => {
        window.localStorage.setItem('token', json.token);
        console.log(data);
        this.setState({
          displayed_form: '',
          username: json.username,
          is_staff: json.is_staff,
          logged_in: true
        });
      });
  };

  handle_logout = () => {
    localStorage.removeItem('token');
    this.setState({ logged_in: false, username: '' });
  };
   google_sign(googleUser) {
    this.setState({
          username: googleUser.getBasicProfile().getName(),
        });
   }
  display_form = form => {
    this.setState({
      displayed_form: form
    });
  };

  render() {
    let form;
    switch (this.state.displayed_form) {
      case 'login':
        form = <LoginForm handle_login={this.handle_login} />;
        break;
      case 'signup':
        form = <SignupForm handle_signup={this.handle_signup} />;
        break;
      default:
        form = null;
    }

     const responseGoogle = (response) => {
      console.log(response.tokenId);
      fetch('https://www.googleapis.com/oauth2/v3/tokeninfo?id_token='+response.tokenId, {
        method:'GET',
    }).then((response) => response.json())
      .then(json => {
        window.localStorage.setItem('token',response.tokenId);
      });
    }
    if(!this.state.logged_in){
    return (
      <div className="App">
        <Nav
          logged_in={this.state.logged_in}
          display_form={this.display_form}
          handle_logout={this.handle_logout}
        />
        {form}
        <h3> OR </h3>
        <br />
        <GoogleLogin
        clientId='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        buttonText="LOGIN WITH GOOGLE"
        onSuccess={responseGoogle}
        onFailure={responseGoogle}
        />
        <h3>
          {this.state.logged_in
            ? `Hello,`
            : 'Login with Google'}

        </h3>
      </div>
    );
  }
  else {
    return (
        <Profile handle_logout={this.handle_logout} username={this.state.username} />
    )
  }
}
}

export default App;

