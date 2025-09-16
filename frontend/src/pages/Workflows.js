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
  Steps,
  List
} from 'antd';
import { 
  EyeOutlined, 
  PlayCircleOutlined, 
  PauseCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';

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
      createdBy: 'system'
    }
  ]);

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

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <Title level={2} style={{ margin: 0 }}>Workflow Automation</Title>
          <Button 
            type="primary" 
            icon={<PlayCircleOutlined />} 
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
      </Card>

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