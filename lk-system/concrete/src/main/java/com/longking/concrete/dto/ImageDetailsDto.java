package com.longking.concrete.dto;

import cn.hutool.core.util.IdUtil;
import lombok.Data;
import org.bson.types.Binary;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.ArrayList;

@Data
@Document(collection = "imageDetails")
public class ImageDetailsDto {
    @Id
    private String id = IdUtil.fastSimpleUUID();
    @Indexed
    private String cid;
    private String fileType;
    private String fileName;
    private Long fileSize;
    private Integer maxWidth;
    private Integer maxHeight;
    private Double meanSize;
    private Integer resolution;
    private Integer number;
    private Integer classes;
    private Integer batchId;
    private ArrayList<Binary> exampleImage;

    public ImageDetailsDto(){
        this.fileType = "image";
    }
}
