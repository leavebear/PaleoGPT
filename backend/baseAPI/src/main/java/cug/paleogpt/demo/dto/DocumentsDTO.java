package cug.paleogpt.demo.dto;

import lombok.Data;
import java.util.ArrayList;

/**
 * 文档传输对象
 *
 * @author xw
 */
@Data
public class DocumentsDTO {
    private ArrayList<Integer> files;
    private Integer proId;

    @Override
    public String toString(){
        return "DocumentsDTO{" +
                "files=" + files +
                ", projectId=" + proId +
                '}';
    }
}
