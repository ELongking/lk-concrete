package com.longking.concrete.controller;

import cn.hutool.core.util.ObjectUtil;
import com.alibaba.fastjson.JSON;
import com.aliyun.oss.model.OSSObject;
import com.github.pagehelper.PageHelper;
import com.github.pagehelper.PageInfo;
import com.longking.concrete.analysis.ImageAna;
import com.longking.concrete.analysis.TabularAna;
import com.longking.concrete.common.CommonResult;
import com.longking.concrete.dto.ImageDetailsDto;
import com.longking.concrete.dto.TabularDetailsDto;
import com.longking.concrete.dto.OssObjectDto;
import com.longking.concrete.model.LogicInfo;
import com.longking.concrete.model.MongoRepo;
import com.longking.concrete.model.StorageInfo;
import com.longking.concrete.service.CaseHandleService;
import com.longking.concrete.utils.GenerateMarker;
import com.longking.concrete.utils.OssUtils;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;

import java.io.ByteArrayOutputStream;
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
    @Autowired
    private MongoRepo mongoRepo;

    @ApiOperation(value = "展示该用户的所有批次")
    @RequestMapping(value = "/page/{pageNum}", method = RequestMethod.GET)
    public CommonResult<PageInfo<StorageInfo>> pageShow(@PathVariable(value = "pageNum") Integer pageNum) {
        String uid = stringRedisTemplate.opsForValue().get("uid");
        PageHelper.startPage(pageNum, 15);
        PageInfo<StorageInfo> page = PageInfo.of(caseHandleService.selectAll(uid));
        return CommonResult.success(page, "success");
    }

    @ApiOperation(value = "直接生成详情信息")
    @RequestMapping(value = "/detail/generate/", method = RequestMethod.POST)
    public void detailGenerate(@RequestParam(value = "cid") String cid) throws Exception {
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

        for (Map<String, Object> map : jsonList) {
            String type = (String) map.get("fileType");
            if (type.equals("tabular")) {
                String ansName = (String) map.get("fileName");
                ansName = "tabular" + "/" + ansName;
                OssObjectDto ansOssObjectDto = ossUtils.getFileObject(uid, cid, ansName);
                OSSObject ansObject = ansOssObjectDto.getOssObject();
                TabularDetailsDto anaRes = TabularAna.generateTabularDetails(map, ansObject);
                mongoRepo.saveTabularDetails(anaRes);

                ansObject.close();
                ansOssObjectDto.getOssClient().shutdown();
            } else {
                String ansName = (String) map.get("fileName");
                String ansFileType = (String) map.get("fileType");

                ansName = "image" + "/" + ansName;
                OssObjectDto ansImageOssObjectDto = ossUtils.getFileObject(uid, cid, ansName);
                OSSObject ansImageObject = ansImageOssObjectDto.getOssObject();

                ImageDetailsDto anaRes = ImageAna.generateImageDetails(map, ansImageObject);
                mongoRepo.saveImageDetails(anaRes);

                ansImageObject.close();
                ansImageOssObjectDto.getOssClient().shutdown();
            }
        }

    }


    @ApiOperation(value = "展示详细信息")
    @RequestMapping(value = "/detail/{cid}", method = RequestMethod.GET)
    public CommonResult<List<Object>> detailShow(@PathVariable(value = "cid") String cid) {
        List<Object> res = new ArrayList<>();
        List<TabularDetailsDto> tdd = mongoRepo.findTabularDetails(cid);
        List<ImageDetailsDto> idd = mongoRepo.findImageDetails(cid);
        res.addAll(tdd);
        res.addAll(idd);
        return CommonResult.success(res, "success");
    }

    @ApiOperation(value = "更新详细信息的上一次查看时间")
    @RequestMapping(value = "/details/update/{cid}", method = RequestMethod.POST)
    public CommonResult<String> detailTimeUpdate(@PathVariable(value = "cid") String cid) {
        long lastModify = new Date().getTime();
        int flag = caseHandleService.updateLastModify(cid, lastModify);
        if (flag == 1) {
            return CommonResult.success(null, "success");
        } else {
            return CommonResult.fail(null, "退出失败, 请稍后重试");
        }
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
