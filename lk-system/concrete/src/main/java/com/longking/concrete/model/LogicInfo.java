package com.longking.concrete.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LogicInfo {
    private String cid;
    private String fileName;
    private String fileType;
    private boolean isOutput;
    private ArrayList<String> leftData;
    private ArrayList<String> rightData;
    private ArrayList<String> cols;
}
