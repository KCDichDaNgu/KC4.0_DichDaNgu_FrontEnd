import React from 'react';
// import LoginGoogle from './LoginGoogle';
import TextField from '@mui/material/TextField';
import { useTranslation } from 'react-i18next';
import { Controller, useForm } from 'react-hook-form';
import * as axiosHelper from '../../helpers/axiosHelper';
import { changeIsLogin } from '../../redux/actions/navbarAction';
import { getCurrentUser } from '../../redux/actions/userAction';
import { useDispatch } from 'react-redux';
import { ACCESS_TOKEN, REFRESH_TOKEN } from '../../constants/envVar';
import { useHistory } from 'react-router-dom';
import styles from './index.module.css';

function Login() {
	const { t } = useTranslation();
	const dispatch = useDispatch();
	const history = useHistory();
	const {
		control, handleSubmit, formState: { errors },
	} = useForm();

	const LoginNormal = async (values) => {
		try {
			const siginInResult = await axiosHelper.SignIn(values);
			dispatch(changeIsLogin(true));
			dispatch(getCurrentUser());
			localStorage.setItem(ACCESS_TOKEN, siginInResult.data.accessToken);
			localStorage.setItem(REFRESH_TOKEN, siginInResult.data.refreshToken);
			history.push('/translate');
		} catch (e) {
			// alert(e);
			// setVisible(false);
		}
	};

	// const LoginNormal = () => {
	// 	alert('Chưa thể đăng nhập');
	// };

	return (
		<div style={{ height: '93.8vh', backgroundColor: 'white', display: 'flex', alignItems: 'center' }}>
			<div className="container">
				{/* Outer Row */}
				<div className="row justify-content-center">
					<div className="col-xl-6 col-lg-6 col-md-9">
						<div className={styles.loginContainer}>
							<div className="card o-hidden border-1 my-5 align-self-center">
								<div className="card-body p-0">
									{/* Nested Row within Card Body */}
									<div className="row mr-0 ">
										{/* <div className="col-lg-6 d-none d-lg-block align-self-center " >
										<h1 className="ml-3">TekSpeech</h1>

										<h5 className="ml-3">Dịch âm thanh, văn bản Trung, Anh - Việt</h5>
									</div> */}

										<div className="col-lg-12 align-self-center">
											<div className="m-5">
												<div className="text-center mb-5">
													<h1 className="ml-3">TekSpeech</h1>

													<h5 className="ml-3">Dịch âm thanh, văn bản Trung, Anh - Việt</h5>
												</div>
												<form className="user" onSubmit={handleSubmit(LoginNormal)}>
													<div className="form-group">

														{/* <input type="email"   {...register('account', { required: true })} style={{ height: 50, borderRadius: 15 }} className="mb-4 form-control" id="exampleInputEmail" aria-describedby="emailHelp" placeholder="Enter Email Address..." /> */}
														<Controller
															control={control}
															rules={{
																required: true,
															}}
															render={({ field: { onChange, value } }) => (
																<TextField
																	error={errors.username}
																	helperText={errors.username ? 'Trường này là bắt buộc' : null}
																	value={value}
																	onChange={onChange}
																	fullWidth
																	id="outlined-basic"
																	label={t('username')}
																	variant="outlined"
																/>
															)}
															name="username"
															defaultValue=""
														/>
														{/* {errors.account && <span className="text-danger">Trường này là bắt buộc</span>} */}
													</div>
													<div className="form-group mb-4">
														{/* <input type="password"  {...register('password', { required: true })} style={{ height: 50, borderRadius: 15 }} className="mb-4 form-control" id="exampleInputPassword" placeholder="Password" /> */}
														<Controller
															control={control}
															rules={{
																required: true,
															}}
															render={({ field: { onChange, value } }) => (
																<TextField
																	error={errors.password}
																	helperText={errors.password ? 'Trường này là bắt buộc' : null}
																	value={value}
																	onChange={onChange}
																	fullWidth
																	type="password"
																	id="outlined-basic"
																	label={t('matKhau')}
																	variant="outlined"
																/>
															)}
															name="password"
															defaultValue=""
														/>
													</div>
													<button type="summit" style={{ backgroundColor: '#4E73DF', borderRadius: 10 }} className="btn btn-primary btn-block">

														<div style={{ color: 'white', alignSelf: 'center', fontWeight: '600', fontSize: '22px' }}>Đăng nhập</div>
													</button>
													{/* <hr /> */}
												</form>
												{/* <LoginGoogle />
											<hr />
											<div className="text-center">
												<a className="small" href="/forgot-password">Quên mật khẩu?</a>
											</div>
											<div className="text-center">
												<a className="small" href="/register">Có tài khoản? Đăng ký!</a>
											</div> */}
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>

					</div>
				</div>
			</div>
		</div>
	);
}

export default Login;

