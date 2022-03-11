const Reducer = (state, action) => {
	switch (action.type) {
	case 'show':
		return {
			...state,
			showSideBar: true
		};
	case 'hiden':
		return {
			...state,
			showSideBar: false
		};
	default:
		return state;
	}
};

export default Reducer;