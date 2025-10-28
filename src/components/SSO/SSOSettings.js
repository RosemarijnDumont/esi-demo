import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, Form, Input, Button, Alert, Spin, Upload, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const SSOSettings = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [messageApi, contextHolder] = message.useMessage();
  const [ssoConfig, setSsoConfig] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSSOSettings();
  }, []);

  const fetchSSOSettings = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('/api/sso/settings');
      if (response.data) {
        setSsoConfig(response.data);
        form.setFieldsValue(response.data);
      }
    } catch (err) {
      setError('Failed to fetch SSO settings.');
      messageApi.error('Failed to fetch SSO settings.');
    } finally {
      setLoading(false);
    }
  };

  const onFinish = async (values) => {
    setLoading(true);
    setError(null);
    try {
      await axios.post('/api/sso/settings', values);
      messageApi.success('SSO settings saved successfully!');
    } catch (err) {
      setError('Failed to save SSO settings.');
      messageApi.error('Failed to save SSO settings.');
    } finally {
      setLoading(false);
    }
  };

  const onFileChange = (info, fieldName) => {
    if (info.file.status === 'done') {
      messageApi.success(`${info.file.name} file uploaded successfully`);
      const reader = new FileReader();
      reader.onload = (e) => {
        form.setFieldsValue({
          [fieldName]: e.target.result
        });
      };
      reader.readAsText(info.file.originFileObj);
    } else if (info.file.status === 'error') {
      messageApi.error(`${info.file.name} file upload failed.`);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      {contextHolder}
      <Card title="SSO Configuration for Trial Accounts" style={{ maxWidth: '800px', margin: '0 auto' }}>
        {loading && <Spin tip="Loading..." />}
        {error && <Alert message="Error" description={error} type="error" showIcon />}
        <p>Configure your SAML Single Sign-On settings here. This will allow your trial users to authenticate via your Identity Provider (IdP).</p>
        <Form
          form={form}
          layout="vertical"
          onFinish={onFinish}
          initialValues={ssoConfig}
        >
          <Form.Item label="IdP Entity ID" name="idpEntityId" rules={[{ required: true, message: 'Please enter the IdP Entity ID!' }]}>
            <Input />
          </Form.Item>

          <Form.Item label="SSO URL" name="ssoUrl" rules={[{ required: true, message: 'Please enter the SSO URL!' }, { type: 'url', message: 'Please enter a valid URL!' }]}>
            <Input />
          </Form.Item>

          <Form.Item label="X.509 Certificate" name="x509Certificate" rules={[{ required: true, message: 'Please upload or paste the X.509 Certificate!' }]}>
            <Input.TextArea rows={6} placeholder="Paste your X.509 Certificate here" />
          </Form.Item>
          <Form.Item>
            <Upload
              showUploadList={false}
              beforeUpload={() => false} // Prevent automatic upload
              onChange={(info) => onFileChange(info, 'x509Certificate')}
            >
              <Button icon={<UploadOutlined />}>Upload Certificate File</Button>
            </Upload>
          </Form.Item>

          <Form.Item label="SAML Metadata XML (Optional)" name="samlMetadata">
            <Input.TextArea rows={6} placeholder="Paste your SAML Metadata XML here" />
          </Form.Item>
          <Form.Item>
            <Upload
              showUploadList={false}
              beforeUpload={() => false}
              onChange={(info) => onFileChange(info, 'samlMetadata')}
            >
              <Button icon={<UploadOutlined />}>Upload Metadata XML File</Button>
            </Upload>
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" loading={loading}>
              Save SSO Settings
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default SSOSettings;