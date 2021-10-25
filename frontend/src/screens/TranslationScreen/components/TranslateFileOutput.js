import React from 'react';
import PropTypes from 'prop-types';
import { 
	Col,
} from 'react-bootstrap';
import { Button } from '@mui/material';
import { translateFileAsync } from '../../../redux/actions/translateFileAction';
import LoadingButton from '@mui/lab/LoadingButton';
import { STATE } from '../../../redux/reducers/translateFileReducer';
import { useTranslation } from 'react-i18next';
import styles from '../translateStyle.module.css';
import { connect } from 'react-redux';
import { isNull } from 'lodash';
import { downloadFile } from '../../../helpers/axiosHelper';


function TranslateFileOutput(props) {
	const { translationFileState, translationState } = props;
	const { t } = useTranslation();

	/**
 	* @description Function dịch từ, (Ấn enter hoặc ấn nút dịch từ)
	* 1. Trong trường hợp có kết quả dịch => reset lại kết quả dịch về rỗng => gọi lại dịch
	* 2. Còn lại thì dịch vs 2 TH => sourcelang === null (Nhận dạng ngôn ngữ) và sourcelang === vi,cn .. 
 	*/
	const handleTranslate = () => {
		const formData = new FormData();
		formData.append('file', translationFileState.file);
		formData.append('sourceLang', translationState.translateCode.sourceLang);
		formData.append('targetLang', translationState.translateCode.targetLang);
		props.translateFileAsync(formData);
	};

	const isDisableTranslateButton = () => {
		if(translationFileState.currentState === STATE.LOADING) {
			return true;
		}
		if(translationFileState.file === null && !props.isTranslate) {
			return true;
		}
		if(translationState.translateCode.sourceLang === null) {
			return true;
		}
		return false;
	};

	const buttonTextDich = () => {
		switch (translationFileState.outputTranslationFile.target_lang) {
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
				backgroundColor: isNull(translationFileState.file) ? '#f3f3f3' : 'white'
			}}>
			<div style={{
				backgroundColor: isNull(translationFileState.file) ? '#f3f3f3' : 'white' , 
				display: 'flex', 
				paddingTop: 10,
				paddingBottom: 10,
				justifyContent: 'start'
			}}>
				{(translationFileState.outputTranslationFile && translationFileState.file) ? 
					<Button 
						variant="contained" 
						color="success" 
						onClick={() => downloadFile(`http://nmtuet.ddns.net:8000/${translationFileState.outputTranslationFile.target_file_full_path}`)}
					>
						{buttonTextDich()}
					</Button> : <LoadingButton 
						variant="contained" 
						onClick={handleTranslate}
						loading={translationFileState.currentState === STATE.LOADING}
						disabled={isDisableTranslateButton()}
						style={{ fontWeight: 'bold', display: 'flex'}}
					>
						{t('dich')}
					</LoadingButton>}
			</div>
		</Col>
	);
}

TranslateFileOutput.propTypes = {
	isTranslate: PropTypes.bool.isRequired,
	translationState: PropTypes.object,
	translationFileState: PropTypes.object,
	translateFileAsync: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationState: state.translateReducer,
	translationFileState: state.translateFileReducer 
});

const mapDispatchToProps = { 
	translateFileAsync,
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslateFileOutput);
