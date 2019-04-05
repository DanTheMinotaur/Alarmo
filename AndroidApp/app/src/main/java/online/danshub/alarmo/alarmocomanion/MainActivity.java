package online.danshub.alarmo.alarmocomanion;

import android.app.AlertDialog;
import android.app.TimePickerDialog;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.support.design.widget.FloatingActionButton;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.MenuItem;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TimePicker;
import android.widget.Toast;

import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AWSActivity {
    static final String sensorTopic = "Sensor/Data";
    static final String commandTopic = "Alarm/Command";

    public List<String> alarmTimeList = new ArrayList<>();
    private ListView alarmTimesList;

    private TimePickerDialog timePickerDialog;
    private final String LOGTAG = MainActivity.class.getCanonicalName();;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        initialiseAWS();

        createDialogs();
        createButtons();

        alarmTimeList.add("11:00");
        alarmTimeList.add("21:00");
        alarmTimeList.add("22:00");
    }
    
    /**
     * Creates UI dialogs for setting alarms and removing them
     */
    private void createDialogs() {
        timePickerDialog = new TimePickerDialog(MainActivity.this, new TimePickerDialog.OnTimeSetListener() {
            @Override
            public void onTimeSet(TimePicker timePicker, int hourOfDay, int minutes) {
                Log.v(LOGTAG, "Hour: " + hourOfDay + " - Minute: " + minutes);
                String alarmTime = hourOfDay + ":" + minutes;
                publish(buildCommand("time", alarmTime), commandTopic);
                alarmTimeList.add(alarmTime);
            }
        }, 0, 0,  true);

        alarmTimesList = findViewById(R.id.alarmTimesList);

        final ArrayAdapter arrayAdapter = new ArrayAdapter(MainActivity.this, android.R.layout.select_dialog_singlechoice, alarmTimeList);

        alarmTimesList.setAdapter(arrayAdapter);

        alarmTimesList.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            @Override
            public void onItemClick(AdapterView<?> parent, View view, final int position, long id) {
                AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                builder.setTitle("Do you want to remove this alarm?");
                builder.setPositiveButton("YES", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        Log.v(LOGTAG, "Clicked Alarm Time");
                        alarmTimeList.remove(position);
                        arrayAdapter.notifyDataSetChanged();
                    }
                });
                builder.show();
            }
        });
    }

    /**
     * Creates Listener events for buttons.
     */
    private void createButtons() {
        FloatingActionButton alarmChooserButton = findViewById(R.id.alarmCreateButton);
        FloatingActionButton sendMessageButton = findViewById(R.id.sendMessageButton);
        alarmChooserButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                timePickerDialog.show();
            }
        });
        sendMessageButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                AlertDialog.Builder builder = new AlertDialog.Builder(MainActivity.this);
                builder.setTitle("Send a Message to Alarmo");
                final EditText messageInput = new EditText(MainActivity.this);
                LinearLayout.LayoutParams l = new LinearLayout.LayoutParams(
                        LinearLayout.LayoutParams.MATCH_PARENT,
                        LinearLayout.LayoutParams.MATCH_PARENT
                );
                messageInput.setLayoutParams(l);
                builder.setView(messageInput);
                builder.setPositiveButton("SEND", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        String inputText = messageInput.getText().toString();
                        Log.v(LOGTAG, inputText);
                        if (inputText.length() > 0) {
                            publish(buildCommand("message", inputText), commandTopic);
                        } else {
                            Toast.makeText(getApplicationContext(), "There was nothing in that message!", Toast.LENGTH_LONG).show();
                        }
                    }
                });
                builder.setNegativeButton("CANCEL", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        dialog.cancel();
                    }
                });
                builder.show();
            }
        });
    }
}
