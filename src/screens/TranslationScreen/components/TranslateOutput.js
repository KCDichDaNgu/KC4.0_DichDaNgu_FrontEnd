import React, { useRef, useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { 
	Row,
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
	changeTargetText
} from '../../../redux/actions/translateAction';
import { useTranslation } from 'react-i18next';
import LoadingButton from '@mui/lab/LoadingButton';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import ThumbsUpDownOutlined from '@mui/icons-material/ThumbsUpDownOutlined';
import CreateIcon from '@mui/icons-material/Create';
import ThumbUpOffAlt from '@mui/icons-material/ThumbUpOffAlt';
import ThumbDownOffAlt from '@mui/icons-material/ThumbDownOffAlt';
import { TRANSLATE_TYPE } from '../../../constants/common';
import Popover from '@mui/material/Popover';

import { Button } from '@mui/material';
import * as axiosHelper from '../../../helpers/axiosHelper';

import { TRANSLATION_HISTORY_RATING, STATUS_CODE } from '../../../constants/common';
import { message } from 'antd';

import CloseIcon from '@mui/icons-material/Close';
import ReplayIcon from '@mui/icons-material/Replay';

// import * as axiosHelper from '../../../helpers/axiosHelper';

function TranslateOutput(props) {
	const { 
		translationState, 
		translateType, 
		currentTranslationHistory, 
		setCurrentTranslationHistory 
	} = props;
	const { t } = useTranslation();

	const [anchorTransFeedbackEl, setAnchorTransFeedbackEl] = useState(null);
	const [isUpdateTextTranslated, setIsUpdateTextTranslated] = useState(false);

	const userEditedTranslationRef = useRef();

	useEffect((anchorTransFeedbackEl) => {
		
		if(isUpdateTextTranslated) {

			handleTransFeedbackClose()

			let check = setInterval(() => {
				if (anchorTransFeedbackEl == null && userEditedTranslationRef.current) {
					userEditedTranslationRef.current.focus(); 
					clearInterval(check)
				}
			}, 100)
		}

	}, [isUpdateTextTranslated,]);

	const allowToSubmitUserEditedTranslation = () => {
		return !!currentTranslationHistory.userEditedTranslation && 
			currentTranslationHistory.userEditedTranslation.length > 0 && 
			translationState.translateText.targetText.trim() !== currentTranslationHistory.userEditedTranslation.trim();
	}

	const allowToClearUserEditedTranslation = () => {
		return !!currentTranslationHistory.userEditedTranslation && 
			currentTranslationHistory.userEditedTranslation.length > 0;
	}

	const updateUserEditedTranslation = (event) => {

		setCurrentTranslationHistory({
			...currentTranslationHistory,
			userEditedTranslation: event.target.value
		})
	}

	const clearUserEditedTranslation = () => {
		setCurrentTranslationHistory({
			...currentTranslationHistory,
			userEditedTranslation: ''
		})
	}

	const handleTransFeedbackClick = (event) => {
		setAnchorTransFeedbackEl(event.currentTarget);
	};

	const handleTransFeedbackClose = () => {
		setAnchorTransFeedbackEl(null);
	};

	const isTransFeedbackElOpen = () => {
		return Boolean(anchorTransFeedbackEl);
	}

	const getTransPopupId = () => {
		return isTransFeedbackElOpen() ? 'simple-popover' : undefined;
	}

	const updateByOwner = async (e, rating, userEditedTranslation) => {

		e.preventDefault()

		let changes = {}

		if (rating) changes['rating'] = rating

		if (userEditedTranslation) changes['userEditedTranslation'] = userEditedTranslation
	
		let result = await axiosHelper.updateByOwner({
			id: currentTranslationHistory.id,
			...changes,
		}) 
		
		if (result.code === STATUS_CODE.success) {
			message.success(t('updateSuccess'));

			setCurrentTranslationHistory(result.data)

			if (userEditedTranslation) setIsUpdateTextTranslated(false)
		}
	}

	const updateTextTranslation = (e) => {

		e.preventDefault();

		if (!(typeof(currentTranslationHistory.userEditedTranslation) == 'string'
			&& currentTranslationHistory.userEditedTranslation.length > 0))
		
			setCurrentTranslationHistory({
				...currentTranslationHistory,
				userEditedTranslation: translationState.translateText.targetText
			})

		setIsUpdateTextTranslated(!isUpdateTextTranslated)
	}

	const isDisableTranslateButton = () => {

		if(translationState.currentState === STATE.LOADING) {
			return true;
		}
		if(translationState.translateText.sourceText === '' && translateType === TRANSLATE_TYPE.plainText) {
			return true;
		}
		if ((translationState.translateCode.sourceLang === null || translationState.translateCode.detectLang != null) && translationState.currentState === STATE.FAILURE) {
			return true;
		};
		return false;
	};

	const cancelUserEditedTranslation = () => {

		clearUserEditedTranslation()

		setIsUpdateTextTranslated(!isUpdateTextTranslated)
	}

	/**
 	* @description Function dịch từ, (Ấn enter hoặc ấn nút dịch từ)
	* 1. Trong trường hợp có kết quả dịch => reset lại kết quả dịch về rỗng => gọi lại dịch
	* 2. Còn lại thì dịch vs 2 TH => sourcelang === null (Nhận dạng ngôn ngữ) và sourcelang === vi,cn .. 
 	*/
	const handleTranslate = (e) => {
		
		e.preventDefault();

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

	const isDetect = () =>{ 
		return translateType === TRANSLATE_TYPE.plainText && (translationState.translateCode.sourceLang === null || translationState.translateCode.detectLang != null);
	};

	return (
		<Col 
			md={6} 
			className={styles.ResultTranslateBox} 
			style={{
				backgroundColor: translationState.translateText.targetText === '' || isUpdateTextTranslated || (
					!isUpdateTextTranslated && typeof(currentTranslationHistory.userEditedTranslation) == 'string'
					&& currentTranslationHistory.userEditedTranslation.length > 0) ? '#f8f9fa' : 'white',
			}}>
				
			{translationState.translateText.targetText ?
				<div>
					<div className={styles.boxdich}>

						{ isUpdateTextTranslated ? 
							<div style={{
								paddingBottom: '30px', 
								display: 'flex',
								width: '100%'
							}}>
								<div style={{ paddingRight: '0', flex: 7 }} >
									<TextareaAutosize
										ref={ userEditedTranslationRef }
										minRows={3}
										style={{backgroundColor: '#f8f9fa'}}
										value={ currentTranslationHistory.userEditedTranslation !== null ? currentTranslationHistory.userEditedTranslation : '' }
										onFocus={ (e)=> e.currentTarget.setSelectionRange(e.currentTarget.value.length - 1, e.currentTarget.value.length - 1) }
										onChange={ updateUserEditedTranslation }
										className={[ styles.from_language ]}
									/> 
									
								</div>

								<div md={1} style={{ padding: '0', position: 'relative', flex: 1 }} className={['text-center']}>
									{ allowToClearUserEditedTranslation() ? 
										<IconButton
											aria-label="Example" 
											onClick={ clearUserEditedTranslation }>
											<CloseIcon fontSize='small'/>
										</IconButton> : null
									}
								</div>
							</div>: null
							
						}

						{ !isUpdateTextTranslated && typeof(currentTranslationHistory.userEditedTranslation) == 'string'
							&& currentTranslationHistory.userEditedTranslation.length > 0 ?
							<TextareaAutosize
								disabled={true}
								minRows={3}
								style={{backgroundColor: '#f8f9fa'}}
								value={ currentTranslationHistory.userEditedTranslation }
								className={[ styles.from_language ]}
							/> : null
						}

						{ !isUpdateTextTranslated && !!!currentTranslationHistory.userEditedTranslation ?
							<TextareaAutosize
								disabled={true}
								minRows={3}
								style={{backgroundColor: 'white'}}
								value={translationState.translateText.targetText}
								className={[ styles.from_language ]}
							/> : null
						}
					</div>

					{
						isUpdateTextTranslated ? 
						
						<>
							<div style={{ justifyContent: 'end', display: 'flex', paddingBottom: 5}}>
								<Button onClick={ cancelUserEditedTranslation }>
									{ t('huy') }
								</Button>

								<Button
									onClick={ (e) => { updateByOwner(e, null, currentTranslationHistory.userEditedTranslation) }} 
									disabled={ !allowToSubmitUserEditedTranslation() }>
									{ t('gui') }
								</Button>
							</div> 

							<div style={{ 
								padding: '1rem', 
								fontSize: '.9rem', 
								backgroundColor: '#eee',
								margin: '0 -.96rem',
								zIndex: -1
							}}>
								{ t('lydodonggopbandich') }
							</div>
						</>:
						
						<div style={{ justifyContent: 'space-between', display: 'flex', paddingBottom: 5}}>

							{ !isUpdateTextTranslated && typeof(currentTranslationHistory.userEditedTranslation) == 'string'
								&& currentTranslationHistory.userEditedTranslation.length > 0 ?
								<>
									<div style={{ 
										display: 'flex',
    									alignItems: 'center',
										fontSize: '.95rem',
									}}>
										({ t("dachinhsua") })
									</div>
								</> : <div></div>
							}

							<div>

								{ !isUpdateTextTranslated && typeof(currentTranslationHistory.userEditedTranslation) == 'string'
									&& currentTranslationHistory.userEditedTranslation.length > 0 ?
									<IconButton
										aria-label="Example" 
										onClick={ (e) => { updateByOwner(e, null, null) } }>
										<ReplayIcon fontSize='small'/>
									</IconButton> : null
								}

								<IconButton aria-label="Example" onClick={() => navigator.clipboard.writeText(translationState.translateText.targetText)}>
									<ContentCopyIcon fontSize='medium'/>
								</IconButton>

								{
									translationState.translateText.targetText !== '' ?
									<>
										<IconButton 
											aria-describedby={getTransPopupId()} 
											variant="contained" 
											onClick={handleTransFeedbackClick}>
											<ThumbsUpDownOutlined fontSize='medium'/>
										</IconButton>

										<Popover
											id={getTransPopupId()}
											open={isTransFeedbackElOpen()}
											anchorEl={anchorTransFeedbackEl}
											onClose={handleTransFeedbackClose}
											anchorOrigin={{
												vertical: 'bottom',
												horizontal: 'right',
											}}
											transformOrigin={{
												vertical: 'top',
												horizontal: 'right',
											}}>
											<div style={{
												padding: '1.5rem',
												maxWidth: '300px'
											}}>
												<div>
													<div style={{ 
														textAlign: 'center',
														fontWeight: 600,
														fontSize: '1.25rem'
													}}>
														{ t('Translate.xephangbandich') }
													</div>
													<Row style={{ padding: '1.5rem' }}>
														<Col style={{ 
															textAlign: 'center',
														}}>
															<Button onClick={ (e) => { updateByOwner(e, TRANSLATION_HISTORY_RATING.good, null) } }>
																<ThumbUpOffAlt 
																	style={{ color: currentTranslationHistory.rating === TRANSLATION_HISTORY_RATING.good ? '#1976d2': '#ddd' }} 
																	fontSize='large'
																/>
															</Button>
															
														</Col>

														<Col style={{ 
															textAlign: 'center',
														}}>
															<Button onClick={ (e) => { updateByOwner(e, TRANSLATION_HISTORY_RATING.bad, null) } } >
																<ThumbDownOffAlt 
																	style={{ color: currentTranslationHistory.rating === TRANSLATION_HISTORY_RATING.bad ? '#1976d2': '#ddd' }} 
																	fontSize='large'
																/>
															</Button>
															
														</Col>
													</Row>
													<div style={{ 
														fontSize: '.9rem'
													}}>
														{ t('Translate.xephangbandich2') }
													</div>
													<hr/>

													<div style={{ textAlign: 'center' }}>
														<Button onClick={ (e) => { updateTextTranslation(e) } }>
															<div style={{ paddingRight: 5, alignContent: 'center' }}>
																<CreateIcon />
															</div>
															{ t('Translate.dexuatchinhsua') }
														</Button>
													</div>
												</div>
											</div>
										</Popover>
									</>: null
								}
							</div>
						</div>
					}
					
				</div>
				: <div style={{
					// backgroundColor: translationState.translateText.targetText === '' ? '#f3f3f3' : 'white' , 
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
						{isDetect() ? t('detectAndTranslate') : t('dich')}
					</LoadingButton>
				</div>	
				
			}
		</Col>
	);
}

TranslateOutput.propTypes = {
	translateType: PropTypes.number,
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

export default connect(mapStateToProps, mapDispatchToProps)(TranslateOutput);
