import request from '@/utils/request.js'

export const getMarkContentDataService = async (pdf_id) => {
    try {
        const data = { pdf_id };
        const response = await request.post('/api/project/entityExtra', data);
        return response;
    } catch (error) {
        console.error('请求失败:', error);
        throw error;
    }
};

export const updateMarkContentDataService = async (updatedData) => {
    try {
        const response = await request.post('/api/project/updateEntity', updatedData);
      return response;  // 返回响应数据
    } catch (error) {
        console.error('请求失败:', error);
        throw error;  // 如果失败则抛出异常
    }
};