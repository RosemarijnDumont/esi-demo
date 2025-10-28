import React from 'react';
import { Tabs } from 'antd';
import UserProfile from '../components/UserProfile'; // Assuming this component exists
import BillingInfo from '../components/BillingInfo'; // Assuming this component exists
import SSOSettings from '../components/SSO/SSOSettings';

const { TabPane } = Tabs;

const TrialAccountSettings = () => {
  return (
    <div style={{ padding: '20px' }}>
      <h1>Trial Account Settings</h1>
      <Tabs defaultActiveKey="sso">
        <TabPane tab="User Profile" key="profile">
          <UserProfile />
        </TabPane>
        <TabPane tab="Billing Info" key="billing">
          <BillingInfo />
        </TabPane>
        <TabPane tab="SSO Configuration" key="sso">
          <SSOSettings />
        </TabPane>
        {/* Add other settings tabs as needed */}
      </Tabs>
    </div>
  );
};

export default TrialAccountSettings;