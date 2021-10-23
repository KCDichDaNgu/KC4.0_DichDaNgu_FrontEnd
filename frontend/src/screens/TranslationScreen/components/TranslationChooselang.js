import React from 'react';
import PropTypes from 'prop-types';

import Tabs, { tabsClasses } from '@mui/material/Tabs';
import { Typography, IconButton, Tab, Tooltip } from '@mui/material';
import PageviewIcon from '@mui/icons-material/Pageview';
import { STATE } from '../../../redux/reducers/translateFileReducer';
import SwapHorizIcon from '@mui/icons-material/SwapHoriz';
import { useTranslation } from 'react-i18next';
import { connect } from 'react-redux';
import { 
	changeSource, 
	changeTarget, 
	swapTranslate, 
	translationAsync, 
	translationAndDetectAsync,
	changeSourceText, 
	reset,
	changeTargetText,
	changeDetectLang,
} from '../../../redux/actions/translateAction';

function TranslationChooselang(props) {
	const { translationFileState, translationState, isTranslate } = props;
	const { t } = useTranslation();

	/**
 	* @description Function hoán đổi loại ngôn ngữ
 	*/
	const handleSwap = () => {
		props.swapTranslate(translationState.translateCode.targetLang,translationState.translateCode.sourceLang);
		if( translationState.translateText.targetText !== '' && isTranslate){
			props.changeSourceText(translationState.translateText.targetText);
			props.changeTargetText(translationState.translateText.sourceText);
		}
	};

	/**
 	* @description Function thay đổi loại ngôn ngữ source
	* Trong TH đã có kết quả dịch, sẽ reset kết quả về rỗng
 	*/
	const handleChangeFrom = (event, newValue) => {
		props.changeSource(newValue);
		if(isTranslate){
			if(translationState.translateCode.detectLang !== null) {
				props.changeDetectLang(null);
			}
			if( translationState.translateText.targetText !== ''){
				props.changeTargetText('');
			}
		}
	};

	/**
 	* @description Function thay đổi ngôn ngữ target, 2 TH: 
	* 1. Có kết quả dịch => reset lại target text => gọi lại hàm dịch.
	* 2. Ko có kết quả dịch => không gọi lại hàm dịch.
 	*/
	const handleChangeTo = (event, newValue) => {
		props.changeTarget(newValue);
		if(isTranslate){
			if( translationState.translateText.targetText !== '' ){
				props.changeTargetText('');
				if(translationState.translateCode.sourceLang){
					props.translationAsync({
						sourceText: translationState.translateText.sourceText,
						sourceLang: translationState.translateCode.sourceLang,
						targetLang: newValue,
					});
				} else {
					props.translationAndDetectAsync({
						sourceText: translationState.translateText.sourceText,
						targetLang: newValue,
					});
				}
			}
		}
	};

	const showColorText = () => {
		if(translationState.currentState === STATE.FAILURE){
			return '#ff1744';
		}
		return null;
	};

	const isDisableTab = () => {
		return translationState.currentState === STATE.LOADING || translationFileState.currentState === STATE.LOADING;
	};

	return (
		<div style={{ borderBottom: '1px solid #ccc', display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}} >
			{/* ChooseLang */}
			<div style={{ flex: 1, display: 'flex', overflow:'auto', whiteSpace: 'nowrap'}}>
				<Tabs 
					value={translationState.translateCode.sourceLang} 
					onChange={handleChangeFrom} 
					variant="scrollable"
					scrollButtons='auto'
					sx={{
						[`& .${tabsClasses.scrollButtons}`]: {
									  '&.Mui-disabled': { opacity: 0.3 },
						},
								  }}
				>
					{isTranslate ?
						<Tab
							icon={translationState.translateCode.detectLang? 
								null : 
								<Tooltip title={t('Translate.phathienngonngu')}><PageviewIcon fontSize='medium'/></Tooltip>}
							label={translationState.translateCode.detectLang?
								<Typography color={showColorText()}>{translationState.translateCode.detectLang}</Typography>:
								null
							}
							sx={{
								minWidth: 'auto',
								minHeight: 'auto',
							}}
							value={null}
							disabled={isDisableTab()} 
							style={{fontWeight: 'bold'}}
						/> : null}
					{translationState.isSwap ? <Tab label={t('Translate.listLanguage.anh')} value={'en'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
					{translationState.isSwap ? <Tab label={t('Translate.listLanguage.trung')} value={'zh'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
					{translationState.isSwap ? <Tab label={t('Translate.listLanguage.lao')} value={'lo'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
					{translationState.isSwap ? <Tab label={t('Translate.listLanguage.khome')} value={'km'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
					{!translationState.isSwap ? <Tab label={t('Translate.listLanguage.viet')} value={'vi'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
				</Tabs>
			</div>
			<div style={{  alignSelf: 'center'}}>
				<IconButton 
					aria-label="Example" 
					onClick={handleSwap} 
					disabled={translationState.translateCode.sourceLang === null || isDisableTab()}>
					<SwapHorizIcon fontSize='medium'/>
				</IconButton>
			</div>
			<div style={{ flex: 1, display: 'flex', overflow:'auto', whiteSpace: 'nowrap'}}>
				<Tabs 
					value={translationState.translateCode.targetLang} 
					onChange={handleChangeTo} 
					variant="scrollable"
					scrollButtons='auto'
					sx={{
						[`& .${tabsClasses.scrollButtons}`]: {
									  '&.Mui-disabled': { opacity: 0.3 },
						},
								  }}
				>
					{!translationState.isSwap ? <Tab label={t('Translate.listLanguage.anh')} value={'en'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
					{!translationState.isSwap ? <Tab label={t('Translate.listLanguage.trung')} value={'zh'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
					{!translationState.isSwap ? <Tab label={t('Translate.listLanguage.lao')} value={'lo'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
					{!translationState.isSwap ? <Tab label={t('Translate.listLanguage.khome')} value={'km'} disabled={isDisableTab()}style={{fontWeight: 'bold'}}/> : null}
					{translationState.isSwap ? <Tab label={t('Translate.listLanguage.viet')} value={'vi'} disabled={isDisableTab()} style={{fontWeight: 'bold'}}/> : null}
				</Tabs>
			</div>
		</div>
	);
}

TranslationChooselang.propTypes = {
	isTranslate: PropTypes.bool.isRequired,
	translationFileState: PropTypes.object,
	translationState: PropTypes.object,
	changeSource: PropTypes.func,
	changeTarget: PropTypes.func,
	swapTranslate: PropTypes.func,
	translationAsync: PropTypes.func,
	translationAndDetectAsync: PropTypes.func,
	changeSourceText: PropTypes.func,
	changeTargetText: PropTypes.func,
	changeDetectLang: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationState: state.translateReducer,
	translationFileState: state.translateFileReducer 
});

const mapDispatchToProps = { 
	changeSource, 
	changeTarget, 
	swapTranslate, 
	translationAsync, 
	translationAndDetectAsync,
	changeSourceText, 
	reset,
	changeTargetText,
	changeDetectLang,
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslationChooselang);
