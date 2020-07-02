package com.example.spug;

import android.content.Intent;
import android.os.AsyncTask;

import androidx.appcompat.app.AppCompatActivity;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;

public class ConnAsyncTask extends AsyncTask<String, Void, Void> {

    private AppCompatActivity appCompatActivity;
    private Class nextClass;

    public ConnAsyncTask(AppCompatActivity appCompatActivity, Class nextClass) {
        this.appCompatActivity = appCompatActivity;
        this.nextClass = nextClass;
    }

    @Override
    protected Void doInBackground(String... strings) {

        HttpURLConnection urlConnection = null;
        try {

            URL url = new URL(strings[0]);
            urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.connect();

            if (urlConnection.getResponseCode() == 200) {
                Intent intent = new Intent(appCompatActivity.getApplicationContext(), this.nextClass);
                this.appCompatActivity.startActivity(intent);
            }
            else {
                MainActivity.responseText.setText("Cant Assign this Cart select another");
            }
        } catch (MalformedURLException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {

        }
        return null;
    }
}
