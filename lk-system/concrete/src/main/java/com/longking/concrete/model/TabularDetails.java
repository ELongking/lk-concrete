package com.longking.concrete.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;


import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TabularDetails {
    private String cid;
    private String fileType = "tabular";
    private List<String> cols;
    private List<String> xCols;
    private List<String> yCols;
    private String fileName;
    private Long fileSize;
    private List<Double> mean;
    private List<Double> std;
    private List<List<Double>> allData;
}
