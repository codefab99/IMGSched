import React, {Component} from 'react';
import Service from './Service';

const service = new Service();

class MeetingDetail extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            users:[1],
            invitees:[1]
        };
        this.handleSubmit = this.handleSubmit.bind(this);
        this.getUsers = this.getUsers.bind(this);
        this.getUsers();
    }

    componentDidMount(){
        const {match: {params}} = this.props;
        if(params && params.pk)
        {
            service.getMeeting(params.pk).then((meeting)=>{
                this.refs.meeting_text.value = meeting.meeting_text;
                this.refs.host.value = meeting.host;
                this.refs.meeting_type.value = meeting.meeting_type;
                this.refs.created_on.value = meeting.created_on;
                this.refs.invitees.value = meeting.invitees;
                this.refs.meeting_time.value = meeting.meeting_time;
            })
        }
        }

        handle_Change2 = m => {
            let value = Array.from(m.target.selectedOptions, option => option.value);
            this.setState({invitees:value});
        }

        handleUpdate(pk){
            serice.updateMeeting(
                {
                    "pk": pk,
                    "text": this.refs.meeting_text.value,
                    "host": this.refs.host.value,
                    "type": this.refs.meeting_type.value,
                    "created": this.refs.created_on.value,
                    "invitees": this.refs.invitees.value,
                    "time": this.refs.meeting_time.value,
                }
            ).then((result)=>{
                alert("Meeting updated!");
            }).catch(function(error){
                console.log(error)
            });

    }

    handleSubmit(event){
        const { match: {params}} = this.props;

        if(params && params.pk){
            this.handleUpdate(params.pk);
        }
        event.preventDefault();

    }

    getUsers() {
        fetch('http://127.0.0.1:8000/IMGSched/userlist', {
            method:'GET',
            headers: {
                'Authorization': `JWT ${window.localStorage.getItem('token')}`
            }
        })

        .then(response => response.json())
        .then((response) => {
            console.log(response.json);
            this.setState({});
        })
        .catch(error => this.setState({ error, isloading: false}));
    }

    render(){
        <form onSubmit={this.handleSubmit}>
        <div className="form-group">
            <label>Meeting Text:</label>
            <input className="form-control" type="text" placeholder="Text"/>

            <label>Type:</label>
            <input className="form-control" type="text" placeholder="Text"/>

            <label>Meeting Text:</label>
            <input className="form-control" type="text" placeholder="Text"/>

            <label>Meeting Text:</label>
            <input className="form-control" type="text" placeholder="Text"/>


        </div>
        </form>
    }
}
export default MeetingDetail;