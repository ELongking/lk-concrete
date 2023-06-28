package com.longking.concrete.service;

import com.longking.concrete.model.UserInfo;
import org.springframework.stereotype.Service;

@Service
public interface UserHandleService {

    int insertUserInfo(UserInfo userInfo);
    UserInfo selectUserInfo(String username, String password);
    int updateUserInfo(UserInfo userInfo);
    UserInfo selectUserInfoByUsername(String username);
    String selectUidByUsername(String username);

}
