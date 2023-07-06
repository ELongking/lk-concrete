package com.longking.concrete.utils;

import com.aliyun.oss.OSSClient;
import com.aliyun.oss.model.*;
import com.longking.concrete.common.CommonResult;
import com.longking.concrete.config.OssConfig;
import com.longking.concrete.dto.OssObjectDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.*;
import java.util.ArrayList;
import java.util.List;

@Component
public class OssUtils {
    @Autowired
    private OssConfig ossConfig;


    public CommonResult<List<String>> upload(
            File file, String mode, String absPath, String uid, String cid) throws Exception {

        String endPoint = ossConfig.getEndPoint();
        String keyId = ossConfig.getAccessKeyId();
        String keySecret = ossConfig.getAccessKeySecret();
        String bucketName = ossConfig.getBucketName();


        List<String> cols = new ArrayList<>();
        if (mode.equals("tabular")) {
            cols = FileReader.excelReader(absPath);
            cols.add(absPath);
        } else {
            String flag = FileReader.compressReader(absPath);
            cols.add(flag);
            if (flag.equals("success")) {
                return CommonResult.fail(cols, cols.get(0));
            }
        }

        OSSClient client = new OSSClient(endPoint, keyId, keySecret);
        String fileUrl = uid + "/" + cid + "/" + mode + "/" + file.getName();
        PutObjectResult res = client.putObject(new PutObjectRequest(bucketName, fileUrl, file));
        client.setBucketAcl(bucketName, CannedAccessControlList.Private);
        client.shutdown();
        if (res != null) {
            return CommonResult.success(cols, "success");
        } else {
            return CommonResult.fail(cols, "上传失败");
        }
    }

    public CommonResult<String> uploadJson(String jsonStr, String uid, String cid) {
        String endPoint = ossConfig.getEndPoint();
        String keyId = ossConfig.getAccessKeyId();
        String keySecret = ossConfig.getAccessKeySecret();
        String bucketName = ossConfig.getBucketName();

        OSSClient client = new OSSClient(endPoint, keyId, keySecret);
        byte[] content = jsonStr.getBytes();
        String fileUrl = uid + "/" + cid + "/" + "config.json";
        PutObjectResult res = client.putObject(new PutObjectRequest(bucketName, fileUrl, new ByteArrayInputStream(content)));
        client.setBucketAcl(bucketName, CannedAccessControlList.Private);
        client.shutdown();
        if (res != null) {
            return CommonResult.success(null, "success");
        } else {
            return CommonResult.fail(null, "上传失败");
        }
    }


    public CommonResult<String> delete(String filepath, String mode, String uid, String cid) {
        String endPoint = ossConfig.getEndPoint();
        String keyId = ossConfig.getAccessKeyId();
        String keySecret = ossConfig.getAccessKeySecret();
        String bucketName = ossConfig.getBucketName();

        OSSClient client = new OSSClient(endPoint, keyId, keySecret);
        String fileUrl = uid + "/" + cid + "/" + mode + "/" + filepath;
        client.deleteObject(bucketName, fileUrl);
        client.shutdown();
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
        do {
            ListObjectsRequest listObjectsRequest = new ListObjectsRequest(bucketName)
                    .withPrefix(dirUrl)
                    .withMarker(nextMarker);
            objectListing = client.listObjects(listObjectsRequest);
            if (objectListing.getObjectSummaries().size() > 0) {
                List<String> keys = new ArrayList<>();
                for (OSSObjectSummary os : objectListing.getObjectSummaries()) {
                    keys.add(os.getKey());
                }
                DeleteObjectsRequest deleteObjectsRequest = new DeleteObjectsRequest(bucketName).withKeys(keys).withEncodingType("url");
                DeleteObjectsResult deleteObjectsResult = client.deleteObjects(deleteObjectsRequest);
                List<String> deletedObjects = deleteObjectsResult.getDeletedObjects();
            }
            nextMarker = objectListing.getNextMarker();
        } while (objectListing.isTruncated());

        client.shutdown();
    }


    public OssObjectDto getFileObject(String uid, String cid, String name) {
        String endPoint = ossConfig.getEndPoint();
        String keyId = ossConfig.getAccessKeyId();
        String keySecret = ossConfig.getAccessKeySecret();
        String bucketName = ossConfig.getBucketName();

        OSSClient client = new OSSClient(endPoint, keyId, keySecret);
        String fileUrl = uid + "/" + cid + "/" + name;
        OSSObject ossObject = client.getObject(bucketName, fileUrl);
        return new OssObjectDto(client, ossObject);
    }


}
