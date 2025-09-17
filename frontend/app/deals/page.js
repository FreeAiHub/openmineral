'use client';

import React, { useState, useEffect } from 'react';
import { Table, Tag, Space, Typography, Button, Input, Select } from 'antd';
import { PlusOutlined, SearchOutlined } from '@ant-design/icons';
import Link from 'next/link';

const { Title } = Typography;
const { Option } = Select;

const DealsPage = () => {
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchText, setSearchText] = useState('');
  const [filterStatus, setFilterStatus] = useState('');

  // Mock data - in real app, fetch from API
  const mockDeals = [
    {
      key: '1',
      dealId: 'OMH-001',
      commodity: 'Copper',
      counterparty: 'Glencore International',
      quantity: '500 tons',
      value: '$4,750,000',
      status: 'Active',
      risk: 'Medium',
      date: '2025-01-15',
    },
    {
      key: '2',
      dealId: 'OMH-002',
      commodity: 'Lithium',
      counterparty: 'SQM Chile',
      quantity: '200 tons',
      value: '$3,000,000',
      status: 'Pending',
      risk: 'High',
      date: '2025-02-01',
    },
    {
      key: '3',
      dealId: 'OMH-003',
      commodity: 'Iron Ore',
      counterparty: 'Vale Brazil',
      quantity: '1,000 tons',
      value: '$110,000',
      status: 'Completed',
      risk: 'Low',
      date: '2025-03-10',
    },
  ];

  useEffect(() => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setDeals(mockDeals);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredDeals = deals.filter(deal => {
    const matchesSearch = deal.dealId.toLowerCase().includes(searchText.toLowerCase()) ||
                          deal.counterparty.toLowerCase().includes(searchText.toLowerCase()) ||
                          deal.commodity.toLowerCase().includes(searchText.toLowerCase());
    const matchesStatus = !filterStatus || deal.status === filterStatus;
    return matchesSearch && matchesStatus;
  });

  const columns = [
    {
      title: 'Deal ID',
      dataIndex: 'dealId',
      key: 'dealId',
    },
    {
      title: 'Commodity',
      dataIndex: 'commodity',
      key: 'commodity',
    },
    {
      title: 'Counterparty',
      dataIndex: 'counterparty',
      key: 'counterparty',
    },
    {
      title: 'Quantity',
      dataIndex: 'quantity',
      key: 'quantity',
    },
    {
      title: 'Value',
      dataIndex: 'value',
      key: 'value',
    },
    {
      title: 'Status',
      key: 'status',
      dataIndex: 'status',
      render: (status) => (
        <Tag color={status === 'Active' ? 'blue' : status === 'Pending' ? 'orange' : 'green'}>
          {status}
        </Tag>
      ),
    },
    {
      title: 'Risk',
      key: 'risk',
      dataIndex: 'risk',
      render: (risk) => (
        <Tag color={risk === 'Low' ? 'green' : risk === 'Medium' ? 'orange' : 'red'}>
          {risk}
        </Tag>
      ),
    },
    {
      title: 'Date',
      dataIndex: 'date',
      key: 'date',
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Space size="middle">
          <Link href={`/deals/${record.key}`}>View</Link>
          <Link href={`/deals/edit/${record.key}`}>Edit</Link>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>Deals Management</Title>
      
      <div style={{ marginBottom: 16 }}>
        <Space>
          <Input
            placeholder="Search deals..."
            prefix={<SearchOutlined />}
            value={searchText}
            onChange={(e) => setSearchText(e.target.value)}
            style={{ width: 200 }}
          />
          <Select
            placeholder="Filter by status"
            value={filterStatus}
            onChange={setFilterStatus}
            style={{ width: 150 }}
            allowClear
          >
            <Option value="Active">Active</Option>
            <Option value="Pending">Pending</Option>
            <Option value="Completed">Completed</Option>
          </Select>
          <Button type="primary" icon={<PlusOutlined />}>
            New Deal
          </Button>
        </Space>
      </div>

      <Table
        columns={columns}
        dataSource={filteredDeals}
        loading={loading}
        pagination={{ pageSize: 10 }}
        scroll={{ x: 1000 }}
      />
    </div>
  );
};

export default DealsPage;
