package com.example.spug;

public class ItemPurchasedDetail {

    String itempurchased;
    String calorie;
    String fat;
    String carbohydrate;
    String protein;
    String salt;
    String time;

    public ItemPurchasedDetail(String itempurchased, String calorie, String fat, String carbohydrate, String protein, String salt, String time) {
        this.itempurchased = itempurchased;
        this.calorie = calorie;
        this.fat = fat;
        this.carbohydrate = carbohydrate;
        this.protein = protein;
        this.salt = salt;
        this.time = time;
    }
}
