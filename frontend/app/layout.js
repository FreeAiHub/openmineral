'use client';

import React from 'react';
import { ConfigProvider } from 'antd';
import { Layout, Menu, theme } from 'antd';
import { DashboardOutlined, FileTextOutlined, BarChartOutlined, SafetyCertificateOutlined, WarningOutlined, PlayCircleOutlined } from '@ant-design/icons';
import './globals.css';

const { Header, Content, Footer, Sider } = Layout;

export default function RootLayout({ children }) {
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const items = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/deals',
      icon: <FileTextOutlined />,
      label: 'Deals',
    },
    {
      key: '/analytics',
      icon: <BarChartOutlined />,
      label: 'Analytics',
    },
    {
      key: '/compliance',
      icon: <SafetyCertificateOutlined />,
      label: 'Compliance',
    },
    {
      key: '/risk',
      icon: <WarningOutlined />,
      label: 'Risk Assessment',
    },
    {
      key: '/workflows',
      icon: <PlayCircleOutlined />,
      label: 'Workflows',
    },
  ];

  return (
    <html lang="en">
      <body>
        <ConfigProvider>
          <Layout style={{ minHeight: '100vh' }}>
            <Sider>
              <div className="demo-logo-vertical" />
              <Menu
                theme="dark"
                mode="inline"
                defaultSelectedKeys={['/dashboard']}
                items={items}
              />
            </Sider>
            <Layout>
              <Header style={{ padding: 0, background: colorBgContainer }} />
              <Content style={{ margin: '24px 16px 0' }}>
                <div style={{ padding: 24, minHeight: 360, background: colorBgContainer }}>
                  {children}
                </div>
              </Content>
              <Footer style={{ textAlign: 'center' }}>
                OpenMineralHub Trading Platform ©2025
              </Footer>
            </Layout>
          </Layout>
        </ConfigProvider>
      </body>
    </html>
  );
}
