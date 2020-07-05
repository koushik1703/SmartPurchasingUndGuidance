package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONObject;

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
                String clientId = MqttClient.generateClientId();
                final MqttAndroidClient mqttAndroidClient = new MqttAndroidClient(getApplicationContext(), "tcp://192.168.0.103:1883", clientId);

                try {
                    IMqttToken token = mqttAndroidClient.connect();
                    token.setActionCallback(new IMqttActionListener() {
                        @Override
                        public void onSuccess(IMqttToken asyncActionToken) {
                            try {
                                for(String item : AddItems.itemList) {
                                    MqttMessage message = new MqttMessage();
                                    String jsonMessage = "{\"itemName\": " + "\"" + item + "\"" +", \"deviceId\": " + "\"" + MainActivity.uniqueID + "\"}";
                                    message.setPayload(jsonMessage.getBytes());
                                    mqttAndroidClient.publish("buyItemFromDevice/", message);
                                }
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
                startActivity(intent);
            }
        });

        for(String item : AddItems.itemList) {
            ItemCountConn itemCountConn = new ItemCountConn();
            itemCountConn.execute(hostUrl + "getItemCount/" + Integer.parseInt(item.substring(4, item.length())));
        }
    }
}
