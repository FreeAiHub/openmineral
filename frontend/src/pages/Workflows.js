import React, { useState, useEffect } from 'react';
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
  Steps,
  List,
  Tabs,
  Alert,
  Progress,
  Spin,
  message,
  Input as AntInput
} from 'antd';
import {
  EyeOutlined,
  PlayCircleOutlined,
  PauseCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  RobotOutlined,
  ThunderboltOutlined,
  BarChartOutlined,
  PlusOutlined,
  SettingOutlined,
  ExperimentOutlined
} from '@ant-design/icons';
import axios from 'axios'; // Assuming axios is available for API calls

const { Title } = Typography;
const { Option } = Select;
const { Step } = Steps;

const Workflows = () => {
  const [workflows, setWorkflows] = useState([
    {
      key: '1',
      id: 1,
      name: 'Deal Approval Process',
      description: 'Standard workflow for approving new deals',
      dealId: 1,
      dealTitle: 'Iron Ore Purchase Agreement',
      status: 'Active',
      currentStep: 3,
      totalSteps: 4,
      startedAt: '2025-09-14',
      createdBy: 'system',
      isAI: false
    }
  ]);

  // AI-Powered Workflow States
  const [aiWorkflows, setAiWorkflows] = useState([]);
  const [isAIGenerating, setIsAIGenerating] = useState(false);
  const [isAIStepExecuting, setIsAIStepExecuting] = useState(false);
  const [aiMetrics, setAiMetrics] = useState(null);
  const [showAIModal, setShowAIModal] = useState(false);
  const [currentAIModal, setCurrentAIModal] = useState(null);
  const [aiPrompt, setAiPrompt] = useState('');
  const [optimizationResults, setOptimizationResults] = useState(null);

  // Load AI metrics on component mount
  useEffect(() => {
    loadAIMetrics();
  }, []);

  const loadAIMetrics = async () => {
    try {
      const response = await axios.get('/api/workflow/ai/metrics', {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setAiMetrics(response.data);
    } catch (error) {
      console.error('Failed to load AI metrics:', error);
    }
  };

  const [workflowSteps, setWorkflowSteps] = useState([
    {
      id: 1,
      workflowId: 1,
      steps: [
        {
          id: 1,
          name: 'Market Analysis',
          description: 'Analyze market conditions for the commodity',
          assignedTo: 'analyst@openmineral.com',
          status: 'Completed',
          deadline: '2025-09-14',
          completedAt: '2025-09-14'
        },
        {
          id: 2,
          name: 'Risk Assessment',
          description: 'Evaluate risks associated with the deal',
          assignedTo: 'risk@openmineral.com',
          status: 'Completed',
          deadline: '2025-09-15',
          completedAt: '2025-09-15'
        },
        {
          id: 3,
          name: 'Legal Review',
          description: 'Review contract terms and conditions',
          assignedTo: 'legal@openmineral.com',
          status: 'In Progress',
          deadline: '2025-09-17'
        },
        {
          id: 4,
          name: 'Final Approval',
          description: 'Obtain final approval from authorized personnel',
          assignedTo: 'director@openmineral.com',
          status: 'Pending',
          deadline: '2025-09-18'
        }
      ]
    }
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedWorkflow, setSelectedWorkflow] = useState(null);

  const showModal = (workflow) => {
    setSelectedWorkflow(workflow);
    setIsModalVisible(true);
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setSelectedWorkflow(null);
  };

  const getStatusTag = (status) => {
    switch (status) {
      case 'Active':
        return <Tag color="blue">{status}</Tag>;
      case 'Completed':
        return <Tag color="green">{status}</Tag>;
      case 'Paused':
        return <Tag color="orange">{status}</Tag>;
      case 'Failed':
        return <Tag color="red">{status}</Tag>;
      default:
        return <Tag>{status}</Tag>;
    }
  };

  const getStepStatus = (stepStatus) => {
    switch (stepStatus) {
      case 'Completed':
        return 'finish';
      case 'In Progress':
        return 'process';
      case 'Pending':
        return 'wait';
      default:
        return 'wait';
    }
  };

  const getStepIcon = (stepStatus) => {
    switch (stepStatus) {
      case 'Completed':
        return <CheckCircleOutlined />;
      case 'In Progress':
        return <PlayCircleOutlined />;
      case 'Pending':
        return <PauseCircleOutlined />;
      default:
        return null;
    }
  };

  const columns = [
    { title: 'Workflow Name', dataIndex: 'name', key: 'name' },
    { title: 'Deal Title', dataIndex: 'dealTitle', key: 'dealTitle' },
    { 
      title: 'Progress', 
      dataIndex: 'currentStep', 
      key: 'progress',
      render: (_, record) => (
        <div>
          Step {record.currentStep} of {record.totalSteps}
          <div style={{ width: 100, marginTop: 5 }}>
            <div style={{ 
              width: `${(record.currentStep / record.totalSteps) * 100}%`, 
              height: 8, 
              backgroundColor: '#1890ff', 
              borderRadius: 4 
            }}></div>
          </div>
        </div>
      )
    },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: status => getStatusTag(status)
    },
    { title: 'Started At', dataIndex: 'startedAt', key: 'startedAt' },
    { title: 'Created By', dataIndex: 'createdBy', key: 'createdBy' },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            icon={<EyeOutlined />} 
            onClick={() => showModal(record)}
          >
            View Details
          </Button>
          <Button 
            icon={<PlayCircleOutlined />} 
            type="primary"
          >
            Execute
          </Button>
        </Space>
      ),
    },
  ];

  // AI Workflow Functions
  const generateAIWorkflow = async () => {
    if (!aiPrompt.trim()) {
      message.warning('Please enter a workflow prompt');
      return;
    }

    setIsAIGenerating(true);
    try {
      const response = await axios.post('/api/workflow/ai/generate-workflow', {
        prompt: aiPrompt,
        workflow_type: 'deal_analysis'
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      message.success('AI workflow generated successfully!');
      setAiWorkflows([...aiWorkflows, response.data.workflow]);
      setAiPrompt('');
    } catch (error) {
      message.error('Failed to generate AI workflow');
    } finally {
      setIsAIGenerating(false);
    }
  };

  const executeAIStep = async (workflowId, stepId) => {
    setIsAIStepExecuting(true);
    try {
      const response = await axios.post(`/api/workflow/ai/execute-step`, {
        workflow_id: workflowId,
        step_id: stepId
      }, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      message.success('AI step executed successfully!');
      return response.data;
    } catch (error) {
      message.error('Failed to execute AI step');
    } finally {
      setIsAIStepExecuting(false);
    }
  };

  const optimizeWorkflow = async (workflowId) => {
    try {
      const response = await axios.post(`/api/workflow/ai/optimize-workflow/${workflowId}`, {}, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      setOptimizationResults(response.data);
      setCurrentAIModal('optimize');
      setShowAIModal(true);
    } catch (error) {
      message.error('Failed to optimize workflow');
    }
  };

  const tabItems = [
    {
      key: 'traditional',
      label: 'Traditional Workflows',
      children: (
        <div>
          <div style={{ marginBottom: 16 }}>
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => {}}
            >
              Create New Workflow
            </Button>
          </div>
          <Table
            dataSource={workflows}
            columns={columns}
            pagination={{ pageSize: 10 }}
          />
        </div>
      ),
    },
    {
      key: 'ai',
      label: (
        <span>
          <RobotOutlined style={{ marginRight: 8 }} />
          AI-Powered Workflows
        </span>
      ),
      children: (
        <div>
          {/* AI Metrics */}
          {aiMetrics && (
            <div style={{ marginBottom: 24 }}>
              <Card size="small">
                <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
                  <div>
                    <div style={{ color: '#666', fontSize: 12 }}>Total AI Workflows</div>
                    <div style={{ fontSize: 24, fontWeight: 'bold' }}>{aiMetrics.total_ai_workflows}</div>
                  </div>
                  <div>
                    <div style={{ color: '#666', fontSize: 12 }}>Success Rate</div>
                    <div style={{ fontSize: 24, fontWeight: 'bold', color: '#52c41a' }}>
                      {(aiMetrics.success_rate * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div>
                    <div style={{ color: '#666', fontSize: 12 }}>Avg Execution Time</div>
                    <div style={{ fontSize: 18, fontWeight: 'bold' }}>{aiMetrics.average_execution_time}</div>
                  </div>
                  <div>
                    <div style={{ color: '#666', fontSize: 12 }}>Cost Savings</div>
                    <div style={{ fontSize: 18, fontWeight: 'bold', color: '#1890ff' }}>
                      {aiMetrics.cost_savings}
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          )}

          {/* AI Workflow Generator */}
          <Card title={<><RobotOutlined /> AI Workflow Generator</>} style={{ marginBottom: 24 }}>
            <div style={{ display: 'flex', gap: 16 }}>
              <AntInput.TextArea
                placeholder="Describe the workflow you want to create (e.g., 'Create a deal approval process for commodity purchases')"
                value={aiPrompt}
                onChange={(e) => setAiPrompt(e.target.value)}
                rows={3}
                style={{ flex: 1 }}
              />
              <Button
                type="primary"
                icon={<ThunderboltOutlined />}
                loading={isAIGenerating}
                onClick={generateAIWorkflow}
                style={{ height: 'auto', padding: '8px 16px' }}
              >
                Generate AI
              </Button>
            </div>
          </Card>

          {/* AI Workflow Actions */}
          <div style={{ marginBottom: 16 }}>
            <Space>
              <Button
                icon={<BarChartOutlined />}
                onClick={() => {
                  setCurrentAIModal('metrics');
                  setShowAIModal(true);
                }}
              >
                View Metrics
              </Button>
              <Button
                icon={<SettingOutlined />}
                onClick={() => {
                  setCurrentAIModal('optimize');
                  setShowAIModal(true);
                }}
              >
                Optimize Workflow
              </Button>
            </Space>
          </div>

          {/* AI Workflows Table */}
          <Table
            dataSource={aiWorkflows}
            columns={[
              { title: 'Name', dataIndex: 'name', key: 'name' },
              { title: 'Goal', dataIndex: 'overall_goal', key: 'goal' },
              {
                title: 'Steps',
                dataIndex: 'steps',
                key: 'steps',
                render: (steps) => steps?.length || 0
              },
              {
                title: 'AI Coordinator',
                dataIndex: 'ai_coordinator',
                key: 'ai',
                render: (ai) => ai ? <Tag color="blue">AI</Tag> : <Tag>Manual</Tag>
              },
              {
                title: 'Actions',
                key: 'actions',
                render: (_, record) => (
                  <Space>
                    <Button
                      icon={<EyeOutlined />}
                      onClick={() => {
                        setSelectedWorkflow(record);
                        setIsModalVisible(true);
                      }}
                    >
                      View
                    </Button>
                    <Button
                      icon={<PlayCircleOutlined />}
                      onClick={() => executeAIStep(record.id, 1)}
                      loading={isAIStepExecuting}
                    >
                      Execute
                    </Button>
                    <Button
                      icon={<ExperimentOutlined />}
                      onClick={() => optimizeWorkflow(record.id)}
                    >
                      Optimize
                    </Button>
                  </Space>
                ),
              },
            ]}
            pagination={{ pageSize: 10 }}
          />
        </div>
      ),
    },
  ];

  return (
    <div>
      <Tabs items={tabItems} defaultActiveKey="traditional" />

      {/* AI Results Modal */}
      <Modal
        title={
          currentAIModal === 'metrics' ? 'AI Workflow Metrics' :
          currentAIModal === 'optimize' ? 'Workflow Optimization Results' :
          'AI Results'
        }
        visible={showAIModal}
        onCancel={() => setShowAIModal(false)}
        width={700}
        footer={<Button onClick={() => setShowAIModal(false)}>Close</Button>}
      >
        {currentAIModal === 'metrics' && aiMetrics && (
          <div>
            <Progress
              type="circle"
              percent={aiMetrics.success_rate * 100}
              format={(percent) => `${percent.toFixed(1)}%`}
              style={{ marginBottom: 16 }}
            />
            <Descriptions column={1} bordered>
              <Descriptions.Item label="Total AI Workflows">{aiMetrics.total_ai_workflows}</Descriptions.Item>
              <Descriptions.Item label="Success Rate">{(aiMetrics.success_rate * 100).toFixed(1)}%</Descriptions.Item>
              <Descriptions.Item label="Average Execution Time">{aiMetrics.average_execution_time}</Descriptions.Item>
              <Descriptions.Item label="Cost Savings">{aiMetrics.cost_savings}</Descriptions.Item>
              <Descriptions.Item label="Accuracy Improvement">{aiMetrics.accuracy_improvement}</Descriptions.Item>
            </Descriptions>
          </div>
        )}

        {currentAIModal === 'optimize' && optimizationResults && (
          <div>
            <Alert
              message="Optimization Completed"
              description={optimizationResults.ai_recommendations}
              type="success"
              style={{ marginBottom: 16 }}
            />
            <List
              dataSource={optimizationResults.optimization_opportunities}
              renderItem={(item) => <List.Item>{item}</List.Item>}
            />
            <div style={{ marginTop: 16, padding: 16, backgroundColor: '#f6ffed', border: '1px solid #b7eb8f' }}>
              <strong>Estimated Improvement:</strong> {optimizationResults.estimated_improvement}
            </div>
          </div>
        )}
      </Modal>

      <Modal
        title="Workflow Details"
        visible={isModalVisible}
        onCancel={handleCancel}
        width={800}
        footer={[
          <Button key="back" onClick={handleCancel}>
            Close
          </Button>
        ]}
      >
        {selectedWorkflow && (
          <div>
            <Descriptions title="Workflow Information" column={2} bordered>
              <Descriptions.Item label="Workflow ID">{selectedWorkflow.id}</Descriptions.Item>
              <Descriptions.Item label="Workflow Name">{selectedWorkflow.name}</Descriptions.Item>
              <Descriptions.Item label="Deal ID">{selectedWorkflow.dealId}</Descriptions.Item>
              <Descriptions.Item label="Deal Title">{selectedWorkflow.dealTitle}</Descriptions.Item>
              <Descriptions.Item label="Status">{getStatusTag(selectedWorkflow.status)}</Descriptions.Item>
              <Descriptions.Item label="Started At">{selectedWorkflow.startedAt}</Descriptions.Item>
              <Descriptions.Item label="Created By">{selectedWorkflow.createdBy}</Descriptions.Item>
              <Descriptions.Item label="Description">{selectedWorkflow.description}</Descriptions.Item>
            </Descriptions>

            <div style={{ marginTop: 24 }}>
              <Title level={4}>Workflow Steps</Title>
              {workflowSteps
                .filter(wf => wf.workflowId === selectedWorkflow.id)
                .map(wf => (
                  <Steps 
                    key={wf.id} 
                    direction="vertical" 
                    size="small" 
                    current={selectedWorkflow.currentStep - 1}
                  >
                    {wf.steps.map(step => (
                      <Step
                        key={step.id}
                        title={step.name}
                        description={
                          <div>
                            <div>{step.description}</div>
                            <div>Assigned to: {step.assignedTo}</div>
                            <div>Deadline: {step.deadline}</div>
                            {step.completedAt && <div>Completed at: {step.completedAt}</div>}
                          </div>
                        }
                        status={getStepStatus(step.status)}
                        icon={getStepIcon(step.status)}
                      />
                    ))}
                  </Steps>
                ))}
            </div>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Workflows;
