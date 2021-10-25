import React from 'react';
import PropTypes from 'prop-types';
import { 
	Col,
} from 'react-bootstrap';
import { IconButton } from '@mui/material';
import styles from '../translateStyle.module.css';
import TextareaAutosize from 'react-textarea-autosize';
import { STATE } from '../../../redux/reducers/translateReducer';
import { connect } from 'react-redux';
import { 
	translationAsync, 
	translationAndDetectAsync,
	changeTargetText,
} from '../../../redux/actions/translateAction';
import { useTranslation } from 'react-i18next';
import LoadingButton from '@mui/lab/LoadingButton';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';

function TranslateInput(props) {
	const { translationState, isTranslate } = props;
	const { t } = useTranslation();

	const isDisableTranslateButton = () => {
		if(translationState.currentState === STATE.LOADING) {
			return true;
		}
		if(translationState.translateText.sourceText === '' && isTranslate) {
			return true;
		}
		return false;
	};

	/**
 	* @description Function dịch từ, (Ấn enter hoặc ấn nút dịch từ)
	* 1. Trong trường hợp có kết quả dịch => reset lại kết quả dịch về rỗng => gọi lại dịch
	* 2. Còn lại thì dịch vs 2 TH => sourcelang === null (Nhận dạng ngôn ngữ) và sourcelang === vi,cn .. 
 	*/
	 const handleTranslate = () => {
		if( translationState.translateText.targetText !== '' ){
			props.changeTargetText('');
		}
		if(translationState.translateCode.sourceLang){
			props.translationAsync({
				sourceText: translationState.translateText.sourceText,
				sourceLang: translationState.translateCode.sourceLang,
				targetLang: translationState.translateCode.targetLang,
			});
		} else {
			props.translationAndDetectAsync({
				sourceText: translationState.translateText.sourceText,
				targetLang: translationState.translateCode.targetLang,
			});
		}
	};

	return (
		<Col 
			md={6} 
			className={styles.ResultTranslateBox} 
			style={{
				backgroundColor: translationState.translateText.targetText === '' ? '#f3f3f3' : 'white'
			}}>
			{translationState.translateText.targetText !== '' ?
				<div>
					<div className={styles.boxdich}>
						<TextareaAutosize
							disabled={true}
							minRows={3}
							style={{backgroundColor: 'white'}}
							value={translationState.translateText.targetText}
							className={[ styles.from_language ]}
						/> 
					</div>
					<div style={{ justifyContent: 'end', display: 'flex', paddingBottom: 5}}>
						<IconButton aria-label="Example" onClick={() => navigator.clipboard.writeText(translationState.translateText.targetText)}>
							<ContentCopyIcon fontSize='medium'/>
						</IconButton>
					</div>
				</div>
				: <div style={{
					backgroundColor: translationState.translateText.targetText === '' ? '#f3f3f3' : 'white' , 
					display: 'flex', 
					paddingTop: 10,
					paddingBottom: 10,
					justifyContent: 'start'
				}}>
					<LoadingButton 
						variant="contained" 
						onClick={handleTranslate}
						loading={translationState.currentState === STATE.LOADING}
						disabled={isDisableTranslateButton()}
						style={{ fontWeight: 'bold', display: 'flex'}}
					>
						{t('dich')}
					</LoadingButton>
				</div>	
			}
		</Col>
	);
}

TranslateInput.propTypes = {
	isTranslate: PropTypes.bool.isRequired,
	translationState: PropTypes.object,
	changeTargetText: PropTypes.func,
	translationAsync: PropTypes.func,
	translationAndDetectAsync: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationState: state.translateReducer,
});

const mapDispatchToProps = { 
	translationAsync, 
	translationAndDetectAsync,
	changeTargetText,
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslateInput);
