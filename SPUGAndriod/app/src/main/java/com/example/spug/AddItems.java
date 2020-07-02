package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.util.ArrayList;

public class AddItems extends AppCompatActivity {

    static ArrayList<String> itemList = new ArrayList<>();

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_add_items);

        final EditText itemToAdd = findViewById(R.id.itemToAdd);
        Button addButton = findViewById(R.id.addButton);
        Button doneButton = findViewById(R.id.doneButton);

        addButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                itemList.add(itemToAdd.getText().toString());
                itemToAdd.setText("");
            }
        });

        doneButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), SubscribeItems.class);
                startActivity(intent);
            }
        });
    }
}
