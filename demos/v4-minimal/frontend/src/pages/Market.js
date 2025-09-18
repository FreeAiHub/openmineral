import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Typography, 
  Row, 
  Col,
  Spin,
  Alert,
  Statistic,
  Space,
  Select,
  message
} from 'antd';
import {
  ArrowUpOutlined,
  ArrowDownOutlined,
  ReloadOutlined,
  BarChartOutlined,
  TrendingUpOutlined
} from '@ant-design/icons';
import apiService from '../services/api';

const { Title, Text } = Typography;
const { Option } = Select;

const Market = () => {
  const [loading, setLoading] = useState(true);
  const [marketData, setMarketData] = useState([]);
  const [selectedCommodity, setSelectedCommodity] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  useEffect(() => {
    loadMarketData();
  }, []);

  const loadMarketData = async () => {
    try {
      setLoading(true);
      const data = await apiService.getMarketPrices();
      setMarketData(data);
    } catch (error) {
      console.error('Failed to load market data:', error);
      message.error('Failed to load market data');
    } finally {
      setLoading(false);
    }
  };

  const loadAnalysis = async (commodity) => {
    try {
      setAnalysisLoading(true);
      const analysisData = await apiService.getCommodityAnalysis(commodity);
      setAnalysis(analysisData);
    } catch (error) {
      console.error('Failed to load analysis:', error);
      message.error('Failed to load analysis');
    } finally {
      setAnalysisLoading(false);
    }
  };

  const handleCommoditySelect = (commodity) => {
    setSelectedCommodity(commodity);
    loadAnalysis(commodity);
  };

  const getTrendIcon = (change) => {
    return change > 0 ? <ArrowUpOutlined /> : <ArrowDownOutlined />;
  };

  const getTrendColor = (change) => {
    return change > 0 ? '#52c41a' : '#ff4d4f';
  };

  const columns = [
    {
      title: 'Commodity',
      dataIndex: 'commodity',
      key: 'commodity',
      render: (text) => <Text strong>{text}</Text>
    },
    {
      title: 'Current Price',
      dataIndex: 'price',
      key: 'price',
      render: (price) => (
        <Text style={{ fontSize: '16px', fontWeight: 'bold' }}>
          ${price.toFixed(2)}
        </Text>
      )
    },
    {
      title: 'Change (%)',
      dataIndex: 'change',
      key: 'change',
      render: (change) => (
        <Space>
          <span style={{ color: getTrendColor(change) }}>
            {getTrendIcon(change)}
            {Math.abs(change).toFixed(1)}%
          </span>
        </Space>
      ),
      sorter: (a, b) => a.change - b.change
    },
    {
      title: 'Volume',
      dataIndex: 'volume',
      key: 'volume',
      render: (volume) => volume.toLocaleString(),
      sorter: (a, b) => a.volume - b.volume
    },
    {
      title: 'Last Updated',
      dataIndex: 'timestamp',
      key: 'timestamp',
      render: (timestamp) => new Date(timestamp).toLocaleString()
    },
    {
      title: 'Action',
      key: 'action',
      render: (_, record) => (
        <Button
          type="link"
          icon={<BarChartOutlined />}
          onClick={() => handleCommoditySelect(record.commodity)}
        >
          Analyze
        </Button>
      )
    }
  ];

  // Calculate summary statistics
  const totalVolume = marketData.reduce((sum, item) => sum + item.volume, 0);
  const avgChange = marketData.length > 0 
    ? marketData.reduce((sum, item) => sum + item.change, 0) / marketData.length 
    : 0;
  const gainers = marketData.filter(item => item.change > 0).length;
  const losers = marketData.filter(item => item.change < 0).length;

  return (
    <div>
      <Title level={2} style={{ marginBottom: '24px' }}>
        Market Data & Analysis
      </Title>

      {/* Market Summary */}
      <Row gutter={16} style={{ marginBottom: '24px' }}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Total Volume"
              value={totalVolume}
              formatter={(value) => Number(value).toLocaleString()}
              prefix={<TrendingUpOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Average Change"
              value={avgChange}
              precision={2}
              suffix="%"
              valueStyle={{ color: getTrendColor(avgChange) }}
              prefix={getTrendIcon(avgChange)}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Gainers"
              value={gainers}
              valueStyle={{ color: '#52c41a' }}
              prefix={<ArrowUpOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Losers"
              value={losers}
              valueStyle={{ color: '#ff4d4f' }}
              prefix={<ArrowDownOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Market Data Table */}
      <Card 
        title="Live Market Prices"
        extra={
          <Button 
            icon={<ReloadOutlined />}
            onClick={loadMarketData}
            loading={loading}
          >
            Refresh
          </Button>
        }
        style={{ marginBottom: '24px' }}
      >
        {loading ? (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
            <p style={{ marginTop: '16px' }}>Loading market data...</p>
          </div>
        ) : (
          <Table
            dataSource={marketData}
            columns={columns}
            rowKey="commodity"
            pagination={false}
            size="middle"
          />
        )}
      </Card>

      {/* Commodity Analysis */}
      {selectedCommodity && (
        <Card 
          title={`${selectedCommodity} Analysis`}
          style={{ marginBottom: '24px' }}
        >
          {analysisLoading ? (
            <div style={{ textAlign: 'center', padding: '30px' }}>
              <Spin />
              <p style={{ marginTop: '16px' }}>Analyzing {selectedCommodity}...</p>
            </div>
          ) : analysis ? (
            <div>
              <Row gutter={16}>
                <Col span={24}>
                  <Title level={4}>Market Analysis</Title>
                  <Text>{analysis.analysis}</Text>
                </Col>
              </Row>
              
              <Row gutter={16} style={{ marginTop: '24px' }}>
                <Col xs={24} md={12}>
                  <Title level={5}>Recommendations</Title>
                  <ul>
                    {analysis.recommendations.map((rec, index) => (
                      <li key={index}>{rec}</li>
                    ))}
                  </ul>
                </Col>
                <Col xs={24} md={12}>
                  <Title level={5}>Risk Factors</Title>
                  <ul>
                    {analysis.risk_factors.map((risk, index) => (
                      <li key={index}>{risk}</li>
                    ))}
                  </ul>
                </Col>
              </Row>
            </div>
          ) : null}
        </Card>
      )}

      {/* Demo Information */}
      <Alert
        message="Market Data Demo"
        description={
          <div>
            <p><strong>Real API Integration:</strong> Market data is fetched from the backend API in real-time.</p>
            <p><strong>Mock Analysis:</strong> Commodity analysis uses basic mock responses for demonstration.</p>
            <p><strong>Features:</strong> Live price updates, trend indicators, volume tracking, and basic analysis.</p>
          </div>
        }
        type="info"
        showIcon
      />
    </div>
  );
};

export default Market;