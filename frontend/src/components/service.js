import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export default class Service{

	constructor(){}

	getMeeting(pk) {
		const url = `${API_URL}/IMGSched/test/${pk}`;
		return axios.get(url).then(response => response.data);
	}

	deleteMeeting(meeting){
          const url = `${API_URL}/IMGSched/test/${meeting.pk}`;
          return axios.delete(url);
	}
	updateMeeting(meeting){
		const url =`${API_URL}/IMGSched/test/${meeting.pk}`;
		const headers = {
         'Authorization': `JWT ${window.localStorage.getItem('token')}`
      };
		return axios.put(url,meeting,{headers});
	}
	getComment(gk) {
		const url = `API_URL/IMGSched/comment/${gk}`;
		const headers = {
         'Authorization': `JWT ${window.localStorage.getItem('token')}`
      };
		return axios.get(url,{headers}).then(response => response.data);

	}
}
