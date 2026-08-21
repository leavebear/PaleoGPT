package cug.paleogpt.demo.controller;

import cug.paleogpt.demo.dto.DocumentDTO;
import cug.paleogpt.demo.dto.DocumentsDTO;
import cug.paleogpt.demo.common.CommonResult;
import cug.paleogpt.demo.service.DocumentService;
import org.simpleframework.xml.Attribute;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 文档库服务
 *
 * @author xw
 */
@RestController
@RequestMapping("/api/document")
public class DocumentController {
    @Autowired
    private DocumentService documentService;

    /**
     * 上传文档
     */
    @PostMapping("/upload")
    public CommonResult uploadDocument(@Attribute DocumentDTO documentDTO){
        return documentService.uploadFile(documentDTO);
    }

    /**
     * 初始化文档库页面
     */
    @PostMapping("/init")
    public CommonResult getAllDocuments(@RequestBody DocumentsDTO documentsDTO){
        return documentService.getAllDocumentsByProjectId(documentsDTO.getProId());
    }
}
