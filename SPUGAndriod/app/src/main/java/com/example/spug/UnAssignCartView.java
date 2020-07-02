package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;

import java.util.ArrayList;

public class UnAssignCartView extends AppCompatActivity {

    String hostUrl = "http://192.168.1.9:5000/";
    AppCompatActivity appCompatActivity = this;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_un_assign_cart_view);

        Button giveButton = findViewById(R.id.giveButton);

        giveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AddItems.itemList = new ArrayList<>();
                ConnAsyncTask connAsyncTask = new ConnAsyncTask(appCompatActivity, MainActivity.class);
                connAsyncTask.execute(hostUrl + "giveCart/" + MainActivity.cartNum);
                MainActivity.cartNum = 0;

            }
        });
    }
}
