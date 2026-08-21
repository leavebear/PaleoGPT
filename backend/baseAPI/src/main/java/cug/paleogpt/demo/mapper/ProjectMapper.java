package cug.paleogpt.demo.mapper;

import cug.paleogpt.demo.entity.Project;
import org.apache.ibatis.annotations.Mapper;

import java.util.ArrayList;

/**
 * 项目信息
 *
 * @author xw
 */
@Mapper
public interface ProjectMapper {
    /**
     * 插入项目信息
     *
     * @param project 项目信息
     */
    public Integer insertProject(Project project);

    /**
     * 更新项目信息
     *
     * @param projectId 项目ID
     * @param projectName 项目名称
     * @param projectDescription 项目描述
     */
    public void updateProject(Integer projectId, String projectName, String projectDescription);

    /**
     * 获取所欲项目信息
     * @return 项目信息
     */
    public ArrayList<Project> getProjects();
}
