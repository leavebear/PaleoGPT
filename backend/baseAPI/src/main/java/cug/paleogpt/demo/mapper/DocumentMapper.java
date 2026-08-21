package cug.paleogpt.demo.mapper;

import cug.paleogpt.demo.entity.Document;
import org.apache.ibatis.annotations.Mapper;

import java.util.ArrayList;

/**
 * 文档信息
 *
 * @author xw
 */
@Mapper
public interface DocumentMapper {
    /**
     * 插入文档信息
     *
     * @param document 文档信息
     */
    public void insertDocument(Document document);

    /**
     * 根据项目Id和文档名称获取文档信息
     *
     * @param projectId 项目id
     * @param pdfName 文档名称
     * @return 文档信息
     */
    public Document getDocumentByProjectIdAndPdfName(Integer projectId,String pdfName);

    /**
     * 根据项目id查询文档信息
     *
     * @param proId 项目id
     * @return 文档信息
     */
    public ArrayList<Document> getDocuments(Integer proId);

}
