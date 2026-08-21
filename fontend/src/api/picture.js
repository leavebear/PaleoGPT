import request from '@/utils/request.js'

export const getImageExtraDataService = async (pdf_id) => {
    try {
        const data = { pdf_id };
        const response = await request.post('/api/project/imageExtra', data);
        return response;
    } catch (error) {
        console.error('获取图像信息失败:', error);
        throw error;
    }
}

export const updateImageExtraDataService = async (data) => {
    try {
        const response = await request.post(`/api/project/updateImage/`, data);
        return response;
    } catch (error) {
        console.error('更新图像信息失败:', error);
        throw error;
    }
};
