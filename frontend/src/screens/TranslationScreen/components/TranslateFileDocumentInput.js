import React, { useState } from 'react';
import PropTypes from 'prop-types';
import {
	Col,
} from 'react-bootstrap';
import { Button, Typography } from '@mui/material';
import { changeFileDocument, changeOutputDocument } from '../../../redux/actions/translateFileAction';
import { STATE } from '../../../redux/reducers/translateFileReducer';
import { useTranslation } from 'react-i18next';
import { connect } from 'react-redux';
import { TRANSLATE_TYPE } from '../../../constants/common';
import styles from '../translateStyle.module.css';
import CancelTranslateModal from '../../../components/CancelTranslateModal';
function TranslateFileDocumentInput(props) {
	const { translationFileState, translateType } = props;
	const [modalShow, setModalShow] = useState(false);
	const { t } = useTranslation();

	/**
	  * @description Function xóa file khỏi ô input
	  */
	const handleReset = () => {
		clearTimeout(translationFileState.setTimeoutId);
		props.changeFileDocument(null);
		props.changeOutputDocument(null);
		setModalShow(false);
	};
	const handleResetTranslate = () => {
		setModalShow(true);
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
					HỦY
				</Button>
			);
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
								<Button variant="outlined" component="span" className={styles.translateButton}>
									{t('timTepTenMayBan')}
								</Button>
							</label>
						</> : 
						<>
							<Typography variant="h6" style={{ marginBottom: '10px' }}>
								{translationFileState.documentFile.name}
							</Typography>
							{cancelButton()}
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
