import { combineReducers } from 'redux';
import translateReducer from './translateReducer';
import navbarReducer from './navbarReducer';
import historyReducer from './historyReducer';
import translateFileReducer from './translateFileReducer';
import userReducer from './userReducer';

export default combineReducers({ translateReducer, navbarReducer, historyReducer, translateFileReducer,userReducer });
