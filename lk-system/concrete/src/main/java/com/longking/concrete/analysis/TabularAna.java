package com.longking.concrete.analysis;


import cn.hutool.poi.excel.ExcelUtil;
import com.alibaba.fastjson.JSON;
import com.alibaba.fastjson.TypeReference;
import com.alibaba.fastjson2.util.TypeUtils;
import com.aliyun.oss.model.OSSObject;
import com.longking.concrete.dto.TabularDetailsDto;
import com.longking.concrete.utils.MathUtils;

import java.io.InputStream;
import java.util.*;
import java.util.stream.Collectors;

public class TabularAna {


    public static List<List<Double>> generateExcelData(OSSObject ossObject) throws Exception {
        InputStream inputStream = ossObject.getObjectContent();
        List<List<Object>> rows = ExcelUtil.getReader(inputStream).read();
        inputStream.close();
        rows.remove(0);

        Map<Integer, Set<String>> cats = new HashMap<>();
        List<List<Object>> resRows = new ArrayList<>();

        for (List<Object> row : rows) {
            for (int i = 0; i < row.size(); i++) {
                try {
                    Double ans = Double.parseDouble(String.valueOf(row.get(i)));
                    row.set(i, ans);
                } catch (Exception e) {
                    String ans = String.valueOf(row.get(i));
                    double kl;
                    if (ans.equals("")) {
                        kl = 0.0;
                    } else {
                        Set<String> _duplicate = cats.get(i);
                        if (_duplicate == null) {
                            _duplicate = new HashSet<>();
                        }
                        _duplicate.add(ans);
                        cats.put(i, _duplicate);
                        kl = (double) _duplicate.size();
                    }
                    kl = MathUtils.formatNumber(kl);
                    row.set(i, kl);
                }
            }
            resRows.add(row);
        }

        return resRows
                .stream()
                .map(row -> row.stream()
                        .map(obj -> Double.parseDouble(String.valueOf(obj)))
                        .collect(Collectors.toList()))
                .collect(Collectors.toList());
    }

    public static List<List<Double>> generateMeanAndStd(List<List<Double>> matrix) {
        int n = matrix.get(0).size();
        List<List<Double>> result = new ArrayList<>(2);

        for (int j = 0; j < n; j++) {
            List<Double> column = new ArrayList<>(matrix.size());
            for (List<Double> row : matrix) {
                column.add(row.get(j));
            }
            double sum = 0.0;
            double sumOfSquares = 0.0;
            for (double x : column) {
                sum += x;
                sumOfSquares += x * x;
            }
            double mean = MathUtils.formatNumber(sum / column.size());
            double variance = MathUtils.formatNumber(sumOfSquares / column.size() - mean * mean);
            List<Double> colResult = new ArrayList<>(2);
            colResult.add(mean);
            colResult.add(variance);
            result.add(colResult);
        }

        List<List<Double>> finalResult = new ArrayList<>(2);
        finalResult.add(new ArrayList<>(n));
        finalResult.add(new ArrayList<>(n));
        for (List<Double> row : result) {
            finalResult.get(0).add(row.get(0));
            finalResult.get(1).add(row.get(1));
        }

        return finalResult;
    }

    public static TabularDetailsDto generateTabularDetails(Map<String, Object> jsonMap, OSSObject ossObject) throws Exception {
        String fileName = (String) jsonMap.get("fileName");
        TabularDetailsDto tabularDetails = new TabularDetailsDto();
        long fileSize = ossObject.getObjectMetadata().getContentLength();

        List<List<Double>> matrix = generateExcelData(ossObject);
        List<List<Double>> ms = generateMeanAndStd(matrix);
        List<Double> mean = ms.get(0);
        List<Double> std = ms.get(1);

        tabularDetails.setCid((String) jsonMap.get("cid"));
        tabularDetails.setAllData(matrix);

        List<HashMap<String, Object>> setting = JSON.parseObject(
                JSON.toJSONString(jsonMap.get("setting")),
                new TypeReference<List<HashMap<String, Object>>>() {
                }
        );

        List<String> cols = new ArrayList<>();
        List<String> xCols = new ArrayList<>();
        List<String> yCols = new ArrayList<>();
        List<String> subs = new ArrayList<>();

        for (Map<String, Object> element : setting) {
            if ((boolean) element.get("isX")) {
                xCols.add((String) element.get("col"));
            } else {
                yCols.add((String) element.get("col"));
            }

            if (element.get("col").equals(element.get("subject"))){
                subs.add((String) element.get("subject"));
            } else {
                subs.add("无");
            }
        }

        for (Object element : TypeUtils.cast(jsonMap.get("cols"), String[].class)) {
            cols.add(String.valueOf(element));
        }
        tabularDetails.setCols(cols);
        tabularDetails.setXCols(xCols);
        tabularDetails.setYCols(yCols);
        tabularDetails.setSubs(subs);

        tabularDetails.setFileName(fileName);
        tabularDetails.setMean(mean);
        tabularDetails.setStd(std);

        tabularDetails.setFileSize(fileSize);

        return tabularDetails;
    }

}
