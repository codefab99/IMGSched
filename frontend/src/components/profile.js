import React, {Component} from 'react';
import PropTypes from 'prop-types';
import MeetingForm from './MeetingForm';
import {Link} from 'react-router-dom';
import axios from 'axios';
import Service from './Service';
import {Redirect} from 'react-router-dom';
import MeetingComment from './MeetingComment';

const service = new Service();
class  profile extends React.Component{
constructor(props) {
    super(props); 
    this.state = {
      meetings: [],
      isloading: true,
      errors: null,
    };
    this.getPosts = this.getPosts.bind(this);
    this.handleDelete = this.handleDelete.bind(this);
    this.getPosts();
   }

   getPosts() {
    fetch('http://127.0.0.1:8000/IMGSched/test/',{
    	method:'GET',
    	headers: {
         'Authorization': `JWT ${window.localStorage.getItem('token')}`
      }
    })
   	.then(response => response.json())
   	.then((response) => {
   		console.log(response.json);
   		this.setState({
   			meetings: response,
   			isloading: false,
   		});
   	})
   	.catch(function(error){
           console.log(error);
       });
   }
   handleDelete(e, pk){
   	service.deleteMeeting({pk : pk}).then(()=>{
   		this.setState({
   			meetings : []
   		})
   	   this.getPosts();
   	});
   }


   render() {
   	   const { isloading,meetings } =this.state;
   	   const username = this.props.username;
   		return(
             <div>
			<h1>hello {this.props.username}  </h1>
			<ul>
              <li onClick = {this.props.handle_logout}>logout</li>
  			</ul>
			<Link to='/MeetingForm'>add meeting</Link>
              <React.Fragment>
              <div>
          {!isloading ? (
            meetings.map(meeting => {
              const { pk,purpose,detail,venue,datetime,host,invitees } = meeting;
              return (
                <div key={pk}>
                <h2>{pk}</h2>
                  <h2>{purpose}</h2>
                  <p>{detail}</p>
                  <h3>{venue}</h3>
                  <h3> {datetime}</h3>
                  <h3> {host} </h3>
                  <button  onClick={(e)=>  this.handleDelete(e,meeting.pk) }> Delete</button>
                  <a href={"/MeetingDetail/"+meeting.pk}>Update </a>
                  <a href={"/Comment/"+meeting.pk+"?user="+username}> COMMENTS </a>
                  
                  <hr />
                </div>
              );
            })
          ) : (
            <p>Loading...</p>
          )}
        </div>
        </React.Fragment>
			 </div>
  )}
  } 
export default profile;
profile.propTypes = {
  handle_logout: PropTypes.func.isRequired
};