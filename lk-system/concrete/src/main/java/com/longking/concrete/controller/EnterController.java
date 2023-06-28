package com.longking.concrete.controller;

import cn.hutool.core.util.ObjectUtil;
import com.longking.concrete.common.CommonResult;
import com.longking.concrete.model.UserInfo;
import com.longking.concrete.service.UserHandleService;
import com.longking.concrete.utils.GenerateCode;
import com.longking.concrete.utils.GenerateMarker;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiImplicitParams;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;

import javax.servlet.ServletOutputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Date;

@RestController
@RequestMapping("/enter")
@Api(value = "登录注册接口", tags = "用户登录注册")
public class EnterController {

    @Autowired
    private UserHandleService userHandleService;
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @RequestMapping(value = "/login", method = RequestMethod.POST)
    @ApiImplicitParams({
            @ApiImplicitParam(name = "username", value = "用户名", required = true),
            @ApiImplicitParam(name = "password", value = "密码", required = true),
            @ApiImplicitParam(name = "code", value = "验证码", required = true)
    })
    @ApiOperation(value = "根据用户名密码和验证码进行登录")
    public CommonResult<UserInfo> userLogin(@RequestParam(value = "username") String username,
                                            @RequestParam(value = "password") String password,
                                            @RequestParam(value = "code") String code) {

        String settingCode = stringRedisTemplate.opsForValue().get("code");
        code = code.toLowerCase();
        assert settingCode != null;
        settingCode = settingCode.toLowerCase();

        if (!settingCode.equals(code)) {
            return CommonResult.fail(null, "登陆失败, 验证码错误");
        }
        UserInfo userInfo = userHandleService.selectUserInfo(username, password);
        if (ObjectUtil.isEmpty(userInfo)) {
            return CommonResult.fail(null, "登陆失败, 请检查用户名和密码是否匹配");
        }
        stringRedisTemplate.opsForValue().set("uid", userInfo.getUid());
        stringRedisTemplate.opsForValue().set("username", username);
        stringRedisTemplate.delete("code");
        return CommonResult.success(userInfo, "success");
    }

    @RequestMapping(value = "/sign", method = RequestMethod.POST)
    @ApiOperation(value = "根据用户名密码进行注册")
    public CommonResult<Integer> userSignIn(@RequestParam(value = "username") String username,
                                            @RequestParam(value = "password") String password) {

        UserInfo infos = userHandleService.selectUserInfoByUsername(username);
        if (infos != null) {
            return CommonResult.fail(null, "用户已存在, 请重新输入或直接登录");
        } else {
            UserInfo userInfo = new UserInfo();
            Long date = new Date().getTime();

            userInfo.setUsername(username);
            userInfo.setPassword(password);
            userInfo.setCreateTime(date);
            userInfo.setUid(GenerateMarker.getUid());
            Integer condition = userHandleService.insertUserInfo(userInfo);

            return CommonResult.success(null, "success");
        }
    }

    @RequestMapping(value = "/verifyCode", method = RequestMethod.GET)
    @ApiOperation(value = "生成验证码图片")
    public void verifyCode(HttpServletResponse response) throws IOException {
        String code = GenerateCode.generateVerifyCode(4);
        stringRedisTemplate.opsForValue().set("code", code);
        response.setContentType("image/png");
        ServletOutputStream outputStream = response.getOutputStream();
        GenerateCode.outputImage(100, 40, outputStream, code);
    }

    @RequestMapping(value="/logout", method = RequestMethod.GET)
    @ApiOperation(value="退出登录")
    public CommonResult<String> logOut(){
        if (stringRedisTemplate.opsForValue().get("uid") != null){
            stringRedisTemplate.delete("uid");
        }
        if (stringRedisTemplate.opsForValue().get("cid") != null){
            stringRedisTemplate.delete("cid");
        }
        if (stringRedisTemplate.opsForValue().get("username") != null){
            stringRedisTemplate.delete("username");
        }

        return CommonResult.success(null, "success");
    }



}
