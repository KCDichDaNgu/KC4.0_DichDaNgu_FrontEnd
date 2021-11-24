import React from 'react';
import PropTypes from 'prop-types';
import {
	Typography,
	Dialog,
	DialogTitle,
	Divider,
	DialogContent,
	DialogActions,
	Button,
} from '@mui/material';
import { useTranslation } from 'react-i18next';
import { Row } from 'antd';

function CancelTranslateModal(props) {
	const { t } = useTranslation();

	return (
		<Dialog
			fullWidth
			maxWidth="xs"
			style={{ height: 'auto' }}
			scroll="paper"
			onClose={props.onHide}
			open={props.show}
			aria-labelledby="draggable-dialog-title"
		>
			<form>
				<DialogTitle id="draggable-dialog-title">
					<Typography style={{ fontWeight: 'bold' }}>
						{t('cancelTranslate')}
					</Typography>
				</DialogTitle>
				<Divider />
				<DialogContent sx={{ py: 1 }}>
					<span>
						{t('cancelTranslateContent')}
					</span>
				</DialogContent>
				<Row justify="end">
					<DialogActions>
						<Button variant="outlined" onClick={props.onHide}>
							{t('cancel')}
						</Button>
					</DialogActions>
					<DialogActions>
						<Button variant="contained" onClick={props.onCancel}>
							{t('huyBo')}
						</Button>
					</DialogActions>
				</Row>

			</form>
		</Dialog>
	);
}

CancelTranslateModal.propTypes = {
	show: PropTypes.bool,
	onHide: PropTypes.func,
	onCancel: PropTypes.func
};

export default CancelTranslateModal;
