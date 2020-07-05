package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class SubscribeItems extends AppCompatActivity {

    String hostUrl = MainActivity.hostUrl;
    static TextView itemsView;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_subscribe_items);

        itemsView = findViewById(R.id.itemsView);
        Button subscribeButton = findViewById(R.id.subcribeButton);

        subscribeButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), UnAssignCartView.class);
                startActivity(intent);
            }
        });

        for(String item : AddItems.itemList) {
            ItemCountConn itemCountConn = new ItemCountConn();
            itemCountConn.execute(hostUrl + "getItemCount/" + Integer.parseInt(item.substring(4, item.length())));
        }
    }
}
