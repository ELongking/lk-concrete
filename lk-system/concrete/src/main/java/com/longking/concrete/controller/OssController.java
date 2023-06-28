package com.longking.concrete.controller;

import com.longking.concrete.common.CommonResult;
import com.longking.concrete.utils.OssUtils;
import io.swagger.annotations.ApiOperation;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.FileOutputStream;

@RestController
@RequestMapping("/oss")
public class OssController {

    @Autowired
    private OssUtils ossUtils;

    @ApiOperation(value="上传文件")
    @RequestMapping(value = "/upload/{mode}", method = RequestMethod.POST)
    public CommonResult<String> upload(@RequestParam("file")MultipartFile file,
                                       @PathVariable(value = "mode")String mode) throws Exception {
        if (file == null){
            return CommonResult.fail(null, "上传文件为空");
        } else {
            String filename = file.getOriginalFilename();
            assert filename != null;

            File newFile = new File(filename);
            FileOutputStream fos = new FileOutputStream(newFile);
            fos.write(file.getBytes());
            fos.close();
            file.transferTo(newFile);
            return ossUtils.upload(newFile, mode, newFile.getAbsolutePath());
        }
    }

    @ApiOperation("上传文件删除")
    @RequestMapping(value="/delete/{mode}", method = RequestMethod.POST)
    public CommonResult<String> delete(@RequestParam("filepath") String filepath,
                                       @PathVariable("mode") String mode){
        return ossUtils.delete(filepath, mode);
    }


}
