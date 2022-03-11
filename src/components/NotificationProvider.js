import React, { useContext, useReducer } from 'react';
import { v4 } from 'uuid';
import { ADD_NOTI, REMOVE_NOTI, INFO_NOTI } from '../constants/notificationConstant';
import NotificationBox from './NotificationBox';

const NotificationContext = React.createContext();

/**
 * Return a function which creates a new notification
 * The returned function takes 2 params
 * 
 * param {string} message the message to be displaed
 * param {string} type SUCCESS, INFO or ERROR, find the constants in
 * constants/notificationConstants.js
 * @author AnLG
 * @return { function(string, string) : void } returned function
*/
export const useNotification = () => {
	const dispatch = useContext(NotificationContext);

	const createNoti = (message, type = INFO_NOTI) => {
		dispatch({
			type: ADD_NOTI,
			payload: {
				id: v4(),
				type,
				message
			}
		});
	};
	
	return createNoti;
};

export default function NotificationProvider(props) {
	// eslint-disable-next-line react/prop-types
	const { children } = props;

	const [notifications, dispatch] = useReducer((state, action) => {
		switch (action.type) {
		case ADD_NOTI:
			return [...state, {...action.payload}];
		case REMOVE_NOTI:
			return state.filter(ele => ele.id !== action.id);
		default:
			break;
		}
	}, []
	);
	
	// {
	// 	id: v4(),
	// 	type: SUCCESS_NOTI,
	// 	message: 'Hello An'
	// }, {
	// 	id: v4(),
	// 	type: SUCCESS_NOTI,
	// 	message: 'Hello Dep Trai'
	// }


	return (
		<NotificationContext.Provider value={dispatch}>
			<div>
				<div className="notification-wrapper">
					{notifications
						.map(note => 
							<NotificationBox
								key={note.id}
								dispatchNoti={dispatch}
								id ={note.id} 
								message={note.message}
								type={note.type} />)
					}
				</div>
				{children}
			</div>
		</NotificationContext.Provider>
	);

}