
import React from 'react';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';

function ToastError(props) {

	const { t } = useTranslation();
	return (
		<>
			{t(props.message)}
		</>
	);
}

ToastError.propTypes = {
	message: PropTypes.string
};

export default ToastError;
