/* eslint-disable react/no-unescaped-entities */
import React from 'react';
import { Container, Row } from 'react-bootstrap';
import styles from './aboutStyle.module.css';
import { useTranslation } from 'react-i18next';

function Products() {
	const { t } = useTranslation();

	return (
		<Container>
			<Row>
				<div className={styles.aboutStyle}>
					<p className={styles.abouttext}>{t('title')}</p>
				</div>
			</Row>
			<Row className="justify-content-center">
				<div className={styles.aboutStyle1}>
					<p className={styles.abouttext1}>{t('contact')}</p>
					<p className={styles.abouttext2}>{t('footer')}</p>
				</div>
			</Row>
		</Container>
	);
}

export default Products;
