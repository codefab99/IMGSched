import React, {Component} from 'react';
import PropTypes from 'prop-types';

var path= window.location.pathname;
var room = path.substring(path.lastIndexOf('/') + 1);
var url = window.location.href;
var myParam = window.location.search.split('user=')[1];

export const CommentSocket = new WebSocket(
    'ws://' + '127.0.0.1:8000' + '/ws/IMGSched/' + room + '/'
);

class Comment extends React.Component{
    constructor(props){
        super(props);
        console.log(this.props);

        this.state = {
            comments:[],
            isloading:true,
            errors:null,
        };
        this.getComment = this.getComment.bind(this);
        this.submit = this.submit.bind(this);
        this.getComment();
        CommentSocket.onmessage = function(e){
            var data = JSON.parse(e.data);
            var message = data['message'];
            document.querySelector('#comment-log').value += (message + '\n');
        };
    }

    getComment(){
        fetch('http://127.0.0.1:8000/IMGSched/comment/'+room,{
            method:'GET',
            headers:{
                'Authorization': `JWT ${window.localStorage.getItem('token')}`
            }
        })

        .then(response => response.json())
        .then((response) => {
            this.setState({
                comments: response,
                isloading: false,
            });
        })
        .catch(function(error){
        console.log(error);
        });
    }

    submit(e){
        document.querySelector('#comment-message-enter').onkeyup = function(e){
            if(e.keyCode === 13){
                document.querySelector('#comment-message-submit').click();
            }
        };

        var messageInputDom = document.querySelector('#comment-message-input');
        var message = messageInputDom.value;
        CommentSocket.send(JSON.stringify({
            'message':message,
            'user': myParam
        }));
        this.getComment();
        messageInputDom.value = '';        
    }

    render(){

        const{ isloading, comments } = this.state;
        return(
            <div>
                <textarea id="comment-log" cols="50" rows="100"></textarea><br/>
                <input id="comment-message-enter" type="text" size="50"/><br/>
                <input id="comment-message-submit" type="button" value="Comment" onClick={this.submit}/>
                <React.Fragment>
                    <div>
                        {!isloading ? (
                            comments.map(comment => {
                                const { id, comment_user, time, comment_text} = comment;
                                return (
                                    <div key={id}>
                                        <h2>{id}</h2>
                                        <h2>{comment_user}</h2>
                                        <h2>{comment_text}</h2>
                                        <h2>{time}</h2>
                                        </div>
                                );
                            })
                        ) : (
                            <p>Loading...</p>
                        )}
                    </div>
                </React.Fragment>
            </div>
        )
    }
}
export default Comment;