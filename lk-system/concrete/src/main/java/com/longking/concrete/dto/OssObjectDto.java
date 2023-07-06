package com.longking.concrete.dto;

import com.aliyun.oss.OSSClient;
import com.aliyun.oss.model.OSSObject;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@AllArgsConstructor
@NoArgsConstructor
@Data
public class OssObjectDto {
    private OSSClient ossClient;
    private OSSObject ossObject;
}
