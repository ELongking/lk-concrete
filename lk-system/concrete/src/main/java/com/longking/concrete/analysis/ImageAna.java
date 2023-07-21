package com.longking.concrete.analysis;

import com.aliyun.oss.model.OSSObject;
import com.longking.concrete.dto.ImageDetailsDto;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.util.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class ImageAna {

    public static Map<String, Double> generateNumericalInfo(OSSObject ossObject) throws Exception {
        ZipInputStream zipInputStream = new ZipInputStream(ossObject.getObjectContent());
        ZipEntry zipEntry = null;

        Map<String, Double> infos = new HashMap<>();
        for (String element : new String[]{"width", "height", "resolution", "size", "number"}) {
            infos.put(element, 0.0);
        }

        while ((zipEntry = zipInputStream.getNextEntry()) != null) {
            BufferedImage image = ImageIO.read(zipInputStream);
            if (image != null) {
                int width = image.getWidth();
                int height = image.getHeight();
                long size = zipEntry.getSize();
                if (width * height > infos.get("resolution")){
                    infos.put("width", (double) width);
                    infos.put("height", (double) height);
                    infos.put("resolution", (double) width * height);
                }
                infos.put("size", infos.get("size") + size);
                infos.put("number", infos.get("number") + 1);
            }
        }
        return infos;
    }

    public static ImageDetailsDto generateImageDetails(Map<String, Object> jsonMap, OSSObject ossObject) throws Exception {
        ImageDetailsDto imageDetails = new ImageDetailsDto();
        Map<String, Double> numericalInfo = generateNumericalInfo(ossObject);

        imageDetails.setCid((String) jsonMap.get("cid"));
        imageDetails.setFileName((String) jsonMap.get("fileName"));
        imageDetails.setFileSize(ossObject.getObjectMetadata().getContentLength());
        imageDetails.setMeanSize(numericalInfo.get("size") / numericalInfo.get("number"));
        imageDetails.setMaxWidth(numericalInfo.get("width"));
        imageDetails.setMaxHeight(numericalInfo.get("height"));
        imageDetails.setResolution(numericalInfo.get("resolution"));
        imageDetails.setNumber(numericalInfo.get("number").intValue());

        return imageDetails;
    }
}
