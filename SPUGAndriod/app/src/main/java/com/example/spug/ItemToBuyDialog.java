package com.example.spug;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDialogFragment;

import org.eclipse.paho.android.service.MqttAndroidClient;
import org.eclipse.paho.client.mqttv3.IMqttActionListener;
import org.eclipse.paho.client.mqttv3.IMqttToken;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.json.JSONException;
import org.json.JSONObject;

public class ItemToBuyDialog extends AppCompatDialogFragment {

    JSONObject json;
    AppCompatActivity previousActivity;

    public ItemToBuyDialog(JSONObject json, AppCompatActivity appCompatActivity) {
        this.json = json;
        this.previousActivity = appCompatActivity;
    }
    @Override
    public Dialog onCreateDialog(Bundle savedInstanceState) {
        AlertDialog.Builder builder = new AlertDialog.Builder(getActivity());
        LayoutInflater inflater = getActivity().getLayoutInflater();
        View view = inflater.inflate(R.layout.dialog_item_to_buy, null);
        String item = "";
        try {
            item = this.json.getString("itemPurchased");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        builder.setView(view).setTitle("Input Required").setMessage("Do you want to buy " + item + " ?").setPositiveButton("YES", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                try {
                    String time = String.valueOf(System.currentTimeMillis());
                    ItemPurchasedList.getInstance().add(new ItemPurchasedDetail(json.getString("itemPurchased"), json.getString("calorie"), json.getString("fat"), json.getString("carbohydrate"), json.getString("protein"), json.getString("salt"), time));
                    UnAssignCartView.listOfItems.append(json.getString("itemPurchased") + " = " + json.getString("cost") + ";");

                    String clientId = MqttClient.generateClientId();
                    final MqttAndroidClient mqttAndroidClient = new MqttAndroidClient(getContext(), MainActivity.mqttUrl, clientId);

                    try {
                        IMqttToken token = mqttAndroidClient.connect();
                        token.setActionCallback(new IMqttActionListener() {
                            @Override
                            public void onSuccess(IMqttToken asyncActionToken) {
                                try {
                                    previousActivity.finish();
                                    MqttMessage message = new MqttMessage();
                                    String jsonMessage = "{\"toBuyItem\": " + "\"" + "YES" + "\"" +", \"deviceId\": " + "\"" + MainActivity.uniqueID + "\"" + ", \"itemPurchased\": " + "\"" + json.getString("itemPurchased") +"\"" +"}";
                                    message.setPayload(jsonMessage.getBytes());
                                    mqttAndroidClient.publish("toBuyItem/", message);
                                } catch (MqttException | JSONException e) {
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
                } catch (JSONException e) {
                    e.printStackTrace();
                }
            }
        }).setNegativeButton("NO", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                String clientId = MqttClient.generateClientId();
                final MqttAndroidClient mqttAndroidClient = new MqttAndroidClient(getContext(), MainActivity.mqttUrl, clientId);

                try {
                    IMqttToken token = mqttAndroidClient.connect();
                    token.setActionCallback(new IMqttActionListener() {
                        @Override
                        public void onSuccess(IMqttToken asyncActionToken) {
                            try {
                                previousActivity.finish();
                                MqttMessage message = new MqttMessage();
                                String jsonMessage = "{\"toBuyItem\": " + "\"" + "NO" + "\"" +", \"deviceId\": " + "\"" + MainActivity.uniqueID + "\"" + ", \"itemPurchased\": " + "\"" + json.getString("itemPurchased") +"\"" +"}";
                                message.setPayload(jsonMessage.getBytes());
                                mqttAndroidClient.publish("toBuyItem/", message);
                            } catch (MqttException | JSONException e) {
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
            }
        });
        return builder.create();
    }
}
