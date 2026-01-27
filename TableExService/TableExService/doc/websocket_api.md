# PaleoGPTEntityExService WebSocket API 文档

## 概述

PaleoGPT提供了WebSocket接口，用于异步处理PDF文档。通过WebSocket可以获取PDF处理的实时状态更新，包括下载、处理、上传等各个环节的进度信息。

## 连接信息

- **WebSocket URL**: `ws://服务器地址:5000/ws`
- **协议**: WebSocket (ws://)
- **格式**: JSON

## 通信流程

```
客户端                                            服务器
   |                                                |
   |--- 建立WebSocket连接 ----------------------->   |
   |                                                |
   |--- 发送PDF处理参数 ------------------------->   |
   |                                                |
   |<-- 接收处理状态("开始处理PDF文件...") ---------  |
   |                                                |
   |<-- 接收状态更新("正在下载PDF文件...") ---------  |
   |                                                |
   |<-- 接收状态更新(处理中的各阶段状态) ------------  |
   |                                                |
   |<-- 接收最终结果(成功/失败) --------------------  |
   |                                                |
   |--- 关闭连接 -------------------------------->   |
```

## 请求格式

连接建立后，客户端需要发送一个JSON格式的消息，包含以下参数：

```json
{
  "pdf_id": "xxx", 
  "pdf_url": "xxx"
}
```

### 参数说明

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| pdf_id | 字符串 | 否 | PDF文档的唯一标识符，用于存储和索引。如果不提供，将使用配置中的默认值。 |
| pdf_url | 字符串 | 否 | PDF文档的URL地址，用于下载文档。如果不提供，将使用配置中的默认值。 |

## 响应格式

服务器会通过 WebSocket 连接发送 JSON格式的状态更新消息，格式如下：

```json
{
  "status": "状态类型",
  "message": "状态描述信息",
  "pdf_id": "文档唯一标识符(仅在最终结果中包含)"
}
```

### status 类型说明

| 状态类型 | 说明 |
|----------|------|
| processing | 表示处理正在进行中，message字段会包含当前的处理阶段 |
| warning | 表示出现警告但处理会继续进行 |
| success | 表示处理成功完成 |
| error | 表示处理过程中出现错误 |

### 处理阶段消息示例

1. **开始处理**:
   ```json
   {"status": "processing", "message": "开始处理PDF文件..."}
   ```

2. **下载阶段**:
   ```json
   {"status": "processing", "message": "正在下载PDF文件..."}
   ```

3. **处理阶段**:
   ```json
   {"status": "processing", "message": "正在处理PDF文件..."}
   ```

4. **完成准备阶段**:
   ```json
   {"status": "processing", "message": "处理完成，正在准备结果..."}
   ```

5. **处理成功**:
   ```json
   {"status": "success", "message": "PDF处理成功", "pdf_id": "01xybTest"}
   ```

6. **处理失败，pdf 处理失败**:
   ```json
   {"status": "error", "message": "PDF处理失败", "pdf_id": "01xybTest"}
   ```

7. **处理失败，pdf 下载失败**:
   ```json
   {"status": "error", "message": "处理失败: 下载PDF失败"}
   ```

## 错误处理

当处理过程中出现错误时，WebSocket 会发送一个包含错误信息的消息，然后继续保持连接。如果发生严重错误导致无法继续处理，连接可能会关闭。

客户端应当处理以下情况：
1. 接收到状态为 "error" 的消息
2. WebSocket 连接意外关闭
3. 长时间没有接收到状态更新

## 使用示例

### 前端 JavaScript 示例代码

```javascript
// 建立WebSocket连接
const socket = new WebSocket('ws://localhost:5000/ws');

// 连接建立后发送参数
socket.onopen = function(e) {
  console.log('WebSocket连接已建立');
  const params = {
    pdf_id: '01xybTest',
    pdf_url: 'https://example.com/sample.pdf'
  };
  
  socket.send(JSON.stringify(params));
};

// 接收服务器消息
socket.onmessage = function(event) {
  const response = JSON.parse(event.data);
  console.log(`收到状态更新: ${response.status} - ${response.message}`);
  
  // 根据状态更新UI
  updateProcessingStatus(response);
  
  // 如果处理完成，可以进行后续操作
  if (response.status === 'success') {
    console.log('PDF处理成功完成');
    // 进行后续操作，如显示结果链接等
  } else if (response.status === 'error') {
    console.error('PDF处理失败:', response.message);
    // 显示错误信息
  }
};

// 处理WebSocket错误
socket.onerror = function(error) {
  console.error('WebSocket错误:', error);
};

// 处理WebSocket连接关闭
socket.onclose = function(event) {
  if (event.wasClean) {
    console.log(`WebSocket连接已关闭，代码=${event.code} 原因=${event.reason}`);
  } else {
    console.error('WebSocket连接意外断开');
  }
};

// 更新处理状态的UI函数示例
function updateProcessingStatus(response) {
  const statusElement = document.getElementById('status-message');
  statusElement.textContent = response.message;
  
  // 根据状态更新UI样式
  if (response.status === 'processing') {
    statusElement.className = 'processing';
  } else if (response.status === 'success') {
    statusElement.className = 'success';
  } else if (response.status === 'error') {
    statusElement.className = 'error';
  } else if (response.status === 'warning') {
    statusElement.className = 'warning';
  }
}
```

### HTML示例

项目提供了一个测试页面，位于 `fontendTest/ws_test.html`。可以通过以下URL访问：

```
http://localhost:5000/fontendTest/ws_test.html
```

## 注意事项

1. WebSocket 连接可能因为网络问题、服务器重启等原因断开，客户端应实现自动重连机制
2. 建议设置适当的超时机制，当长时间没有收到状态更新时进行重试
3. 处理大型 PDF 文件时，整个过程可能需要较长时间，客户端UI应当给用户提供足够的反馈
4. 对于生产环境，建议使用安全的 WebSocket 连接 (wss://)

## 常见问题排查

1. **连接失败**: 检查服务器地址和端口是否正确，服务是否已启动
2. **参数错误**: 确保发送的 JSON 格式正确，包含必要的参数
3. **处理超时**: 对于大型 PDF 文件，处理时间可能较长，请耐心等待
4. **无法下载PDF**: 检查 PDF URL 是否可访问，服务器是否有外网连接 