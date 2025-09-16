import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Layout, Menu, theme, message } from 'antd';
import {
  DashboardOutlined,
  FileTextOutlined,
  BarChartOutlined,
  LogoutOutlined,
  UserOutlined
} from '@ant-design/icons';
import './App.css';

// Import pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Deals from './pages/Deals';
import Market from './pages/Market';

// API service
import apiService from './services/api';

const { Header, Content, Footer, Sider } = Layout;

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [collapsed, setCollapsed] = useState(false);

  const {
    token: { colorBgContainer },
  } = theme.useToken();

  // Check if user is logged in on app load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      apiService.setAuthToken(token);
      // Verify token by fetching user info
      apiService.getCurrentUser()
        .then(userData => {
          setUser(userData);
        })
        .catch(() => {
          // Invalid token
          localStorage.removeItem('token');
          apiService.setAuthToken(null);
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  const handleLogin = async (username, password) => {
    try {
      const response = await apiService.login(username, password);
      const { access_token } = response;
      
      // Store token and set in API service
      localStorage.setItem('token', access_token);
      apiService.setAuthToken(access_token);
      
      // Get user info
      const userData = await apiService.getCurrentUser();
      setUser(userData);
      
      message.success('Login successful!');
      return true;
    } catch (error) {
      message.error('Login failed: ' + (error.response?.data?.detail || 'Unknown error'));
      return false;
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    apiService.setAuthToken(null);
    setUser(null);
    message.success('Logged out successfully');
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        height: '100vh' 
      }}>
        Loading...
      </div>
    );
  }

  if (!user) {
    return <Login onLogin={handleLogin} />;
  }

  const menuItems = [
    {
      key: '1',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
      path: '/dashboard'
    },
    {
      key: '2',
      icon: <FileTextOutlined />,
      label: 'Deals',
      path: '/deals'
    },
    {
      key: '3',
      icon: <BarChartOutlined />,
      label: 'Market',
      path: '/market'
    }
  ];

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider
          collapsible
          collapsed={collapsed}
          onCollapse={(value) => setCollapsed(value)}
          breakpoint="lg"
          collapsedWidth="0"
        >
          <div className="demo-logo-vertical" style={{
            height: '64px',
            margin: '16px',
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'white',
            fontWeight: 'bold'
          }}>
            {collapsed ? 'OM' : 'OpenMineral'}
          </div>
          
          <Menu
            theme="dark"
            defaultSelectedKeys={['1']}
            mode="inline"
            items={menuItems.map(item => ({
              key: item.key,
              icon: item.icon,
              label: item.label,
              onClick: () => window.location.hash = item.path
            }))}
          />
        </Sider>

        <Layout>
          <Header
            style={{
              padding: '0 24px',
              background: colorBgContainer,
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>
              OpenMineral Trading Platform - Minimal Demo
            </div>
            
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <span>
                <UserOutlined /> Welcome, {user.full_name || user.username}
              </span>
              <button
                onClick={handleLogout}
                style={{
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  color: '#1890ff'
                }}
              >
                <LogoutOutlined /> Logout
              </button>
            </div>
          </Header>

          <Content style={{ margin: '24px 16px 0' }}>
            <div
              style={{
                padding: 24,
                minHeight: 360,
                background: colorBgContainer,
                borderRadius: '6px'
              }}
            >
              <Routes>
                <Route path="/" element={<Navigate to="/dashboard" />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/deals" element={<Deals />} />
                <Route path="/market" element={<Market />} />
              </Routes>
            </div>
          </Content>

          <Footer style={{ textAlign: 'center' }}>
            OpenMineral Hub ©2025 - Minimal Demo Version
          </Footer>
        </Layout>
      </Layout>
    </Router>
  );
}

export default App;