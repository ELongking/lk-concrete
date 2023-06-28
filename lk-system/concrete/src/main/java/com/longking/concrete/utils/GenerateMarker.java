package com.longking.concrete.utils;


import cn.hutool.core.util.IdUtil;
import cn.hutool.core.util.RandomUtil;

public class GenerateMarker {
    public static String getUid() {
        return IdUtil.randomUUID();
    }

    public static String getCid(String uid) {
        String[] uidPart = uid.split("-");
        String prefix = "";
        for (String part : uidPart) {
            prefix += part.charAt(0);
        }
            return prefix + RandomUtil.randomNumbers(5);
    }
}
