export const messageHandler = {
  formatMessage(role, content, reasoning_content, files = []) {
    return {
      id: Date.now(),
      role,
      content,
      reasoning_content,
      files,
      completion_tokens: 0,
      speed: 0,
      loading: false,
    }
  },

  // 处理流式响应
  async handleStreamResponse(sseUrl, updateCallback) {
    const eventSource = new EventSource(sseUrl);  // 使用 EventSource 打开流

    let accumulatedContent = ''; // 存储累积的回答内容
    let accumulatedReasoning = ''; // 存储累积的推理内容
    let startTime = Date.now();  // 记录开始时间

    // 监听 EventSource 的 onmessage 事件来处理流数据
    eventSource.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);  // 解析每条流数据

        if (data.error) {
          console.error("错误:", data.error);
          eventSource.close();  // 出现错误时关闭流
          return;
        }

        const content = data.choices[0].delta.content || '';  // 获取内容
        const reasoning = data.choices[0].delta.reasoning_content || '';  // 获取推理内容

        // 累积内容
        accumulatedContent += content;
        accumulatedReasoning += reasoning;

        // 通过回调更新消息
        updateCallback(
          accumulatedContent,
          accumulatedReasoning,
          data.usage?.completion_tokens || 0,  // 传递消耗的token
          ((data.usage?.completion_tokens || 0) / ((Date.now() - startTime) / 1000)).toFixed(2)  // 计算token速率
        );
      } catch (error) {
        console.error("JSON 解析失败:", error, "收到的数据:", e.data);
      }
    };

    // 错误处理
    eventSource.onerror = (e) => {
      console.error("SSE 连接错误:", e);
      eventSource.close();  // 出现错误时关闭流
    };
  },


  // 处理非流式响应
  handleNormalResponse(response, updateCallback) {
    updateCallback(
      response.choices[0].message.content,
      response.choices[0].message.reasoning_content || '',
      response.usage.completion_tokens,
      response.speed,
    )
  },

  // 统一的响应处理函数
  async handleResponse(response, isStream, updateCallback) {
    if (isStream) {
      await this.handleStreamResponse(response, updateCallback)
    } else {
      this.handleNormalResponse(response, updateCallback)
    }
  },
}
