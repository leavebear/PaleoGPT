package cug.paleogpt.demo.service.impl;

import cug.paleogpt.demo.dto.AccountDTO;
import cug.paleogpt.demo.dto.MemberDTO;
import cug.paleogpt.demo.dto.ProjectDTO;
import cug.paleogpt.demo.common.CommonResult;
import cug.paleogpt.demo.entity.Member;
import cug.paleogpt.demo.entity.Project;
import cug.paleogpt.demo.mapper.AccountMapper;
import cug.paleogpt.demo.mapper.MemberMapper;
import cug.paleogpt.demo.mapper.ProjectMapper;
import cug.paleogpt.demo.service.ProjectService;
import io.minio.MakeBucketArgs;
import io.minio.MinioClient;
import io.minio.SetBucketPolicyArgs;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 项目库服务
 *
 * @author xw
 */
@Service
@Slf4j
public class ProjectServiceImpl implements ProjectService {
    @Autowired
    private AccountMapper accountMapper;

    @Autowired
    private ProjectMapper projectMapper;

    @Autowired
    private MemberMapper memberMapper;

    @Autowired
    private MinioClient minioClient;

    @Override
    @Transactional(rollbackFor = Exception.class)
    public CommonResult getAccountNameById(AccountDTO accountDTO) {
        String accountName = accountMapper.getAccountName(accountDTO.getAccountId());
        if(accountName==null){
            return CommonResult.success("不存在该用户");
        } else {
            //存在该用户
            HashMap<String, Object> data = new HashMap<>();
            data.put("accountName",accountName);
            return CommonResult.success(data);
        }
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public CommonResult createNewProject(ProjectDTO projectDTO) {
            Project project = new Project();
            project.setProjectName(projectDTO.getProName());
            project.setProjectDescription(projectDTO.getProDes());
            //添加project至MySQL
            projectMapper.insertProject(project);
            Integer projectId = project.getProjectId();
            //添加该项目的成员
            List<MemberDTO> members=projectDTO.getMembers();
            insertMembers(projectId, members);
            //创建bucket
            String bucketName = projectId + "bucket";
            try{
                createBucket(bucketName);
            }
            catch (Exception e){
                log.error("创建桶失败");
                throw new RuntimeException("创建桶失败");
            }
            return CommonResult.success();
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public CommonResult saveProjectInformation(ProjectDTO projectDTO) {
        //更新project的信息
        Integer proId = projectDTO.getProId();
        String projectName = projectDTO.getProName();
        String projectDescription = projectDTO.getProDes();
        projectMapper.updateProject(proId, projectName, projectDescription);
        //更新成员列表
        //删除原来的所有成员
        memberMapper.deleteMembers(proId);
        //添加新的成员
        for(MemberDTO memberDTO : projectDTO.getMembers()){
            Member member = new Member();
            member.setProjectId(proId);
            member.setMemberName(memberDTO.getMemName());
            member.setAuth(memberDTO.getAuth());
            memberMapper.insertMember(member);
        };
        return CommonResult.success();
    }

    @Override
    @Transactional(rollbackFor = Exception.class)
    public CommonResult getAllProjects(){
        HashMap<String, Object> data = new HashMap<>();
        ArrayList<ProjectDTO> projectDTOs = new ArrayList<>();
        //查询所有项目
        ArrayList<Project> projects = projectMapper.getProjects();
        for(Project project : projects){
            //查询项目的成员
            ArrayList<Member> members = memberMapper.getMembers(project.getProjectId());
            //封装返回值
            ArrayList<MemberDTO> memberDTOs = new ArrayList<>();
            for(Member member : members){
                MemberDTO memberDTO = new MemberDTO();
                memberDTO.setMemName(member.getMemberName());
                memberDTO.setAuth(member.getAuth());
                memberDTOs.add(memberDTO);
            }
            ProjectDTO projectDTO = new ProjectDTO();
            projectDTO.setProId(project.getProjectId());
            projectDTO.setProName(project.getProjectName());
            projectDTO.setProDes(project.getProjectDescription());
            projectDTO.setMembers(memberDTOs);
            projectDTOs.add(projectDTO);
        }
        data.put("projects", projectDTOs);
        return CommonResult.success(data);
    }

    /**
     * 批量插入成员
     *
     * @param projectId 项目id
     * @param members 成员列表
     */
    private void insertMembers(Integer projectId, List<MemberDTO> members){
            for (MemberDTO memberDTO : members) {
                //封装member
                Member member = new Member();
                member.setMemberName(memberDTO.getAccountName());
                member.setAuth(memberDTO.getAuth());
                member.setProjectId(projectId);
                memberMapper.insertMember(member);
            }
    }

    /**
     * 创建桶
     *
     * @param bucketName 桶名
     */
    private void createBucket(String bucketName) throws Exception{
        minioClient.makeBucket(MakeBucketArgs.builder()
                .bucket(bucketName)
                .build());
        //设置bucket的权限为public
        setBucketPolicy(bucketName);
    }

    /**
     * 设置bucket的权限炜public
     *
     * @param bucketName 桶名
     */
    private void setBucketPolicy(String bucketName) throws Exception{
        String policy = "{\"Version\":\"2012-10-17\"," +
                "\"Statement\":[" +
                "{\"Effect\":\"Allow\"," +
                "\"Principal\":{\"AWS\":[\"*\"]}," +
                "\"Action\":[\"s3:GetObject\"]," +
                "\"Resource\":[\"arn:aws:s3:::" + bucketName + "/*\"]}]" +
                "}";
        minioClient.setBucketPolicy(SetBucketPolicyArgs.builder()
                .bucket(bucketName)
                .config(policy)
                .build());
    }
}
