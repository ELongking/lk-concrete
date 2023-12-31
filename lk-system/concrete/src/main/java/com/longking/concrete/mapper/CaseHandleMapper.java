package com.longking.concrete.mapper;

import com.longking.concrete.model.CaseTypes;
import com.longking.concrete.model.StorageInfo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.Map;

@Mapper
public interface CaseHandleMapper {
    List<StorageInfo> selectAllByPage(String uid);

    int insertByInfo(StorageInfo storageInfo);

    int deleteByCid(String cid);

    int updateByLastModify(@Param("cid") String cid,
                           @Param("lastModify") long lastModify);

    List<CaseTypes> selectTypesByCid(String cid);

}
