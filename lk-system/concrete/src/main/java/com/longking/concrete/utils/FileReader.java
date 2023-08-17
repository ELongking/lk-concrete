package com.longking.concrete.utils;

import cn.hutool.poi.excel.ExcelReader;
import cn.hutool.poi.excel.ExcelUtil;

import java.io.File;
import java.io.IOException;
import java.nio.charset.Charset;

import java.util.*;
import java.util.stream.Collectors;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

public class FileReader {
    private static final List<String> dirBase = new ArrayList<>();
    private static final List<String> imageFormatBase = new ArrayList<>();
    private static final List<String> annoFormatBase = new ArrayList<>();
    private List<String> fileNames = new ArrayList<>();
    private int number;

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
        boolean b = path.lastIndexOf("//") == path.length() - 2;
        if (b && path.indexOf("/") == path.length() - 2) {
            boolean flag = dirBase.contains(path.substring(0, path.lastIndexOf("//")));
            return flag ? "success" : "只允许子文件夹名为image或annotation";
        } else if (b && path.indexOf("/") != path.length() - 2) {
            return "存在二级子文件夹";
        } else {
            String suffix = path.substring(path.lastIndexOf(".") + 1).toLowerCase();
            if (path.indexOf("image") == 0) {
                boolean flag = imageFormatBase.contains(suffix);
                if (flag) {
                    fileNames.add(path.substring(path.lastIndexOf("/") + 1));
                    return "success";
                } else {
                    return "图片文件夹内存在格式为 --- " + suffix + " --- 的文件";
                }
            } else {
                return annoFormatBase.contains(suffix) ? "success" : "标注文件夹内存在格式为 --- " + suffix + " --- 的文件";
            }
        }
    }

    public List<String> compressReader(String path) throws IOException {

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
                        List<String> res = new ArrayList<>(7);
                        res.set(0, flag);
                        return res;
                    }
                }
            }
        }
        int length = fileNames.size();
        number = length;
        List<String> expList = new ArrayList<>(Collections.nCopies(7, null));
        Random random = new Random();
        for (int i = 0; i < 6; i++) {
            int randomIndex = random.nextInt(length);
            String randomElement = fileNames.get(randomIndex);
            expList.set(i + 1, randomElement);
            fileNames.remove(randomIndex);
        }
        expList.set(0, "success");
        return expList;
    }

    public int getImagesNumber() {
        return this.number;
    }
}
