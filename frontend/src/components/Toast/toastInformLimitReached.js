
import React from 'react';
import { useTranslation } from 'react-i18next';
import PropTypes from 'prop-types';

function ToastInformLimitReached(props) {

	const { t } = useTranslation();
	const unit = props.type === 'text' ? t('character') : t('minute');
	const used = props.type === 'text' ? props.used : Math.ceil(props.used / 60);
	const quota = props.type === 'text' ? props.quota : Math.floor(props.quota / 60);
	return (
		<>
			{t(`${props.message}`)}:&nbsp;
			{t(used)}/{t(quota)} {unit}
		</>
	);
}

ToastInformLimitReached.propTypes = {
	used: PropTypes.string,
	quota: PropTypes.string,
	type: PropTypes.string,
	message: PropTypes.string,
};

export default ToastInformLimitReached;
