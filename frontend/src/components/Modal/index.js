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
import { useTranslation } from 'react-i18next';
import * as axiosHelper from '../../helpers/axiosHelper';
import { USER_IMG_URL } from '../../constants/envVar';

function ModalInfo(props) {
	const { t } = useTranslation();
	const [isLoading, setIsloading] = useState(false);
	const [userInfo, setUserInfo] = useState();

	useEffect(() => {
		if(props.show){
			const getInfo = async () => {
				try{
					setIsloading(true);
					const result = await axiosHelper.getMe();
					setUserInfo(result.data);
					setIsloading(false);
				}catch (e) {
					setIsloading(false);
					alert(e);
				}
			};
			getInfo();
		}
	},[props.show]);

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
				<DialogContent sx={{py: 1}}>
					<Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
						<Avatar sx={{ width: 60, height: 60 }} src={localStorage.getItem(USER_IMG_URL)}/>
					</Box>
					<Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
						<PersonIcon fontSize="medium" sx={{ color: 'action.active', mr: 1 }} />
						<TextField
							id="name"
							label={t('ten')}
							fullWidth
							InputProps={{
								readOnly: true,
							}}
							size='small'
							value={userInfo ? userInfo.firstName : ''}
							variant="standard"
						/>
					</Box>
					<Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mt: 1 }}>
						<EmailIcon fontSize="medium" sx={{ color: 'action.active', mr: 1 }} />
						<TextField
							id="name"
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
				</DialogContent>
				<Divider />
				<DialogActions>
					<Button variant="contained" onClick={props.onHide}>
						{t('huyBo')}
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
