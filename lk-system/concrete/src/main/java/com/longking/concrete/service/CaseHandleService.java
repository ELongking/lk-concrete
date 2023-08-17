package com.longking.concrete.service;

import com.longking.concrete.model.CaseTypes;
import com.longking.concrete.model.StorageInfo;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public interface CaseHandleService {
    List<StorageInfo> selectAll(String uid);

    int addCase(StorageInfo storageInfo);

    int deleteCase(String cid);

    int updateLastModify(String cid, long lastModify);

    List<CaseTypes> getCaseTypes(String cid);
}
