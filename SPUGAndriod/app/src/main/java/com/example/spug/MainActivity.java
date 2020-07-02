package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {

    String resultText = null;
    String hostUrl = "http://192.168.1.9:5000/";
    static int cartNum;
    AppCompatActivity appCompatActivity = this;
    static TextView responseText;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Button goButton = findViewById(R.id.goButton);
        final EditText inputText = findViewById(R.id.inputText);

        responseText = findViewById(R.id.responseText);

        goButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resultText = inputText.getText().toString();
                cartNum = Integer.parseInt(resultText);
                 ConnAsyncTask connAsyncTask = new ConnAsyncTask(appCompatActivity, AddItems.class);
                 connAsyncTask.execute(hostUrl + "getCart/" + resultText);
            }
        });
    }
}
