import React, { useEffect } from 'react';
import {
    Input,
    Button,
    message,
    Card,
    Row,
    Col,
    Form,
} from 'antd';

import * as axiosHelper from '../../helpers/axiosHelper';

import { useTranslation } from 'react-i18next';

import { STATUS_CODE } from '../../constants/common';

import { useForm } from 'antd/lib/form/Form';

import styles from './systemSettingStyle.module.css';

const SettingPage = () => {
    
    const { t } = useTranslation();

    const [form] = useForm();
    
    const updateFormRules = {
        content: {
            taskExpiredDuration: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
            translationApiUrl: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
            translationApiAllowedConcurrentReq: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
            languageDetectionApiUrl: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
            languageDetectionApiAllowedConcurrentReq: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
            translationSpeedForEachSentence: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
            languageDetectionSpeed: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
            emailForSendingEmail: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
            emailPasswordForSendingEmail: [
                {
                    required: true,
                    message: t('requiredField'),
                },
            ],
        }
    };

    useEffect(() => {
        getSetting();
    }, []);

    const getSetting = async () => {
        let result = await axiosHelper.getSystemSetting();

        if (result.code == STATUS_CODE.success) {
            form.setFieldsValue(result.data);
        }
    };

    const updateSetting = async (updatedData) => {

        let result = await axiosHelper.updateSystemSetting(updatedData);

        if (result.code == STATUS_CODE.success) {
            message.success(t('updateSuccess'));

            getSetting();
        }
    };
    
    return (
        <React.Fragment>
            <div className={styles.outerContainer}>
				<div className={styles.outerTab} >
                    <Card className='user-table-card'>

                        <Form 
                            form={ form }
                            onFinish={ updateSetting }>

                            <Row gutter={{ xs: 0, sm: 0, md: 24, lg: 32 }}>

                                <Col xs={ 24 } md={ 24 }>

                                    <label>{ t('SystemSetting.taskExpiredDuration') }</label>

                                    <Form.Item 
                                        name={ ['taskExpiredDuration'] }
                                        rules={ updateFormRules.taskExpiredDuration }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col>

                                {/* <Col xs={ 24 } md={ 12 }>

                                    <label>{ t('SystemSetting.translationApiUrl') }</label>

                                    <Form.Item 
                                        name={ ['translationApiUrl'] }
                                        rules={ updateFormRules.translationApiUrl }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col> */}

                                <Col xs={ 24 } md={ 12 }>

                                    <label>{ t('SystemSetting.translationApiAllowedConcurrentReq') }</label>

                                    <Form.Item 
                                        name={ ['translationApiAllowedConcurrentReq'] }
                                        rules={ updateFormRules.translationApiAllowedConcurrentReq }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col>

                                {/* <Col xs={ 24 } md={ 12 }>

                                    <label>{ t('SystemSetting.languageDetectionApiUrl') }</label>

                                    <Form.Item 
                                        name={ ['languageDetectionApiUrl'] }
                                        rules={ updateFormRules.languageDetectionApiUrl }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col> */}

                                <Col xs={ 24 } md={ 12 }>

                                    <label>{ t('SystemSetting.languageDetectionApiAllowedConcurrentReq') }</label>

                                    <Form.Item 
                                        name={ ['languageDetectionApiAllowedConcurrentReq'] }
                                        rules={ updateFormRules.languageDetectionApiAllowedConcurrentReq }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col>

                                <Col xs={ 24 } md={ 12 }>

                                    <label>{ t('SystemSetting.translationSpeedForEachSentence') }</label>

                                    <Form.Item 
                                        name={ ['translationSpeedForEachSentence'] }
                                        rules={ updateFormRules.translationSpeedForEachSentence }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col>

                                <Col xs={ 24 } md={ 12 }>

                                    <label>{ t('SystemSetting.languageDetectionSpeed') }</label>

                                    <Form.Item 
                                        name={ ['languageDetectionSpeed'] }
                                        rules={ updateFormRules.languageDetectionSpeed }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col>

                                <Col xs={ 24 } md={ 12 }>

                                    <label>{ t('SystemSetting.emailForSendingEmail') }</label>

                                    <Form.Item 
                                        name={ ['emailForSendingEmail'] }
                                        rules={ updateFormRules.emailForSendingEmail }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col>

                                <Col xs={ 24 } md={ 12 }>

                                    <label>{ t('SystemSetting.emailPasswordForSendingEmail') }</label>

                                    <Form.Item 
                                        name={ ['emailPasswordForSendingEmail'] }
                                        rules={ updateFormRules.emailPasswordForSendingEmail }>
                                        <Input className='user-input' /> 
                                    </Form.Item>
                                </Col>
                            </Row>

                            <Button 
                                type="primary" 
                                htmlType="submit">
                                { t('update') }
                            </Button>
                        </Form>
                    </Card>
                </div>
            </div>
        </React.Fragment>
    );
};

export default SettingPage;
