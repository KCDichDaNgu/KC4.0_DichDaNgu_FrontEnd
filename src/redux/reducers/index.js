import { combineReducers } from 'redux';
import translateReducer from './translateReducer';
import navbarReducer from './navbarReducer';
import historyReducer from './historyReducer';
import translateFileReducer from './translateFileReducer';
import userReducer from './userReducer';
import systemSettingReducer from './systemSettingReducer';

export default combineReducers({ 
    translateReducer, 
    navbarReducer, 
    historyReducer, 
    translateFileReducer,
    userReducer,
    systemSettingReducer 
});
