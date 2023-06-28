package com.longking.concrete.model;

import com.sun.org.apache.xpath.internal.operations.String;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LogicInfo {
    private String cid;
    private String dataType;
    private String taskType;
    private List<String> labels;
    private List<String> targets;
    private List<String> images;
    private List<String> annotations;
}
