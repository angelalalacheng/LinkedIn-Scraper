import React, { useState } from "react";
import { Button, Form, Input, Table, Spin } from "antd";
import { saveAs } from "file-saver";
import * as Papa from "papaparse";

function scraperAPI(email, password, url, setData, setLoading) {
  setLoading(true);
  fetch("http://127.0.0.1:8080/scrape", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password, url }),
  })
    .then((res) => {
      // Check if the response is not successful
      if (!res.ok) {
        // Parse the response body as JSON to get the error message
        return res.json().then((error) => {
          throw new Error(error.error || `HTTP error! status: ${res.status}`);
        });
      }
      return res.json();
    })
    .then((data) => {
      setData(data);
      setLoading(false);
    })
    .catch((error) => {
      alert(error);
      setLoading(false);
    });
}

function Homepage() {
  // State for storing the scraped data
  const [data, setData] = useState(null);
  // State for managing the spinner
  const [loading, setLoading] = useState(false);

  const onFinish = (values) => {
    alert("Please wait for a few seconds to scrape the data!");
    const { username, password, url } = values;
    scraperAPI(username, password, url, setData, setLoading);
  };

  const onFinishFailed = (errorInfo) => {
    alert("Please input your username, password, and LinkedIn Post URL!");
  };

  const downloadCSV = () => {
    const csv = Papa.unparse(data);
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    saveAs(blob, "data.csv");
  };

  const columns = [
    {
      title: "Name",
      dataIndex: "Name",
      key: "Name",
    },
    {
      title: "Current Position",
      dataIndex: "Current Position",
      key: "Current Position",
    },
    {
      title: "Profile Link",
      dataIndex: "Profile Link",
      key: "Profile Link",
      render: (text) => (
        <a href={text} target="_blank" rel="noopener noreferrer">
          {text}
        </a>
      ),
    },
    {
      title: "Comment",
      dataIndex: "Comment",
      key: "Comment",
    },
  ];

  return (
    <>
      <h1>LinkedIn Post Scraper</h1>
      <h3>Input your LinkedIn account and LinkedIn Post URL</h3>
      <Form
        name="basic"
        labelCol={{
          span: 8,
        }}
        wrapperCol={{
          span: 16,
        }}
        style={{
          maxWidth: 600,
        }}
        initialValues={{
          remember: true,
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        autoComplete="off"
      >
        <Form.Item
          label="Username"
          name="username"
          rules={[
            {
              required: true,
              message: "Please input your username!",
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Password"
          name="password"
          rules={[
            {
              required: true,
              message: "Please input your password!",
            },
          ]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item
          label="URL"
          name="url"
          rules={[
            {
              required: true,
              message: "Please input LinkedIn Post URL!",
            },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          wrapperCol={{
            offset: 8,
            span: 16,
          }}
        >
          <Button type="primary" htmlType="submit">
            Submit
          </Button>
        </Form.Item>
      </Form>
      <Spin spinning={loading}>
        {data && (
          <div>
            <h3>Scraped Data:</h3>
            <Table columns={columns} dataSource={data} rowKey="Name" />
            <Button type="primary" onClick={downloadCSV}>
              Download CSV
            </Button>
          </div>
        )}
      </Spin>
    </>
  );
}

export default Homepage;
