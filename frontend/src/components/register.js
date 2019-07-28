import React, {Component} from 'react';
import PropTypes from 'prop-types';

class Signup extends React.Component {
    state = {
        username:'',
        password:'',
        is_staff:false,
    };

    handle_change = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState(prevstate => {
            const newState = { ...prevstate };
            newState[name] = value;
            return newState;
        });
    };

    toggle_change = e => {
        this.setState({
            is_staff: !this.state.is_staff,
        });
    }

    render(){
        return(
            <form onSubmit={e => this.props.handle_submit(e, this.state)}>
                <h3>Signup</h3>
                <label>Username</label>
                <input type="text" name="username" placeholder="Username" value={this.state.username} onChange={this.handle_change}/>
                <label>Admin</label>
                <input type="checkbox" name="is_staff" value={this.state.is_staff} onChange={this.toggle_change}/>
                <label>Password</label>
                <input type="password" name="password" placeholder="********" value={this.state.password} onChange={this.state.handle_change}/>
                <input type="submit"/>
            </form>
        );
    }
}

export default Signup;

Signup.propTypes = {
    handle_submit: PropTypes.func.isRequired
}