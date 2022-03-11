/* eslint-disable react/prop-types */
import React from 'react';
import { Button, Modal } from 'react-bootstrap';

function ModalFeedBack(props) {
	return (
		<Modal
			{...props}
			size="md"
			aria-labelledby="contained-modal-title-vcenter"
			centered
		>
			<Modal.Header style={{ backgroundColor: '#34639E' }}>
				<Modal.Title style={{ color: '#fff' }} id="contained-modal-title-vcenter">
                    Đăng nhập để xem lịch sử và từ vựng
				</Modal.Title>
			</Modal.Header>
			<Modal.Body>
				<div>
                    Quản lý lịch sử và quản lý từ vựng liên kết với tài khoản của bạn
				</div>
			</Modal.Body>
			<Modal.Footer>
				<a href='/login' variant="primary">Đăng nhập</a>
				<Button variant="light" onClick={props.onHide}>Hủy</Button>
			</Modal.Footer>
		</Modal>
	);
}

export default ModalFeedBack;
