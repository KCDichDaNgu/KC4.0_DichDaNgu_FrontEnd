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
import { TRANSLATE_TYPE } from '../../../constants/common';
import MicRecorder from 'mic-recorder-to-mp3';
import { AudioTwoTone, PauseCircleTwoTone } from '@ant-design/icons';
import styles from '../translateStyle.module.css';
import { toastError } from '../../../components/Toast';
import { getConvertedText } from '../../../helpers/axiosHelper';
function TranslateFileAudioOutput(props) {
	const inputEl = useRef(null);
	const { translationFileState, translateType, translationState } = props;
	const [Mp3Recorder, setMp3Recorder] = useState(new MicRecorder({ bitRate: 128 }));
	const { t } = useTranslation();
	const [isRecording, setIsRecording] = useState(false);
	const [isConverting, setIsConverting] = useState(true);
	const [blobUrl, setBlobUrl] = useState('');
	const [isBlocked, setIsBlocked] = useState(true);
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
		setConvertedText('');
		setIsConverting(true);
		props.changeFileAudioVoiceInput(null, false);
		props.changeOutputAudio(null);
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

	return (
		<Col md={6} style={{
			borderRight: '1px solid #ccc',
			backgroundColor: translationFileState.currentState === STATE.LOADING || translationFileState.voiceInput === true ? '#f3f3f3' : 'white'
		}}>
			<div style={{
				paddingTop: '10px',
				paddingBottom: '30px',
				display: 'flex',
			}}>

				<div style={ translationFileState.voiceInput != true ? {
					flex: 1,
					display: 'flex',
					alignItems: 'center',
					justifyContent: 'center',
					flexDirection: translationFileState.audioFile ? 'row' : 'column'
				}: {width: '100%' }}>
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
									props.changeFileAudio(event.target.files[0]);
								}}
							/>
							<label htmlFor="contained-button-file">
								<Button variant="contained" size='small' component="span">
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
									<Typography variant="h6" className={['text-center']}>
										{translationFileState.audioFile.name}
									</Typography>

									<div md={1} style={{ padding: '0' }} className={['text-center']}>
										<Button variant="contained" onClick={handleReset} type="file">
											{/* <CloseIcon fontSize='small' /> */}
											Dịch tiếp
										</Button>
									</div>
								</div> :
								<div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', width: '100%'}}>
									{isConverting ? <Spin style={{marginTop: '20px'}}/> : <>
										<div style={{ paddingRight: '0', flex: 1 }} >
											<TextareaAutosize
												ref={inputEl}
												minRows={3}
												disabled
												value={convertedText}
												className={[styles.from_language]}
											/>
										</div>
										<div md={1} style={{ padding: '0' }} className={['text-center']}>
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
