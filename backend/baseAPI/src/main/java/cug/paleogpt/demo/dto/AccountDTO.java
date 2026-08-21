package cug.paleogpt.demo.dto;

import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * 用户传输对象
 *
 * @author xw
 */
@Data
@NoArgsConstructor
public class AccountDTO {
    private String email;
    private String password;
    private Integer accountId;
    private String accountName;

    @Override
    public String toString() {
        return "AccountDTO{" +
                "email='" + email + '\'' +
                ", password='" + password + '\'' +
                ", accountId=" + accountId +
                ", accountName='" + accountName + '\'' +
                '}';
    }

    public String getEmail() {
        return email;
    }

    public String getPassword() {
        return password;
    }
}
