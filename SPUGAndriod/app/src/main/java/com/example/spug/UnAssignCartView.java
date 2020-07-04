package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import org.json.JSONObject;

import java.util.ArrayList;

public class UnAssignCartView extends AppCompatActivity {

    String hostUrl = "http://192.168.0.104:5000/";
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
        final MqttAndroidClient mqttAndroidClient = new MqttAndroidClient(this.getApplicationContext(), "tcp://192.168.0.104:1883", clientId, new MemoryPersistence());

        MqttConnectOptions mqttConnectOptions = new MqttConnectOptions();
        mqttConnectOptions.setCleanSession(true);

        try {
            mqttAndroidClient.connect(mqttConnectOptions, null, new IMqttActionListener() {
                @Override
                public void onSuccess(IMqttToken asyncActionToken) {
                    try {
                        String topic = "deviceUpdate/" + MainActivity.uniqueID + "/";
                        mqttAndroidClient.subscribe(topic, 2);
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
                    } catch (MqttException ex) {

                    }
                }

                @Override
                public void onFailure(IMqttToken asyncActionToken, Throwable exception) {

                }
            });
        } catch (MqttException ex) {
            System.out.println(ex.toString());
        }

    }
}
