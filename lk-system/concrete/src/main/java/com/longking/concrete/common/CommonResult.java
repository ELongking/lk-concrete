package com.longking.concrete.common;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class CommonResult<T> {
    private long code;
    private String msg;
    private T data;

    public static <T> CommonResult<T> success(T data, String msg){
        return new CommonResult<T>(1, msg, data);
    }

    public static <T> CommonResult<T> fail(T data, String msg){
        return new CommonResult<T>(-1, msg, data);
    }
}
