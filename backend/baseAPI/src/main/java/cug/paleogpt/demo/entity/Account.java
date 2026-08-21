package cug.paleogpt.demo.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 用户信息
 *
 * @author xw
 */
@Data
@AllArgsConstructor
@NoArgsConstructor
public class Account {
    /**
     * 用户Id
     */
    private Integer accountId;

    /**
     * 邮箱
     */
    private String email;

    /**
     * 密码
     */
    private String password;

    /**
     * 用户名
     */
    private String accountName;

    @Override
    public String toString()
    {
        return "Account{" +
                "accountId=" + accountId +
                ", email='" + email + '\'' +
                ", password='" + password + '\'' +
                ", accountName='" + accountName + '\'' +
                '}';
    }
}
