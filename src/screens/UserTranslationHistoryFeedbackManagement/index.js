/* eslint-disable no-unused-vars */
import React, { useEffect, useState } from 'react';
import { getUserListAsync } from '../../redux/actions/userAction';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { Table, Button, Radio, Row, Col, Card } from 'antd';
import EditIcon from '@mui/icons-material/Edit';
import { useTranslation } from 'react-i18next';
import { STATUS_CODE, USER_STATUS, LANG_CODE } from '../../constants/common';
import * as axiosHelper from '../../helpers/axiosHelper';
import { toast } from 'react-toastify';
import authHoc from '../../hocs/authHoc';
import { TRANSLATION_HISTORY_RATING, TRANSLATION_HISTORY_STATUS } from '../../constants/common';

import 'moment/locale/vi';
import locale from 'antd/es/date-picker/locale/vi_VN';

import {
    Form,
    Input,
    Select,
    DatePicker,
    Space
} from 'antd';

import { ArrowRightOutlined } from '@ant-design/icons';


function UserTranslationHistoryFeedbackManagement(props) {
    
	const { t } = useTranslation();
    const [currentUser, setCurrentUser] = useState(
        JSON.parse(localStorage.getItem('user'))
    )
    const [dataSource, setDataSource] = useState({
        list: [],
        total_entries: 0,
        page: 0,
        per_page: 0
    })

    const [filter, setFilter] = useState({
        pagination__page: 1,
        score__from: 0,
        score__to: 0,
        status: Object.keys(TRANSLATION_HISTORY_STATUS),
        rating: ['good', 'bad', 'not_rated'],
        source_lang: Object.keys(LANG_CODE),
        target_lang: Object.keys(LANG_CODE),
        userUpdatedAt__from: null,
        userUpdatedAt__to: null,
        createdAt__from: null,
        createdAt__to: null,
        sort__field: null,
        sort__direction: 1 
    })

    const searchUserTranslationHistoryFeedback = async () => {
		let result = await axiosHelper.getUserTranslationHistoryFeedbackList(filter)

        setDataSource(result.data)
	}

	useEffect(() => {

        const getFeedbackList = async () => {
            if (isAdmin(currentUser)) {
                await searchUserTranslationHistoryFeedback()
            }
        }

		getFeedbackList()

	}, [filter]);

	const isAdmin = (user) => {
		return user?.role === 'admin' && user?.status === USER_STATUS.active;
	};

    const renderStatus = (status, record) => {
		return t(`translationHistory.status.${status}`);
	};

	const renderTranslationType = (translationType, record) => {
		return t(`translationHistory.translationType.${translationType}`);
	};

    const handleFilterChange = (searchData, key) => {
        
        if (key === 'text') {
            setFilter({
                ...filter,
                text1: searchData,
                text2: searchData,
                pagination__page: 1
            })
        } else if (key === 'createdAt') {
            
            let fromDate = searchData == null ? null : searchData[0].valueOf();
            let toDate = searchData == null ? null : searchData[1].valueOf();

            if (fromDate) {
                fromDate = new Date(fromDate);
                fromDate.setHours(0,0,0,0);
                fromDate = fromDate.getTime();
            }
            
            if (toDate) {
                toDate = new Date(toDate);
                toDate.setHours(0,0,0,0);
                toDate = toDate.getTime();
            }

            setFilter({
                ...filter,
                createdAt__from: fromDate,
                createdAt__to: toDate,
                pagination__page: 1
            })

        } else if (key === 'userUpdatedAt') {
            
            let fromDate = searchData == null ? null : searchData[0].valueOf();
            let toDate = searchData == null ? null : searchData[1].valueOf();

            if (fromDate) {
                fromDate = new Date(fromDate);
                fromDate.setHours(0,0,0,0);
                fromDate = fromDate.getTime();
            }
            
            if (toDate) {
                toDate = new Date(toDate);
                toDate.setHours(0,0,0,0);
                toDate = toDate.getTime();
            }

            setFilter({
                ...filter,
                userUpdatedAt__from: fromDate,
                userUpdatedAt__to: toDate,
                pagination__page: 1
            })

        } else {
            setFilter({
                ...filter,
                [key]: searchData,
                pagination__page: 1
            })
        }
    };

    const renderRating = (rating, record) => {
        if (rating) return t(`translationHistory.rating.${rating}`);
        else return t('translationHistory.rating.not_rated')
    }

    const convertSortDirection = (direction) => {

        return {
            'ascend': 1,
            'descend': -1,
            '1': 'ascend',
            '-1': 'descend'
        }[direction]
    }

	const columns = [
		{
			title: t('username'),
			dataIndex: 'username',
			key: 'username',
		},
		{
			title: t('translationType'),
			dataIndex: 'translationType',
			key: 'translationType',
            render: (translationType, record) => {
				return renderTranslationType(translationType, record);
			}
		},
		{
			title: t('status'),
			align: 'center',
			dataIndex: 'status',
			key: 'status',
			render: (currentStatus, record) => {
				return renderStatus(currentStatus, record);
			}
		},
        {
			title: t('rating'),
			align: 'center',
			dataIndex: 'rating',
			key: 'rating',
			render: (rating, record) => {
				return renderRating(rating, record);
			}
		},
        {
			title: t('sourceLang'),
            align: 'center',
			dataIndex: 'sourceLang',
			key: 'source_lang',
            render: (lang_code, record) => {
				return t(lang_code);
			}
		},
        {
			title: t('sourceText'),
			dataIndex: 'sourceText',
			key: 'sourceText',
		},
        {
			title: t('targetLang'),
            align: 'center',
			dataIndex: 'targetLang',
			key: 'target_lang',
            render: (lang_code, record) => {
				return t(lang_code);
			}
		},
        {
			title: t('translatedText'),
			dataIndex: 'translatedText',
			key: 'translatedText',
		},
		{
			title: t('userEditedTranslation'),
			dataIndex: 'userEditedTranslation',
			key: 'userEditedTranslation',
		},
        {
			title: t('userUpdatedAt'),
			dataIndex: 'userUpdatedAt',
			key: 'user_updated_at',
            // sorter: (a, b) => true,
            // sortOrder: filter.sort__field === 'userUpdatedAt' ? convertSortDirection(filter.sort__direction) : null,
		},
        {
			title: t('createdAt'),
			dataIndex: 'createdAt',
			key: 'created_at',
            // sorter: (a, b) => true,
            // sortOrder: filter.sort__field === 'createdAt' ? convertSortDirection(filter.sort__direction) : null,
		},
	];

    const onTableChange = async (pagination, filters, sorter) => {

        let params = {
            ...filter,
            // sort__field: sorter['columnKey'],
            // sort__direction: convertSortDirection(sorter['order']),
            pagination__page: pagination['current']
        }
        
        setFilter(params)
    }
 

	if (!isAdmin(JSON.parse(localStorage.getItem('user')))) return <div>No authorized</div>;

    const ratingOptions = [...Object.keys(TRANSLATION_HISTORY_RATING), 'not_rated']

	return (
		<div style={{
            padding: '50px 200px'
        }}>

            <Space direction="vertical" size="middle" style={{ display: 'flex' }}>
                <Card title={ t('filter') }>
                    <Row gutter={{ xs: 8, sm: 16, md: 24, lg: 32 }}>

                        <Col style={{ marginTop: '1rem' }} xs={ 24 } md={ 8 }>

                            <div style={{ 
                                marginBottom: '10px',
                                fontSize: '20px',
                                fontWeight: 500
                            }}>
                                { t('rating') }
                            </div>

                            <Select
                                mode="multiple"
                                allowClear
                                style={{ width: '100%' }}
                                defaultValue={ ratingOptions }
                                onChange={ date => handleFilterChange(date, 'rating') }>
                                {
                                    ratingOptions.map((r) => {
                                        return <Select.Option key={ r }>{ t(`translationHistory.rating.${r}`) }</Select.Option>
                                    })
                                }
                            </Select>
                        </Col>

                        <Col style={{ marginTop: '1rem' }} xs={ 24 } md={ 8 }>

                            <div style={{ 
                                marginBottom: '10px',
                                fontSize: '20px',
                                fontWeight: 500
                            }}>
                                { t('sourceLang') }
                            </div>

                            <Select
                                mode="multiple"
                                allowClear
                                style={{ width: '100%' }}
                                defaultValue={ Object.keys(LANG_CODE) }
                                onChange={ value => handleFilterChange(value, 'source_lang') }>
                                {
                                    Object.keys(LANG_CODE).map((lc) => {
                                        return <Select.Option key={ lc }>{ t(lc) }</Select.Option>
                                    })
                                }
                            </Select>
                        </Col>

                        <Col style={{ marginTop: '1rem' }} xs={ 24 } md={ 8 }>

                            <div style={{ 
                                marginBottom: '10px',
                                fontSize: '20px',
                                fontWeight: 500
                            }}>
                                { t('targetLang') }
                            </div>

                            <Select
                                mode="multiple"
                                allowClear
                                style={{ width: '100%' }}
                                defaultValue={ Object.keys(LANG_CODE) }
                                onChange={ date => handleFilterChange(date, 'target_lang') }>
                                {
                                    Object.keys(LANG_CODE).map((lc) => {
                                        return <Select.Option key={ lc }>{ t(lc) }</Select.Option>
                                    })
                                }
                            </Select>
                        </Col>

                        <Col style={{ marginTop: '1rem' }} xs={ 24 } md={ 8 }>

                            <div style={{ 
                                marginBottom: '10px',
                                fontSize: '20px',
                                fontWeight: 500
                            }}>
                                { t('status') }
                            </div>

                            <Select
                                mode="multiple"
                                allowClear
                                style={{ width: '100%' }}
                                defaultValue={Object.keys(TRANSLATION_HISTORY_STATUS)}
                                onChange={ date => handleFilterChange(date, 'status') }>
                                {
                                    Object.keys(TRANSLATION_HISTORY_STATUS).map((r) => {
                                        return <Select.Option key={ r }>{ t(`translationHistory.status.${r}`) }</Select.Option>
                                    })
                                }
                            </Select>
                        </Col>

                        <Col style={{ marginTop: '1rem' }} xs={ 24 } md={ 8 }>

                            <div style={{ 
                                marginBottom: '10px',
                                fontSize: '20px',
                                fontWeight: 500
                            }}>
                                { t('createdAt') }
                            </div>

                            <DatePicker.RangePicker 
                                style={{ width: '100%' }}
                                locale={ locale }
                                allowClear={ true }
                                onChange={ date => handleFilterChange(date, 'createdAt') }
                                separator={<ArrowRightOutlined style={{display: "flex", color: "#bfbfbf"}}/>}
                            />
                        </Col>

                        <Col style={{ marginTop: '1rem' }} xs={ 24 } md={ 8 }>

                            <div style={{ 
                                marginBottom: '10px',
                                fontSize: '20px',
                                fontWeight: 500
                            }}>
                                { t('userUpdatedAt') }
                            </div>

                            <DatePicker.RangePicker 
                                style={{ width: '100%' }}
                                locale={ locale }
                                allowClear={ true }
                                onChange={ date => handleFilterChange(date, 'userUpdatedAt') }
                                separator={<ArrowRightOutlined style={{display: "flex", color: "#bfbfbf"}}/>}
                            />
                        </Col>
                    </Row>
                </Card>
                
                <Card>
                    <Table
                        className='table-striped-rows'
                        dataSource={dataSource.list.map(d => ({ ...d, key: d.id }))}
                        columns={columns}
                        onChange={onTableChange}
                        pagination={{
                            pageSize: dataSource.per_page,
                            total: dataSource.total_entries,
                            current: dataSource.page
                        }}
                        footer={() => (
                            <div style={{display: "flex", justifyContent: "end"}}>
                                <div style={{lineHeight: "32px"}}>
                                    {`${t('total')} ${dataSource['total_entries']} ${t('records').toLowerCase()}`}
                                </div>
                            </div>
                        )}
                    >
                    </Table>
                </Card>
            </Space>
		</div>
	);
}

UserTranslationHistoryFeedbackManagement.propTypes = {
	navbarState: PropTypes.object,
};

const mapStateToProps = (state) => ({
	navbarState: state.navbarReducer,
});

const mapDispatchToProps = {
	getUserListAsync
};

export default connect(mapStateToProps, mapDispatchToProps)(authHoc(UserTranslationHistoryFeedbackManagement));
