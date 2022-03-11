import React from 'react';
import traslateImage from '../../assets/images/icondangonngu.png';
import { Image } from 'react-bootstrap';
import { useForm } from 'react-hook-form';

function Forgot() {
	const {
		register, handleSubmit, formState: { errors },
	} = useForm();
	const ForgotAccount = () => {
		alert('Server chưa hỗ trợ');
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
									<div className="col-lg-6 d-none d-lg-block align-self-center" >
										<Image style={{ border: 0 }} src={traslateImage} thumbnail />
									</div>
									<div className="col-lg-6 align-self-center pt-4 pb-4">
										<div className="m-5">
											<div className="text-center">
												<h1 className="h4 text-gray-900 mb-4">Quên mật khẩu?</h1>
											</div>
											<form className="user" onSubmit={handleSubmit(ForgotAccount)}>
												<div className="form-group">
													<input type="email" name='email'  {...register('email', { required: true })} style={{ height: 50, borderRadius: 15 }} className="mb-4 form-control" id="exampleInputEmail" aria-describedby="emailHelp" placeholder="Email" />
													{errors.email && <span className="text-danger">Trường này là bắt buộc</span>}
												</div>
												<button type='submit' style={{ backgroundColor: '#4E73DF', borderRadius: 10 }} className="btn btn-primary btn-block">
													Gửi
												</button>
											</form>
											<hr />
											<div className="text-center">
												<a className="small" href="/register">Tạo tài khoản</a>
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

export default Forgot;

