import React, { useState } from 'react';
import { Card, Button, Avatar, Upload, message, Progress } from 'antd';
import { UploadOutlined, UserOutlined } from '@ant-design/icons';

const AvatarUpload = ({ currentAvatar, onUploadSuccess }) => {
  const [loading, setLoading] = useState(false);
  const [previewImage, setPreviewImage] = useState(null);
  const [progress, setProgress] = useState(0);

  const getBase64 = (img, callback) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => callback(reader.result));
    reader.readAsDataURL(img);
  };

  const beforeUpload = (file) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
      message.error('You can only upload JPG/PNG file!');
    }
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
      message.error('Image must smaller than 2MB!');
    }
    return isJpgOrPng && isLt2M;
  };

  const customRequest = ({ file, onSuccess, onError }) => {
    setLoading(true);
    setProgress(0);

    // Simulate upload progress
    let currentProgress = 0;
    const interval = setInterval(() => {
      currentProgress += 10;
      setProgress(currentProgress);
      if (currentProgress === 100) {
        clearInterval(interval);
        // Simulate API call
        setTimeout(() => {
          // In a real application, you would send 'file' to your backend here
          // and get the new avatar URL back.

          // For demonstration, let's just use the preview image as the new avatar
          getBase64(file, (imageUrl) => {
            onSuccess(null, file);
            onUploadSuccess(imageUrl); // Update parent component with new avatar
            setPreviewImage(null);
            message.success(`${file.name} file uploaded successfully.`);
            setLoading(false);
            setProgress(0);
          });
        }, 1000);
      }
    }, 100);

    // You would typically handle API errors here
    // if (error) onError(error);
  };

  const handleChange = (info) => {
    if (info.file.status === 'uploading') {
      setLoading(true);
      return;
    }
    if (info.file.status === 'done') {
      // Get this url from response in real world.
      getBase64(info.file.originFileObj, (imageUrl) => {
        setPreviewImage(imageUrl);
      });
    }
  };

  return (
    <Card title="Profile Avatar" style={{ width: 300 }}>
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Avatar
          size={128}
          icon={<UserOutlined />}
          src={currentAvatar || previewImage}
          style={{ marginBottom: 16 }}
        />
        <Upload
          name="avatar"
          listType="picture"
          className="avatar-uploader"
          showUploadList={false}
          beforeUpload={beforeUpload}
          customRequest={customRequest}
          onChange={handleChange}
        >
          <Button icon={<UploadOutlined />} loading={loading}>
            {loading ? 'Uploading' : 'Upload Avatar'}
          </Button>
        </Upload>
        {loading && <Progress percent={progress} style={{ marginTop: 16, width: '100%' }} />}
      </div>
    </Card>
  );
};

export default AvatarUpload;
