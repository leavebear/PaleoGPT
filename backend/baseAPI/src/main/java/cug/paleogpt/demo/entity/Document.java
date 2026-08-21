package cug.paleogpt.demo.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 文档信息
 *
 * @author xw
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Document {
    /**
     * 项目Id
     */
    private Integer projectId;

    /**
     * 文档Id
     */
    private String pdfId;

    /**
     * 文档名称
     */
    private String pdfName;

    /**
     * 文档大小（mb）
     */
    private Double pdfSize;

    /**
     * 文档上传时间
     */
    private String pdfUploadTime;

    /**
     * 文档上传者
     */
    private String pdfUploader;

    /**
     * 文档更新时间
     */
    private String pdfUpdateTime;

    /**
     * 图片抽取状态
     */
    private String imageStatus;

    /**
     * 表格抽取状态
     */
    private String tableStatus;

    /**
     * 实体抽取状态
     */
    private String entityStatus;

    /**
     * 文档校准状态
     */
    private String correctionStatus;

    /**
     * 文档审核状态
     */
    private String approvalStatus;

    /**
     * 文档访问地址
     */
    private String pdfUrl;

    @Override
    public String toString()
    {
        return "Document{" +
                "projectId=" + projectId +
                ", pdfId='" + pdfId + '\'' +
                ", pdfName='" + pdfName + '\'' +
                ", pdfSize=" + pdfSize +
                ", pdfUploadTime='" + pdfUploadTime + '\'' +
                ", pdfUploader='" + pdfUploader + '\'' +
                ", pdfUpdateTime='" + pdfUpdateTime + '\'' +
                ",imageStatus='" + imageStatus + '\'' +
                ",tableStatus='" + tableStatus + '\'' +
                ",entityStatus='" + entityStatus + '\'' +
                ",correctionStatus='" + correctionStatus + '\'' +
                ",approvalStatus='" + approvalStatus + '\'' +
                ",pdfUrl='" + pdfUrl + '\'' +
                '}';
    }
}
