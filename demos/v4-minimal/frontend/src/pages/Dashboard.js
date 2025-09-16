import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Table, Typography, Spin, Alert } from 'antd';
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  FileTextOutlined,
  DollarCircleOutlined,
  TrophyOutlined,
  ClockCircleOutlined
} from '@ant-design/icons';
import apiService from '../services/api';

const { Title, Text } = Typography;

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState(null);
  const [deals, setDeals] = useState([]);
  const [marketData, setMarketData] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load data in parallel
      const [statsResponse, dealsResponse, marketResponse] = await Promise.all([
        apiService.getDashboardStats(),
        apiService.getDeals(),
        apiService.getMarketPrices()
      ]);

      setStats(statsResponse);
      setDeals(dealsResponse.slice(0, 5)); // Show only recent 5 deals
      setMarketData(marketResponse);

    } catch (err) {
      console.error('Failed to load dashboard data:', err);
      setError('Failed to load dashboard data. Please try refreshing the page.');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <p style={{ marginTop: '16px' }}>Loading dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <Alert
        message="Error"
        description={error}
        type="error"
        showIcon
        style={{ margin: '20px 0' }}
      />
    );
  }

  const dealColumns = [
    { 
      title: 'Deal', 
      dataIndex: 'title', 
      key: 'title',
      render: (text) => <Text strong>{text}</Text>
    },
    { 
      title: 'Commodity', 
      dataIndex: 'commodity', 
      key: 'commodity' 
    },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: (status) => (
        <span style={{
          padding: '2px 8px',
          borderRadius: '4px',
          fontSize: '12px',
          background: status === 'active' ? '#f6ffed' : '#fff7e6',
          color: status === 'active' ? '#52c41a' : '#fa8c16',
          border: `1px solid ${status === 'active' ? '#b7eb8f' : '#ffd591'}`
        }}>
          {status.toUpperCase()}
        </span>
      )
    },
    { 
      title: 'Value', 
      dataIndex: 'price', 
      key: 'value',
      render: (price, record) => `$${(price * record.quantity).toLocaleString()}`
    }
  ];

  const marketColumns = [
    { 
      title: 'Commodity', 
      dataIndex: 'commodity', 
      key: 'commodity',
      render: (text) => <Text strong>{text}</Text>
    },
    { 
      title: 'Price', 
      dataIndex: 'price', 
      key: 'price',
      render: (price) => `$${price.toFixed(2)}`
    },
    { 
      title: 'Change', 
      dataIndex: 'change', 
      key: 'change',
      render: (change) => (
        <span style={{ color: change > 0 ? '#52c41a' : '#ff4d4f' }}>
          {change > 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
          {' '}
          {Math.abs(change)}%
        </span>
      )
    },
    { 
      title: 'Volume', 
      dataIndex: 'volume', 
      key: 'volume',
      render: (volume) => volume.toLocaleString()
    }
  ];

  return (
    <div>
      <Title level={2} style={{ marginBottom: '24px' }}>
        Trading Dashboard
      </Title>
      
      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Deals"
              value={stats?.total_deals || 0}
              prefix={<FileTextOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Active Deals"
              value={stats?.active_deals || 0}
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Pending Deals"
              value={stats?.pending_deals || 0}
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Value"
              value={stats?.total_value || 0}
              prefix={<DollarCircleOutlined />}
              precision={0}
              formatter={(value) => `$${Number(value).toLocaleString()}`}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Data Tables */}
      <Row gutter={16}>
        <Col xs={24} lg={12}>
          <Card 
            title="Recent Deals" 
            extra={<a href="#/deals">View All</a>}
            style={{ marginBottom: '16px' }}
          >
            <Table 
              dataSource={deals} 
              columns={dealColumns} 
              pagination={false} 
              size="small"
              rowKey="id"
            />
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card 
            title="Market Prices" 
            extra={<a href="#/market">View Details</a>}
          >
            <Table 
              dataSource={marketData} 
              columns={marketColumns} 
              pagination={false} 
              size="small"
              rowKey="commodity"
            />
          </Card>
        </Col>
      </Row>

      {/* Footer Info */}
      <Card style={{ marginTop: '24px', background: '#fafafa' }}>
        <div style={{ textAlign: 'center' }}>
          <Text type="secondary">
            📊 This is a minimal demo version showing real API integration<br />
            ⚡ All data is stored in memory and updates in real-time<br />
            🔗 Backend API: Connected and operational
          </Text>
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;