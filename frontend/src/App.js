import React from 'react';
import './App.css';
import { BrowserRouter as Router, Switch, Route } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import TranslateScreen from './screens/TranslationScreen';
import About from './screens/about';
import HistoryAndFavorite from './screens/HistoryAndFavorite';
import Login from './screens/Login';
import Register from './screens/Register';
import ForgotPassword from './screens/ForgotPassword';
import RulesAndPolicy from './screens/RulesAndPolicy';
import Help from './screens/Help';

function App() {
	return (
		<Router>
			<Navbar />
			<Switch>
				<Route path='/' exact component={TranslateScreen} />
				<Route path='/about' exact component={About} />
				<Route path='/historyAndFavorite' exact component={HistoryAndFavorite} />
				<Route path='/login' exact component={Login} />
				<Route path='/register' exact component={Register} />
				<Route path='/forgot-password' exact component={ForgotPassword} />
				<Route path='/rules-and-policy' exact component={RulesAndPolicy} />
				<Route path='/help' exact component={Help} />
			</Switch>
		</Router>
	);
}

export default App;
