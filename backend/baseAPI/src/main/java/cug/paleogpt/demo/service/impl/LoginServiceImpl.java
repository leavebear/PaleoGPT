package cug.paleogpt.demo.service.impl;

import com.alibaba.fastjson.JSON;
import cug.paleogpt.demo.util.JedisUtil;
import cug.paleogpt.demo.dto.AccountDTO;
import cug.paleogpt.demo.common.CommonResult;
import cug.paleogpt.demo.entity.Account;
import cug.paleogpt.demo.mapper.AccountMapper;
import cug.paleogpt.demo.service.LoginService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.HashMap;

/**
 * 登录服务
 *
 * @author xw
 */
@Service
@Slf4j
public class LoginServiceImpl implements LoginService {

    @Autowired
    private AccountMapper accountMapper;

    /**
     * 根据账号和密码登录
     *
     * @param accountDTO 账号传输对象
     * @return 通用返回结果
     */
    @Override
    public CommonResult checkLoginByPwd(AccountDTO accountDTO){
        //获取email和password
        String email = accountDTO.getEmail();
        String password = accountDTO.getPassword();
        //查询用户数据
        Account account = queryAccountInfo(email);
        return checkLogin(account, password);
    }

    /**
     * 检查能否登录
     *
     * @param account  用户账号信息
     * @param password 用户输入的密码
     * @return 通用返回结果
     */
    private CommonResult checkLogin(Account account, String password) {
        if(account == null){
            return CommonResult.success("不存在账号");
        } else{
            HashMap<String, Object> data = new HashMap<>();
            if (password.equals(account.getPassword())) {
                //设置缓存
                JedisUtil.set(account.getEmail(), JSON.toJSONString(account));
                data.put("accountId", account.getAccountId());
                data.put("accountName", account.getAccountName());
                return CommonResult.success(data);
            } else {
                return CommonResult.success("密码错误");
            }
        }
    }

    /**
     * 查询缓存
     *
     * @param email 邮箱
     * @return 账号信息
     */
    private Account queryCache(String email){
        String result = JedisUtil.get(email);
        if (result != null){
            return JSON.parseObject(result, Account.class);
        } else{
            return null;
        }
    }

    /**
     * 查询数据库
     *
     * @param email 邮箱
     * @return 账号信息
     */
    private Account queryDataBase(String email){
        return accountMapper.getAccountByEmail(email);
    }

    /**
     * 查询账号信息
     *
     * @param email 邮箱
     * @return 账号信息
     */
    private Account queryAccountInfo(String email){
        Account account = queryCache(email);
        if(account != null){
            return account;
        } else{
            account = queryDataBase(email);
            return account;
        }
    }

}
