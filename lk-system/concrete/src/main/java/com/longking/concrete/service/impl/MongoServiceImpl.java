package com.longking.concrete.service.impl;

import com.longking.concrete.dto.ImageDetailsDto;
import com.longking.concrete.dto.TabularDetailsDto;
import com.longking.concrete.service.MongoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MongoServiceImpl implements MongoService {
    @Autowired
    private MongoTemplate mongoTemplate;

    public void saveTabularDetails(TabularDetailsDto tabularDetailsDto) {
        mongoTemplate.save(tabularDetailsDto);
    }

    public void saveImageDetails(ImageDetailsDto imageDetailsDto) {
        mongoTemplate.save(imageDetailsDto);
    }

    public List<TabularDetailsDto> findTabularDetails(String cid) {
        Query query = new Query(Criteria.where("cid").is(cid));
        return mongoTemplate.find(query, TabularDetailsDto.class, "tabularDetails");
    }

    public List<ImageDetailsDto> findImageDetails(String cid) {
        Query query = new Query(Criteria.where("cid").is(cid));
        return mongoTemplate.find(query, ImageDetailsDto.class, "imageDetails");
    }

    public void deleteDetails(String cid) {
        Query query = new Query(Criteria.where("cid").is(cid));
        mongoTemplate.remove(query, TabularDetailsDto.class, "tabularDetails");
        mongoTemplate.remove(query, ImageDetailsDto.class, "imageDetails");
    }
}
