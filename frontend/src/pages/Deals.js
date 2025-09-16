import React, { useState } from 'react';
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
  Card
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';

const { Title } = Typography;
const { Option } = Select;

const Deals = () => {
  const [deals, setDeals] = useState([
    {
      key: '1',
      id: 1,
      title: 'Iron Ore Purchase Agreement',
      description: 'Purchase of iron ore from Brazilian supplier',
      commodity: 'Iron Ore',
      quantity: 10000,
      price: 85.50,
      counterparty: 'Brazilian Mining Corp',
      status: 'Active'
    },
    {
      key: '2',
      id: 2,
      title: 'Copper Sale Contract',
      description: 'Sale of copper concentrate to European smelter',
      commodity: 'Copper',
      quantity: 5000,
      price: 9200,
      counterparty: 'European Copper Ltd',
      status: 'Pending'
    }
  ]);

  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingDeal, setEditingDeal] = useState(null);
  const [form] = Form.useForm();

  const showModal = (deal = null) => {
    setEditingDeal(deal);
    if (deal) {
      form.setFieldsValue(deal);
    } else {
      form.resetFields();
    }
    setIsModalVisible(true);
  };

  const handleOk = () => {
    form.validateFields().then(values => {
      if (editingDeal) {
        // Update existing deal
        setDeals(deals.map(deal => 
          deal.id === editingDeal.id ? { ...deal, ...values } : deal
        ));
      } else {
        // Add new deal
        const newDeal = {
          key: String(deals.length + 1),
          id: deals.length + 1,
          ...values,
          status: 'Draft'
        };
        setDeals([...deals, newDeal]);
      }
      setIsModalVisible(false);
      form.resetFields();
      setEditingDeal(null);
    });
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    form.resetFields();
    setEditingDeal(null);
  };

  const handleDelete = (id) => {
    setDeals(deals.filter(deal => deal.id !== id));
  };

  const columns = [
    { title: 'Title', dataIndex: 'title', key: 'title' },
    { title: 'Commodity', dataIndex: 'commodity', key: 'commodity' },
    { title: 'Quantity', dataIndex: 'quantity', key: 'quantity' },
    { title: 'Price', dataIndex: 'price', key: 'price', render: price => `$${price}` },
    { title: 'Counterparty', dataIndex: 'counterparty', key: 'counterparty' },
    { title: 'Status', dataIndex: 'status', key: 'status' },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button 
            icon={<EditOutlined />} 
            onClick={() => showModal(record)}
          >
            Edit
          </Button>
          <Button 
            icon={<DeleteOutlined />} 
            danger 
            onClick={() => handleDelete(record.id)}
          >
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Card>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
          <Title level={2} style={{ margin: 0 }}>Deal Management</Title>
          <Button 
            type="primary" 
            icon={<PlusOutlined />} 
            onClick={() => showModal()}
          >
            Create New Deal
          </Button>
        </div>

        <Table 
          dataSource={deals} 
          columns={columns} 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={editingDeal ? "Edit Deal" : "Create New Deal"}
        visible={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item 
            name="title" 
            label="Deal Title" 
            rules={[{ required: true, message: 'Please input deal title!' }]}
          >
            <Input />
          </Form.Item>
          
          <Form.Item 
            name="description" 
            label="Description"
          >
            <Input.TextArea rows={3} />
          </Form.Item>
          
          <Form.Item 
            name="commodity" 
            label="Commodity" 
            rules={[{ required: true, message: 'Please select commodity!' }]}
          >
            <Select>
              <Option value="Iron Ore">Iron Ore</Option>
              <Option value="Copper">Copper</Option>
              <Option value="Gold">Gold</Option>
              <Option value="Silver">Silver</Option>
              <Option value="Zinc">Zinc</Option>
              <Option value="Lead">Lead</Option>
            </Select>
          </Form.Item>
          
          <Form.Item 
            name="quantity" 
            label="Quantity" 
            rules={[{ required: true, message: 'Please input quantity!' }]}
          >
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item 
            name="price" 
            label="Price per Unit" 
            rules={[{ required: true, message: 'Please input price!' }]}
          >
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item 
            name="counterparty" 
            label="Counterparty" 
            rules={[{ required: true, message: 'Please input counterparty!' }]}
          >
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Deals;