import React, { useState } from 'react';
import { 
  Card, 
  Row, 
  Col, 
  Select, 
  DatePicker, 
  Table, 
  Typography,
  Space
} from 'antd';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const Analytics = () => {
  // Mock data for price charts
  const priceData = [
    { date: '2025-09-01', ironOre: 82.5, copper: 9100, gold: 1920, silver: 22.8 },
    { date: '2025-09-02', ironOre: 83.2, copper: 9150, gold: 1925, silver: 22.9 },
    { date: '2025-09-03', ironOre: 84.1, copper: 9180, gold: 1930, silver: 23.1 },
    { date: '2025-09-04', ironOre: 83.8, copper: 9120, gold: 1935, silver: 23.0 },
    { date: '2025-09-05', ironOre: 84.5, copper: 9200, gold: 1940, silver: 23.2 },
    { date: '2025-09-06', ironOre: 85.0, copper: 9180, gold: 1945, silver: 23.3 },
    { date: '2025-09-07', ironOre: 85.5, copper: 9200, gold: 1950, silver: 23.5 },
  ];

  // Mock data for deal volume
  const volumeData = [
    { month: 'Jan', deals: 12, volume: 45.2 },
    { month: 'Feb', deals: 15, volume: 52.8 },
    { month: 'Mar', deals: 18, volume: 61.5 },
    { month: 'Apr', deals: 14, volume: 48.3 },
    { month: 'May', deals: 20, volume: 72.1 },
    { month: 'Jun', deals: 22, volume: 78.9 },
    { month: 'Jul', deals: 19, volume: 68.4 },
    { month: 'Aug', deals: 21, volume: 75.6 },
    { month: 'Sep', deals: 16, volume: 58.7 },
  ];

  // Mock data for market forecasts
  const forecastData = [
    { commodity: 'Iron Ore', current: 85.5, forecast: 88.2, confidence: '75%' },
    { commodity: 'Copper', current: 9200, forecast: 9100, confidence: '68%' },
    { commodity: 'Gold', current: 1950, forecast: 1980, confidence: '82%' },
    { commodity: 'Silver', current: 23.5, forecast: 24.1, confidence: '71%' },
  ];

  const forecastColumns = [
    { title: 'Commodity', dataIndex: 'commodity', key: 'commodity' },
    { title: 'Current Price', dataIndex: 'current', key: 'current' },
    { title: 'Forecast Price', dataIndex: 'forecast', key: 'forecast' },
    { title: 'Confidence', dataIndex: 'confidence', key: 'confidence' },
  ];

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <Title level={2} style={{ margin: 0 }}>Market Analytics</Title>
          <Space>
            <Select defaultValue="30d" style={{ width: 120 }}>
              <Option value="7d">Last 7 Days</Option>
              <Option value="30d">Last 30 Days</Option>
              <Option value="90d">Last 90 Days</Option>
              <Option value="1y">Last Year</Option>
            </Select>
            <RangePicker />
          </Space>
        </div>

        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={12}>
            <Card title="Commodity Prices Trend">
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={priceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="ironOre" stroke="#8884d8" name="Iron Ore ($)" />
                  <Line type="monotone" dataKey="copper" stroke="#82ca9d" name="Copper ($)" />
                  <Line type="monotone" dataKey="gold" stroke="#ffc658" name="Gold ($)" />
                  <Line type="monotone" dataKey="silver" stroke="#ff7300" name="Silver ($)" />
                </LineChart>
              </ResponsiveContainer>
            </Card>
          </Col>
          <Col span={12}>
            <Card title="Deal Volume & Value">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={volumeData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <Tooltip />
                  <Legend />
                  <Bar yAxisId="left" dataKey="deals" fill="#8884d8" name="Number of Deals" />
                  <Bar yAxisId="right" dataKey="volume" fill="#82ca9d" name="Volume (Million $)" />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={24}>
            <Card title="AI Price Forecasts">
              <Table 
                dataSource={forecastData} 
                columns={forecastColumns} 
                pagination={false}
              />
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  );
};

export default Analytics;