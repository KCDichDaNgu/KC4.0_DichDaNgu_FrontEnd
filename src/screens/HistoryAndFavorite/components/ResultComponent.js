import React from 'react';
import PropTypes from 'prop-types';
import { Typography, IconButton } from '@mui/material';
import styles from '../historyAndFavorite.module.css';
import { connect } from 'react-redux';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import TextareaAutosize from 'react-textarea-autosize';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import { useTranslation } from 'react-i18next';
import SendIcon from '@mui/icons-material/Send';
import { get } from 'lodash';
import { Link } from 'react-router-dom';
import { 
	changeSource,
	changeSourceText,
	changeTarget,
	changeTargetText,
	swapTranslate
} from '../../../redux/actions/translateAction';

function ResultComponent(props) {
	const {historyState, translateState} = props;
	const { t } = useTranslation();

	const changeCodeToText = (code) => {
		switch (code) {
		case 'en':
			return t('Translate.listLanguage.anh');
		case 'vi':
			return t('Translate.listLanguage.viet');
		case 'zh':
			return t('Translate.listLanguage.trung');
		case 'lo':
			return t('Translate.listLanguage.lao');
		case 'km':
			return t('Translate.listLanguage.khome');
		default:
			return code;
		}
	};

	return (
		<div className={styles.innerBodyRight}>
			<div style={{display: 'flex', justifyContent: 'space-between', marginBottom: 20, alignItems: 'center'}}>
				<Typography variant='h5'>
					{changeCodeToText(get(historyState.currentHistory, 'source_lang', ''))} 
					<ArrowForwardIcon style={{marginLeft: 10, marginRight: 10}}/> 
					{changeCodeToText(get(historyState.currentHistory, 'target_lang', ''))} 
				</Typography>
				{historyState.currentHistory ? 
					<div style={{display: 'flex'}}>
						<Link to='/'>
							<IconButton type="submit" sx={{ p: '10px' }} aria-label="search" onClick={() => {
								// Swap true: en, zh, lo, km => vn , False: vn => en, zh, lo, km
								if(translateState.isSwap){
									if(historyState.currentHistory.source_lang === 'vi'){
										props.swapTranslate(historyState.currentHistory.source_lang, historyState.currentHistory.target_lang);
									}else {
										props.changeSource(historyState.currentHistory.source_lang);
										props.changeTarget(historyState.currentHistory.target_lang);
									}
								}else{
									if(historyState.currentHistory.source_lang !== 'vi'){
										props.swapTranslate(historyState.currentHistory.source_lang, historyState.currentHistory.target_lang);
									}else{
										props.changeSource(historyState.currentHistory.source_lang);
										props.changeTarget(historyState.currentHistory.target_lang);
									}
								}
								props.changeSourceText(historyState.currentHistory.source_text);
								props.changeTargetText(historyState.currentHistory.target_text);
							}}>
								<SendIcon />
							</IconButton>
						</Link>
					</div> : null}
			</div>
			<div className={styles.innerBodyRightBox} style={{marginBottom: 40}}>
				<TextareaAutosize
					minRows={3}
					disabled
					value={get(historyState.currentHistory, 'source_text', '')}
					className={[styles.from_language]}
				/>
				<div style={{marginTop: 30, display: 'flex', justifyContent: 'flex-end'}}>
					<IconButton 
						type="submit" 
						sx={{ p: '10px' }} 
						aria-label="search" 
						size='large' 
						onClick={() => navigator.clipboard.writeText(historyState.currentHistory.source_text)}
					>
						<ContentCopyIcon />
					</IconButton>
				</div>
			</div>
			<div className={styles.innerBodyRightBox}>
				<TextareaAutosize
					minRows={3}
					disabled
					value={get(historyState.currentHistory, 'target_text', '')}
					className={[styles.from_language]}
				/>
				<div style={{marginTop: 30, display: 'flex', justifyContent: 'flex-end'}}>
					<IconButton 
						type="submit" 
						sx={{ p: '10px' }} 
						aria-label="search" 
						size='large' 
						onClick={() => navigator.clipboard.writeText(historyState.currentHistory.target_text)}
					>
						<ContentCopyIcon fontSize='medium'/>
					</IconButton>
				</div>
			</div>
		</div>
	);
}

ResultComponent.propTypes = {
	historyState: PropTypes.object,
	translateState: PropTypes.object,
	changeSource: PropTypes.func,
	changeSourceText: PropTypes.func,
	changeTarget: PropTypes.func,
	changeTargetText: PropTypes.func,
	swapTranslate: PropTypes.func,
};

const mapStateToProps = (state) => ({
	historyState: state.historyReducer,
	translateState: state.translateReducer,
});

const mapDispatchToProps = { 
	changeSource,
	changeSourceText,
	changeTarget,
	changeTargetText,
	swapTranslate,
};

export default connect(mapStateToProps, mapDispatchToProps)(ResultComponent);