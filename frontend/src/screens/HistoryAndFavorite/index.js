import React, { useEffect } from 'react';
import styles from './historyAndFavorite.module.css';
import { 
	Tab, 
	Tabs, 
	Typography, 
	LinearProgress,
	Divider,
} from '@mui/material';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { useTranslation } from 'react-i18next';
import ResultComponent from './components/ResultComponent';
import { STATE } from '../../redux/reducers/historyReducer';
import { getHistoryAsync } from '../../redux/actions/historyAction';
import { isEmpty } from 'lodash';
import TranslationItem from './components/TranslationItem';
import Pagination from '@mui/material/Pagination';

const PER_PAGE = 9;
const STATUS = 'translated';
const TRANSLATIONTYPE = 'public_plain_text_translation';

function HistoryAndFavorite(props) {
	const { historyState, navbarState } = props;
	const { t } = useTranslation();

	/**
	 * @description useEffect cho việc check kết quả và báo noti cho 
	 * người dùng
	 */
		 useEffect(() => {
		switch (historyState.currentState) {
		case STATE.SUCCESS:
			break;
		case STATE.FAILURE:
			alert(`${historyState.err}`);
			break;
		default:
			break;
		}
	}, [historyState.currentState]);

	/**
	 * @description useEffect cho việc gọi danh sách lúc đầu vào trang
	 */
	useEffect(() => {
		props.getHistoryAsync({
			status: STATUS,
			translationType: TRANSLATIONTYPE,
			perPage: PER_PAGE,
			page: 1,
		});
	}, [navbarState.isLogin]);

	/**
	 * @description Hàm gọi danh sách khi thay đổi trang
	 */
	const handleChange = (event, value) => {
		props.getHistoryAsync({
			status: STATUS,
			translationType: TRANSLATIONTYPE,
			perPage: PER_PAGE,
			page: value,
		});
	};

	/**
	 * @description Trả về element chữ cho trường hợp danh sách rỗng
	 */
	const TextListEmpty = () => {
		return  <Typography sx={{p: 2}} align="center" variant="subtitle1">{t('danhSachTrong')}</Typography>;
	};

	/**
	 * @description Tính toán số trang hiện thị ở pagnination
	 * VD: total: 100 và perPage: 9, => getCount() trả về 12 
	 * ? Kết quả thực tế là 11.111 => Làm tròn lên thành 12.
	 */
	const getCount = (total) => {
		return Math.ceil(total/9);
	};

	return (
		<div style={{ display: 'flex', flex: 1, backgroundColor: 'white', height:'94vh' }}>
			<div className={styles.innerBox}>
				<div className={styles.tabBox}>
					<Tabs
						value="history"
						variant="scrollable"
						scrollButtons="auto"
					>
						<Tab label={t('History.lichsu')} value={'history'} style={{fontWeight: 'bold'}}/>
					</Tabs>
				</div>
				<div className={styles.innerBody}>
					<div className={styles.innerBodyLeft}>
						{/* <div className={styles.innerSearchBox}>
							<InputBase
								sx={{ ml: 1, flex: 1 }}
								placeholder="Tìm kiếm"
								inputProps={{ 'aria-label': 'Tìm kiếm' }}
							/>
							<IconButton type="submit" sx={{ p: '10px' }} aria-label="search">
								<SearchIcon />
							</IconButton>
						</div> */}
						{historyState.currentState === STATE.LOADING ? <LinearProgress /> : null}
						<div className="form-select" style={{flex: 1, overflow: 'auto'}} id='list'>
							{isEmpty(historyState.listHistory) ?  
								<TextListEmpty /> 
								: props.historyState.listHistory.map((item) => <TranslationItem key={item.id} item={item} id={item.taskId}/>)
							}
						</div>
						<Divider />
						<Pagination
							sx={{display: 'flex', marginTop: 1, marginBottom: 1, justifyContent: 'center'}}
							size="large"
							onChange={handleChange}
							count={getCount(props.historyState.total)}
						/>
					</div>
					<ResultComponent />
				</div>
			</div>
			{/* <FeedBack
				show={modelShown}
				onHide={() => setModelShown(false)} 
			/> */}
		</div>
	);
}

HistoryAndFavorite.propTypes = {
	historyState: PropTypes.object,
	navbarState: PropTypes.object,
	getHistoryAsync: PropTypes.func,
};

const mapStateToProps = (state) => ({
	historyState: state.historyReducer,
	navbarState: state.navbarReducer,
});

const mapDispatchToProps = { 
	getHistoryAsync
};

export default connect(mapStateToProps, mapDispatchToProps)(HistoryAndFavorite);