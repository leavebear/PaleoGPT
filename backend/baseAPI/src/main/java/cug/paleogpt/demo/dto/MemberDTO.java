package cug.paleogpt.demo.dto;

import cug.paleogpt.demo.entity.Member;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 成员传输对象
 *
 * @author xw
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class MemberDTO {
    private String memName;
    private String auth;
    private Integer proId;
    private String accountName;

    public MemberDTO(Member member) {
        this.memName = member.getMemberName();
        this.auth = member.getAuth();
        this.proId = member.getProjectId();
    }

    @Override
    public String toString() {
        return "MemberDTO{" +
                "memName='" + memName + '\'' +
                ", auth='" + auth + '\'' +
                ", projectId=" + proId +
                ", accountName='" + accountName + '\'' +
                '}';
    }
}
