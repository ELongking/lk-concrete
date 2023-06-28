package com.longking.concrete.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class UserInfo {
    private int id;
    private String uid;
    private String username;
    private String password;
    private Long createTime;
    private Long lastModify;
    private Long lastLogin;
}
