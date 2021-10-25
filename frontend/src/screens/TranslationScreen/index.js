import React, { useEffect, useState } from 'react';
import {
	Row,
	Col,
} from 'react-bootstrap';
import PropTypes from 'prop-types';
import styles from './translateStyle.module.css';
import { Button, Fab, } from '@mui/material';
import { connect } from 'react-redux';
import { STATE } from '../../redux/reducers/translateReducer';
import {
	changeSourceText,
	changeTargetText,
} from '../../redux/actions/translateAction';
import {
	changeFile, changeOutput
} from '../../redux/actions/translateFileAction';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import AlbumIcon from '@mui/icons-material/Album';
import TranslateIcon from '@mui/icons-material/Translate';
import KeyboardArrowUpIcon from '@mui/icons-material/KeyboardArrowUp';
import { useTranslation } from 'react-i18next';
import ScrollTop from '../../components/ScrollTop';
import TranslateFileDocumentOutput from './components/TranslateFileDocumentOutput';
import TranslateFileAudioOutput from './components/TranslateFileAudioOutput';
import TranslateFileInput from './components/TranslateFileInput';
import TranslationChooselang from './components/TranslationChooselang';
import TranslateOutput from './components/TranslateOutput';
import TranslateInput from './components/TranslateInput';
import { TRANSLATE_TYPE } from '../../constants/common';

function Index(props) {
	const { translationState, translationFileState } = props;
	const { t } = useTranslation();
	const [translateType, setTranslateType] = useState(TRANSLATE_TYPE.plainText);

	/**
	 * @description useEffect cho việc check kết quả và báo noti cho 
	 * người dùng
	 */
	useEffect(() => {
		switch (translationState.currentState) {
		case STATE.SUCCESS:
			break;
		case STATE.FAILURE:
			alert(`${translationState.err}`);
			break;
		default:
			break;
		}
	}, [translationState.currentState]);

	/**
	 * @description useEffect cho việc check kết quả và báo noti cho 
	 * người dùng
	 */
	useEffect(() => {
		switch (translationFileState.currentState) {
		case STATE.SUCCESS:
			break;
		case STATE.FAILURE:
			alert(`${translationFileState.err}`);
			break;
		default:
			break;
		}
	}, [translationFileState.currentState]);

	const renderOutput = () => {
		switch (translateType) {
		case TRANSLATE_TYPE.plainText:
			return <TranslateOutput translateType={translateType} />;
		case TRANSLATE_TYPE.document:
			return <TranslateFileDocumentOutput translateType={translateType} />;
		case TRANSLATE_TYPE.audio:
			return <TranslateFileAudioOutput translateType={translateType} />;
		}
	};

	return (
		<>
			<div className={styles.outerContainer}>
				<div className={styles.outerTab} >
					<Button
						onClick={() => {
							setTranslateType(TRANSLATE_TYPE.plainText);
							props.changeFile(null);
							props.changeOutput(null);
						}}
						style={{ fontWeight: 'bold', marginRight: '20px', display: 'flex', backgroundColor: 'white', color: 'grey', borderColor: 'grey' }}
						variant={translateType == TRANSLATE_TYPE.plainText ? 'outlined' : null}
						disabled={translationState.currentState === STATE.LOADING || translationFileState.currentState === STATE.LOADING}
					>
						<div style={{ paddingRight: 5, alignContent: 'center' }}>
							<TranslateIcon />
						</div>
						{t('Translate.vanban')}
					</Button>
					<Button
						onClick={() => {
							setTranslateType(TRANSLATE_TYPE.document);
							props.changeTargetText('');
							props.changeSourceText('');
						}}
						style={{ fontWeight: 'bold', marginRight: '20px', display: 'flex', backgroundColor: 'white', color: 'grey', borderColor: 'grey' }}
						variant={translateType == TRANSLATE_TYPE.document ? 'outlined' : null}
						disabled={translationState.currentState === STATE.LOADING || translationFileState.currentState === STATE.LOADING}
					>
						<div style={{ paddingRight: 5, alignContent: 'center' }}>
							<InsertDriveFileIcon />
						</div>
						{t('Translate.tailieu')}
					</Button>
					<Button
						onClick={() => {
							setTranslateType(TRANSLATE_TYPE.audio);
							props.changeTargetText('');
							props.changeSourceText('');
						}}
						style={{ fontWeight: 'bold', marginRight: '20px', display: 'flex', backgroundColor: 'white', color: 'grey', borderColor: 'grey' }}
						variant={translateType == TRANSLATE_TYPE.audio ? 'outlined' : null}
						disabled={translationState.currentState === STATE.LOADING || translationFileState.currentState === STATE.LOADING}
					>
						<div style={{ paddingRight: 5, alignContent: 'center' }}>
							<AlbumIcon />
						</div>
						{t('Translate.amthanh')}
					</Button>
				</div>
				<div className={styles.content} >
					{/* ChooseLang */}
					<TranslationChooselang translateType={translateType} />
					{/* Box translate */}
					<Col md={12} className={styles.boxTranslate}>
						<Row style={{ minHeight: '150px' }}>
							{/* Input of translation */}
							{translateType === TRANSLATE_TYPE.plainText ? <TranslateInput /> : <TranslateFileInput translateType={translateType} />}
							{/* Output of translation */}
							{renderOutput()}
						</Row>
					</Col>
				</div>
				<div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 5 }}>
					<button onClick={() => { }} style={{ backgroundColor: '#fff', borderWidth: 0, color: '#63676C', fontStyle: 'italic', fontSize: 13 }}>
						Gửi phản hồi
					</button>
				</div>
				<ScrollTop {...props}>
					<Fab color="primary" size="medium" aria-label="scroll back to top">
						<KeyboardArrowUpIcon />
					</Fab>
				</ScrollTop>
			</div>
		</>
	);
}

Index.propTypes = {
	translationState: PropTypes.object,
	translationFileState: PropTypes.object,
	changeSourceText: PropTypes.func,
	changeTargetText: PropTypes.func,
	changeFile: PropTypes.func,
	changeOutput: PropTypes.func,
};

const mapStateToProps = (state) => ({
	translationState: state.translateReducer,
	translationFileState: state.translateFileReducer
});

const mapDispatchToProps = {
	changeSourceText,
	changeTargetText,
	changeFile,
	changeOutput,
};

export default connect(mapStateToProps, mapDispatchToProps)(Index);
