package com.example.spug;

import java.util.ArrayList;

public class ItemPurchasedList {

    public static ArrayList<ItemPurchasedDetail> itemPurchasedDetailList= null;

    public static ArrayList<ItemPurchasedDetail> getInstance() {
        if(itemPurchasedDetailList == null) {
            itemPurchasedDetailList = new ArrayList<ItemPurchasedDetail>();
        }
        return itemPurchasedDetailList;
    }
}
