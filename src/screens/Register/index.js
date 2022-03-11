import React from 'react';
import traslateImage from '../../assets/images/icondangonngu.png';
import { Image } from 'react-bootstrap';
import { useForm } from 'react-hook-form';

function Register() {
	const {
		register, handleSubmit, formState: { errors },
	} = useForm();
	const RegisterAccount = () => {
		alert('Chưa thể đăng ký tài khoản');
	};
	return (
		<div style={{ height: '93.8vh', backgroundColor: '#4e73df' }}>
			<div className="container">
				{/* Outer Row */}
				<div className="row justify-content-center">
					<div className="col-xl-10 col-lg-12 col-md-9">
						<div className="card o-hidden border-0 shadow-lg my-5">
							<div className="card-body p-0">
								{/* Nested Row within Card Body */}
								<div className="row m-0">
									<div className="col-lg-6 d-none d-lg-block pr-0 align-self-center" >
										<Image style={{ border: 0 }} src={traslateImage} thumbnail />
									</div>
									<div className="col-lg-6 align-self-center p-0">
										<div className="m-5">
											<div className="text-center">
												<h1 className="h4 text-gray-900 mb-4">Tạo tài khoản</h1>
											</div>
											<form className="user" onSubmit={handleSubmit(RegisterAccount)}>
												<div className="form-group">
													<input type="text" name='name' {...register('name', { required: true })} style={{ height: 50, borderRadius: 15 }} className="mb-4 form-control" id="exampleInputPassword" placeholder="Tên" />
													{errors.email && <span className="text-danger">Trường này là bắt buộc</span>}
												</div>
												<div className="form-group">
													<input type="email" name='email' {...register('email', { required: true })} style={{ height: 50, borderRadius: 15 }} className="mb-4 form-control" id="exampleInputEmail" aria-describedby="emailHelp" placeholder="Email" />
													{errors.email && <span className="text-danger">Trường này là bắt buộc</span>}
												</div>
												<div className="form-group">
													<input type="password" name='password' style={{ height: 50, borderRadius: 15 }} {...register('password', { required: true, minLength: 6, pattern: /^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{6,}$/ })} className="form-control" id="exampleInputPassword" placeholder="Mật khẩu" />
													{errors.password?.type === 'required' && <span className="text-danger">Không được để trống</span>}
													{errors.password?.type === 'minLength' && <span className="text-danger">Tối thiểu phải 6 ký tự</span>}
													{errors.password?.type === 'pattern' && <span className="text-danger">Mật khẩu chưa đủ phức tạp</span>}
												</div>
												<div className="form-group">
													<input type="password" name='rePassword' style={{ height: 50, borderRadius: 15 }} {...register('rePassword', { required: true, minLength: 6, pattern: /^(?:(?=.*[a-z])(?:(?=.*[A-Z])(?=.*[\d\W])|(?=.*\W)(?=.*\d))|(?=.*\W)(?=.*[A-Z])(?=.*\d)).{6,}$/ })} className="form-control" id="exampleInputPassword" placeholder="Xác nhận mật khẩu" />
													{errors.rePassword?.type === 'required' && <span className="text-danger">Không được để trống</span>}
													{errors.rePassword?.type === 'minLength' && <span className="text-danger">Tối thiểu phải 6 ký tự</span>}
													{errors.rePassword?.type === 'pattern' && <span className="text-danger">Mật khẩu chưa đủ phức tạp</span>}
												</div>
												<button type='submit' style={{ backgroundColor: '#4E73DF', borderRadius: 10 }} className="btn btn-primary btn-block">
													Đăng ký
												</button>
											</form>
											<hr />
											<div className="text-center">
												<a className="small" href="/forgot-password">Quên mật khẩu?</a>
											</div>
											<div className="text-center">
												<a className="small" href="/login">Có tài khoản? Đăng nhập!</a>
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

export default Register;

