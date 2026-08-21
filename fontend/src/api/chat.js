import request from '@/utils/request.js';

export const submitQuestionService = async (post) => {
    try {
        const response = await request.post('/api/QAsystemStream', {post});
        console.log("Response from API:", response);
        return response;  // 返回响应数据，包括 session_id 和 status
    } catch (error) {
        console.error('提交问题失败:', error);
        throw error;  // 如果失败则抛出异常
    }
};

export const startSSEStreamService = (session_id) => {
    return new EventSource(`http://localhost:8000/api/QAsystemStream?session_id=${session_id}`);
};

export const waitForReferencesReady = async (session_id, maxRetries = 10, interval = 1000) => {
    let retries = 0;
  
    while (retries < maxRetries) {
      try {
        const response = await request.get(`/api/get_references?session_id=${session_id}`);
        const references = response.references;
  
        if (response.ready) {
            return references;
          }          
  
        await new Promise(resolve => setTimeout(resolve, interval)); // 💤 等待 interval 毫秒
        retries++;
      } catch (error) {
        console.error('轮询失败:', error);
        throw error;
      }
    }
  
    throw new Error('等待超时：未能获取到参考资料');
  };
  



// const API_BASE_URL = 'http://localhost:8000'

// export const createChatCompletion = async (messages) => {
//   const settingStore = useSettingStore()
//   const payload = {
//     model: settingStore.settings.model,
//     messages,
//     stream: settingStore.settings.stream,
//     max_tokens: settingStore.settings.maxTokens,
//     temperature: settingStore.settings.temperature,
//     top_p: settingStore.settings.topP,
//     top_k: settingStore.settings.topK,
//   }

//   const options = {
//     method: 'POST',
//     headers: {
//       Authorization: `Bearer ${settingStore.settings.apiKey}`,
//       'Content-Type': 'application/json',
//     },
//     body: JSON.stringify(payload),
//   }

//   try {
//     const startTime = Date.now() // 记录开始时间
//     const response = await fetch(`${API_BASE_URL}/api/QAsystem`, options)

//     if (!response.ok) {
//       throw new Error(`HTTP error! status: ${response.status}`)
//     }

//     if (settingStore.settings.stream) {
//       return response // 直接返回响应对象以支持流式读取
//     } else {
//       const data = await response.json()
//       const duration = (Date.now() - startTime) / 1000 // 使用本地计时
//       data.speed = (data.usage.completion_tokens / duration).toFixed(2)
//       return data
//     }
//   } catch (error) {
//     console.error('Chat API Error:', error)
//     throw error
//   }
// }
