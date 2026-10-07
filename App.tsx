import React from 'react';
import { Transfer } from 'antd';

export default function App() {
  return (
    <Transfer
      dataSource={[{ key: 'a', title: 'Alpha' }]}
      targetKeys={[]}
      selectedKeys={[]}
      selectAllLabels={[0, 0]}
      render={(item) => item.title}
    />
  );
}
