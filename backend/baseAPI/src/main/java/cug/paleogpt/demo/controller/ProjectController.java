package cug.paleogpt.demo.controller;

import cug.paleogpt.demo.dto.AccountDTO;
import cug.paleogpt.demo.dto.ProjectDTO;
import cug.paleogpt.demo.common.CommonResult;
import cug.paleogpt.demo.service.ProjectService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

/**
 * 项目库服务
 *
 * @author xw
 */
@RestController
@RequestMapping("/api/project")
public class ProjectController {
    @Autowired
    private ProjectService projectService;

    /**
     * 添加成员
     */
    @PostMapping("/addMem")
    public CommonResult getMemberName(@RequestBody AccountDTO accountDTO) {
        return projectService.getAccountNameById(accountDTO);
    }

    /**
     * 创建新项目
     */
    @PostMapping("/create")
    public CommonResult createProject(@RequestBody ProjectDTO projectDTO) {
        return projectService.createNewProject(projectDTO);
    }

    /**
     * 更改项目信息
     */
    @PostMapping("/saveDetailInfo")
    public CommonResult saveDetailInfo(@RequestBody ProjectDTO projectDTO) {
        return projectService.saveProjectInformation(projectDTO);
    }

    /**
     * 初始化项目库页面
     */
    @GetMapping("/init")
    public CommonResult getAllProjects() {
        return projectService.getAllProjects();
    }

    /**
     * 删除项目
     */
    @PostMapping("/delete")
    public CommonResult deleteProject(@RequestBody ProjectDTO projectDTO) {
        return null;
    }
}
