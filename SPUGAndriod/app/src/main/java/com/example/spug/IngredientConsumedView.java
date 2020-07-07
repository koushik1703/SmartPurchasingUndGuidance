package com.example.spug;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class IngredientConsumedView extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ingredient_consumed_view);

        final EditText startTime = findViewById(R.id.startTime);
        final EditText endTime = findViewById(R.id.endTime);

        Button showButton = findViewById(R.id.showButton);

        final TextView calorieTextView = findViewById(R.id.calorieTextView);
        final TextView fatTextView = findViewById(R.id.fatTextView);
        final TextView carbohydrateTextView = findViewById(R.id.carbohydrateTexttView);
        final TextView proteinTextView = findViewById(R.id.proteinTextView);
        final TextView saltTextView = findViewById(R.id.saltTextView);

        showButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String start = startTime.getText().toString();
                String end = endTime.getText().toString();
                long startmilliseconds = 0;
                long endmilliseconds = 0;
                SimpleDateFormat dateFormat = new SimpleDateFormat("MM/dd/yyyy", Locale.ENGLISH);
                try {
                    startmilliseconds = dateFormat.parse(start).getTime();
                    endmilliseconds = dateFormat.parse(end).getTime();
                } catch (ParseException e) {
                    e.printStackTrace();
                }

                int calorieValue = 0;
                int fatValue = 0;
                int carbohydrateValue = 0;
                int proteinValue = 0;
                int saltValue = 0;

                for(ItemPurchasedDetail item : ItemPurchasedList.getInstance()) {
                    if((Long.parseLong(item.time) >= startmilliseconds) && (Long.parseLong(item.time) <= endmilliseconds)) {
                        calorieValue = calorieValue + Integer.parseInt(item.calorie);
                        fatValue = fatValue + Integer.parseInt(item.fat);
                        carbohydrateValue = carbohydrateValue + Integer.parseInt(item.carbohydrate);
                        proteinValue = proteinValue + Integer.parseInt(item.protein);
                        saltValue = saltValue + Integer.parseInt(item.salt);
                    }
                }

                calorieTextView.setText("Calorie quantity :" + calorieValue);
                fatTextView.setText("Fat quantity :" + fatValue);
                carbohydrateTextView.setText("Carbohydrate quantity :" + carbohydrateValue);
                proteinTextView.setText("Protein quantity :" + proteinValue);
                saltTextView.setText("Salt quantity :" + saltValue);
            }
        });
    }
}
