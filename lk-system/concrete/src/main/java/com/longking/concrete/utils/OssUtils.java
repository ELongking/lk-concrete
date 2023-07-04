package com.longking.concrete.utils;

import com.aliyun.oss.OSSClient;
import com.aliyun.oss.model.*;
import com.longking.concrete.common.CommonResult;
import com.longking.concrete.config.OssConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Component;

import java.io.ByteArrayInputStream;
import java.io.File;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.util.ArrayList;
import java.util.List;

@Component
public class OssUtils {
    @Autowired
    private OssConfig ossConfig;
    @Autowired
    private StringRedisTemplate stringRedisTemplate;


    public CommonResult<List<String>> upload(File file, String mode, String absPath) {
        String endPoint = ossConfig.getEndPoint();
        String keyId = ossConfig.getAccessKeyId();
        String keySecret = ossConfig.getAccessKeySecret();
        String bucketName = ossConfig.getBucketName();

        String uid = stringRedisTemplate.opsForValue().get("uid");
        String cid = stringRedisTemplate.opsForValue().get("cid");

        List<String> cols = null;
        if (mode.equals("tabular")){
            cols = FileReader.excelReader(absPath);
            cols.add(absPath);
        }

        OSSClient client = new OSSClient(endPoint, keyId, keySecret);
        String fileUrl = uid + "/" + cid + "/" + mode + "/" + file.getName();
        PutObjectResult res = client.putObject(new PutObjectRequest(bucketName, fileUrl, file));
        client.setBucketAcl(bucketName, CannedAccessControlList.Private);
        if (client != null) {
            client.shutdown();
        }
        if (res != null) {
            return CommonResult.success(cols, "success");
        } else {
            return CommonResult.fail(null, "上传失败");
        }
    }

    public CommonResult<String> uploadJson(String jsonStr){
        String endPoint = ossConfig.getEndPoint();
        String keyId = ossConfig.getAccessKeyId();
        String keySecret = ossConfig.getAccessKeySecret();
        String bucketName = ossConfig.getBucketName();

        String uid = stringRedisTemplate.opsForValue().get("uid");
        String cid = stringRedisTemplate.opsForValue().get("cid");
        OSSClient client = new OSSClient(endPoint, keyId, keySecret);
        byte[] content = jsonStr.getBytes();
        String fileUrl = uid + "/" + cid + "/" + "config.json";
        PutObjectResult res = client.putObject(new PutObjectRequest(bucketName, fileUrl, new ByteArrayInputStream(content)));
        client.setBucketAcl(bucketName, CannedAccessControlList.Private);
        if (client != null) {
            client.shutdown();
        }
        if (res != null) {
            return CommonResult.success(null, "success");
        } else {
            return CommonResult.fail(null, "上传失败");
        }
    }


    public CommonResult<String> delete(String filepath, String mode) {
        String endPoint = ossConfig.getEndPoint();
        String keyId = ossConfig.getAccessKeyId();
        String keySecret = ossConfig.getAccessKeySecret();
        String bucketName = ossConfig.getBucketName();

        String uid = stringRedisTemplate.opsForValue().get("uid");
        String cid = stringRedisTemplate.opsForValue().get("cid");

        OSSClient client = new OSSClient(endPoint, keyId, keySecret);
        String fileUrl = uid + "/" + cid + "/" + mode + "/" + filepath;
        client.deleteObject(bucketName, fileUrl);
        if (client != null) {
            client.shutdown();
        }
        return CommonResult.success(null, "success");
    }


    public void deleteDirectory(String uid, String cid) {
        String endPoint = ossConfig.getEndPoint();
        String keyId = ossConfig.getAccessKeyId();
        String keySecret = ossConfig.getAccessKeySecret();
        String bucketName = ossConfig.getBucketName();

        OSSClient client = new OSSClient(endPoint, keyId, keySecret);
        String dirUrl = uid + "/" + cid;

        ObjectListing objectListing = null;
        String nextMarker = null;
        do{
            ListObjectsRequest listObjectsRequest = new ListObjectsRequest(bucketName)
                    .withPrefix(dirUrl)
                    .withMarker(nextMarker);
            objectListing = client.listObjects(listObjectsRequest);
            if (objectListing.getObjectSummaries().size() > 0){
                List<String> keys = new ArrayList<>();
                for (OSSObjectSummary os: objectListing.getObjectSummaries()){
                    keys.add(os.getKey());
                }
                DeleteObjectsRequest deleteObjectsRequest = new DeleteObjectsRequest(bucketName).withKeys(keys).withEncodingType("url");
                DeleteObjectsResult deleteObjectsResult = client.deleteObjects(deleteObjectsRequest);
                List<String> deletedObjects = deleteObjectsResult.getDeletedObjects();
            }
            nextMarker = objectListing.getNextMarker();
        } while (objectListing.isTruncated());

        if (client != null) {
            client.shutdown();
        }
    }


}
