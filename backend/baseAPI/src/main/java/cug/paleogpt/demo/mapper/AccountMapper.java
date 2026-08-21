package cug.paleogpt.demo.mapper;

import cug.paleogpt.demo.entity.Account;
import org.apache.ibatis.annotations.Mapper;

/**
 * 用户信息
 *
 * @author xw
 */
@Mapper
public interface AccountMapper {
    /**
     * 根据账号id获取账号名
     *
     * @param accountId 账号id
     * @return 账号名
     */
    public String getAccountName(Integer accountId);

    /**
     * 根据账号邮箱获取账号信息
     *
     * @param email 账号邮箱
     * @return 账号信息
     */
    public Account getAccountByEmail(String email);
}
