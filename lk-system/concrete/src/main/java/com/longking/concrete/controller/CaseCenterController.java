package com.longking.concrete.controller;

import cn.hutool.core.util.ObjectUtil;
import cn.hutool.log.Log;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;
import com.aliyun.oss.model.OSSObject;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.longking.concrete.analysis.TabularAna;
import com.longking.concrete.common.CommonResult;
import com.longking.concrete.dto.OssObjectDto;
import com.longking.concrete.model.LogicInfo;
import com.longking.concrete.model.StorageInfo;
import com.longking.concrete.service.CaseHandleService;
import com.longking.concrete.utils.GenerateMarker;
import com.longking.concrete.utils.OssUtils;
import io.swagger.annotations.ApiOperation;
import org.apache.ibatis.logging.stdout.StdOutImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/cases")
public class CaseCenterController {
    @Autowired
    private StringRedisTemplate stringRedisTemplate;
    @Autowired
    private CaseHandleService caseHandleService;
    @Autowired
    private OssUtils ossUtils;

    @ApiOperation(value = "展示该用户的所有批次")
    @RequestMapping(value = "/page/{pageNum}", method = RequestMethod.GET)
    public CommonResult<PageInfo<StorageInfo>> pageShow(@PathVariable(value = "pageNum") Integer pageNum) {
        String uid = stringRedisTemplate.opsForValue().get("uid");
        PageHelper.startPage(pageNum, 15);
        PageInfo<StorageInfo> page = PageInfo.of(caseHandleService.selectAll(uid));
        return CommonResult.success(page, "success");
    }

    @ApiOperation(value = "展示详细信息")
    @RequestMapping(value = "/detail/{cid}", method = RequestMethod.GET)
    public CommonResult<List<Object>> detailShow(@PathVariable(value = "cid") String cid) throws Exception {
        String uid = stringRedisTemplate.opsForValue().get("uid");
        OssObjectDto ossObjectDto = ossUtils.getFileObject(uid, cid, "config.json");
        OSSObject ossObject = ossObjectDto.getOssObject();
        InputStream inputStream = ossObject.getObjectContent();
        ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
        byte[] buffer = new byte[1024];
        int len;
        while ((len = inputStream.read(buffer)) != -1) {
            outputStream.write(buffer, 0, len);
        }
        String jsonStr = outputStream.toString("UTF-8");

        ossObject.close();
        inputStream.close();
        outputStream.close();
        ossObjectDto.getOssClient().shutdown();

        List<Map<String, Object>> jsonList = JSON.parseObject(jsonStr, List.class);

        List<Object> res = new ArrayList<>();
        for (Map<String, Object> map : jsonList) {
            String type = (String) map.get("fileType");
            if (type.equals("tabular")) {
                String ansName = (String) map.get("fileName");
                ansName = "tabular" + "/" + ansName.substring(ansName.lastIndexOf("\\") + 1);
                OssObjectDto ansOssObjectDto = ossUtils.getFileObject(uid, cid, ansName);
                OSSObject ansObject = ansOssObjectDto.getOssObject();
                Object anaRes = TabularAna.generateTabularDetails(map, ansObject);
                res.add(anaRes);

                ansObject.close();
                ansOssObjectDto.getOssClient().shutdown();
            }
        }
        return CommonResult.success(res, "success");

    }

    @ApiOperation(value = "删除某一个批次")
    @RequestMapping(value = "/delete/{cid}", method = RequestMethod.POST)
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

    @ApiOperation(value = "创建新批次-基本信息")
    @RequestMapping(value = "/create/intro", method = RequestMethod.POST)
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

    @ApiOperation(value = "创建新批次-逻辑信息")
    @RequestMapping(value = "/create/logic", method = RequestMethod.POST)
    public CommonResult<String> logicCreate(@RequestBody List<LogicInfo> logicInfos) throws Exception {

        if (ObjectUtil.isEmpty(logicInfos)) {
            return CommonResult.fail(null, "上传失败, 不存在需上传的逻辑数据");
        } else {
            String uid = stringRedisTemplate.opsForValue().get("uid");
            String cid = stringRedisTemplate.opsForValue().get("cid");
            String jsonStr = JSON.toJSONString(logicInfos);
            return ossUtils.uploadJson(jsonStr, uid, cid);
        }
    }

}
