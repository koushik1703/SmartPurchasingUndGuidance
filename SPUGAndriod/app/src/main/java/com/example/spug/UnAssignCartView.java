package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_un_assign_cart_view);

        Button giveButton = findViewById(R.id.giveButton);
        final TextView listOfItems = findViewById(R.id.ListOfItem);

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
        final MqttAndroidClient mqttAndroidClient = new MqttAndroidClient(this.getApplicationContext(), "tcp://192.168.1.9:1883", clientId);

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
                JSONObject json = new JSONObject(new String(message.getPayload()));
                listOfItems.append(json.getString("itemPurchased") + " = " + json.getString("cost") + ";");
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }
        });
    }
}
