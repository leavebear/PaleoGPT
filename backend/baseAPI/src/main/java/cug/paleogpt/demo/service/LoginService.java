package cug.paleogpt.demo.service;

import cug.paleogpt.demo.dto.AccountDTO;
import cug.paleogpt.demo.common.CommonResult;

/**
 * 登录服务
 *
 * @author xw
 */
public interface LoginService {
    /**
     * 账号和密码登录
     *
     * @param accountDTO 账号传输对象
     * @return 通用返回结果
     */
    public CommonResult checkLoginByPwd(AccountDTO accountDTO);
}
