import React, { useState } from 'react';
import { Card, Col, Row, Typography } from 'antd';
import AvatarUpload from '../components/AvatarUpload';

const { Title, Text } = Typography;

const UserProfile = () => {
  const [avatarUrl, setAvatarUrl] = useState('https://zos.alipayobjects.com/rmsportal/ODTLcjxAfvqbxHnVXCYX.png'); // Default avatar

  const handleAvatarUploadSuccess = (newAvatarUrl) => {
    setAvatarUrl(newAvatarUrl);
  };

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Row gutter={16} align="middle">
          <Col span={6}>
            <AvatarUpload currentAvatar={avatarUrl} onUploadSuccess={handleAvatarUploadSuccess} />
          </Col>
          <Col span={18}>
            <Title level={3}>John Doe</Title>
            <Text>Email: john.doe@example.com</Text><br/>
            <Text>Member since: January 1, 2023</Text>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default UserProfile;
