
import React from 'react';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';

function ToastSuccess(props) {

	const { t } = useTranslation();
	console.log(props.message);
	return (
		<>
			{t(props.message)}
		</>
	);
}

ToastSuccess.propTypes = {
	message: PropTypes.string
};

export default ToastSuccess;
