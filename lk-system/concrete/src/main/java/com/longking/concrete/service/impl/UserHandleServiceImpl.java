package com.longking.concrete.service.impl;


import com.longking.concrete.mapper.UserHandleMapper;
import com.longking.concrete.model.UserInfo;
import com.longking.concrete.service.UserHandleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserHandleServiceImpl implements UserHandleService {

    @Autowired
    UserHandleMapper userHandleMapper;

    @Override
    public int insertUserInfo(UserInfo userInfo) {
        return userHandleMapper.insertByUsernameAndPassword(userInfo);
    }

    @Override
    public UserInfo selectUserInfo(String username, String password) {
        return userHandleMapper.selectByUsernameAndPassword(username, password);
    }

    @Override
    public int updateUserInfo(UserInfo userInfo) {
        return userHandleMapper.updateByUsernameAndPassword(userInfo);
    }

    @Override
    public UserInfo selectUserInfoByUsername(String username) {
        return userHandleMapper.selectByUsername(username);
    }

    @Override
    public String selectUidByUsername(String username) {
        return userHandleMapper.selectUid(username);
    }


}
