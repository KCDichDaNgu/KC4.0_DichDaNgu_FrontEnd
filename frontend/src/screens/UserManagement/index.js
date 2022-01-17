import React, { useEffect, useState } from 'react';
import styles from './userManagement.module.css';
import { getUserListAsync } from '../../redux/actions/userAction';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Table, Radio } from 'antd';
import { Button } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import { useTranslation } from 'react-i18next';
import CreateUserModal from './components/CreateUserModal';
import { STATUS_CODE, USER_STATUS } from '../../constants/common';
import * as axiosHelper from '../../helpers/axiosHelper';
import { toast } from 'react-toastify';
import EditQuotaModal from './components/EditQuotaModal';
import authHoc from '../../hocs/authHoc';

function UserManagement(props) {
	const { userState, navbarState } = props;
	const { t } = useTranslation();
	const [isLoading, setIsLoading] = useState(true);
	const [createUserModalVisible, setCreateUserModalVisible] = useState(false);
	const [editUserQuotaModalVisible, setEditUserQuotaModalVisible] = useState(false);
	const [editingUserId, setEditingUserId] = useState('');
	const [currentUser, setCurrentUser] = useState('');

	useEffect(() => {
		const user = JSON.parse(localStorage.getItem('user'));

		if (isAdmin(user)) {
			props.getUserListAsync({});
			setCurrentUser(user);
			setIsLoading(false);
		}

		setIsLoading(false);
	}, []);

	useEffect(() => {
		if (navbarState.isLogin) {
			props.getUserListAsync({});
			setIsLoading(false);
		}
	}, [navbarState.isLogin, createUserModalVisible, editUserQuotaModalVisible]);

	const isAdmin = (user) => {
		return user?.role === 'admin' && user?.status === USER_STATUS.active;
	};

	const renderStatus = (currentStatus, record) => {
		return (
			<Radio.Group defaultValue={currentStatus} disabled={record.id === currentUser.id}>
				{
					Object.keys(USER_STATUS).map(statusKey => {
						return (
							<Radio.Button key={statusKey} value={statusKey} onClick={(e) =>
								handleStatusChange(e, currentStatus, record)
							}>
								{t(`${statusKey}`)}
							</Radio.Button>
						);
					})
				}
			</Radio.Group>
		);
	};

	const renderStatistic = (id, quota, used, type) => {
		return (

			<div style={{ display: 'flex', flexDirection: 'column' }}>
				{type === 'audio' ?
					<div>
						{t('ViEn')}: {Math.floor(used['vi-en'] / 6) / 10}/{Math.floor(quota['vi-en'] / 60)} {t('minute')}<br />
						{t('ViZh')}: {Math.floor(used['vi-zh'] / 6) / 10}/{Math.floor(quota['vi-zh'] / 60)} {t('minute')}
					</div> :
					<div>
						{t('ViEn')}: {used['vi-en']}/{quota['vi-en']} {t('sentence')}<br />
						{t('ViZh')}: {used['vi-zh']}/{quota['vi-zh']} {t('sentence')}
					</div>
				}

				<EditIcon fontSize='small' style={{ marginLeft: 'auto', cursor: 'pointer' }} onClick={() => { setEditUserQuotaModalVisible(true); setEditingUserId(id); }} />

			</div>
		);
	};

	const renderDelete = (record) => {
		return (
			<Button onClick={() => handleDelete(record)} disabled={record.id === currentUser.id}>
				Xóa
			</Button>
		);
	};

	const handleStatusChange = async (e, currentStatus, record) => {
		const status = e.target.value;

		const body = {
			id: record.id,
			role: record.role,
			status: status,
			audio_translation_quota: record.audioTranslationQuota,
			text_translation_quota: record.textTranslationQuota
		};

		const result = await axiosHelper.updateUser(body);

		if (result.code === STATUS_CODE.success) {
			props.getUserListAsync({});
			toast.success(t('updateSuccess'));
		}
	};

	const handleDelete = async (record) => {

		const body = {
			username: record.username,
		};
		
		const result = await axiosHelper.deleteUser(body);

		if (result.code === STATUS_CODE.success) {
			props.getUserListAsync({});
			toast.success(t('deleteUserSuccess'));
		}
	};


	const columns = [
		{
			title: t('username'),
			dataIndex: 'username',
			key: 'username',
			// render: (username, user) => (
			// 	<Tooltip
			// 		trigger={['focus']}
			// 		title={t('changeInput')}
			// 		placement='topLeft'>
			// 		<Input
			// 			className='user-input'
			// 			defaultValue={username}
			// 			disabled={disableUpdate(user)}
			// 			onPressEnter={event => {
			// 				updateUser(user.id, { username: event.target.value });
			// 			}
			// 			} />
			// 	</Tooltip>
			// ),
		},
		{
			title: t('email'),
			dataIndex: 'email',
			key: 'email',
			// render: (email, user) => (
			// 	<Tooltip
			// 		trigger={['focus']}
			// 		title={t('changeInput')}
			// 		placement='topLeft'>
			// 		<Input
			// 			className='user-input'
			// 			defaultValue={email}
			// 			disabled={disableUpdate(user)}
			// 			onPressEnter={event => {
			// 				updateUser(user.id, { email: event.target.value });
			// 			}
			// 			} />
			// 	</Tooltip>
			// ),
		},
		{
			title: t('password'),
			dataIndex: 'password',
			key: 'password',
		},
		{
			title: t('audioQuota'),
			align: 'center',
			dataIndex: 'audioTranslationQuota',
			key: 'audioQuota',
			render: (audioQuota, record) => {
				return renderStatistic(record.id, record.audioTranslationQuota, record.totalTranslatedAudio, 'audio');
			}
		},
		{
			title: t('textQuota'),
			align: 'center',
			dataIndex: 'textTranslationQuota',
			key: 'textQuota',
			render: (textQuota, record) => {
				return renderStatistic(record.id, record.textTranslationQuota, record.totalTranslatedText, 'text');
			}
		},
		{
			title: t('status'),
			align: 'center',
			dataIndex: 'status',
			key: 'status',
			render: (currentStatus, record) => {
				return renderStatus(currentStatus, record);
			}
		},
		{
			title: t('role'),
			dataIndex: 'role',
			key: 'role',
			render: (role) => t(`${role}`)
		},
		{
			align: 'center',
			key: 'status',
			render: (record) => {
				return renderDelete(record);
			}
		},
	];

	if (isLoading) return <></>;

	if (!isAdmin(JSON.parse(localStorage.getItem('user')))) return <div className={styles.pageContainer}>No authorized</div>;

	return (
		<div className={styles.pageContainer} >
			<Button onClick={() => setCreateUserModalVisible(true)} variant="outlined" className={styles.createButton}>{t('createUser')}</Button>

			<Table
				bordered
				className='table-striped-rows'
				dataSource={userState.listUser.map(d => ({ ...d, key: d.id }))}
				columns={columns}
			>
			</Table>

			{createUserModalVisible && <CreateUserModal visible={createUserModalVisible} setVisible={setCreateUserModalVisible} />}
			{editUserQuotaModalVisible && <EditQuotaModal userId={editingUserId} visible={editUserQuotaModalVisible} setVisible={setEditUserQuotaModalVisible} />}
		</div>
	);
}

UserManagement.propTypes = {
	userState: PropTypes.object,
	navbarState: PropTypes.object,
	getUserListAsync: PropTypes.func,
};

const mapStateToProps = (state) => ({
	userState: state.userReducer,
	navbarState: state.navbarReducer,
});

const mapDispatchToProps = {
	getUserListAsync
};

export default connect(mapStateToProps, mapDispatchToProps)(authHoc(UserManagement));