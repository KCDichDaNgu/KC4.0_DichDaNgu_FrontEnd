import React, { useEffect, useState } from 'react';
import {
	Row,
	Col,
	Form
} from 'react-bootstrap';
import { message } from 'antd';
import LoadingButton from '@mui/lab/LoadingButton';
import PropTypes from 'prop-types';
import styles from './translateStyle.module.css';
import { Button, Fab } from '@mui/material';
import { connect } from 'react-redux';
import { STATE } from '../../redux/reducers/translateReducer';
import {
	changeSourceText,
	changeTargetText,
	changeSource,
	changeDetectLang
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
import { STATUS_CODE, TRANSLATE_TYPE } from '../../constants/common';
import TranslateFileDocumentInput from './components/TranslateFileDocumentInput';
import authHoc from '../../hocs/authHoc';
import { toastError } from '../../components/Toast';
import * as axiosHelper from '../../helpers/axiosHelper';


function Index(props) {
	const { translationState, translationFileState } = props;
	const { t } = useTranslation();
	const [translateType, setTranslateType] = useState(TRANSLATE_TYPE.plainText);

	const [ currentTranslationHistory, setCurrentTranslationHistory ] = useState({});
	const [ currentLangDetectionHistory, setCurrentLangDetectionHistory ] = useState();

	const [ updateReceiverEmailForm, setUpdateReceiverEmailForm ] = useState({
		receiverEmail: "",
	});

	const handleChange = (event) => {
		setUpdateReceiverEmailForm((values) => ({
		  	...values,
		  	[event.target.name]: event.target.value,
		}));
	};

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
		case STATE.LOADING: {
			break;
		}
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
		case STATE.LOADING: {
			break;
		}
		default:
			break;
		}
	}, [translationFileState.currentState]);

	useEffect(() => {
		
		if (translationState.currentState === STATE.LOADING && translateType == TRANSLATE_TYPE.plainText) {

			const interval1 = setInterval(() => {
				setCurrentTranslationHistory(oldX => translationState.currentTranslationHistory)
				setCurrentLangDetectionHistory(oldX => translationState.currentLangDetectionHistory)
			}, 1);

			return () => { 
				clearInterval(interval1);
			};
		}

		if (translationFileState.currentState === STATE.LOADING && translateType == TRANSLATE_TYPE.document) {

			const interval1 = setInterval(() => {
				setCurrentTranslationHistory(oldX => translationFileState.currentTranslationHistory)
				setCurrentLangDetectionHistory(oldX => translationFileState.currentLangDetectionHistory)
			}, 1);

			return () => { 
				clearInterval(interval1);
			};
		}

		
	}, [
		translationState, 
		translationFileState,
	])

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

	const renderEstimatedTranslation = () => {

		if (!(!!currentTranslationHistory && !!currentTranslationHistory?.taskId)) return;

		let posInTranslationQueue = 0;
		let estimatedWattingTime = 0;

		if (translationState.currentState === STATE.LOADING && translationState.currentTranslationHistory && translateType == TRANSLATE_TYPE.plainText) {
			posInTranslationQueue = translationState.currentTranslationHistory.posInTranslationQueue;
			estimatedWattingTime = translationState.currentTranslationHistory.estimatedWattingTime;
		}

		if (translationFileState.currentState === STATE.LOADING && translationFileState.currentTranslationHistory && translateType == TRANSLATE_TYPE.document) {
			posInTranslationQueue = translationFileState.currentTranslationHistory.posInTranslationQueue;
			estimatedWattingTime = translationFileState.currentTranslationHistory.estimatedWattingTime;
		}
		
		if (posInTranslationQueue > 0) {
			return <div className='mt-3' style={{
				fontWeight: 700,
				width: '100%',
				color: '#212529',
				lineHeight: '2.5rem',
				textAlign: 'center',
				fontSize: '1.5rem'
			}}>
				{ t('viTriTrongHangChoDich') }: {posInTranslationQueue}
				<br/>
				{ t('thoiGianChoUocTinh') }: {Math.round(estimatedWattingTime)} s
			</div>
		} 
	}

	const renderEstimatedLangDetection = () => {

		if (!(!!currentLangDetectionHistory && !!currentLangDetectionHistory?.taskId)) return;

		let posInLangDetectionQueue = 0;
		let estimatedWattingTime = 0;
		
		if (translationState.currentState === STATE.LOADING && translationState.currentLangDetectionHistory && translateType == TRANSLATE_TYPE.plainText) {
			posInLangDetectionQueue = translationState.currentLangDetectionHistory.posInLangDetectionQueue;
			estimatedWattingTime = translationState.currentLangDetectionHistory.estimatedWattingTime;
		}

		if (translationFileState.currentState === STATE.LOADING && translationFileState.currentLangDetectionHistory && translateType == TRANSLATE_TYPE.document) {
			posInLangDetectionQueue = translationFileState.currentLangDetectionHistory.posInLangDetectionQueue;
			estimatedWattingTime = translationFileState.currentLangDetectionHistory.estimatedWattingTime;
		}
		
		if (posInLangDetectionQueue > 0) {
			return <div className='mt-3' style={{
				fontWeight: 700,
				width: '100%',
				color: '#212529',
				lineHeight: '2.5rem',
				textAlign: 'center',
				fontSize: '1.5rem'
			}}>
				{ t('viTriTrongHangChoNhanDienNgonNgu') }: {posInLangDetectionQueue}
				<br/>
				{ t('thoiGianChoUocTinh') }: {Math.round(estimatedWattingTime)} s
			</div>
		} 
	}

	const updateReceiverEmail = async (e) => {
		e.preventDefault()

		let result = await axiosHelper.updateReceiverEmail({
			taskId: currentTranslationHistory.taskId,
			receiverEmail: updateReceiverEmailForm.receiverEmail
		}) 
		
		if (result.code == STATUS_CODE.success) {
			message.success(t('updateSuccess'));
		}
	}

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
							props.changeDetectLang(null);
							// if (props.translationState.translateCode.sourceLang === null) props.changeSource('en');
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

				<div className='mt-5'></div>

				{ renderEstimatedLangDetection() }

				{ renderEstimatedTranslation() }

				{ (!!currentTranslationHistory && !!currentTranslationHistory?.taskId) ? 
					<Col md={5} xs={12} className="mt-3" style={{ margin: 'auto' }}>
						
						<Form onSubmit={ updateReceiverEmail }>
							<Form.Group>
								<Form.Label>{ t('emailNhanketQua') }</Form.Label>
								<Form.Control 
									type="email" 
									placeholder="example@gmail.com" 
									name="receiverEmail"
									value={ updateReceiverEmailForm.receiverEmail }
                      				onChange={ handleChange }/>
								<Form.Text className="text-muted">
									{ t('damBaoEmail') }
								</Form.Text>
							</Form.Group>

							{ updateReceiverEmailForm.receiverEmail ?
								<LoadingButton 
									
									type='submit'
									variant="contained" 
									// onClick={handleTranslate}
									// loading={translationState.currentState === STATE.LOADING}
									// disabled={isDisableTranslateButton()}
									style={{ 
										fontWeight: 'bold', 
										display: 'flex', 
										marginLeft: 'auto' 
									}}>
									{ t('gui') }
								</LoadingButton> : <></>
							}
						</Form>
					</Col>: <></>
				}

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
	changeDetectLang: PropTypes.func,
	
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
	changeDetectLang
};

export default connect(mapStateToProps, mapDispatchToProps)(authHoc(Index));
