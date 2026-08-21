package cug.paleogpt.demo.controller;

import cug.paleogpt.demo.dto.AccountDTO;
import cug.paleogpt.demo.common.CommonResult;
import cug.paleogpt.demo.service.LoginService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * 登录服务
 *
 * @author xw
 */
@RestController
@RequestMapping("/api/login")
public class LoginController {
    @Autowired
    private LoginService loginService;

    /**
     * 账号密码登录
     */
    @PostMapping("/pwd")
    public CommonResult checkLoginByPwd(@RequestBody AccountDTO accountDTO){
        return loginService.checkLoginByPwd(accountDTO);
        // String email = accountDTO.getEmail();
        // String password = accountDTO.getPassword();

        // // 这里可以打印看看是不是接收到了
        // System.out.println("Email: " + email);
        // System.out.println("Password: " + password);

        // // 登录验证逻辑（比如查数据库）...
        // if ("admin@163.com".equals(email) && "admin".equals(password)) {
        //     return CommonResult.success("登录成功");
        // } else {
        //     return CommonResult.failed("账号或密码错误");
        // }
    }
}
