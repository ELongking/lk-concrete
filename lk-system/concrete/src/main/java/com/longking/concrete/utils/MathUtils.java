package com.longking.concrete.utils;

import java.text.DecimalFormat;

public class MathUtils {

    public static double formatNumber(Double number){
        DecimalFormat decimalFormat = new DecimalFormat("#.####");
        decimalFormat.setGroupingUsed(false); // 禁用千分位分组

        String formattedNumber = decimalFormat.format(number);
        return Double.parseDouble(formattedNumber);
    }

}
