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
											<Nav.Link eventKey="first">Hướng dẫn dùng phần mềm dịch trên Web</Nav.Link>
										</Nav.Item>
										<Nav.Item>
											<Nav.Link eventKey="second">Hướng dẫn dùng phần mềm dịch trên iOS</Nav.Link>
										</Nav.Item>
										<Nav.Item>
											<Nav.Link eventKey="three">Hướng dẫn dùng phần mềm dịch trên Android</Nav.Link>
										</Nav.Item>
									</Nav>
								</Col>
								<Col sm={9}>
									<Tab.Content>
										<Tab.Pane eventKey="first">
											<div>
												<h4>a. Đăng nhập</h4>
												Người dùng có thể đăng nhập vào phần mềm dịch bằng tài khoản gmail.
											
												<h4 style={{ marginTop: '1rem' }}>b. Dịch văn bản</h4>
												Người dùng nhập văn bản cần dịch
												Ấn nút “phát hiện và dịch”

												<h4 style={{ marginTop: '1rem' }}>c. Dịch tệp</h4>
												Người dùng ấn nút “Tài liệu”
												Lựa chọn tệp văn bản cần dịch
												Ấn nút “phát hiện và dịch”
											</div>
											{/* <p>
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
											</Tabs> */}
										</Tab.Pane>
										<Tab.Pane eventKey="second">
											<div>
												<h4>a. Cài đặt</h4>
												<div>Bước 1: Tải và cài đặt ứng dụng “UET Dịch đa ngôn ngữ” tại App-Store.</div>
												<div>Bước 2: Thiết lập UET Dịch đa ngôn ngữ.</div>
												Vào lần đầu tiên mở ứng dụng  dịch, bạn sẽ được yêu cầu chọn ngôn ngữ chính và ngôn ngữ bạn dịch thường xuyên nhất. Để chọn từ các ngôn ngữ có sẵn, hãy nhấn vào biểu tượng mũi tên xuống và chọn ngôn ngữ dịch hoặc chọn tự động nhận diện ngôn ngữ.

												<h4 style={{ marginTop: '1rem' }}>b. Dịch văn bản</h4>
												Nhập thông tin vào “Nhập nội dung văn bản” sau đó nhấn vào nút “Dịch”

												<h4 style={{ marginTop: '1rem' }}>c. Dịch tệp</h4>
												Nhấp vào ô “Chọn tài liệu" lựa chọn tài liệu cần dịch, sau đó nhấn vào nút Dịch
												Lưu ý: Hệ thống chỉ hỗ trợ dịch file dạng docx, ppt, excell, txt.

											</div>
										</Tab.Pane>
										<Tab.Pane eventKey="three">
											<div>
												<h4>a. Cài đặt</h4>
												<div>Bước 1: Tải và cài đặt ứng dụng “UET Dịch đa ngôn ngữ” tại CH-Play.</div>
												<div>Bước 2: Thiết lập UET Dịch đa ngôn ngữ.</div>
												Vào lần đầu tiên mở ứng dụng  dịch, bạn sẽ được yêu cầu chọn ngôn ngữ chính và ngôn ngữ bạn dịch thường xuyên nhất. Để chọn từ các ngôn ngữ có sẵn, hãy nhấn vào biểu tượng mũi tên xuống và chọn ngôn ngữ dịch hoặc chọn tự động nhận diện ngôn ngữ.
											
												<h4 style={{ marginTop: '1rem' }}>b. Dịch văn bản</h4>
												Nhập thông tin vào “Nhập nội dung văn bản” sau đó nhấn vào nút “Dịch”

												<h4 style={{ marginTop: '1rem' }}>c. Dịch tệp</h4>
												Nhấp vào ô “Chọn tài liệu" lựa chọn tài liệu cần dịch, sau đó nhấn vào nút Dịch
												Lưu ý: Hệ thống chỉ hỗ trợ dịch file dạng docx, ppt, excell, txt.

											</div>
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

