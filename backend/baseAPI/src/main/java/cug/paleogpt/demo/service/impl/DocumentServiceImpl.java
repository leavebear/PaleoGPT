package cug.paleogpt.demo.service.impl;
import cug.paleogpt.demo.common.Constants;
import cug.paleogpt.demo.dto.DocumentDTO;
import cug.paleogpt.demo.common.CommonResult;
import cug.paleogpt.demo.entity.Document;
import cug.paleogpt.demo.mapper.DocumentMapper;
import cug.paleogpt.demo.service.DocumentService;
import io.minio.MinioClient;
import io.minio.PutObjectArgs;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.multipart.MultipartFile;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.UUID;

/**
 * 文档库服务
 *
 * @author xw
 */
@Service
@Slf4j
public class DocumentServiceImpl implements DocumentService {
    @Autowired
    private DocumentMapper documentMapper;

    @Autowired
    private MinioClient minioClient;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public CommonResult uploadFile(DocumentDTO documentDTO){
        //封装数据
        Document document = makeDocument(documentDTO);
        String bucketName = documentDTO.getProId().toString()+"bucket";
        //检测文件是否存在
        if(documentMapper.getDocumentByProjectIdAndPdfName(document.getProjectId(), document.getPdfName()) != null) {
            return CommonResult.success("文件已经存在");
        } else {
            documentMapper.insertDocument(document);
            try {
                uploadFileToMinio(bucketName, documentDTO.getFile());
            } catch (Exception e){
                log.error("上传文档失败");
                throw new RuntimeException("上传文档失败");
            }
            HashMap<String, Object> data = new HashMap<>();
            data.put("pdfId", document.getPdfId());
            data.put("pdfName", document.getPdfName());
            data.put("pdfSize", document.getPdfSize());
            data.put("pdfUploadTime", document.getPdfUploadTime());
            data.put("pdfUrl", document.getPdfUrl());
            return CommonResult.success("上传成功", data);
        }
    }

    @Override
    public CommonResult getAllDocumentsByProjectId(Integer proId) {
        ArrayList<Document> documents = documentMapper.getDocuments(proId);
        HashMap<String, Object> data = new HashMap<>();
        data.put("fileMetaDataList", documents);
        return CommonResult.success(data);
    }

    /**
     * 封装文档信息
     * @param documentDTO 文件传输对象
     * @return 文档对象
     */
    private Document makeDocument(DocumentDTO documentDTO){
        Document document = new Document();
        UUID pdfId = UUID.randomUUID();
        document.setPdfId(pdfId.toString());
        document.setProjectId(documentDTO.getProId());
        document.setPdfUploader(documentDTO.getPdfUploader());
        String pdfName = documentDTO.getFile().getOriginalFilename();
        document.setPdfName(pdfName);
        Double pdfSize = documentDTO.getFile().getSize()/(1024.0 * 1024.0);
        document.setPdfSize(pdfSize);
        LocalDate pdfUploadTime = LocalDate.now();
        document.setPdfUploadTime(pdfUploadTime.toString());
        document.setPdfUpdateTime(pdfUploadTime.toString());
        document.setImageStatus(documentDTO.getImageStatus());
        document.setTableStatus(documentDTO.getTableStatus());
        document.setEntityStatus(documentDTO.getEntityStatus());
        document.setCorrectionStatus(documentDTO.getCorrectionStatus());
        document.setApprovalStatus(documentDTO.getApprovalStatus());
        String bucketName = documentDTO.getProId().toString()+"bucket";
        String pdfUrl = Constants.MINIO_URL + "/"+bucketName+"/"+documentDTO.getFile().getOriginalFilename();
        document.setPdfUrl(pdfUrl);
        return document;
    }

    /**
     *  上传文件到minio
     * @param bucketName 桶名
     * @param file 待上传文件
     **/
    private void uploadFileToMinio(String bucketName,MultipartFile file) throws Exception {
        minioClient.putObject(PutObjectArgs.builder()
                .bucket(bucketName)
                .object(file.getOriginalFilename())
                .stream(file.getInputStream(), file.getSize(), -1)
                .contentType(file.getContentType())
                .build());
    }
}
