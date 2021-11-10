/* eslint-disable no-unused-vars */
import React, { useState, useMemo, useEffect } from 'react';
import PropTypes from 'prop-types';
import {
	Col,
} from 'react-bootstrap';
import { Button, Typography, IconButton } from '@mui/material';
import { changeFileAudio, changeOutput, changeOutputAudio } from '../../../redux/actions/translateFileAction';
import { STATE } from '../../../redux/reducers/translateFileReducer';
import { useTranslation } from 'react-i18next';
import { connect } from 'react-redux';
import CloseIcon from '@mui/icons-material/Close';
import { TRANSLATE_TYPE } from '../../../constants/common';
import MicRecorder from 'mic-recorder-to-mp3';
import { AudioTwoTone, PauseCircleTwoTone } from '@ant-design/icons';
import styles from '../translateStyle.module.css';
import { toastError } from '../../../components/Toast';
function TranslateFileAudioOutput(props) {
	const { translationFileState, translateType } = props;
	const [Mp3Recorder, setMp3Recorder] = useState(new MicRecorder({ bitRate: 128 }));
	const { t } = useTranslation();
	const [isRecording, setIsRecording] = useState(false);
	const [blobUrl, setBlobUrl] = useState('');
	const [isBlocked, setIsBlocked] = useState(true);

	/**
	  * @description Function xóa file khỏi ô input
	  */
	const handleReset = () => {
		props.changeFileAudio(null);
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
				props.changeFileAudio(audioFile);
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
			backgroundColor: translationFileState.currentState === STATE.LOADING ? '#f3f3f3' : 'white'
		}}>
			<div style={{
				paddingTop: '10px',
				paddingBottom: '30px',
				display: 'flex',
			}}>

				<div style={{
					flex: 1,
					display: 'flex',
					alignItems: 'center',
					justifyContent: 'center',
					flexDirection: translationFileState.audioFile ? 'row' : 'column'
				}}>
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
								accept="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
								style={{ display: 'none' }}
								id="contained-button-file"
								onChange={(event) => {
									console.log(event.target.files[0]);
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
							<Typography variant="h6">
								{translationFileState.audioFile.name}
							</Typography>
							<div md={1} style={{ padding: '0' }} className={['text-center']}>
								<IconButton aria-label="Example" onClick={handleReset} type="file">
									<CloseIcon fontSize='small' />
								</IconButton>
							</div>
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
	changeFileAudio: PropTypes.func,
	changeOutputAudio: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationFileState: state.translateFileReducer
});

const mapDispatchToProps = {
	changeFileAudio,
	changeOutput,
	changeOutputAudio
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslateFileAudioOutput);
