package uk.co.appharriso.sixthform;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Typeface;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.util.Arrays;

public class Settings extends AppCompatActivity {
Context context = this;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);
        registerReceiver(new MyReceiver(),
                new IntentFilter("dealwithit"));

        getStuff();
    }


    public void getStuff(){

        databaseHelper database = new databaseHelper(this);
        TextView st = (TextView) findViewById(R.id.nameBox);
        st.setText("You're "+database.getName());
        Intent sender = new Intent(this,connect.class);
        sender.putExtra("toSend","cur");
        startService(sender);


    }

    public void logout(View view){

        databaseHelper database = new databaseHelper(this);

        database.logOutDatabase();
        Intent intent = new Intent(this,login.class);
        startActivity(intent);
        finish();



    }


    private  void errorConnect(){

        new AlertDialog.Builder(this)
                .setTitle("Unable to connect")
                .setMessage("Check that you are connected to the network or try again later. (No response)")
                .setNegativeButton("Okay", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface dialog, int which) {
                        // do nothing
                    }
                })
                .setIcon(android.R.drawable.ic_dialog_alert)
                .show();


    }
    public class MyReceiver extends BroadcastReceiver {
        Dialog dialog = new Dialog(context);

        @Override
        public void onReceive(Context context, Intent intent) {
            Bundle extra = intent.getExtras();


            try{
                if(extra.get("details").equals("errorConnect")){
                    errorConnect();
                }
                if(extra.get("details").equals("wrong")) {

                    new AlertDialog.Builder(context)
                            .setTitle("Incorrect details")
                            .setMessage("Username or password is wrong.")
                            .setNegativeButton("Okay", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    // do nothing
                                }
                            })
                            .setIcon(android.R.drawable.ic_dialog_alert)
                            .show();
                    Intent intent2 = new Intent(context,login.class);
                    startActivity(intent2);
                    finish();


                }




            }
            catch (Exception e){}

            try{
                if(extra.get("current").equals("yes")){
                    TextView st = (TextView) findViewById(R.id.status);
                    st.setText("You're currently in school");
                }
                if(extra.get("current").equals("no")) {
                    TextView st = (TextView) findViewById(R.id.status);
                    st.setText("You're currently out of school");


                }
            }
            catch (Exception e){}
        }

    }



}
