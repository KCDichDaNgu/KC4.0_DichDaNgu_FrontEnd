/* eslint-disable react/no-unescaped-entities */
import React from 'react';
import { Container, Row, Col, Nav, Tab, Tabs } from 'react-bootstrap';
import './HelpStyle.module.css';

function index() {
	return (
		<div>
			<div className="d-flex justify-content-center p-4">
				<h3>Chúng tôi có thể giúp gì cho bạn?</h3>
			</div>
			<Container fluid>
				<Row>
					<Col md={{ span: 10, offset: 1 }}>
						<Tab.Container id="left-tabs-example" defaultActiveKey="first">
							<Row>
								<Col sm={3}>
									<Nav variant="pills" className="flex-column">
										<Nav.Item>
											<Nav.Link eventKey="first">Bắt đầu với App Dịch</Nav.Link>
										</Nav.Item>
										<Nav.Item>
											<Nav.Link eventKey="second">Dịch văn bản, hình ảnh, chữ viết tay hoặc lời nói</Nav.Link>
										</Nav.Item>
										<Nav.Item>
											<Nav.Link eventKey="three">Sử dụng lịch sử và từ vựng của bạn</Nav.Link>
										</Nav.Item>
										<Nav.Item>
											<Nav.Link eventKey="four">Thông báo</Nav.Link>
										</Nav.Item>
									</Nav>
								</Col>
								<Col sm={9}>
									<Tab.Content>
										<Tab.Pane eventKey="first">
											<p>
												Tải xuống và sử dụng app Dịch
											</p>
											<p>
												Bạn có thể dịch văn bản, chữ viết tay, ảnh và lời nói trong các  ngôn ngữ bằng ứng dụng Dịch. Bạn cũng có thể sử dụng app dịch này trên web.
											</p>
											<Tabs
												defaultActiveKey="pc"
												transition={false}
												id="noanim-tab-example"
												className="mb-3"
											>
												<Tab eventKey="pc" title="PC">
													Để dịch văn bản, lời nói và trang web, hãy truy cập vào trang UET Multilingual Neural Machine Translation.
												</Tab>
												<Tab eventKey="android" title="Android">
													<p>
														Bước 1: Tải ứng dụng  Neural Machine Dịch xuống
														Để bắt đầu, hãy tải ứng dụng  Neural Machine Dịch dành cho Android xuống.
													</p>
													<p>
														Lưu ý: Để dịch hình ảnh bằng máy ảnh của bạn trong tất cả các ngôn ngữ được hỗ trợ, thiết bị của bạn phải có máy ảnh tự động lấy nét và CPU lõi kép với ARMv7. Để biết chi tiết kỹ thuật, hãy xem hướng dẫn của nhà sản xuất thiết bị.
													</p>
													<p>
														Bước 2: Thiết lập  Neural Machine Dịch
														Mẹo: Trong phiên bản 6.10 trở lên, bạn có thể sử dụng Giao diện tối trong ứng dụng Dịch.
													</p>
													<p>
														Vào lần đầu tiên mở  Neural Machine Dịch, bạn sẽ được yêu cầu chọn ngôn ngữ chính và ngôn ngữ bạn dịch thường xuyên nhất. Để chọn từ các ngôn ngữ có sẵn, hãy nhấn vào biểu tượng Mũi tên xuống Mũi tên xuống.
													</p>
													<p>
														Để tải xuống cả hai ngôn ngữ để sử dụng ngoại tuyến, hãy chọn "Dịch ngoại tuyến". Nếu một trong hai ngôn ngữ không có sẵn để tải xuống thì sẽ có thông báo "Không có sẵn ngoại tuyến".
													</p>
													<p>
														Lưu ý: Để tải một ngôn ngữ xuống, theo mặc định, bạn phải kết nối với mạng Wi-Fi.
													</p>
												</Tab>
												<Tab eventKey="ios" title="IOS">
													IOS
												</Tab>
											</Tabs>
										</Tab.Pane>
										<Tab.Pane eventKey="second">
											Dịch văn bản, hình ảnh, chữ viết tay hoặc lời nói
										</Tab.Pane>
										<Tab.Pane eventKey="three">
											Sử dụng lịch sử và từ vựng của bạn
										</Tab.Pane>
										<Tab.Pane eventKey="four">
											Thông báo
										</Tab.Pane>
									</Tab.Content>
								</Col>
							</Row>
						</Tab.Container>
					</Col>
				</Row >
			</Container >
		</div >
	);
}

export default index;

