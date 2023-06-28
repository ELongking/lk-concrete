package com.longking.concrete.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class StorageInfo {
    private Integer id;
    private String uid;
    private String cid;
    private String cname;
    private String fileType;
    private String tabularType;
    private String imageType;
    private Long createTime;
    private Long lastModify;
    private Integer isTrained;
}
