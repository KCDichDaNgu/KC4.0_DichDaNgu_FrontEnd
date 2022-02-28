import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import {
	Typography,
	TextField,
	Dialog,
	DialogTitle,
	Divider,
	DialogContent,
	DialogActions,
	Button,
	Box,
	LinearProgress,
	Avatar,
} from '@mui/material';
import PersonIcon from '@mui/icons-material/Person';
import EmailIcon from '@mui/icons-material/Email';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import { useTranslation } from 'react-i18next';
import * as axiosHelper from '../../helpers/axiosHelper';
import { USER_IMG_URL } from '../../constants/envVar';
import { toast } from 'react-toastify';
import { STATUS_CODE } from '../../constants/common';

function ModalInfo(props) {
	const { t } = useTranslation();
	const [isLoading, setIsloading] = useState(false);
	const [userInfo, setUserInfo] = useState();

	useEffect(() => {
		if (props.show) {
			const getInfo = async () => {
				try {
					setIsloading(true);
					const result = await axiosHelper.getMe();
					setUserInfo(result.data);
					setIsloading(false);
				} catch (e) {
					setIsloading(false);
					// alert(e);
				}
			};
			getInfo();
		}
	}, [props.show]);

	const onSave = async () => {
		try {
			// const new_values = (({ username, password, email, last_name, first_name, role, status }) => ({ username, password, email, last_name, first_name, role, status }))(values);
			const new_values = {
				first_name: userInfo.firstName,
				last_name: userInfo.lastName,
				avatar: userInfo.avatar,
			};

			const result = await axiosHelper.updateUserSelf(new_values);

			if (result.code === STATUS_CODE.success) {
				toast.success(t('updateSuccess'));
			}

			props.onHide();
		} catch (e) {
			toast(e);
			props.onHide();
		}
	};

	if (isLoading) return <></>;

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
						{t('thongTinCaNhan')}
					</Typography>
				</DialogTitle>
				<Divider />
				{isLoading ? <LinearProgress /> : null}
				<DialogContent sx={{ py: 1 }}>
					<Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
						<Avatar sx={{ width: 60, height: 60 }} src={localStorage.getItem(USER_IMG_URL)} />
					</Box>
					<Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
						<PersonIcon fontSize="medium" sx={{ color: 'action.active', mr: 1 }} />
						<TextField
							id="firstName"
							label={t('ho')}
							fullWidth
							size='small'
							value={userInfo ? userInfo.firstName : ''}
							variant="standard"
							onChange={e => setUserInfo({...userInfo, firstName: e.target.value})}
						/>
						<TextField
							id="lastName"
							label={t('ten')}
							fullWidth
							size='small'
							value={userInfo ? userInfo.lastName : ''}
							onChange={e => setUserInfo({...userInfo, lastName: e.target.value})}
							variant="standard"
						/>
					</Box>
					<Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
						<EmailIcon fontSize="medium" sx={{ color: 'action.active', mr: 1 }} />
						<TextField
							id="email"
							label={t('email')}
							InputProps={{
								readOnly: true,
							}}
							fullWidth
							size='small'
							value={userInfo ? userInfo.email : ''}
							variant="standard"
						/>
					</Box>

					<Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'start', mt: 1 }}>
						<InsertDriveFileIcon fontSize="medium" sx={{ color: 'action.active', mr: 1 }} />
						{userInfo ?
							<div>
								{t('ViEn')}: {userInfo.totalTranslatedText['vi-en']}/{userInfo.textTranslationQuota['vi-en']} {t('sentence')}<br/>
								{t('ViZh')}: {userInfo.totalTranslatedText['vi-zh']}/{userInfo.textTranslationQuota['vi-zh']} {t('sentence')}<br/>
								{t('ViLo')}: {userInfo.totalTranslatedText['vi-lo']}/{userInfo.textTranslationQuota['vi-lo']} {t('sentence')}<br/>
								{t('ViKm')}: {userInfo.totalTranslatedText['vi-km']}/{userInfo.textTranslationQuota['vi-km']} {t('sentence')}
							</div> :
							<></>
						}
					</Box>
				</DialogContent>
				<Divider />
				<DialogActions>
					<Button variant="contained" onClick={props.onHide}>
						{t('cancel')}
					</Button>
					<Button variant="contained" onClick={onSave}>
						{t('edit')}
					</Button>
				</DialogActions>
			</form>
		</Dialog>
	);
}

ModalInfo.propTypes = {
	show: PropTypes.bool,
	onHide: PropTypes.func,
};

export default ModalInfo;
