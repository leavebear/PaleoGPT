package cug.paleogpt.demo.service;

import cug.paleogpt.demo.dto.DocumentDTO;
import cug.paleogpt.demo.common.CommonResult;

/**
 * 文档库服务
 *
 * @author xw
 */
public interface DocumentService {
    /**
     * 上传文档
     *
     * @param documentDTO 文档传输对象
     * @return 通用返回结果
     */
    public CommonResult uploadFile(DocumentDTO documentDTO);

    /**
     * 查询项目的所有文档
     *
     * @param proId 项目id
     * @return 通用返回结果
     */
    public CommonResult getAllDocumentsByProjectId(Integer proId);
}
