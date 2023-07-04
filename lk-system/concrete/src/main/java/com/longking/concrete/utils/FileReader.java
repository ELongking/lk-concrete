package com.longking.concrete.utils;

import cn.hutool.poi.excel.ExcelReader;
import cn.hutool.poi.excel.ExcelUtil;

import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

public class FileReader {
    public static List<String> excelReader(String path) {
        ExcelReader reader = ExcelUtil.getReader(path);
        List<String> headers = reader.readRow(0).stream()
                .map(Object::toString)
                .collect(Collectors.toList());
        return headers;
    }

}
