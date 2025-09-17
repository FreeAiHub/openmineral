'use client';

import React from 'react';
import { Row, Col, Card, Statistic, Table, Typography } from 'antd';
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  FileTextOutlined,
  BarChartOutlined,
  SafetyCertificateOutlined,
  WarningOutlined
} from '@ant-design/icons';
import Link from 'next/link';

const { Title } = Typography;

const DashboardPage = () => {
  // Mock data for statistics
  const statsData = [
    { title: 'Total Deals', value: 24, icon: <FileTextOutlined /> },
    { title: 'Active Deals', value: 8, icon: <FileTextOutlined /> },
    { title: 'Pending Compliance', value: 3, icon: <SafetyCertificateOutlined /> },
    { title: 'High Risk Deals', value: 2, icon: <WarningOutlined /> },
  ];

  // Mock data for recent deals
  const recentDeals = [
    { key: '1', deal: 'Iron Ore Purchase', counterparty: 'Brazilian Mining Corp', value: '$855,000', status: 'Active' },
    { key: '2', deal: 'Copper Sale', counterparty: 'European Copper Ltd', value: '$46,000,000', status: 'Pending' },
    { key: '3', deal: 'Gold Forward', counterparty: 'Swiss Refinery', value: '$19,500,000', status: 'Completed' },
    { key: '4', deal: 'Silver Spot', counterparty: 'US Trader', value: '$2,350,000', status: 'Active' },
  ];

  const dealColumns = [
    { title: 'Deal', dataIndex: 'deal', key: 'deal' },
    { title: 'Counterparty', dataIndex: 'counterparty', key: 'counterparty' },
    { title: 'Value', dataIndex: 'value', key: 'value' },
    { title: 'Status', dataIndex: 'status', key: 'status' },
  ];

  // Mock data for market updates
  const marketData = [
    { key: '1', commodity: 'Iron Ore', price: '$85.50', change: '+2.3%', trend: 'up' },
    { key: '2', commodity: 'Copper', price: '$9,200', change: '-1.2%', trend: 'down' },
    { key: '3', commodity: 'Gold', price: '$1,950', change: '+0.8%', trend: 'up' },
    { key: '4', commodity: 'Silver', price: '$23.50', change: '+3.1%', trend: 'up' },
  ];

  const marketColumns = [
    { title: 'Commodity', dataIndex: 'commodity', key: 'commodity' },
    { title: 'Price', dataIndex: 'price', key: 'price' },
    { 
      title: 'Change', 
      dataIndex: 'change', 
      key: 'change',
      render: (text, record) => (
        <span style={{ color: record.trend === 'up' ? '#52c41a' : '#ff4d4f' }}>
          {record.trend === 'up' ? <ArrowUpOutlined /> : <ArrowDownOutlined />} {text}
        </span>
      )
    },
  ];

  return (
    <div>
      <Title level={2}>Dashboard</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        {statsData.map((stat, index) => (
          <Col span={6} key={index}>
            <Card>
              <Statistic
                title={stat.title}
                value={stat.value}
                prefix={stat.icon}
              />
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="Recent Deals" extra={<Link href="/deals">View All</Link>}>
            <Table 
              dataSource={recentDeals} 
              columns={dealColumns} 
              pagination={false} 
              size="small"
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Market Updates" extra={<Link href="/analytics">View All</Link>}>
            <Table 
              dataSource={marketData} 
              columns={marketColumns} 
              pagination={false} 
              size="small"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default DashboardPage;
