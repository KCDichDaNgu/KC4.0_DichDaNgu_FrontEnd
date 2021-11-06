import React, { useEffect, useRef, useState } from 'react';
import {
	Container,
	Row,
	// Image,
} from 'react-bootstrap';
import { IconButton, Typography, CircularProgress } from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';

import { Link } from 'react-router-dom';
import { SidebarData, AdminSidebarData, UnauthorizedSidebarData } from './SidebarData';
// import Logo from '../../assets/images/lg.png';
import { sideBarHide, sideBarShow, changeIsLogin } from '../../redux/actions/navbarAction';
import styles from './navbarStyle.module.css';
import { useTranslation } from 'react-i18next';
import { useSelector, useDispatch } from 'react-redux';
import OutsideClick from '../../helpers/outsideClick';
import Modal from '../Modal';
import NavBarProfile from './NavBarProfile';
import LoadingButton from '@mui/lab/LoadingButton';
import { ACCESS_TOKEN, } from '../../constants/envVar';
import LoginModal from '../LoginModal';
import { USER_STATUS } from '../../constants/common';
import { useHistory } from 'react-router-dom';

function Navbar() {
	const boxRef = useRef(null);
	const history = useHistory();
	const boxOutsideClick = OutsideClick(boxRef);
	const [modalShow, setModalShow] = useState(false);
	const [loginModalVisible, setLoginModalVisible] = useState(false);
	const [isLoading, setIsLoading] = useState(false);
	const [sidebarData, setSidebarData] = useState(SidebarData);
	const navBarState = useSelector(state => state.navbarReducer);
	const dispatch = useDispatch();
	const { t } = useTranslation();

	useEffect(() => {
		if (boxOutsideClick) {
			dispatch(sideBarHide(false));
		}

		const user = JSON.parse(localStorage.getItem('user'));

		if (!user?.username) { setSidebarData(UnauthorizedSidebarData); }
		else if (isAdmin(user)) {
			setSidebarData(AdminSidebarData);
		} else setSidebarData(SidebarData);;

	}, [boxOutsideClick, dispatch]);

	const isAdmin = (user) => {
		return user?.role === 'admin' && user?.status === USER_STATUS.active;
	};

	useEffect(() => {
		if (localStorage.getItem(ACCESS_TOKEN)) {
			dispatch(changeIsLogin(true));
			setIsLoading(false);
		}

	}, []);

	const showSidebar = () => {
		dispatch(sideBarShow(true));
	};

	const hideSidebar = () => {
		dispatch(sideBarHide(false));
	};

	// eslint-disable-next-line no-unused-vars
	const onFailure = (res) => { };
	return (
		// 	<nav className={navBarState.shownavbar ? [styles.nav_menu,styles.active].join(' ') : styles.nav_menu}>
		<div ref={boxRef}>
			<Container fluid>
				<Row className={styles.headerTop}>
					<IconButton onClick={() => showSidebar()}><MenuIcon size="large" sx={{ color: 'white' }} /></IconButton>
					<div style={{ display: 'flex', width: 'calc(100% - 50px)', paddingRight: '16px' }}>
						<Typography sx={{}} variant="h5" className={styles.title}>
							{t('Translate.title')}
						</Typography>

						<div className={styles.loginContainer}>
							{navBarState.isLogin ? (
								<NavBarProfile setIsSignIn={(value) => dispatch(changeIsLogin(value))} setModalShow={setModalShow} />
							) :
								<Row justify='end'>
									<LoadingButton
										loadingIndicator={<CircularProgress sx={{ color: 'white' }} size={20} />}
										loading={isLoading}
										variant="text"
										sx={{ color: 'white' }}
										onClick={() => history.push('/login')}
									>
										{t('dangNhap')}
									</LoadingButton>
								</Row>
							}

						</div>

						<Modal
							show={modalShow}
							onHide={() => setModalShow(false)} />
						<LoginModal
							visible={loginModalVisible}
							setVisible={setLoginModalVisible} />
					</div>
				</Row>
			</Container>
			<nav className={navBarState.shownavbar ? [styles.nav_menu, styles.active].join(' ') : styles.nav_menu}>
				<ul className={styles.nav_menu_items}>
					<li className={styles.logo}>
						{/* <div className={styles.logosub}>
							<Image style={{ width: '80px', padding: '10px 0' }} src={Logo} alt="" roundedCircle />
						</div> */}
					</li>
					{sidebarData.map((item, index) => {
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
