import React, {createContext, useState} from 'react';
// import Reducer from './reducerSidebar';

// const initialState = {
// 	showSideBar: false,
// };
export const Context = createContext(null);
// eslint-disable-next-line react/prop-types
const Store = ({children}) => {
	const [sidebar, setSidebar] = useState(false);
	// const [state, dispatch] = useReducer(Reducer, initialState);
	return (
		<Context.Provider value={[sidebar, setSidebar]}>
			{children}
		</Context.Provider>
	);
};

export default Store;