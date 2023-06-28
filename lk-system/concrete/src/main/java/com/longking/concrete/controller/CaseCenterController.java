package com.longking.concrete.controller;

import cn.hutool.json.JSON;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.longking.concrete.common.CommonResult;
import com.longking.concrete.model.StorageInfo;
import com.longking.concrete.service.CaseHandleService;
import com.longking.concrete.utils.GenerateMarker;
import com.longking.concrete.utils.OssUtils;
import io.swagger.annotations.ApiOperation;
import io.swagger.models.auth.In;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;

@Controller
@RequestMapping("/cases")
public class CaseCenterController {
    @Autowired
    private StringRedisTemplate stringRedisTemplate;
    @Autowired
    private CaseHandleService caseHandleService;
    @Autowired
    private OssUtils ossUtils;

    @ApiOperation(value = "展示该用户的所有批次")
    @RequestMapping(value = "/page/{pageNum}-{pageSize}", method = RequestMethod.GET)
    @ResponseBody
    public CommonResult<PageInfo<StorageInfo>> pageShow(@PathVariable(value = "pageNum") Integer pageNum,
                                                        @PathVariable(value = "pageSize") Integer pageSize) {
        String uid = stringRedisTemplate.opsForValue().get("uid");
        List<StorageInfo> allData = caseHandleService.selectAll(uid);
        PageHelper.startPage(pageNum, pageSize);
        PageInfo<StorageInfo> page = new PageInfo<>(allData);
        return CommonResult.success(page, "success");
    }

    @ApiOperation(value = "删除某一个批次")
    @RequestMapping(value = "/delete/{cid}", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult<String> caseDelete(@PathVariable(value = "cid") String cid) {
        int flag = caseHandleService.deleteCase(cid);
        String uid = stringRedisTemplate.opsForValue().get("uid");

        if (flag > 0) {
            ossUtils.deleteDirectory(uid, cid);
            return CommonResult.success(null, "success");
        } else {
            return CommonResult.fail(null, "删除失败, 请重试");
        }
    }

    @ApiOperation(value = "创建新批次")
    @RequestMapping(value = "/create", method = RequestMethod.POST)
    @ResponseBody
    public CommonResult<String> caseCreate(@RequestParam(value = "cname") String cname,
                                                @RequestParam(value = "fileType") String fileType,
                                                @RequestParam(value = "tabularType") String tabularType,
                                                @RequestParam(value = "imageType") String imageType) {
        StorageInfo storageInfo = new StorageInfo();
        String uid = stringRedisTemplate.opsForValue().get("uid");
        Long nowTime = new Date().getTime();
        String cid = GenerateMarker.getCid(uid);
        stringRedisTemplate.opsForValue().set("cid", cid);

        storageInfo.setUid(uid);
        storageInfo.setCid(cid);
        storageInfo.setCreateTime(nowTime);
        storageInfo.setLastModify(nowTime);
        storageInfo.setCname(cname);
        storageInfo.setFileType(fileType);
        storageInfo.setTabularType(tabularType);
        storageInfo.setImageType(imageType);


        int condition = caseHandleService.addCase(storageInfo);
        if (condition > 0) {
            return CommonResult.success(cid, "success");
        } else {
            return CommonResult.fail(null, "提交失败, 请重试");
        }

    }
}
