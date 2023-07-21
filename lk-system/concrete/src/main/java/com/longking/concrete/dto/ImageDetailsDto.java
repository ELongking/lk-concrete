package com.longking.concrete.dto;

import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "imageDetails")
public class ImageDetailsDto {
    @Id
    private Integer id;
    @Indexed
    private String cid;
    private final String fileType = "image";
    private String fileName;
    private Long fileSize;
    private Double maxWidth;
    private Double maxHeight;
    private Double meanSize;
    private Double resolution;
    private Integer number;
    private Integer classes;
}
