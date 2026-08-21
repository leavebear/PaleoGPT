package cug.paleogpt.demo.mapper;

import cug.paleogpt.demo.entity.Member;
import org.apache.ibatis.annotations.Mapper;

import java.util.ArrayList;

/**
 * 成员信息
 *
 * @author xw
 */
@Mapper
public interface MemberMapper {
    /**
     * 插入成员信息
     *
     * @param member 成员信息
     */
    void insertMember(Member member);

    /**
     * 删除成员信息
     *
     * @param projectId 项目id
     */
    void deleteMembers(Integer projectId);

    /**
     * 根据项目id获取成员信息
     *
     * @param projectId 项目id
     * @return 成员信息
     */
    ArrayList<Member> getMembers(Integer projectId);
}
