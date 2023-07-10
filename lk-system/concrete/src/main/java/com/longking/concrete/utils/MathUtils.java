package com.longking.concrete.utils;

import java.text.DecimalFormat;

public class MathUtils {

    public static double formatNumber(Double number){
        DecimalFormat decimalFormat = new DecimalFormat("#.####");
        decimalFormat.setGroupingUsed(false);

        String formattedNumber = decimalFormat.format(number);
        return Double.parseDouble(formattedNumber);
    }

    public static long formatNumber(long number){
        DecimalFormat decimalFormat = new DecimalFormat("#.####");
        decimalFormat.setGroupingUsed(false);

        String formattedNumber = decimalFormat.format(number);
        return Long.parseLong(formattedNumber);
    }

}
