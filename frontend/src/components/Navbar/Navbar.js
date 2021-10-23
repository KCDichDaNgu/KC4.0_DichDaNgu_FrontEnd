import React, { useEffect, useRef, useState } from 'react';
import {
	Container,
	Row,
	Image,
} from 'react-bootstrap';
import { IconButton, Typography, CircularProgress } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

import { Link } from 'react-router-dom';
import { SidebarData } from './SidebarData';
import Logo from '../../assets/images/lg.png';
import { sideBarHide, sideBarShow, changeIsLogin } from '../../redux/actions/navbarAction';
import styles from './navbarStyle.module.css';
import { useTranslation } from 'react-i18next';
import { useSelector, useDispatch } from 'react-redux';
import OutsideClick from '../../helpers/outsideClick';
import { useGoogleLogin } from 'react-google-login';
import Modal from '../Modal';
import * as axiosHelper from '../../helpers/axiosHelper';
import NavBarProfile from './NavBarProfile';
import LoadingButton from '@mui/lab/LoadingButton';
import { ACCESS_TOKEN, REFRESH_TOKEN, USER_IMG_URL } from '../../constants/envVar';

function Navbar() {
	const boxRef = useRef(null);
	const boxOutsideClick = OutsideClick(boxRef);
	const [modalShow, setModalShow] = useState(false);
	const [isLoading, setIsLoading] = useState(false);
	const navBarState = useSelector(state => state.navbarReducer);
	const dispatch = useDispatch();
	const { t } = useTranslation();
	
	useEffect(() => {
		if (boxOutsideClick) {
			dispatch(sideBarHide(false));
		}
	}, [boxOutsideClick, dispatch]);

	useEffect(() => {
		if(localStorage.getItem(ACCESS_TOKEN)){
			dispatch(changeIsLogin(true));
		}
	}, []);

	const showSidebar = () => {
		dispatch(sideBarShow(true));
	};

	const hideSidebar = () => {
		dispatch(sideBarHide(false));
	};

	const onSuccess = async (res) => {
		try {
			setIsLoading(true);
			const siginInResult = await axiosHelper.SignIn({
				access_token: res.accessToken,
				platform: 'web'
			});
			dispatch(changeIsLogin(true));
			localStorage.setItem(ACCESS_TOKEN, siginInResult.data.accessToken);
			localStorage.setItem(REFRESH_TOKEN, siginInResult.data.refreshToken);
			localStorage.setItem(USER_IMG_URL, res.profileObj.imageUrl);
			setIsLoading(false);
		}catch (e) {
			setIsLoading(false);
			alert(e);
		}
		// refreshTokenSetup(res);
	};

	// eslint-disable-next-line no-unused-vars
	const onFailure = (res) => {};

	const { signIn } = useGoogleLogin({
		onSuccess,
		onFailure,
		// eslint-disable-next-line no-undef
		clientId: process.env.REACT_APP_CLIENT_ID,
		isSignedIn: false,
		accessType: 'offline',
	});

	return (
		// 	<nav className={navBarState.shownavbar ? [styles.nav_menu,styles.active].join(' ') : styles.nav_menu}>
		<div ref={boxRef}>
			<Container fluid>
				<Row className={styles.headerTop}>
					<IconButton onClick={() => showSidebar()}><MenuIcon size="large" sx={{color: 'white'}}/></IconButton>
					<div style={{ display: 'flex', flex: 1, justifyContent: 'space-between' }}>
						<Typography sx={{}} variant="h5" className={styles.title}>
							{t('Translate.title')}
						</Typography>
						{navBarState.isLogin ? (
							<NavBarProfile setIsSigIn={(value) => dispatch(changeIsLogin(value))} setModalShow={setModalShow}/>
						) : 
							<LoadingButton 
								loadingIndicator={<CircularProgress sx={{color: 'white'}} size={20} />} 
								loading={isLoading}
								variant="text" 
								sx={{color: 'white'}} 
								onClick={() => signIn()}
							>
								{t('dangNhapVoiGoogle')}
							</LoadingButton>
						}
						<Modal
							show={modalShow}
							onHide={() => setModalShow(false)} />
					</div>
				</Row>
			</Container>
			<nav className={navBarState.shownavbar ? [styles.nav_menu, styles.active].join(' ') : styles.nav_menu}>
				<ul className={styles.nav_menu_items}>
					<li className={styles.logo}>
						<div className={styles.logosub}>
							<Image style={{ width: '80px', padding: '10px 0' }} src={Logo} alt="" roundedCircle />
						</div>
					</li>
					{SidebarData.map((item, index) => {
						return (
							<li key={index} className={styles.nav_text}>
								<Link to={item.path} onClick={() => hideSidebar()}>
									<span>{item.title}</span>
								</Link>
							</li>
						);
					})}
				</ul>
			</nav>
		</div>
	);
}

export default Navbar;
