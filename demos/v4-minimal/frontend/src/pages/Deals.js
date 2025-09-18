import React, { useState, useEffect } from 'react';
import { 
  Table, 
  Button, 
  Modal, 
  Form, 
  Input, 
  InputNumber, 
  Select, 
  Space, 
  Typography,
  Card,
  message,
  Popconfirm,
  Spin,
  Alert,
  Tag
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, ReloadOutlined } from '@ant-design/icons';
import apiService from '../services/api';

const { Title } = Typography;
const { Option } = Select;

const Deals = () => {
  const [deals, setDeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingDeal, setEditingDeal] = useState(null);
  const [submitLoading, setSubmitLoading] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    loadDeals();
  }, []);

  const loadDeals = async () => {
    try {
      setLoading(true);
      const dealsData = await apiService.getDeals();
      setDeals(dealsData);
    } catch (error) {
      console.error('Failed to load deals:', error);
      message.error('Failed to load deals');
    } finally {
      setLoading(false);
    }
  };

  const showModal = (deal = null) => {
    setEditingDeal(deal);
    if (deal) {
      form.setFieldsValue({
        title: deal.title,
        description: deal.description,
        commodity: deal.commodity,
        quantity: deal.quantity,
        price: deal.price,
        counterparty: deal.counterparty
      });
    } else {
      form.resetFields();
    }
    setModalVisible(true);
  };

  const handleSubmit = async (values) => {
    try {
      setSubmitLoading(true);
      
      if (editingDeal) {
        // Update existing deal
        await apiService.updateDeal(editingDeal.id, values);
        message.success('Deal updated successfully');
      } else {
        // Create new deal
        await apiService.createDeal(values);
        message.success('Deal created successfully');
      }
      
      setModalVisible(false);
      form.resetFields();
      setEditingDeal(null);
      loadDeals(); // Refresh the list
      
    } catch (error) {
      console.error('Failed to save deal:', error);
      message.error('Failed to save deal');
    } finally {
      setSubmitLoading(false);
    }
  };

  const handleDelete = async (dealId) => {
    try {
      await apiService.deleteDeal(dealId);
      message.success('Deal deleted successfully');
      loadDeals(); // Refresh the list
    } catch (error) {
      console.error('Failed to delete deal:', error);
      message.error('Failed to delete deal');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'green';
      case 'pending': return 'orange';
      case 'completed': return 'blue';
      case 'draft': return 'default';
      default: return 'default';
    }
  };

  const columns = [
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      render: (text) => <strong>{text}</strong>
    },
    {
      title: 'Commodity',
      dataIndex: 'commodity',
      key: 'commodity'
    },
    {
      title: 'Quantity',
      dataIndex: 'quantity',
      key: 'quantity',
      render: (quantity) => quantity.toLocaleString()
    },
    {
      title: 'Price per Unit',
      dataIndex: 'price',
      key: 'price',
      render: (price) => `$${price.toFixed(2)}`
    },
    {
      title: 'Total Value',
      key: 'total_value',
      render: (_, record) => `$${(record.quantity * record.price).toLocaleString()}`
    },
    {
      title: 'Counterparty',
      dataIndex: 'counterparty',
      key: 'counterparty'
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={getStatusColor(status)}>
          {status.toUpperCase()}
        </Tag>
      )
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date) => new Date(date).toLocaleDateString()
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            icon={<EditOutlined />} 
            onClick={() => showModal(record)}
            type="link"
            size="small"
          >
            Edit
          </Button>
          <Popconfirm
            title="Are you sure you want to delete this deal?"
            onConfirm={() => handleDelete(record.id)}
            okText="Yes"
            cancelText="No"
          >
            <Button 
              icon={<DeleteOutlined />}
              type="link" 
              danger
              size="small"
            >
              Delete
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          marginBottom: '24px' 
        }}>
          <Title level={2} style={{ margin: 0 }}>
            Deal Management
          </Title>
          <Space>
            <Button 
              icon={<ReloadOutlined />}
              onClick={loadDeals}
              loading={loading}
            >
              Refresh
            </Button>
            <Button 
              type="primary" 
              icon={<PlusOutlined />} 
              onClick={() => showModal()}
            >
              Create New Deal
            </Button>
          </Space>
        </div>

        {loading ? (
          <div style={{ textAlign: 'center', padding: '50px' }}>
            <Spin size="large" />
            <p style={{ marginTop: '16px' }}>Loading deals...</p>
          </div>
        ) : (
          <Table 
            dataSource={deals} 
            columns={columns} 
            rowKey="id"
            pagination={{ 
              pageSize: 10,
              showSizeChanger: true,
              showQuickJumper: true,
              showTotal: (total, range) => 
                `${range[0]}-${range[1]} of ${total} deals`
            }}
            scroll={{ x: 1200 }}
          />
        )}

        <Alert
          message="Real-time API Integration"
          description="All deal operations are connected to the backend API. Data persists during the session and updates in real-time."
          type="info"
          showIcon
          style={{ marginTop: '16px' }}
        />
      </Card>

      <Modal
        title={editingDeal ? "Edit Deal" : "Create New Deal"}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
          setEditingDeal(null);
        }}
        footer={null}
        width={600}
      >
        <Form 
          form={form} 
          layout="vertical" 
          onFinish={handleSubmit}
        >
          <Form.Item 
            name="title" 
            label="Deal Title" 
            rules={[{ required: true, message: 'Please input deal title!' }]}
          >
            <Input placeholder="Enter deal title" />
          </Form.Item>
          
          <Form.Item 
            name="description" 
            label="Description"
            rules={[{ required: true, message: 'Please input description!' }]}
          >
            <Input.TextArea rows={3} placeholder="Enter deal description" />
          </Form.Item>
          
          <Form.Item 
            name="commodity" 
            label="Commodity" 
            rules={[{ required: true, message: 'Please select commodity!' }]}
          >
            <Select placeholder="Select commodity">
              <Option value="Iron Ore">Iron Ore</Option>
              <Option value="Copper">Copper</Option>
              <Option value="Gold">Gold</Option>
              <Option value="Silver">Silver</Option>
              <Option value="Zinc">Zinc</Option>
              <Option value="Lead">Lead</Option>
              <Option value="Aluminum">Aluminum</Option>
              <Option value="Nickel">Nickel</Option>
            </Select>
          </Form.Item>
          
          <Form.Item 
            name="quantity" 
            label="Quantity" 
            rules={[
              { required: true, message: 'Please input quantity!' },
              { type: 'number', min: 1, message: 'Quantity must be greater than 0!' }
            ]}
          >
            <InputNumber 
              style={{ width: '100%' }} 
              placeholder="Enter quantity"
              formatter={(value) => `${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={(value) => value.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>
          
          <Form.Item 
            name="price" 
            label="Price per Unit ($)" 
            rules={[
              { required: true, message: 'Please input price!' },
              { type: 'number', min: 0.01, message: 'Price must be greater than 0!' }
            ]}
          >
            <InputNumber 
              style={{ width: '100%' }} 
              placeholder="Enter price per unit"
              precision={2}
              formatter={(value) => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={(value) => value.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>
          
          <Form.Item 
            name="counterparty" 
            label="Counterparty" 
            rules={[{ required: true, message: 'Please input counterparty!' }]}
          >
            <Input placeholder="Enter counterparty name" />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>
                Cancel
              </Button>
              <Button 
                type="primary" 
                htmlType="submit"
                loading={submitLoading}
              >
                {editingDeal ? 'Update Deal' : 'Create Deal'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Deals;