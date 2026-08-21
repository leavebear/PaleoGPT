package cug.paleogpt.demo.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 成员信息
 *
 * @author xw
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Member {
    /**
     * 项目Id
     */
    private Integer projectId;

    /**
     * 成员Id
     */
    private Integer memberId;

    /**
     * 成员权限
     */
    private String auth;

    /**
     * 成员名称
     */
    private String memberName;

    /**
     * 成员的账号Id
     */
    private Integer accountId;

    @Override
    public String toString()
    {
        return "Member{" +
                "projectId=" + projectId +
                ", memberId=" + memberId +
                ", auth='" + auth + '\'' +
                ", memberName='" + memberName + '\'' +
                ", accountId=" + accountId +
                '}';
    }
}
