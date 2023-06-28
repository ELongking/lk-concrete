package com.longking.concrete.controller;

import cn.hutool.core.util.ObjectUtil;
import com.longking.concrete.common.CommonResult;
import com.longking.concrete.model.UserInfo;
import com.longking.concrete.service.UserHandleService;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiImplicitParams;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;

import javax.servlet.http.HttpServletRequest;
import java.util.Date;

@RestController
@RequestMapping("/uc")
public class UserCenterMapper {
    @Autowired
    UserHandleService userHandleService;
    @Autowired
    StringRedisTemplate stringRedisTemplate;

    @RequestMapping(value = "/changePwd", method = RequestMethod.POST)
    @ResponseBody
    @ApiImplicitParams({
            @ApiImplicitParam(name = "password", value = "输入的原密码", required = true),
            @ApiImplicitParam(name = "newPassword", value = "输入的新密码", required = true),
            @ApiImplicitParam(name = "request", value = "请求体", required = true)
    })
    @ApiOperation(value = "用户修改密码")
    public CommonResult<UserInfo> changePassword(@RequestParam("oriPwd") String password,
                                                 @RequestParam("newPwd") String newPassword) {

        String username = stringRedisTemplate.opsForValue().get("username");
        UserInfo userInfo = userHandleService.selectUserInfo(username, password);
        if (ObjectUtil.isEmpty(userInfo)) {
            return CommonResult.fail(null, "原密码输入错误");
        } else {
            Long date = new Date().getTime();
            userInfo.setPassword(newPassword);
            userInfo.setLastModify(date);
            int flag = userHandleService.updateUserInfo(userInfo);
            return CommonResult.success(userInfo, "success");
        }
    }

    @RequestMapping("/show")
    @ApiOperation(value = "欢迎页")
    public CommonResult<UserInfo> welcomeShow(){
        String username = stringRedisTemplate.opsForValue().get("username");
        UserInfo userInfo = userHandleService.selectUserInfoByUsername(username);
        userInfo.setLastLogin(new Date().getTime());
        return CommonResult.success(userInfo, "success");
    }

}
