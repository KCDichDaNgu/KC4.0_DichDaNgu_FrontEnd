import React from 'react';
import PropTypes from 'prop-types';
import {
	Col,
} from 'react-bootstrap';
import { Button } from '@mui/material';
import { translateFileAudioAsync } from '../../../redux/actions/translateFileAction';
import LoadingButton from '@mui/lab/LoadingButton';
import { STATE } from '../../../redux/reducers/translateFileReducer';
import { useTranslation } from 'react-i18next';
import styles from '../translateStyle.module.css';
import { connect } from 'react-redux';
import { isNull } from 'lodash';
import { downloadSpeechRecognitionResultFile } from '../../../helpers/axiosHelper';


function TranslateFileAudioOutput(props) {
	const { translationFileState, translationState } = props;
	const { t } = useTranslation();

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
			<div style={{
				backgroundColor: isNull(translationFileState.audioFile) ? '#f3f3f3' : 'white',
				display: 'flex',
				paddingTop: 10,
				paddingBottom: 10,
				justifyContent: 'start',
			}}>
				{(translationFileState.outputAudioFile && translationFileState.audioFile) ?
					<Col style={{
						display: 'flex',
						flexDirection: 'column',
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


					</Col>
					: <LoadingButton
						variant="contained"
						onClick={handleTranslate}
						loading={translationFileState.currentState === STATE.LOADING && !translationFileState.outputAudioFile}
						disabled={isDisableTranslateButton()}
						style={{ fontWeight: 'bold', display: 'flex' }}
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
