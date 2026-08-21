package cug.paleogpt.demo.dto;

import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

/**
 * 文档传输对象
 *
 * @author xw
 */
@Data
public class  DocumentDTO {
    private MultipartFile file;
    private Integer proId;
    private String pdfName;
    private Double pdfSize;
    private String pdfUploadTime;
    private String pdfUploader;
    private String pdfUpdateTime;
    private String imageStatus;
    private String tableStatus;
    private String entityStatus;
    private String correctionStatus;
    private String approvalStatus;

    @Override
    public String toString()
    {
        return "DocumentDTO{" +
                "file=" + file +
                ", projectId=" + proId +
                ", pdfName='" + pdfName + '\'' +
                ", pdfSize=" + pdfSize +
                ", pdfUploadTime='" + pdfUploadTime + '\'' +
                ", pdfUploader='" + pdfUploader + '\'' +
                ", pdfUpdateTime='" + pdfUpdateTime + '\'' +
                ", imageStatus='"+ imageStatus + '\'' +
                ", tableStatus='"+ tableStatus + '\'' +
                ", entityStatus='"+ entityStatus + '\'' +
                ", correctionStatus='"+ correctionStatus + '\'' +
                ", approvalStatus='"+ approvalStatus + '\'' +
                '}';
    }
}
