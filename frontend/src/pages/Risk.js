import React, { useState } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  Select, 
  Space, 
  Typography,
  Tag,
  Descriptions,
  Progress,
  List
} from 'antd';
import { 
  EyeOutlined, 
  ExclamationCircleOutlined, 
  CheckCircleOutlined,
  CloseCircleOutlined,
  PlayCircleOutlined
} from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

const Risk = () => {
  const [riskAssessments, setRiskAssessments] = useState([
    {
      key: '1',
      id: 1,
      dealId: 1,
      dealTitle: 'Iron Ore Purchase Agreement',
      counterparty: 'Brazilian Mining Corp',
      overallScore: 6.2,
      riskLevel: 'Medium',
      lastAssessed: '2025-09-15',
      assessedBy: 'risk@openmineral.com',
      status: 'Assessed'
    },
    {
      key: '2',
      id: 2,
      dealId: 2,
      dealTitle: 'Copper Sale Contract',
      counterparty: 'European Copper Ltd',
      overallScore: 3.8,
      riskLevel: 'Low',
      lastAssessed: '2025-09-10',
      assessedBy: 'risk@openmineral.com',
      status: 'Assessed'
    }
  ]);

  const [mitigationPlans, setMitigationPlans] = useState([
    {
      key: '1',
      id: 1,
      dealId: 1,
      steps: [
        'Establish hedging position',
        'Obtain letter of credit',
        'Set up monthly monitoring'
      ],
      responsibleParties: ['trader@openmineral.com', 'risk@openmineral.com'],
      deadline: '2025-09-30',
      status: 'In Progress'
    }
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedAssessment, setSelectedAssessment] = useState(null);
  const [viewMode, setViewMode] = useState('assessment'); // 'assessment' or 'mitigation'

  const showModal = (assessment, mode = 'assessment') => {
    setSelectedAssessment(assessment);
    setViewMode(mode);
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setSelectedAssessment(null);
  };

  const getRiskLevelTag = (level) => {
    switch (level) {
      case 'Low':
        return <Tag color="green">{level}</Tag>;
      case 'Medium':
        return <Tag color="orange">{level}</Tag>;
      case 'High':
        return <Tag color="red">{level}</Tag>;
      default:
        return <Tag>{level}</Tag>;
    }
  };

  const getStatusTag = (status) => {
    switch (status) {
      case 'Assessed':
        return <Tag color="blue">{status}</Tag>;
      case 'In Progress':
        return <Tag color="orange">{status}</Tag>;
      case 'Completed':
        return <Tag color="green">{status}</Tag>;
      default:
        return <Tag>{status}</Tag>;
    }
  };

  const assessmentColumns = [
    { title: 'Deal Title', dataIndex: 'dealTitle', key: 'dealTitle' },
    { title: 'Counterparty', dataIndex: 'counterparty', key: 'counterparty' },
    { 
      title: 'Risk Score', 
      dataIndex: 'overallScore', 
      key: 'overallScore',
      render: score => <Progress percent={score * 10} size="small" />
    },
    { 
      title: 'Risk Level', 
      dataIndex: 'riskLevel', 
      key: 'riskLevel',
      render: level => getRiskLevelTag(level)
    },
    { title: 'Last Assessed', dataIndex: 'lastAssessed', key: 'lastAssessed' },
    { title: 'Assessed By', dataIndex: 'assessedBy', key: 'assessedBy' },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: status => getStatusTag(status)
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            icon={<EyeOutlined />} 
            onClick={() => showModal(record, 'assessment')}
          >
            View Assessment
          </Button>
          <Button 
            icon={<PlayCircleOutlined />} 
            onClick={() => showModal(record, 'mitigation')}
          >
            Mitigation Plan
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <Title level={2} style={{ margin: 0 }}>Risk Assessment</Title>
          <Button 
            type="primary" 
            icon={<ExclamationCircleOutlined />} 
            onClick={() => {}}
          >
            New Risk Assessment
          </Button>
        </div>

        <Table 
          dataSource={riskAssessments} 
          columns={assessmentColumns} 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={viewMode === 'assessment' ? "Risk Assessment Details" : "Risk Mitigation Plan"}
        visible={isModalVisible}
        onCancel={handleCancel}
        width={800}
        footer={[
          <Button key="back" onClick={handleCancel}>
            Close
          </Button>
        ]}
      >
        {selectedAssessment && viewMode === 'assessment' && (
          <div>
            <Descriptions title="Deal Information" column={2} bordered>
              <Descriptions.Item label="Deal ID">{selectedAssessment.dealId}</Descriptions.Item>
              <Descriptions.Item label="Deal Title">{selectedAssessment.dealTitle}</Descriptions.Item>
              <Descriptions.Item label="Counterparty">{selectedAssessment.counterparty}</Descriptions.Item>
              <Descriptions.Item label="Risk Level">{getRiskLevelTag(selectedAssessment.riskLevel)}</Descriptions.Item>
              <Descriptions.Item label="Overall Score">
                <Progress percent={selectedAssessment.overallScore * 10} />
              </Descriptions.Item>
              <Descriptions.Item label="Last Assessed">{selectedAssessment.lastAssessed}</Descriptions.Item>
              <Descriptions.Item label="Assessed By">{selectedAssessment.assessedBy}</Descriptions.Item>
              <Descriptions.Item label="Status">{getStatusTag(selectedAssessment.status)}</Descriptions.Item>
            </Descriptions>

            <div style={{ marginTop: 24 }}>
              <Title level={4}>Risk Factors</Title>
              <List
                bordered
                dataSource={[
                  { name: 'Price Volatility', category: 'Market', score: 7.5, description: 'High volatility in iron ore prices' },
                  { name: 'Counterparty Risk', category: 'Credit', score: 5.0, description: 'New counterparty with limited credit history' }
                ]}
                renderItem={item => (
                  <List.Item>
                    <List.Item.Meta
                      title={item.name}
                      description={
                        <div>
                          <div>Category: {item.category}</div>
                          <div>Score: <Progress percent={item.score * 10} size="small" /></div>
                          <div>Description: {item.description}</div>
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            </div>

            <div style={{ marginTop: 24 }}>
              <Title level={4}>Recommendations</Title>
              <List
                bordered
                dataSource={[
                  'Hedge 50% of exposure',
                  'Require letter of credit',
                  'Monitor counterparty financials monthly'
                ]}
                renderItem={item => <List.Item>{item}</List.Item>}
              />
            </div>
          </div>
        )}

        {selectedAssessment && viewMode === 'mitigation' && (
          <div>
            <Descriptions title="Mitigation Plan" column={2} bordered>
              <Descriptions.Item label="Deal ID">{selectedAssessment.dealId}</Descriptions.Item>
              <Descriptions.Item label="Deal Title">{selectedAssessment.dealTitle}</Descriptions.Item>
              <Descriptions.Item label="Deadline">2025-09-30</Descriptions.Item>
              <Descriptions.Item label="Status">{getStatusTag('In Progress')}</Descriptions.Item>
            </Descriptions>

            <div style={{ marginTop: 24 }}>
              <Title level={4}>Mitigation Steps</Title>
              <List
                bordered
                dataSource={[
                  { step: 'Establish hedging position', status: 'Completed' },
                  { step: 'Obtain letter of credit', status: 'Completed' },
                  { step: 'Set up monthly monitoring', status: 'In Progress' }
                ]}
                renderItem={item => (
                  <List.Item>
                    <List.Item.Meta
                      title={item.step}
                      description={
                        item.status === 'Completed' ? 
                        <Tag icon={<CheckCircleOutlined />} color="success">{item.status}</Tag> :
                        <Tag icon={<PlayCircleOutlined />} color="processing">{item.status}</Tag>
                      }
                    />
                  </List.Item>
                )}
              />
            </div>

            <div style={{ marginTop: 24 }}>
              <Title level={4}>Responsible Parties</Title>
              <List
                bordered
                dataSource={['trader@openmineral.com', 'risk@openmineral.com']}
                renderItem={item => <List.Item>{item}</List.Item>}
              />
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Risk;