package com.longking.concrete.model;

import com.longking.concrete.dto.ImageDetailsDto;
import com.longking.concrete.dto.TabularDetailsDto;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Repository;

import java.util.List;

@Component
public class MongoRepo {

    @Autowired
    private MongoTemplate mongoTemplate;

    public void saveTabularDetails(TabularDetailsDto tabularDetailsDto) {
        mongoTemplate.save(tabularDetailsDto);
    }

    public void saveImageDetails(ImageDetailsDto imageDetailsDto) {
        mongoTemplate.save(imageDetailsDto);
    }

    public List<TabularDetailsDto> findTabularDetails(String cid){
        Query query = new Query(Criteria.where("cid").is(cid));
        return mongoTemplate.find(query, TabularDetailsDto.class, "tabularDetails");
    }

    public List<ImageDetailsDto> findImageDetails(String cid){
        Query query = new Query(Criteria.where("cid").is(cid));
        return mongoTemplate.find(query, ImageDetailsDto.class, "imageDetails");
    }
}
