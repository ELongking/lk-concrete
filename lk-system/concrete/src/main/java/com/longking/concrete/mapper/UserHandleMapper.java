package com.longking.concrete.mapper;

import com.longking.concrete.model.UserInfo;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;


@Mapper
public interface UserHandleMapper {
    UserInfo selectByUsernameAndPassword(@Param("username") String username, @Param("password") String password);

    int insertByUsernameAndPassword(UserInfo userInfo);

    int updateByUsernameAndPassword(UserInfo userInfo);

    UserInfo selectByUsername(@Param("username") String username);

    String selectUid(@Param("username") String username);
}
