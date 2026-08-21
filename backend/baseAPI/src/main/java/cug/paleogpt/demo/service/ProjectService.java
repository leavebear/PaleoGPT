package cug.paleogpt.demo.service;

import cug.paleogpt.demo.dto.AccountDTO;
import cug.paleogpt.demo.dto.ProjectDTO;
import cug.paleogpt.demo.common.CommonResult;

/**
 * 项目库服务
 *
 * @author xw
 */
public interface ProjectService {
    /**
     * 通过id查询用户名
     *
     * @param accountDTO 用户传输对象
     * @return 通用返回结果
     */
    public CommonResult getAccountNameById(AccountDTO accountDTO);

    /**
     * 创建新项目
     *
     * @param projectDTO 项目传输对象
     * @return 通用返回结果
     */
    public CommonResult createNewProject(ProjectDTO projectDTO);

    /**
     * 保存项目信息
     *
     * @param projectDTO 项目传输对象
     * @return 通用返回结果
     */
    public CommonResult saveProjectInformation(ProjectDTO projectDTO);

    /**
     * 获取所有项目的信息
     *
     * @return 通用返回结果
     */
    public CommonResult getAllProjects();
}
