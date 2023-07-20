package com.longking.concrete.utils;

import cn.hutool.poi.excel.ExcelReader;
import cn.hutool.poi.excel.ExcelUtil;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;

import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

public class FileReader {
    private static final List<String> dirBase = new ArrayList<>();
    private static final List<String> imageFormatBase = new ArrayList<>();
    private static final List<String> annoFormatBase = new ArrayList<>();

    public FileReader() {
        dirBase.add("image");
        dirBase.add("annotation");

        imageFormatBase.add("jpg");
        imageFormatBase.add("bmp");
        imageFormatBase.add("png");
        imageFormatBase.add("jpeg");
        imageFormatBase.add("tif");

        annoFormatBase.add("txt");
        annoFormatBase.add("json");
    }

    public static List<String> excelReader(String path) {
        ExcelReader reader = ExcelUtil.getReader(path);
        List<String> headers = reader.readRow(0).stream()
                .map(Object::toString)
                .collect(Collectors.toList());
        return headers;
    }

    public String compressCheck(String path) {
        System.out.println(path);
        if (path.lastIndexOf("//") == path.length() - 2 && !path.contains("/")) {
            boolean flag = dirBase.contains(path.substring(0, path.lastIndexOf("//")));
            return flag ? "success" : "只允许子文件夹名为image或annotation";
        } else if (path.contains("//") && path.contains("/")) {
            return "存在二级子文件夹";
        } else {
            String suffix = path.substring(path.lastIndexOf(".") + 1).toLowerCase();
            if (path.indexOf("image") == 0) {
                return imageFormatBase.contains(suffix) ? "success" : "图片文件夹内存在格式为 --- " + suffix + " --- 的文件";
            } else {
                return annoFormatBase.contains(suffix) ? "success" : "标注文件夹内存在格式为 --- " + suffix + " --- 的文件";
            }
        }
    }

    public String compressReader(String path) throws IOException {
        File comFile = new File(path);
        String suffix = path.substring(path.lastIndexOf(".") + 1);
        if (suffix.equalsIgnoreCase("zip")) {
            try (ZipFile zip = new ZipFile(comFile, Charset.forName("GBK"))) {
                Enumeration<? extends ZipEntry> entries = zip.entries();
                while (entries.hasMoreElements()) {
                    ZipEntry entry = entries.nextElement();
                    String name = entry.getName();
                    if (entry.isDirectory()) {
                        name = name + "/";
                    }
                    String flag = compressCheck(name);
                    if (!flag.equals("success")) {
                        return flag;
                    }
                }
            }
        }
        return "success";
    }


}
