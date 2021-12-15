import React, { useEffect, useState } from 'react';
import {
	Row,
	Col,
} from 'react-bootstrap';
import PropTypes from 'prop-types';
import styles from './translateStyle.module.css';
import { Button, Fab, } from '@mui/material';
import { connect } from 'react-redux';
import { STATE } from '../../redux/reducers/translateReducer';
import {
	changeSourceText,
	changeTargetText,
	changeSource,
} from '../../redux/actions/translateAction';
import {
	changeFileDocument, changeOutput
} from '../../redux/actions/translateFileAction';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import TranslateIcon from '@mui/icons-material/Translate';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { useTranslation } from 'react-i18next';
import ScrollTop from '../../components/ScrollTop';
import TranslateFileDocumentOutput from './components/TranslateFileDocumentOutput';
import TranslationChooselang from './components/TranslationChooselang';
import TranslateOutput from './components/TranslateOutput';
import TranslateInput from './components/TranslateInput';
import { TRANSLATE_TYPE, USER_STATUS } from '../../constants/common';
import TranslateFileDocumentInput from './components/TranslateFileDocumentInput';
import authHoc from '../../hocs/authHoc';
import { toastError } from '../../components/Toast';

function Index(props) {
	const { translationState, translationFileState } = props;
	const { t } = useTranslation();
	const [translateType, setTranslateType] = useState(TRANSLATE_TYPE.plainText);

	/**
	 * @description useEffect cho việc check kết quả và báo noti cho 
	 * người dùng
	 */
	useEffect(() => {
		switch (translationState.currentState) {
		case STATE.SUCCESS:
			break;
		case STATE.FAILURE:
			// toastError(translationState.err);
			break;
		default:
			break;
		}
	}, [translationState.currentState]);

	/**
	 * @description useEffect cho việc check kết quả và báo noti cho 
	 * người dùng
	 */
	useEffect(() => {
		switch (translationFileState.currentState) {
		case STATE.SUCCESS:
			break;
		case STATE.FAILURE:
			toastError(translationFileState.err);
			break;
		default:
			break;
		}
	}, [translationFileState.currentState]);


	const getIsAdmin = () => {
		const user = JSON.parse(localStorage.getItem('user'));

		return user?.role === 'admin' && user?.status === USER_STATUS.active;
	};

	const isDetectInfoShow = () =>{ 
		return getIsAdmin() && translateType === TRANSLATE_TYPE.plainText && (translationState.translateCode.sourceLang == null || translationState.translateCode.detectLang != null);
	};

	const renderOutput = () => {
		switch (translateType) {
		case TRANSLATE_TYPE.plainText:
			return <TranslateOutput translateType={translateType} />;
		case TRANSLATE_TYPE.document:
			return <TranslateFileDocumentOutput translateType={translateType} />;
		}
	};

	const renderInput = () => {
		switch (translateType) {
		case TRANSLATE_TYPE.plainText:
			return <TranslateInput translateType={translateType} />;
		case TRANSLATE_TYPE.document:
			return <TranslateFileDocumentInput translateType={translateType} />;
		}
	};

	return (
		<>
			<div className={styles.outerContainer}>
				<div className={styles.outerTab} >
					<Button
						onClick={() => {
							setTranslateType(TRANSLATE_TYPE.plainText);
							// props.changeOutput(null);
						}}
						style={{ fontWeight: 'bold', marginRight: '20px', display: 'flex', backgroundColor: 'white', color: 'grey', borderColor: 'grey' }}
						variant={translateType == TRANSLATE_TYPE.plainText ? 'outlined' : null}
						disabled={translationState.currentState === STATE.LOADING || translationFileState.currentState === STATE.LOADING}
					>
						<div style={{ paddingRight: 5, alignContent: 'center' }}>
							<TranslateIcon />
						</div>
						{t('Translate.vanban')}
					</Button>
					
					<Button
						onClick={() => {
							setTranslateType(TRANSLATE_TYPE.document);
							if (props.translationState.translateCode.sourceLang === null) props.changeSource('en');
							// props.changeTargetText('');
							// props.changeSourceText('');
							// props.changeOutput(null);
						}}
						style={{ fontWeight: 'bold', marginRight: '20px', display: 'flex', backgroundColor: 'white', color: 'grey', borderColor: 'grey' }}
						variant={translateType == TRANSLATE_TYPE.document ? 'outlined' : null}
						disabled={translationState.currentState === STATE.LOADING || translationFileState.currentState === STATE.LOADING}
					>
						<div style={{ paddingRight: 5, alignContent: 'center' }}>
							<InsertDriveFileIcon />
						</div>
						{t('Translate.tailieu')}
					</Button>
				</div>

				<div className={styles.content} >
					{/* ChooseLang */}
					<TranslationChooselang translateType={translateType} />
					{/* Box translate */}
					<Col md={12} className={styles.boxTranslate}>
						<Row style={{ minHeight: '150px' }}>
							{/* Input of translation */}
							{renderInput()}
							{/* Output of translation */}
							{renderOutput()}
						</Row>
					</Col>
				</div>

				{/* <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 5 }}>
					<button onClick={() => { }} style={{ backgroundColor: '#fff', borderWidth: 0, color: '#63676C', fontStyle: 'italic', fontSize: 13 }}>
						Gửi phản hồi
					</button>
				</div> */}
				<ScrollTop {...props}>
					<Fab color="primary" size="medium" aria-label="scroll back to top">
						<KeyboardArrowUpIcon />
					</Fab>
				</ScrollTop>
				{isDetectInfoShow() && `Ngôn ngữ được detect: ${translationState.translateCode.sourceLang}`}
			</div>
		</>
	);
}

Index.propTypes = {
	translationState: PropTypes.object,
	translationFileState: PropTypes.object,
	changeSourceText: PropTypes.func,
	changeTargetText: PropTypes.func,
	changeFile: PropTypes.func,
	changeOutput: PropTypes.func,
	changeSource: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationState: state.translateReducer,
	translationFileState: state.translateFileReducer
});

const mapDispatchToProps = {
	changeSource,
	changeSourceText,
	changeTargetText,
	changeFileDocument,
	changeOutput,
};

export default connect(mapStateToProps, mapDispatchToProps)(authHoc(Index));
