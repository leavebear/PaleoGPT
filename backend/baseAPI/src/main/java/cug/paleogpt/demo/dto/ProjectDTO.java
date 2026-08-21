package cug.paleogpt.demo.dto;

import cug.paleogpt.demo.entity.Project;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;

/**
 * 项目传输对象
 *
 * @author xw
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class ProjectDTO {
    private Integer proId;
    private String proName;
    private String proDes;
    private ArrayList<MemberDTO> members;

    public ProjectDTO(Project project) {
        this.proId = project.getProjectId();
        this.proName = project.getProjectName();
        this.proDes = project.getProjectDescription();
    }

    @Override
    public String toString() {
        return "ProjectDTO{" +
                "projectId=" + proId +
                ", proName='" + proName + '\'' +
                ", proDes='" + proDes + '\'' +
                ", members=" + members +
                '}';
    }
}
