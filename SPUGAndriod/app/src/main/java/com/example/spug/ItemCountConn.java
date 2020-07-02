package com.example.spug;

import android.os.AsyncTask;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

public class ItemCountConn extends AsyncTask<String, Void, Void> {

    @Override
    protected Void doInBackground(String... strings) {
        StringBuilder count = new StringBuilder();
        try {
            URL url = new URL(strings[0]);
            HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
            urlConnection.connect();
            InputStream in = new BufferedInputStream(urlConnection.getInputStream());

            BufferedReader reader = new BufferedReader(new InputStreamReader(in));

            String line;
            while ((line = reader.readLine()) != null) {
                count.append(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        SubscribeItems.itemsView.append(count.toString());
        return null;
    }
}
