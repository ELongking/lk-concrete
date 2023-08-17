package com.longking.concrete.analysis;

import com.aliyun.oss.model.OSSObject;
import com.longking.concrete.dto.ImageDetailsDto;


import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class ImageAna {

    public static Map<String, Object> generateNumericalInfo(OSSObject ossObject, List<String> exampleNames) throws Exception {
        ZipInputStream zipInputStream = new ZipInputStream(ossObject.getObjectContent());
        ZipEntry zipEntry;
        HashSet<String> countSet = new HashSet<>();
        List<byte[]> selectedImages = new ArrayList<>();

        Map<String, Object> infos = new HashMap<>();
        for (String element : new String[]{"width", "height", "resolution", "size", "classes", "example"}) {
            infos.put(element, 0);
        }

        while ((zipEntry = zipInputStream.getNextEntry()) != null) {
            BufferedImage image = ImageIO.read(zipInputStream);
            if (image != null) {

                if (exampleNames.contains(zipEntry.getName())) {
                    byte[] buffer = new byte[1024];
                    int bytesRead;
                    ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
                    while ((bytesRead = zipInputStream.read(buffer)) != -1) {
                        outputStream.write(buffer, 0, bytesRead);
                    }
                    selectedImages.add(outputStream.toByteArray());
                }

                int width = image.getWidth();
                int height = image.getHeight();
                int size = (int) zipEntry.getSize();

                if (width * height > (Integer) infos.get("resolution")) {
                    infos.put("width", width);
                    infos.put("height", height);
                    infos.put("resolution", width * height);
                }
                infos.put("size", (Integer) infos.get("size") + size);
            } else if (zipEntry.getName().endsWith("txt")) {
                ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
                byte[] buffer = new byte[1024];
                int length;
                while ((length = zipInputStream.read(buffer)) > 0) {
                    outputStream.write(buffer, 0, length);
                }
                outputStream.close();
                String text = new String(outputStream.toByteArray(), StandardCharsets.UTF_8);
                BufferedReader reader = new BufferedReader(new StringReader(text));
                String line;
                while ((line = reader.readLine()) != null) {
                    String[] part = line.split("\\s+");
                    countSet.addAll(Arrays.asList(part).subList(1, part.length));
                }
                reader.close();
            }
        }
        infos.put("classes", countSet.size());
        infos.put("example", selectedImages);
        zipInputStream.close();
        return infos;
    }

    public static ImageDetailsDto generateImageDetails(Map<String, Object> jsonMap, OSSObject ossObject) throws
            Exception {
        ImageDetailsDto imageDetails = new ImageDetailsDto();
        int number = (int) jsonMap.get("number");
        List<String> exampleNames = (List<String>) jsonMap.get("exampleNames");
        Map<String, Object> numericalInfo = generateNumericalInfo(ossObject, exampleNames);

        imageDetails.setCid((String) jsonMap.get("cid"));
        imageDetails.setFileName((String) jsonMap.get("fileName"));
        imageDetails.setFileSize(ossObject.getObjectMetadata().getContentLength());
        imageDetails.setMeanSize(Double.valueOf((Integer) numericalInfo.get("size")) / number);
        imageDetails.setMaxWidth((Integer) numericalInfo.get("width"));
        imageDetails.setMaxHeight((Integer) numericalInfo.get("height"));
        imageDetails.setResolution((Integer) numericalInfo.get("resolution"));
        imageDetails.setNumber(number);
        imageDetails.setClasses((Integer) numericalInfo.get("classes"));

        return imageDetails;
    }
}
