import React from 'react';
import PropTypes from 'prop-types';
import { 
	Col,
} from 'react-bootstrap';
import { Button, Typography, IconButton } from '@mui/material';
import { changeFileDocument, changeOutputDocument } from '../../../redux/actions/translateFileAction';
import { STATE } from '../../../redux/reducers/translateFileReducer';
import { useTranslation } from 'react-i18next';
import { connect } from 'react-redux';
import CloseIcon from '@mui/icons-material/Close';
import { TRANSLATE_TYPE } from '../../../constants/common';

function TranslateFileDocumentInput(props) {
	const { translationFileState, translateType } = props;
	const { t } = useTranslation();

	/**
 	* @description Function xóa file khỏi ô input
 	*/
	const handleReset = () => {
		props.changeFileDocument(null);
		props.changeOutputDocument(null);
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
					flexDirection: translationFileState.file ? 'row' : 'column'
				}}> 
					{translationFileState.documentFile === null ?
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
									props.changeFileDocument(event.target.files[0]);
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
								{translationFileState.documentFile.name}
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

TranslateFileDocumentInput.propTypes = {
	translateType: PropTypes.number,
	translationFileState: PropTypes.object,
	changeFileDocument: PropTypes.func,
	changeOutputDocument: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationFileState: state.translateFileReducer 
});

const mapDispatchToProps = { 
	changeFileDocument,
	changeOutputDocument
};

export default connect(mapStateToProps, mapDispatchToProps)(TranslateFileDocumentInput);
