/* eslint-disable react/no-unescaped-entities */
import React, { useEffect } from 'react';
import { Container, Row } from 'react-bootstrap';
import styles from './aboutStyle.module.css';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { useHistory } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import authHoc from '../../hocs/authHoc';
function Products(props) {
	const { t } = useTranslation();
	const history = useHistory();
	const { navbarState } = props;
	useEffect(() => {
		if (navbarState.isLogin) {
			history.push('/translate');
		}
	}, [navbarState.isLogin]);

	return (
		<Container>
			<Row>
				<div className={styles.aboutStyle}>
					<span className={styles.abouttext}>{t('warningNoAuth1')}</span>
					<Link to='/login' className={styles.abouttext1}>{t('warningNoAuth2')}</Link>
					<span className={styles.abouttext}>{t('warningNoAuth3')}</span>
				</div>
			</Row>
		</Container>
	);
}

Products.propTypes = {
	navbarState: PropTypes.object,
};

const mapStateToProps = (state) => ({
	navbarState: state.navbarReducer,
});


export default connect(mapStateToProps)(authHoc(Products));
