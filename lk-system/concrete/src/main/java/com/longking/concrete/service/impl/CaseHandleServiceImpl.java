package com.longking.concrete.service.impl;


import com.longking.concrete.mapper.CaseHandleMapper;
import com.longking.concrete.model.StorageInfo;
import com.longking.concrete.service.CaseHandleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class CaseHandleServiceImpl implements CaseHandleService {
    @Autowired
    private CaseHandleMapper caseHandleMapper;
    @Override
    public List<StorageInfo> selectAll(String uid) {
        return caseHandleMapper.selectAllByPage(uid);
    }

    @Override
    public int addCase(StorageInfo storageInfo){
        return caseHandleMapper.insertByInfo(storageInfo);
    }

    @Override
    public int deleteCase(String cid) {return caseHandleMapper.deleteByCid(cid);}
}
