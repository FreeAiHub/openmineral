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
  Descriptions
} from 'antd';
import { PlusOutlined, EyeOutlined, CheckOutlined, CloseOutlined } from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

const Compliance = () => {
  const [complianceRecords, setComplianceRecords] = useState([
    {
      key: '1',
      id: 1,
      dealId: 1,
      dealTitle: 'Iron Ore Purchase Agreement',
      counterparty: 'Brazilian Mining Corp',
      regulations: ['IMCO Maritime Law', 'EU Sanctions List'],
      status: 'Compliant',
      lastChecked: '2025-09-15',
      checkedBy: 'compliance@openmineral.com'
    },
    {
      key: '2',
      id: 2,
      dealId: 2,
      dealTitle: 'Copper Sale Contract',
      counterparty: 'European Copper Ltd',
      regulations: ['EU Export Controls', 'OECD Guidelines'],
      status: 'Pending',
      lastChecked: '2025-09-10',
      checkedBy: 'system'
    }
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [form] = Form.useForm();

  const showModal = (record = null) => {
    setSelectedRecord(record);
    setIsModalVisible(true);
  };

  const handleOk = () => {
    form.validateFields().then(values => {
      // In a real implementation, this would submit the KYC request
      setIsModalVisible(false);
      form.resetFields();
      setSelectedRecord(null);
    });
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    form.resetFields();
    setSelectedRecord(null);
  };

  const handleApprove = (id) => {
    setComplianceRecords(complianceRecords.map(record => 
      record.id === id ? { ...record, status: 'Compliant' } : record
    ));
  };

  const handleReject = (id) => {
    setComplianceRecords(complianceRecords.map(record => 
      record.id === id ? { ...record, status: 'Non-Compliant' } : record
    ));
  };

  const getStatusTag = (status) => {
    switch (status) {
      case 'Compliant':
        return <Tag color="green">{status}</Tag>;
      case 'Non-Compliant':
        return <Tag color="red">{status}</Tag>;
      case 'Pending':
        return <Tag color="orange">{status}</Tag>;
      default:
        return <Tag>{status}</Tag>;
    }
  };

  const columns = [
    { title: 'Deal Title', dataIndex: 'dealTitle', key: 'dealTitle' },
    { title: 'Counterparty', dataIndex: 'counterparty', key: 'counterparty' },
    { 
      title: 'Regulations', 
      dataIndex: 'regulations', 
      key: 'regulations',
      render: regulations => regulations.join(', ')
    },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: status => getStatusTag(status)
    },
    { title: 'Last Checked', dataIndex: 'lastChecked', key: 'lastChecked' },
    { title: 'Checked By', dataIndex: 'checkedBy', key: 'checkedBy' },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            icon={<EyeOutlined />} 
            onClick={() => showModal(record)}
          >
            View
          </Button>
          {record.status === 'Pending' && (
            <>
              <Button 
                icon={<CheckOutlined />} 
                type="primary"
                onClick={() => handleApprove(record.id)}
              >
                Approve
              </Button>
              <Button 
                icon={<CloseOutlined />} 
                danger
                onClick={() => handleReject(record.id)}
              >
                Reject
              </Button>
            </>
          )}
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <Title level={2} style={{ margin: 0 }}>Compliance & KYC</Title>
          <Button 
            type="primary" 
            icon={<PlusOutlined />} 
            onClick={() => showModal()}
          >
            New KYC Request
          </Button>
        </div>

        <Table 
          dataSource={complianceRecords} 
          columns={columns} 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={selectedRecord ? "Compliance Details" : "New KYC Request"}
        visible={isModalVisible}
        onOk={selectedRecord ? handleCancel : handleOk}
        onCancel={handleCancel}
        width={600}
        footer={[
          <Button key="back" onClick={handleCancel}>
            Close
          </Button>,
          !selectedRecord && (
            <Button key="submit" type="primary" onClick={handleOk}>
              Submit Request
            </Button>
          )
        ]}
      >
        {selectedRecord ? (
          <div>
            <Descriptions title="Deal Information" column={1} bordered>
              <Descriptions.Item label="Deal ID">{selectedRecord.dealId}</Descriptions.Item>
              <Descriptions.Item label="Deal Title">{selectedRecord.dealTitle}</Descriptions.Item>
              <Descriptions.Item label="Counterparty">{selectedRecord.counterparty}</Descriptions.Item>
              <Descriptions.Item label="Regulations">{selectedRecord.regulations.join(', ')}</Descriptions.Item>
              <Descriptions.Item label="Status">{getStatusTag(selectedRecord.status)}</Descriptions.Item>
              <Descriptions.Item label="Last Checked">{selectedRecord.lastChecked}</Descriptions.Item>
              <Descriptions.Item label="Checked By">{selectedRecord.checkedBy}</Descriptions.Item>
            </Descriptions>
          </div>
        ) : (
          <Form form={form} layout="vertical">
            <Form.Item 
              name="fullName" 
              label="Full Name" 
              rules={[{ required: true, message: 'Please input full name!' }]}
            >
              <Input />
            </Form.Item>
            
            <Form.Item 
              name="dateOfBirth" 
              label="Date of Birth" 
              rules={[{ required: true, message: 'Please input date of birth!' }]}
            >
              <Input type="date" />
            </Form.Item>
            
            <Form.Item 
              name="nationality" 
              label="Nationality" 
              rules={[{ required: true, message: 'Please input nationality!' }]}
            >
              <Input />
            </Form.Item>
            
            <Form.Item 
              name="address" 
              label="Address" 
              rules={[{ required: true, message: 'Please input address!' }]}
            >
              <Input.TextArea rows={3} />
            </Form.Item>
            
            <Form.Item 
              name="idType" 
              label="Identification Type" 
              rules={[{ required: true, message: 'Please select ID type!' }]}
            >
              <Select>
                <Option value="passport">Passport</Option>
                <Option value="idCard">National ID Card</Option>
                <Option value="driverLicense">Driver's License</Option>
              </Select>
            </Form.Item>
            
            <Form.Item 
              name="idNumber" 
              label="Identification Number" 
              rules={[{ required: true, message: 'Please input ID number!' }]}
            >
              <Input />
            </Form.Item>
          </Form>
        )}
      </Modal>
    </div>
  );
};

export default Compliance;