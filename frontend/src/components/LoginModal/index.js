import React from 'react';
import { Modal, Form, Input, } from 'antd';
import PropTypes from 'prop-types';
import * as axiosHelper from '../../helpers/axiosHelper';
import { changeIsLogin } from '../../redux/actions/navbarAction';
import { getCurrentUser } from '../../redux/actions/userAction';
import { useDispatch } from 'react-redux';
import { ACCESS_TOKEN, REFRESH_TOKEN} from '../../constants/envVar';
import { useTranslation } from 'react-i18next';
const LoginModal = (props) => {
	const dispatch = useDispatch();
	const [form] = Form.useForm();
	const { visible, setVisible } = props;
	const { t }  = useTranslation();
	const onCancel = () => {
		setVisible(false);
	};

	const onSubmit = () => {
		form.submit();
	};

	const onCreate = async (values) => {
		try {
			const siginInResult = await axiosHelper.SignIn(values);
			dispatch(changeIsLogin(true));
			dispatch(getCurrentUser());
			localStorage.setItem(ACCESS_TOKEN, siginInResult.data.accessToken);
			localStorage.setItem(REFRESH_TOKEN, siginInResult.data.refreshToken);
			setVisible(false);
		}catch (e) {
			alert(e);
			setVisible(false);
		}
	};


	return (<Modal
		visible={visible}
		title={t('login')}
		okText="Submit"
		onCancel={onCancel}
		onOk={onSubmit}
	>
		<Form layout="vertical" form={form} onFinish={onCreate}>
			<Form.Item name='username' label={t('username')}>
				<Input/>
			</Form.Item>
			<Form.Item name='password' label={t('password')}>
				<Input type="password"/>
			</Form.Item>
		</Form>
	</Modal>);
};

LoginModal.propTypes = {
	visible: PropTypes.bool,
	setVisible: PropTypes.func,

};

export default LoginModal;