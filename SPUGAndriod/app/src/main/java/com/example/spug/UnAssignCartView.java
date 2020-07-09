package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.*;
import org.json.JSONObject;

import java.util.ArrayList;

public class UnAssignCartView extends AppCompatActivity {

    String hostUrl = MainActivity.hostUrl;
    AppCompatActivity appCompatActivity = this;
    static TextView listOfItems = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_un_assign_cart_view);

        Button giveButton = findViewById(R.id.giveButton);
        listOfItems = findViewById(R.id.ListOfItem);

        giveButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AddItems.itemList = new ArrayList<>();
                ConnAsyncTask connAsyncTask = new ConnAsyncTask(appCompatActivity, MainActivity.class);
                connAsyncTask.execute(hostUrl + "giveCart/" + MainActivity.cartNum);
                MainActivity.cartNum = 0;

            }
        });

        String clientId = MqttClient.generateClientId();
        final MqttAndroidClient mqttAndroidClient = new MqttAndroidClient(this.getApplicationContext(), MainActivity.mqttUrl, clientId);

        try {
            IMqttToken token = mqttAndroidClient.connect();
            token.setActionCallback(new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    try {
                        mqttAndroidClient.subscribe("deviceUpdate/" + MainActivity.uniqueID + '/', 2);
                    } catch (MqttException e) {
                        e.printStackTrace();
                    }
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {

                }
            });


        } catch (MqttException ex) {
            System.out.println(ex.toString());
        }

        mqttAndroidClient.setCallback(new MqttCallback() {
            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Intent intent = new Intent(getApplicationContext(), QRCodeScanner.class);
                startActivity(intent);
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}
