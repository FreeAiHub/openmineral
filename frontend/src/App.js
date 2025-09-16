import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, Menu, theme } from 'antd';
import {
  DashboardOutlined,
  FileTextOutlined,
  BarChartOutlined,
  SafetyCertificateOutlined,
  WarningOutlined,
  PlayCircleOutlined
} from '@ant-design/icons';
import './App.css';

// Import page components
import Dashboard from './pages/Dashboard';
import Deals from './pages/Deals';
import Analytics from './pages/Analytics';
import Compliance from './pages/Compliance';
import Risk from './pages/Risk';
import Workflows from './pages/Workflows';

const { Header, Content, Footer, Sider } = Layout;

function App() {
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider
          breakpoint="lg"
          collapsedWidth="0"
          onBreakpoint={(broken) => {
            console.log(broken);
          }}
          onCollapse={(collapsed, type) => {
            console.log(collapsed, type);
          }}
        >
          <div className="demo-logo-vertical" />
          <Menu
            theme="dark"
            mode="inline"
            defaultSelectedKeys={['1']}
            items={[
              {
                key: '1',
                icon: <DashboardOutlined />,
                label: 'Dashboard',
              },
              {
                key: '2',
                icon: <FileTextOutlined />,
                label: 'Deals',
              },
              {
                key: '3',
                icon: <BarChartOutlined />,
                label: 'Analytics',
              },
              {
                key: '4',
                icon: <SafetyCertificateOutlined />,
                label: 'Compliance',
              },
              {
                key: '5',
                icon: <WarningOutlined />,
                label: 'Risk Assessment',
              },
              {
                key: '6',
                icon: <PlayCircleOutlined />,
                label: 'Workflows',
              },
            ]}
          />
        </Sider>
        <Layout>
          <Header style={{ padding: 0, background: colorBgContainer }} />
          <Content style={{ margin: '24px 16px 0' }}>
            <div style={{ padding: 24, minHeight: 360, background: colorBgContainer }}>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/deals" element={<Deals />} />
                <Route path="/analytics" element={<Analytics />} />
                <Route path="/compliance" element={<Compliance />} />
                <Route path="/risk" element={<Risk />} />
                <Route path="/workflows" element={<Workflows />} />
              </Routes>
            </div>
          </Content>
          <Footer style={{ textAlign: 'center' }}>
            OpenMineralHub Trading Platform ©2025
          </Footer>
        </Layout>
      </Layout>
    </Router>
  );
}

export default App;
