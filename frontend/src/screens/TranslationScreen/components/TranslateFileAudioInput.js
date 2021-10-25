import React from 'react';
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

function TranslateFileAudioOutput(props) {
	const { translationFileState, translateType } = props;
	const { t } = useTranslation();

	/**
 	* @description Function xóa file khỏi ô input
 	*/
	const handleReset = () => {
		props.changeFileAudio(null);
		props.changeOutputAudio(null);
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
									props.changeFileAudio(event.target.files[0]);
								}}
							/>
							<label htmlFor="contained-button-file">
								<Button variant="contained" size='small' component="span">
									{t('timTepTenMayBan')}
								</Button>
							</label>
						</> : 
						<>
							<Typography variant="h6">
								{translationFileState.audioFile.name}
							</Typography>
							<div md={1} style={{ padding: '0' }} className={['text-center']}>
								<IconButton aria-label="Example" onClick={handleReset} type="file">
									<CloseIcon fontSize='small'/>
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
