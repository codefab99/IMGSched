import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Redirect} from 'react-router-dom';

class MeetingForm extends React.Component{
    constructor(props){
        super(props);
        this.state= {
            users:[],
            success:0,
            meeting_text:"",
            meeting_type:1,
            host:2,
            invitees:[1],
            meeting_time:"2019--07-22T06:45:07Z",
            errors:null,
        };
        this.getUsers=this.getUsers.bind(this);
        this.getUsers();        
    }

    handleSubmit(e, data){
        e.preventDefault();
        let x=0;
        fetch('http://127.0.0.1:8000/IMGSched/test/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        }).then((response) => response.json())
        .then(json => {
            this.setState({
                success:1,
            })
        });
    }

    getUsers(){
        fetch('http://127.0.0.0:8000/IMGSched/userlist/', {
            method:'GET',
            headers: {
                'Authorization': `JWT ${window.localStorage.getItem('token')}`
            }
        })
        .then(response => response.json())
        .then((response) => {
            this.setState({
                users:response,
            });
        })
        .catch(function(error){
            console.log(error);
        });
    }

    handle_change = e => {
        const name = e.target.name;
        const value = e.target.value;
        this.setState({
            [name]: value
        });
        console.log(value);
    };

    handle_change2 = e => {
        let value = Array.from(e.target.selectedOptions, option => option.value);
        this.setState({invitees : value});
        console.log(this.state.invitees);
    }

    render(){
        if(this.state.success==1){
            return <Redirect to ="./"/>
        }

        return(
            <form onSubmit={e => this.handleSubmit(e, this.state)}>
                <label>Meeting Text</label>
                <input name="meeting_text" type="text" value={this.state.meeting_text} onChange={this.handle_change}/><br/>
                <label>Meeting Type</label>
                <select name="meeting_type" value={this.state.meeting_type} onChange={this.handle_change}>
                    <option value='1'>Public</option>
                    <option value='2'>Private</option>
                </select><br/>
                <label>Time</label>
                <input name="meeting_time" type="datetime-local" value={this.state.datetime} onChange={this.handle_change}/><br/>
                <label>Host</label>
                <select name="host" onChange={this.handle_change} value = {this.state.host} >
                {this.state.users.map(user => <option value={user.id}>{user.username}</option>)}
                </select><br />
                <label>Invitees</label>
                <select name="invitees" onChange={this.handle_change2} value = {this.state.invitees} multiple>
                {this.state.users.map(user => <option value={user.id}>{user.username}</option>)}
                </select>
                <input type="submit" />
            </form>
        );
    }

}

export default MeetingForm;