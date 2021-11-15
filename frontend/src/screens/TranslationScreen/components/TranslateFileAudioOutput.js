import React, {useState, useEffect} from 'react';
import PropTypes from 'prop-types';
import {
	Col,
} from 'react-bootstrap';
import { Button, IconButton, TextareaAutosize } from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import { translateFileAudioAsync } from '../../../redux/actions/translateFileAction';
import LoadingButton from '@mui/lab/LoadingButton';
import { STATE } from '../../../redux/reducers/translateFileReducer';
import { useTranslation } from 'react-i18next';
import styles from '../translateStyle.module.css';
import { connect } from 'react-redux';
import { isNull } from 'lodash';
import { downloadSpeechRecognitionResultFile } from '../../../helpers/axiosHelper';
import { getConvertedText } from '../../../helpers/axiosHelper';
import { Spin } from 'antd';

function TranslateFileAudioOutput(props) {
	const { translationFileState, translationState } = props;
	const [ translatedText, setTranslatedText ] = useState('');
	const [ isTranslating, setIsTranslating ] = useState(false);
	const { t } = useTranslation();

	const getConvertedTextResult = async () => {
		const result = await getConvertedText(translationFileState.outputAudioTranslatedFile.translated_file_full_path);
		setTranslatedText(result);
		setIsTranslating(false);
	};

	useEffect(() => {

		if (translationFileState.outputAudioTranslatedFile != null) {
			getConvertedTextResult();
		} else setIsTranslating(true);

	}, [translationFileState.outputAudioTranslatedFile]);

	/**
	  * @description Function dịch từ, (Ấn enter hoặc ấn nút dịch từ)
	* 1. Trong trường hợp có kết quả dịch => reset lại kết quả dịch về rỗng => gọi lại dịch
	* 2. Còn lại thì dịch vs 2 TH => sourcelang === null (Nhận dạng ngôn ngữ) và sourcelang === vi,cn .. 
	  */
	const handleTranslate = () => {
		const formData = new FormData();
		formData.append('file', translationFileState.audioFile);
		formData.append('sourceLang', translationState.translateCode.sourceLang);
		formData.append('targetLang', translationState.translateCode.targetLang);
		props.translateFileAudioAsync(formData);
	};

	const isDisableTranslateButton = () => {
		if (translationFileState.currentState === STATE.LOADING) {
			return true;
		}
		if (translationFileState.audioFile === null && !props.isTranslate) {
			return true;
		}
		if (translationState.translateCode.sourceLang === null) {
			return true;
		}
		return false;
	};

	const convertedDocument = () => {
		switch (translationFileState.outputAudioFile.source_lang) {
		case 'vi':
			return t('taiChuyenNguTiengViet');
		case 'en':
			return t('taiChuyenNguTiengAnh');
		case 'zh':
			return t('taiChuyenNguTiengTrung');
		case 'lo':
			return t('taiChuyenNguTiengLao');
		case 'km':
			return t('taiChuyenNguTiengKhome');
		default:
			return t('taiChuyenNgu');
		}
	};

	const translatedDocument = () => {
		switch (translationFileState.outputAudioFile.target_lang) {
		case 'vi':
			return t('taiTaiLieuTiengViet');
		case 'en':
			return t('taiTaiLieuTiengAnh');
		case 'zh':
			return t('taiTaiLieuTiengTrung');
		case 'lo':
			return t('taiTaiLieuTiengLao');
		case 'km':
			return t('taiTaiLieuTiengKhome');
		default:
			return t('taiTaiLieu');
		}
	};

	return (
		<Col
			md={6}
			className={styles.ResultTranslateBox}
			style={{
				backgroundColor: isNull(translationFileState.audioFile) ? '#f3f3f3' : 'white'
			}}>
			<div 
				style={ translationFileState.voiceInput != true ? {
					backgroundColor: isNull(translationFileState.audioFile) ? '#f3f3f3' : 'white',
					display: 'flex',
					paddingBottom: 10,
					justifyContent: 'start',
				}: {}}
			>
				{(translationFileState.outputAudioFile && translationFileState.audioFile) ?
					<>
						{translationFileState.voiceInput != true ? 
							<Col style={{
								display: 'flex',
								flexDirection: 'column',
								paddingTop: 10,
								paddingLeft: '0'
							}}>
								<Button
									variant="contained"
									color="primary"
									onClick={() => downloadSpeechRecognitionResultFile(translationFileState.outputAudioConvertedFile.converted_file_full_path)}
									style={{
										width: '300px',
										marginBottom: '10px'
									}}
								>
									{convertedDocument()}
								</Button>

								{translationFileState.outputAudioTranslatedFile ? <Button
									variant="contained"
									color="success"
									onClick={() => downloadSpeechRecognitionResultFile(translationFileState.outputAudioTranslatedFile.translated_file_full_path)}
									style={{
										width: '300px',
										marginBottom: '10px'
									}}
								>
									{translatedDocument()}
								</Button> : <LoadingButton
									variant="contained"
									loading
									style={{ fontWeight: 'bold', display: 'flex', width: '65px', }}
								>
									{t('dich')}
								</LoadingButton>}
							</Col> :
							<div style={isTranslating ?{ display: 'flex', justifyContent: 'center', alignItems: 'center'} : {}} >
								{ isTranslating ? 
									<Spin style={{marginTop: '20px'}}/> : 
									<> 
										<div className={styles.boxdich}>
											<TextareaAutosize
												disabled={true}
												minRows={3}
												style={{ backgroundColor: 'white' }}
												value={translatedText}
												className={[styles.from_language]}
											/>
										</div>

										<div style={{ justifyContent: 'end', display: 'flex', paddingBottom: 5 }}>
											<IconButton aria-label="Example" onClick={() => navigator.clipboard.writeText(translationState.translateText.targetText)}>
												<ContentCopyIcon fontSize='medium' />
											</IconButton>
										</div>
									</>
								}
								
							</div>
						}
					</>

					: <LoadingButton
						variant="contained"
						onClick={handleTranslate}
						loading={translationFileState.currentState === STATE.LOADING && !translationFileState.outputAudioFile && translationFileState.voiceInput != true}
						disabled={isDisableTranslateButton()}
						style={{ fontWeight: 'bold', display: 'flex', marginTop: 10, }}
					>
						{t('dich')}
					</LoadingButton>}
			</div>
		</Col>
	);
}

TranslateFileAudioOutput.propTypes = {
	isTranslate: PropTypes.bool.isRequired,
	translationState: PropTypes.object,
	translationFileState: PropTypes.object,
	translateFileAudioAsync: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationState: state.translateReducer,
	translationFileState: state.translateFileReducer
});

const mapDispatchToProps = {
	translateFileAudioAsync,
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslateFileAudioOutput);
