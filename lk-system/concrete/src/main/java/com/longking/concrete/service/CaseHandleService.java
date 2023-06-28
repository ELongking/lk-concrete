package com.longking.concrete.service;

import com.longking.concrete.model.StorageInfo;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface CaseHandleService {
    List<StorageInfo> selectAll(String uid);

    int addCase(StorageInfo storageInfo);

    int deleteCase(String cid);
}
