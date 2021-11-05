import React from 'react';
import { Modal, Form, Input, Select, Row, Col, InputNumber } from 'antd';
import PropTypes from 'prop-types';
import * as axiosHelper from '../../../../helpers/axiosHelper';
// import { useDispatch } from 'react-redux';
import { useTranslation } from 'react-i18next';
import { toast } from 'react-toastify';
import { STATUS_CODE } from '../../../../constants/common';

const CreateUserModal = (props) => {
	// const dispatch = useDispatch();
	const { t } = useTranslation();
	const [form] = Form.useForm();
	const { visible, setVisible } = props;
	const onCancel = () => {
		setVisible(false);
	};

	const onSubmit = () => {
		form.submit();
	};

	const onCreate = async (values) => {
		try {
			const new_values = (({ username, password, email, last_name, first_name, role, status }) => ({ username, password, email, last_name, first_name, role, status }))(values);
			new_values['audio_translation_quota'] = {
				'vi-en': values.audio_quota_vi_en,
				'vi-zh': values.audio_quota_vi_zh,
			};

			new_values['text_translation_quota'] = {
				'vi-en': values.text_quota_vi_en,
				'vi-zh': values.text_quota_vi_zh,
			};
			const result = await axiosHelper.CreateUserByAdmin(new_values);

			if (result.code === STATUS_CODE.success) {
				toast.success(t('createUserSuccess'));
			}

			setVisible(false);
		} catch (e) {
			toast(e);
			setVisible(false);
		}
	};

	return (<Modal
		visible={visible}
		title={t('createUser')}
		okText="Submit"
		onCancel={onCancel}
		onOk={onSubmit}
	>
		<Form layout="vertical" form={form} onFinish={onCreate}>
			<Row gutter={12}>
				<Col xs={24} md={12}>
					<Form.Item name='username' label={t('username')}>
						<Input />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='password' label={t('password')}>
						<Input />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='email' label={t('email')}>
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
					<Form.Item name='first_name' label={t('firstName')}>
						<Input />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='text_quota_vi_en' label={t('textQuotaViEn')}>
						<InputNumber />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='text_quota_vi_zh' label={t('textQuotaViZh')}>
						<InputNumber />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='audio_quota_vi_en' label={t('audioQuotaViEn')}>
						<InputNumber />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='audio_quota_vi_zh' label={t('audioQuotaViZh')}>
						<InputNumber />
					</Form.Item>
				</Col>

				<Col xs={24} md={12}>
					<Form.Item name='role' label={t('role')}>
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
					<Form.Item name='status' label={t('status')}>
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

CreateUserModal.propTypes = {
	visible: PropTypes.bool,
	setVisible: PropTypes.func,

};

export default CreateUserModal;