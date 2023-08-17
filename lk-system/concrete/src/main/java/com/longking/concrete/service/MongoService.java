package com.longking.concrete.service;

import com.longking.concrete.dto.ImageDetailsDto;
import com.longking.concrete.dto.TabularDetailsDto;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface MongoService {
    void saveTabularDetails(TabularDetailsDto tabularDetailsDto);


    void saveImageDetails(ImageDetailsDto imageDetailsDto);


    List<TabularDetailsDto> findTabularDetails(String cid);


    List<ImageDetailsDto> findImageDetails(String cid);


    void deleteDetails(String cid);


}
