package com.longking.concrete.controller;

import com.longking.concrete.common.CommonResult;
import com.longking.concrete.utils.OssUtils;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.FileOutputStream;
import java.util.List;

@RestController
@RequestMapping("/oss")
public class OssController {

    @Autowired
    private OssUtils ossUtils;
    @Autowired
    private StringRedisTemplate stringRedisTemplate;

    @ApiOperation(value = "上传文件")
    @RequestMapping(value = "/upload/{mode}", method = RequestMethod.POST)
    public CommonResult<List<String>> upload(@RequestParam("file") MultipartFile file,
                                             @PathVariable(value = "mode") String mode) throws Exception {
        if (file == null) {
            return CommonResult.fail(null, "上传文件为空");
        } else {

            String filename = file.getOriginalFilename();
            assert filename != null;

            File newFile = new File(filename);
            FileOutputStream fos = new FileOutputStream(newFile);
            fos.write(file.getBytes());
            fos.close();
            file.transferTo(newFile);

            String uid = stringRedisTemplate.opsForValue().get("uid");
            String cid = stringRedisTemplate.opsForValue().get("cid");
            return ossUtils.upload(newFile, mode, newFile.getAbsolutePath(), uid, cid);
        }
    }

    @ApiOperation("上传文件删除")
    @RequestMapping(value = "/delete", method = RequestMethod.POST)
    public CommonResult<String> delete(@RequestParam("filePath") String filepath,
                                       @RequestParam("mode") String mode) {

        String uid = stringRedisTemplate.opsForValue().get("uid");
        String cid = stringRedisTemplate.opsForValue().get("cid");
        return ossUtils.delete(filepath, mode, uid, cid);
    }


}
