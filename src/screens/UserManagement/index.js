/* eslint-disable no-unused-vars */
import React, { useEffect, useState } from 'react';
import styles from './userManagement.module.css';
import { getUserListAsync } from '../../redux/actions/userAction';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Table, Button, Radio, Row, Col } from 'antd';
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

	const renderStatistic = (id, quota, used) => {
		return (

			<div style={{ display: 'flex', flexDirection: 'column' }}>
				<Row>
					<Col span={12}>
						<div style={{ flexDirection: 'column', textAlign: 'start' }}>
							{t('ViEn')}: {used['vi-en']}/{quota['vi-en']} {t('character')}<br />
							{t('ViZh')}: {used['vi-zh']}/{quota['vi-zh']} {t('character')}

						</div>
					</Col>

					<Col span={12}>
						<div style={{ flexDirection: 'column', textAlign: 'start' }}>
							{t('ViLo')}: {used['vi-lo']}/{quota['vi-lo']} {t('character')}<br />
							{t('ViKm')}: {used['vi-km']}/{quota['vi-km']} {t('character')}
						</div>
					</Col>
				</Row>

				<EditIcon fontSize='small' style={{ marginLeft: 'auto', cursor: 'pointer' }} onClick={() => { setEditUserQuotaModalVisible(true); setEditingUserId(id); }} />

			</div>
		);
	};

	const handleStatusChange = async (e, currentStatus, record) => {
		const status = e.target.value;

		const body = {
			id: record.id,
			role: record.role,
			status: status,
			text_translation_quota: record.textTranslationQuota
		};

		const result = await axiosHelper.updateUser(body);

		if (result.code === STATUS_CODE.success) {
			props.getUserListAsync({});
			toast.success(t('updateSuccess'));
		}
	};


	const columns = [
		{
			title: t('username'),
			dataIndex: 'username',
			key: 'username',
		},
		{
			title: t('email'),
			dataIndex: 'email',
			key: 'email',
		},
		{
			title: t('textQuota'),
			align: 'center',
			dataIndex: 'textTranslationQuota',
			key: 'textQuota',
			render: (textQuota, record) => {
				return renderStatistic(record.id, record.textTranslationQuota, record.totalTranslatedText);
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
			{/* <Button onClick={() => setCreateUserModalVisible(true)} type="primary" className={styles.createButton}>{t('createUser')}</Button> */}

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