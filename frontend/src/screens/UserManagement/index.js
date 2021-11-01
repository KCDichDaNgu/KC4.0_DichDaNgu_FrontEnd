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

function UserManagement(props) {
	const { userState, navbarState } = props;
	const { t } = useTranslation();
	const [isLoading, setIsLoading] = useState(true);
	const [visible, setVisible] = useState(false);

	useEffect(() => {
		const user = JSON.parse(localStorage.getItem('user'));

		console.log(user);
		if (isAdmin(user)) {
			props.getUserAsync({});
			setIsLoading(false);
		}
		setIsLoading(false);
	}, []);

	useEffect(() => {
		props.getUserAsync({});
		setIsLoading(false);
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

	const handleStatusChange = async (e, currentStatus, record) => {
		const status = e.target.value;

		const body = {
			id: record.id,
			role: record.role,
			status: status
		};

		console.log(record);

		const result = await axiosHelper.updateUser(body);

		if (result.code === STATUS_CODE.success) {
			props.getUserAsync({});
			alert(t('updateSuccess'));
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
			// render: (password, user) => (
			// 	<Tooltip
			// 		trigger={['focus']}
			// 		title={t('changeInput')}
			// 		placement='topLeft'>
			// 		<Input
			// 			className='user-input'
			// 			defaultValue={password}
			// 			disabled={disableUpdate(user)}
			// 			onPressEnter={event => {
			// 				updateUser(user.id, { password: event.target.value });
			// 			}
			// 			} />
			// 	</Tooltip>
			// ),
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