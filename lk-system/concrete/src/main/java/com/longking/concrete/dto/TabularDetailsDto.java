package com.longking.concrete.dto;

import cn.hutool.core.util.IdUtil;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Data
@Document(collection = "tabularDetails")
public class TabularDetailsDto {
    @Id
    private String id = IdUtil.fastSimpleUUID();
    @Indexed
    private String cid;
    private String fileType;
    private List<String> cols;
    private List<String> xCols;
    private List<String> yCols;
    private List<String> subs;
    private String fileName;
    private Long fileSize;
    private List<Double> mean;
    private List<Double> std;
    private List<List<Double>> allData;

    public TabularDetailsDto() {
        this.fileType = "tabular";
    }
}
