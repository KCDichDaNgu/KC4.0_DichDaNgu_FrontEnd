import React, { useEffect, useState } from 'react';
import { Modal, Form, Row, Col, InputNumber, Spin } from 'antd';
import PropTypes from 'prop-types';
import * as axiosHelper from '../../../../helpers/axiosHelper';
// import { useDispatch } from 'react-redux';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { STATUS_CODE } from '../../../../constants/common';
import styles from './index.module.css';

const EditQuotaModal = (props) => {
	// const dispatch = useDispatch();
	const { t } = useTranslation();
	const [form] = Form.useForm();
	const { visible, setVisible, userId } = props;
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

	const onCreate = async (values) => {
		try {
			// const new_values = (({ username, password, email, last_name, first_name, role, status }) => ({ username, password, email, last_name, first_name, role, status }))(values);
			const new_values = {};
			new_values['audio_translation_quota'] = {
				'vi-en': values.audio_quota_vi_en * 60,
				'vi-zh': values.audio_quota_vi_zh * 60,
			};

			new_values['text_translation_quota'] = {
				'vi-en': values.text_quota_vi_en,
				'vi-zh': values.text_quota_vi_zh,
			};

			new_values['id'] = userId;

			const result = await axiosHelper.updateUserQuota(new_values);

			if (result.code === STATUS_CODE.success) {
				toast.success(t('updateSuccess'));
			}

			setVisible(false);
		} catch (e) {
			toast(e);
			setVisible(false);
		}
	};

	if (isLoading) return <Spin />;

	return (<Modal
		visible={visible}
		title={t('updateUserQuota')}
		okText={t('edit')}
		cancelText={t('cancel')}
		onCancel={onCancel}
		onOk={onSubmit}
	>
		<Form layout="vertical" form={form} onFinish={onCreate} initialValues={userData}>
			<Row gutter={12}>
				<Col span={24}>
					<div className={styles.user}>{t('member')}: {userData.username}</div>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='text_quota_vi_en' label={t('textViEn')} rules={[{ required: true, message: t('requiredField') }]}>
						<InputNumber type="number" suffix={t('sentence')} min={0} className={styles.formQuota} />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='text_quota_vi_zh' label={t('textViZh')} rules={[{ required: true, message: t('requiredField') }]}>
						<InputNumber type="number" suffix={t('sentence')} min={0} className={styles.formQuota} />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='audio_quota_vi_en' label={t('audioViEn')} rules={[{ required: true, message: t('requiredField') }]}>
						<InputNumber type="number" suffix={t('minute')} min={0} className={styles.formQuota} />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='audio_quota_vi_zh' label={t('audioViZh')} rules={[{ required: true, message: t('requiredField') }]}>
						<InputNumber type="number" suffix={t('minute')} min={0} className={styles.formQuota} />
					</Form.Item>
				</Col>
			</Row>
		</Form>
	</Modal>);
};

EditQuotaModal.propTypes = {
	visible: PropTypes.bool,
	setVisible: PropTypes.func,
	userId: PropTypes.string,

};

export default EditQuotaModal;