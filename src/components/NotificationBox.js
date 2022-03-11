import React, { useState, useEffect } from 'react';
import { REMOVE_NOTI, INFO_NOTI, FAILURE_NOTI } from '../constants/notificationConstant';
import Alert from 'react-bootstrap/Alert';
import { useTranslation  } from 'react-i18next'; 

export default function NotificationBox(props) {
	// eslint-disable-next-line react/prop-types
	const { message, dispatchNoti, id, type = INFO_NOTI } = props;
	const { t } = useTranslation();
	const [exit, setExit] = useState(false);

	const typeVariantMapper = {};
	typeVariantMapper[INFO_NOTI] = 'info';
	typeVariantMapper[FAILURE_NOTI] = 'danger';

	useEffect(() => {
		// Wait 3 sec b4 close the noti
		setTimeout(() => {
			setExit(true);
			// remove this from DOM
			// Wait 2 sec b4 remove
			setTimeout(() => {
				dispatchNoti({
					type: REMOVE_NOTI,
					id,
				});
			}, 2000);
		}, 3000);
	});

	return (
		<Alert variant={typeVariantMapper[type]} className={`notification-item ${exit ? 'notification-exit' : ''}`}>
			{!exit ? (
				<>
					{ type === FAILURE_NOTI ? <Alert.Heading>{t('loi')}</Alert.Heading> : null }
					<p>{message}</p>
				</>
			) : null}
		</Alert>
	);
}
