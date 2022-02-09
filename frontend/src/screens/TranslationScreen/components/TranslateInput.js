import React, { useRef } from 'react';
import PropTypes from 'prop-types';
import { 
	Col,
} from 'react-bootstrap';
import { IconButton } from '@mui/material';
import styles from '../translateStyle.module.css';
import TextareaAutosize from 'react-textarea-autosize';
import { STATE } from '../../../redux/reducers/translateReducer';
import { useTranslation } from 'react-i18next';
import { connect } from 'react-redux';
import { 
	changeSourceText, 
	reset,
	changeTargetText,
	changeDetectLang,
} from '../../../redux/actions/translateAction';
import CloseIcon from '@mui/icons-material/Close';

function TranslateInput(props) {
	const inputEl = useRef(null);

	const { translationState } = props;
	const { t } = useTranslation();

	/**
 	* @description Function check điều kiện để hiển thị nút x
 	*/
	 const isShowCloseButton = () => {
		if(translationState.currentState === STATE.LOADING) {
			return true;
		}
		if(translationState.translateText.sourceText === '') {
			return true;
		}
		if(translationState.translateText.sourceText === null) {
			return true;
		}
		return false;
	};

	/**
 	* @description Function thay đổi source text, đồng thời reset lại target text, detectLang
 	*/
	 const handleChangeSourceText = (evt) => {
		evt.preventDefault();
		props.changeSourceText(evt.target.value);
		if( translationState.translateText.targetText !== '' ){
			props.changeTargetText('');
		}
		if( translationState.translateCode.detectLang ){
			props.changeDetectLang(null);
		}
	};

	/**
 	* @description Function reset text nhập vào về rỗng => reset cả output text về rỗng
 	*/
	 const handleResetInput = () => {
		props.reset();
		inputEl.current.focus();
	};

	return (
		<Col md={6} style={{ 
			borderRight: '1px solid #ccc', 
			backgroundColor: translationState.currentState === STATE.LOADING ? '#f3f3f3' : 'white'  
		}}>
			<div style={{
				paddingTop: '10px', 
				paddingBottom: '30px', 
				display: 'flex',
			}}>
				<>
					<div style={{ paddingRight: '0', flex: 1 }} >
						<TextareaAutosize
							ref={inputEl}
							minRows={3}
							disabled={translationState.currentState === STATE.LOADING}
							onChange={handleChangeSourceText}
							value={translationState.translateText.sourceText}
							className={[styles.from_language]}
							// onKeyPress={(e) => e.key === 'Enter' ? handleTranslate() : null }
							placeholder={t('Translate.nhapVanBan')}
						/>
					</div>
					<div md={1} style={{ padding: '0' }} className={['text-center']}>
						{!isShowCloseButton() ? 
							<IconButton aria-label="Example" onClick={handleResetInput} type="file">
								<CloseIcon fontSize='small'/>
							</IconButton> : null}
					</div>
				</>
			</div>
		</Col>
	);
}

TranslateInput.propTypes = {
	translationState: PropTypes.object,
	changeSourceText: PropTypes.func,
	changeTargetText: PropTypes.func,
	changeDetectLang: PropTypes.func,
	reset: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationState: state.translateReducer,
});

const mapDispatchToProps = { 
	changeSourceText, 
	reset,
	changeTargetText,
	changeDetectLang,
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslateInput);
