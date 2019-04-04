package online.danshub.alarmo.alarmocomanion;

import android.app.AlertDialog;
import android.app.TimePickerDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.DialogFragment;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TimePicker;
import android.widget.Toast;

import com.amazonaws.mobile.client.AWSMobileClient;
import com.amazonaws.mobile.client.Callback;
import com.amazonaws.mobile.client.UserStateDetails;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class MainActivity extends AWSActivity {

    public List<String> staticListAlarms = new ArrayList<>();
    private ListView alarmTimesList;

    private TimePickerDialog timePickerDialog;
    private final String LOGTAG = MainActivity.class.getCanonicalName();;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        createDialogs();
        createButtons();

        staticListAlarms.add("11:00");
        staticListAlarms.add("21:00");
        staticListAlarms.add("22:00");

        alarmTimesList = findViewById(R.id.alarmTimesList);

        final ArrayAdapter arrayAdapter = new ArrayAdapter(MainActivity.this, android.R.layout.select_dialog_singlechoice, staticListAlarms);

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
                        staticListAlarms.remove(position);
                        arrayAdapter.notifyDataSetChanged();
                    }
                });
                builder.show();
            }
        });

    }

    private void createDialogs() {
        timePickerDialog = new TimePickerDialog(MainActivity.this, new TimePickerDialog.OnTimeSetListener() {
            @Override
            public void onTimeSet(TimePicker timePicker, int hourOfDay, int minutes) {
                Log.v(LOGTAG, "Hour: " + hourOfDay + " - Minute: " + minutes);
            }
        }, 0, 0,  true);
    }

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
                        Toast.makeText(getApplicationContext(), "Message Sent: " + inputText, Toast.LENGTH_LONG).show();
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

        Button testButton = findViewById(R.id.testButton);

        testButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                connectAWS();
            }
        });
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
