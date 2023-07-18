package com.longking.concrete.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.ArrayList;
import java.util.HashMap;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LogicInfo {
    private String cid;
    private String fileName;
    private String fileType;
    private boolean isTrained = false;
    private ArrayList<String> cols;
    private ArrayList<HashMap<String, Object>> setting;
}
