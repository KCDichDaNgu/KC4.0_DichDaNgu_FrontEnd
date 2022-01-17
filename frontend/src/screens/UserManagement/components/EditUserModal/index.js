import React, { useEffect, useState } from 'react';
import { Modal, Form, Input, Select, Row, Col, InputNumber, Spin } from 'antd';
import PropTypes from 'prop-types';
import * as axiosHelper from '../../../../helpers/axiosHelper';
// import { useDispatch } from 'react-redux';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { STATUS_CODE } from '../../../../constants/common';
import styles from './index.module.css';

const EditUserModal = (props) => {
	// const dispatch = useDispatch();
	const { t } = useTranslation();
	const [form] = Form.useForm();
	const {visible, setVisible, userId} = props;
	const [userData, setUserData] = useState({});
	const [isLoading, setIsloading] = useState(true);

	const onCancel = () => {
		setVisible(false);
	};

	const fetchUserData = async (userId) => {
		const result = await axiosHelper.getUser(userId);
		return result.data;
	};

	useEffect(async () => {
		const _userData = await fetchUserData(userId);;

		setUserData({
			username: _userData.username,
			password:_userData.password,
			email:_userData.email,
			first_name:_userData.firstName,
			last_name:_userData.lastName,
			role:_userData.role,
			status:_userData.status,
			audio_quota_vi_en: Math.floor(_userData.audioTranslationQuota['vi-en'] / 60),
			audio_quota_vi_zh: Math.floor(_userData.audioTranslationQuota['vi-zh'] / 60),
			text_quota_vi_en: _userData.textTranslationQuota['vi-en'],
			text_quota_vi_zh: _userData.textTranslationQuota['vi-zh'],
		});
		setIsloading(false);
	}, [visible]);

	const onSubmit = () => {
		form.submit();
	};

	if (isLoading) return <Spin />;

	const onSave = async (values) => {
		try {
			const new_values = (({ username, password, email, last_name, first_name, role, status }) => ({ username, password, email, last_name, first_name, role, status }))(values);
			new_values['id'] = userId;
			new_values['audio_translation_quota'] = {
				'vi-en': values.audio_quota_vi_en * 60,
				'vi-zh': values.audio_quota_vi_zh * 60,
			};

			new_values['text_translation_quota'] = {
				'vi-en': values.text_quota_vi_en,
				'vi-zh': values.text_quota_vi_zh,
			};
			const result = await axiosHelper.updateUser(new_values);

			if (result.code === STATUS_CODE.success) {
				toast.success(t('editUserSuccess'));
			}

			setVisible(false);
		} catch (e) {
			toast(e);
			setVisible(false);
		}
	};

	return (<Modal
		visible={visible}
		title={t('editUser')}
		okText={t('edit')}
		cancelText={t('cancel')}
		onCancel={onCancel}
		onOk={onSubmit}
	>
		<Form layout="vertical" form={form} onFinish={onSave} initialValues={userData}>
			<Row gutter={12}>
				<Col xs={24} md={12}>
					<Form.Item name='username' label={t('username')} rules={[{ required: true, message: t('requiredField') }]}>
						<Input />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='password' label={t('password')} rules={[{ required: true, message: t('requiredField') }]}>
						<Input />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='email' label={t('email')} rules={[{ required: true, message: t('requiredField') }]}>
						<Input />
					</Form.Item>
				</Col>
			</Row>

			<Row gutter={12}>

				<Col xs={24} md={12}>
					<Form.Item name='last_name' label={t('lastName')}>
						<Input />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='first_name' label={t('firstName')} >
						<Input />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<div className={styles.formQuota}>
						<Form.Item name='text_quota_vi_en' label={t('textQuotaViEn')} rules={[{ required: true, message: t('requiredField') }]}>
							<InputNumber type="number" suffix={t('sentence')} min={0} className={styles.formQuota} />
						</Form.Item>
					</div>

				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='text_quota_vi_zh' label={t('textQuotaViZh')} rules={[{ required: true, message: t('requiredField') }]}>
						<InputNumber type="number" suffix={t('sentence')} min={0} className={styles.formQuota} />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='audio_quota_vi_en' label={t('audioQuotaViEn')} rules={[{ required: true, message: t('requiredField') }]}>
						<InputNumber type="number" suffix={t('minute')} min={0} className={styles.formQuota} />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='audio_quota_vi_zh' label={t('audioQuotaViZh')} rules={[{ required: true, message: t('requiredField') }]}>
						<InputNumber type="number" suffix={t('minute')} min={0} className={styles.formQuota} />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='role' label={t('role')} rules={[{ required: true, message: t('requiredField') }]}>
						<Select >
							<Select.Option value='admin'>
								{t('admin')}
							</Select.Option>

							<Select.Option value='member'>
								{t('member')}
							</Select.Option>
						</Select>
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='status' label={t('status')} rules={[{ required: true, message: t('requiredField') }]}>
						<Select >
							<Select.Option value='active'>
								{t('active')}
							</Select.Option>
							<Select.Option value='inactive'>
								{t('inactive')}
							</Select.Option>
						</Select>
					</Form.Item>
				</Col>
			</Row>
		</Form>
	</Modal>);
};

EditUserModal.propTypes = {
	visible: PropTypes.bool,
	setVisible: PropTypes.func,
	userId: PropTypes.string,

};

export default EditUserModal;