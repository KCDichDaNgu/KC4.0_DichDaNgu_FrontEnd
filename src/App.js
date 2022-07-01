import React from 'react';
import './App.css';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';
import { BrowserRouter as Router, Switch, Route,  } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import TranslateScreen from './screens/TranslationScreen';
import About from './screens/about';
import HistoryAndFavorite from './screens/HistoryAndFavorite';
import Login from './screens/Login';
// import Register from './screens/Register';
// import ForgotPassword from './screens/ForgotPassword';
import RulesAndPolicy from './screens/RulesAndPolicy';
import Help from './screens/Help';
import UserManagement from './screens/UserManagement';
import UserTranslationHistoryFeedbackManagement from './screens/UserTranslationHistoryFeedbackManagement';
import SystemSetting from './screens/SystemSetting';

function App() {
	return (
		<Router>
			<Navbar />

			<Switch>
				<Route path='/translate' exact component={TranslateScreen} />
				<Route path='/' exact component={TranslateScreen}/> 
				<Route path='/about' exact component={About} />
				<Route path='/history-and-favorite' exact component={HistoryAndFavorite} />
				<Route path='/user-management' exact component={UserManagement} />
				<Route path='/system-setting' exact component={SystemSetting} />
				<Route path='/login' exact component={Login} />
				{/* <Route path='/register' exact component={Register} />
				<Route path='/forgot-password' exact component={ForgotPassword} /> */}
				<Route path='/rules-and-policy' exact component={RulesAndPolicy} />
				<Route path='/help' exact component={Help} />
				<Route path='/user-feedback-management' exact component={UserTranslationHistoryFeedbackManagement} />
			</Switch>

			<ToastContainer position="top-right" autoClose={5000} hideProgressBar={false} newestOnTop={false} closeOnClick rtl={false} pauseOnFocusLoss draggable pauseOnHover />
		</Router>
	);
}

export default App;
