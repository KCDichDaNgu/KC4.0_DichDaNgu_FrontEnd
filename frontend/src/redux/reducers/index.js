import { combineReducers } from 'redux';
import translateReducer from './translateReducer';
import navbarReducer from './navbarReducer';
import historyReducer from './historyReducer';
import translateFileReducer from './translateFileReducer';

export default combineReducers({ translateReducer, navbarReducer, historyReducer, translateFileReducer });
