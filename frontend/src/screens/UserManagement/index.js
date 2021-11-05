import React, { useEffect, useState } from 'react';
import styles from './userManagement.module.css';
import { getUserAsync } from '../../redux/actions/userAction';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Table, Button, Radio } from 'antd';
import { useTranslation } from 'react-i18next';
import CreateUserModal from './components/CreateUserModal';
import { STATUS_CODE, USER_STATUS } from '../../constants/common';
import * as axiosHelper from '../../helpers/axiosHelper';
import { toast } from 'react-toastify';

function UserManagement(props) {
	const { userState, navbarState } = props;
	const { t } = useTranslation();
	const [isLoading, setIsLoading] = useState(true);
	const [visible, setVisible] = useState(false);

	useEffect(() => {
		const user = JSON.parse(localStorage.getItem('user'));
		if (isAdmin(user)) {
			props.getUserAsync({});
			setIsLoading(false);
		}
		setIsLoading(false);
	}, []);

	useEffect(() => {
		if (navbarState.isLogin) {
			props.getUserAsync({});
			setIsLoading(false);
		}
	}, [navbarState.isLogin, visible]);



	const isAdmin = (user) => {
		return user?.role === 'admin' && user?.status === USER_STATUS.active;
	};

	const renderStatus = (currentStatus, record) => {
		return (
			<Radio.Group defaultValue={currentStatus}>
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

	const renderStatistic = (quota, used) => {
		return (
			<div>				
				vi-en: {used['vi-en']}/{quota['vi-en']}<br/>
				vi-zh: {used['vi-zh']}/{quota['vi-zh']}
			</div>
		);
	};

	const handleStatusChange = async (e, currentStatus, record) => {
		const status = e.target.value;

		const body = {
			id: record.id,
			role: record.role,
			status: status,
			audio_translation_quota: record.textTranslationQuota,
			text_translation_quota: record.audioTranslationQuota
		};

		const result = await axiosHelper.updateUser(body);

		if (result.code === STATUS_CODE.success) {
			props.getUserAsync({});
			toast.success(t('updateSuccess'));
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
			title: t('audioQuota'),
			align: 'center',
			dataIndex: 'audioTranslationQuota',
			key: 'audioQuota',
			render: (audioQuota, record) => {
				return renderStatistic(record.audioTranslationQuota, record.totalTranslatedAudio);
			}
		},
		{
			title: t('textQuota'),
			align: 'center',
			dataIndex: 'textTranslationQuota',
			key: 'textQuota',
			render: (textQuota, record) => {
				return renderStatistic(record.textTranslationQuota, record.totalTranslatedText);
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
	];

	if (isLoading) return <></>;

	if (!isAdmin(JSON.parse(localStorage.getItem('user')))) return <div className={styles.pageContainer}>No authorized</div>;

	return (
		<div className={styles.pageContainer} >
			<Button onClick={() => setVisible(true)} type="primary" className={styles.createButton}>{t('createUser')}</Button>

			<Table
				bordered
				className='table-striped-rows'
				dataSource={userState.listUser.map(d => ({ ...d, key: d.id }))}
				columns={columns}
			>
			</Table>
			<CreateUserModal visible={visible} setVisible={setVisible} />
		</div>
	);
}

UserManagement.propTypes = {
	userState: PropTypes.object,
	navbarState: PropTypes.object,
	getUserAsync: PropTypes.func,
};

const mapStateToProps = (state) => ({
	userState: state.userReducer,
	navbarState: state.navbarReducer,
});

const mapDispatchToProps = {
	getUserAsync
};

export default connect(mapStateToProps, mapDispatchToProps)(UserManagement);