/* eslint-disable import/no-unresolved */
import React from 'react';
import { Container, Row, Col, Tabs, Tab, Image } from 'react-bootstrap';
import './HistoryTranslate.css';
import styles from './historyStyle.module.css';
import DieuKhoan from '../../assets/images/dieukhoan.png';
import ChinhSach from '../../assets/images/chinhsach.png';

function index() {
	return (
		<Container fluid>
			<Row style={{ marginTop: '20px' }}>
				<Col md={{ span: 8, offset: 2 }} className={styles.content__history}>
					<Tabs defaultActiveKey="home" id="uncontrolled-tab-examples">
						<Tab eventKey="home" title="Điều khoản" tabClassName="Tab_style" >
							<div style={{ display: 'flex', justifyContent: 'center' }}>
								<Image style={{ border: 0 }} src={DieuKhoan} thumbnail />
							</div>
							<div style={{ display: 'flex', justifyContent: 'center', padding: 10 }}>
								<h3>NỘI DUNG ĐIỀU KHOẢN</h3>
							</div>
							<p style={{ fontWeight: 'bold' }}>
								Dù biết rằng bạn rất dễ bỏ qua những Điều khoản dịch vụ này, nhưng chúng tôi cần phải nêu rõ trách nhiệm của chúng tôi cũng như trách nhiệm của bạn trong quá trình bạn sử dụng các dịch vụ của UET Multilingual Neural Machine Translation.
							</p>
							<p>
								Các Điều khoản dịch vụ này phản ánh cách thức kinh doanh của UET Multilingual Neural Machine Translation, những điều luật mà công ty chúng tôi phải tuân theo và một số điều mà chúng tôi vẫn luôn tin là đúng. Do đó, các Điều khoản dịch vụ này giúp xác định mối quan hệ giữa Google với bạn khi bạn tương tác với các dịch vụ của chúng tôi. Ví dụ: Các điều khoản này trình bày các chủ đề sau:
							</p>
							<p>
								Trách nhiệm của chúng tôi: Đây là phần mô tả cách chúng tôi cung cấp và phát triển các dịch vụ của mình
							</p>
							<p>
								Trách nhiệm của bạn: Phần này nêu ra một số quy tắc mà bạn phải tuân theo khi sử dụng các dịch vụ của chúng tôi
							</p>
							<p>
								Nội dung trong các dịch vụ của UET Multilingual Neural Machine Translation: Phần này mô tả quyền sở hữu trí tuệ đối với nội dung mà bạn thấy trong các dịch vụ của chúng tôi, bất kể nội dung đó thuộc về bạn, UET Multilingual Neural Machine Translation hay người khác
								Trong trường hợp xảy ra vấn đề hoặc bất đồng: Phần này mô tả các quyền hợp pháp khác mà bạn có và những điều bạn nên biết trong trường hợp có người vi phạm các điều khoản này
								Việc hiểu rõ các điều khoản này là rất quan trọng vì bằng việc sử dụng các dịch vụ của chúng tôi, bạn đồng ý với các điều khoản này.
							</p>
							<p>
								Bên cạnh các điều khoản này, chúng tôi cũng ban hành Chính sách quyền riêng tư. Mặc dù không nằm trong các điều khoản này, nhưng đây là một chính sách bạn nên đọc để hiểu rõ hơn cách bạn có thể cập nhật, quản lý, xuất và xóa thông tin của mình.
							</p>
						</Tab>
						<Tab eventKey="profile" title="Chính sách" tabClassName="Tab_style">
							<div style={{ display: 'flex', justifyContent: 'center', padding: 10 }}>
								<Image style={{ border: 0 }} src={ChinhSach} thumbnail />
							</div>
							<div style={{ display: 'flex', justifyContent: 'center' }}>
								<h3>CHÍNH SÁCH BẢO MẬT CỦA UET Multilingual Neural Machine Translation</h3>
							</div>
							<p>
								Khi sử dụng dịch vụ của chúng tôi, bạn tin tưởng cung cấp thông tin của bạn cho chúng tôi. Chúng tôi hiểu rằng đây là một trách nhiệm lớn và chúng tôi nỗ lực bảo vệ thông tin của bạn cũng như để bạn nắm quyền kiểm soát.
							</p>
							<p>
								Chính sách bảo mật này nhằm mục đích giúp bạn hiểu rõ những thông tin chúng tôi thu thập, lý do chúng tôi thu thập và cách bạn có thể cập nhật, quản lý, xuất và xóa thông tin của mình.
							</p>
							<p style={{
								textAlign: 'center',
								fontSize: 20,
								color: '#34639E',
								marginBottom: 0
							}}>Contact UET-NLP Team</p>
							<p style={{
								textAlign: 'center',
								fontSize: 20,
								color: '#6E6E6E',
							}}>© 2019 UET Machine Translation Team</p>
						</Tab>
					</Tabs>
				</Col>
			</Row >
		</Container >
	);
}

export default index;

