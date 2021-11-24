/* eslint-disable no-unused-vars */
import React, { useState, useMemo, useEffect, useRef } from 'react';
import PropTypes from 'prop-types';
import {
	Col
} from 'react-bootstrap';
import { Spin } from 'antd';
import { Button, Typography, IconButton, TextareaAutosize } from '@mui/material';
import { changeFileAudio, changeFileAudioVoiceInput, changeOutput, changeOutputAudio, translateFileAudioAsync } from '../../../redux/actions/translateFileAction';
import { STATE } from '../../../redux/reducers/translateFileReducer';
import { useTranslation } from 'react-i18next';
import { connect } from 'react-redux';
import CloseIcon from '@mui/icons-material/Close';
import { AUDIO_FILE_TYPE, TRANSLATE_TYPE } from '../../../constants/common';
import MicRecorder from 'mic-recorder-to-mp3';
import { AudioTwoTone, PauseCircleTwoTone } from '@ant-design/icons';
import styles from '../translateStyle.module.css';
import { toastError } from '../../../components/Toast';
import { getConvertedText } from '../../../helpers/axiosHelper';
import CancelTranslateModal from '../../../components/CancelTranslateModal';
function TranslateFileAudioOutput(props) {
	const inputEl = useRef(null);
	const { translationFileState, translateType, translationState } = props;
	const [Mp3Recorder, setMp3Recorder] = useState(new MicRecorder({ bitRate: 128 }));
	const { t } = useTranslation();
	const [isRecording, setIsRecording] = useState(false);
	const [isConverting, setIsConverting] = useState(true);
	const [blobUrl, setBlobUrl] = useState('');
	const [isBlocked, setIsBlocked] = useState(true);
	const [modalShow, setModalShow] = useState(false);
	const [convertedText, setConvertedText] = useState('');

	const isShowCloseButton = () => {
		if (translationFileState.currentState === STATE.LOADING) {
			return true;
		}
		return false;
	};

	/**
	  * @description Function xóa file khỏi ô input
	  */
	const handleReset = () => {
		clearTimeout(translationFileState.setTimeoutId);
		setConvertedText('');
		setIsConverting(true);
		props.changeFileAudioVoiceInput(null, false);
		props.changeOutputAudio(null);
		setModalShow(false);
	};

	const handleResetTranslate = () => {
		setModalShow(true);
	};

	useEffect(() => {
		try {
			navigator.getUserMedia(
				{ audio: true },
				() => {
					console.log('Permission Granted');
					setIsBlocked(false);
				},
				() => {
					console.log('Permission Denied');
					setIsBlocked(true);
				}
			);
		} catch (e) {
			toastError('no_access_media');
		}

	}, []);

	const getConvertedTextResult = async () => {
		const result = await getConvertedText(translationFileState.outputAudioConvertedFile.converted_file_full_path);
		setConvertedText(result);
		setIsConverting(false);
	};

	useEffect(() => {

		if (translationFileState.outputAudioConvertedFile != null) {
			getConvertedTextResult();
		}

	}, [translationFileState.outputAudioConvertedFile]);

	const start = () => {
		if (isBlocked) {
			console.log('Permission Denied');
		} else {
			Mp3Recorder
				.start()
				.then(() => {
					setIsRecording(true);
				}).catch((e) => toastError('no_access_media'));
		}
	};

	const stop = () => {
		Mp3Recorder
			.stop()
			.getMp3()
			.then(([buffer, blob]) => {
				const blobURL = URL.createObjectURL(blob);
				setBlobUrl(blobURL);
				const audioFile = new File([blob], 'audio.mp3', { type: 'audio/*' });
				props.changeFileAudioVoiceInput(audioFile, true);

				const formData = new FormData();
				formData.append('file', audioFile);
				formData.append('sourceLang', translationState.translateCode.sourceLang);
				formData.append('targetLang', translationState.translateCode.targetLang);
				props.translateFileAudioAsync(formData);
				setIsRecording(false);
			}).catch((e) => console.log(e));
	};

	const handleRecording = () => {
		if (isRecording) {
			stop();
		} else {
			start();
		}
	};

	const cancelButton = () => {
		if (translationFileState.currentState !== STATE.LOADING)
			return (
				<Button
					variant="outlined"
					onClick={handleReset}
					type="file"
					className={styles.translateButton}
					style={{ minWidth: '65px', }}
				>
					{translationFileState.currentState == STATE.SUCCESS ? 'Dịch tiếp' : 'HỦY'}
				</Button>
			);
		else
			return (
				<Button
					variant="outlined"
					onClick={handleResetTranslate}
					type="file"
					className={styles.translateButton}
					style={{ minWidth: '65px', }}
				>
					Dịch tiếp
				</Button>
			);
	};

	const handleUploadFile = (file) => {
		try {
			const file_ext = file.name.split('.').pop();

			if (AUDIO_FILE_TYPE.includes(file_ext)) {
				props.changeFileAudio(file);
			}
			else {
				toastError(t('fileTypeNotSupported'));
			}
		}
		catch (e) {
			toastError(e);
		}
	};

	return (
		<Col md={6} style={{
			borderRight: '1px solid #ccc',
			backgroundColor: translationFileState.currentState === STATE.LOADING || translationFileState.voiceInput === true ? '#f3f3f3' : 'white'
		}}>
			<div style={translationFileState.voiceInput != true ? {
				paddingTop: '10px',
				paddingBottom: '30px',
				display: 'flex',
				height: '100%'
			} : {
				padding: 0,
				display: 'flex',
				height: '100%'
			}}>

				<div style={translationFileState.voiceInput != true ? {
					flex: 1,
					display: 'flex',
					alignItems: 'center',
					justifyContent: 'center',
					flexDirection: translationFileState.audioFile ? 'row' : 'column'
				} : { width: '100%', height: '100%' }}>
					{translationFileState.audioFile === null ?
						<>
							<Typography variant="h6">
								{t('chonTaiLieu')}
							</Typography>
							<Typography p={1}>
								{translateType == TRANSLATE_TYPE.document ? t('taiTepTaiLieu') : t('taiTepAmThanh')}
							</Typography>
							<input
								type="file"
								accept="audio/mpeg, audio/wav, .aac"
								style={{ display: 'none' }}
								id="contained-button-file"
								onChange={(event) => {
									handleUploadFile(event.target.files[0]);
								}}
							/>
							<label htmlFor="contained-button-file">
								<Button variant="outlined" component="span" className={styles.translateButton}>
									{t('timTepTenMayBan')}
								</Button>
							</label>
							{
								isRecording ?
									<PauseCircleTwoTone
										className={isRecording ? styles.recordIconAnimate : styles.recordIcon}
										fill='rgba(0,0,255,1)'
										onClick={handleRecording}
									/> :
									<AudioTwoTone
										style={isBlocked ? { cursor: 'not-allowed' } : {}}
										className={isRecording ? styles.recordIconAnimate : styles.recordIcon}
										twoToneColor={isBlocked ? 'grey' : ''}
										onClick={handleRecording}
										type='button'
									/>
							}
						</> :
						<>
							{translationFileState.voiceInput != true ?
								<div>
									<Typography variant="h6" className={['text-center']} style={{ marginBottom: '10px' }}>
										{translationFileState.audioFile.name}
									</Typography>

									<div md={1} style={{ padding: '0' }} className={['text-center']}>
										{cancelButton()}
									</div>
								</div> :
								<div style={{ display: 'flex', justifyContent: 'center', width: '100%', height: '100%' }}>
									{isConverting ?
										<div style={{ display: 'flex', justifyContent: 'center', flexDirection: 'column', alignItems: 'center' }}>
											<Spin style={{ marginBottom: '20px' }} />

											<div md={1} style={{ padding: '0' }} className={['text-center']}>
												{cancelButton()}
											</div>
										</div> :
										<>
											<div style={{ paddingRight: '0', flex: 1 }} className={styles.boxdich}>
												<TextareaAutosize
													disabled={true}
													minRows={3}
													value={convertedText}
													className={[styles.from_language]}
												/>
											</div>

											<div style={{ padding: '0', alignSelf: 'flex-end', paddingBottom: 5 }} className={['text-center']}>
												{!isShowCloseButton() ?
													<IconButton aria-label="Example" onClick={handleReset} type="file">
														<CloseIcon fontSize='small' />
													</IconButton> : null}
											</div>
										</>}
								</div>}

						</>
					}
				</div>
			</div>

			<CancelTranslateModal
				show={modalShow}
				onHide={() => setModalShow(false)}
				onCancel={handleReset}
			/>
		</Col>
	);
}

TranslateFileAudioOutput.propTypes = {
	translateType: PropTypes.number,
	translationFileState: PropTypes.object,
	translationState: PropTypes.object,
	changeFileAudio: PropTypes.func,
	changeFileAudioVoiceInput: PropTypes.func,
	changeOutputAudio: PropTypes.func,
	translateFileAudioAsync: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationFileState: state.translateFileReducer,
	translationState: state.translateReducer
});

const mapDispatchToProps = {
	changeFileAudio,
	changeFileAudioVoiceInput,
	changeOutput,
	changeOutputAudio,
	translateFileAudioAsync
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslateFileAudioOutput);
