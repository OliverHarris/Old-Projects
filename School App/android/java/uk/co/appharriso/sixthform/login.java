package uk.co.appharriso.sixthform;

import android.app.AlertDialog;
import android.app.Dialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.TimeoutException;

public class login extends AppCompatActivity {
    Context context = this;
    databaseHelper database = new databaseHelper(this);
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_login);




        String loginDetails = database.getLogin();
        if(loginDetails.length()>3) {

            Intent intent = new Intent(this,MainActivity.class);
            startActivity(intent);
            finish();
        }

        registerReceiver(new MyReceiver(),
                new IntentFilter("dealwithit"));
    }


    public void loginClick(View view){

        //get username
        EditText username = (EditText) findViewById(R.id.username);
        final String u = username.getText().toString();
        //get password
        EditText password = (EditText) findViewById(R.id.password);
        final String p = password.getText().toString();

        //check if username or password is blank
        if(u.length()==0 || p.length()==0){
            new AlertDialog.Builder(this)
                    .setTitle("Username/password")
                    .setMessage("Please enter a value!")
                    .setNegativeButton("Okay", new DialogInterface.OnClickListener() {
                        public void onClick(DialogInterface dialog, int which) {
                            // do nothing
                        }
                    })
                    .setIcon(android.R.drawable.ic_dialog_alert)

                    .show();
        }
        else{
            //send the info to the sending system thingy

            final String what =u+":"+p;
            Socket socket = null;

            final int SERVERPORT = 2030;
            final String SERVER_IP =  "chepstow.website";
            new Thread(new Runnable() {
                public void run() {
                    databaseHelper database = new databaseHelper(context);
                    Socket socket = null;
                    //we only need to connect once..
                    try {
                        InetAddress serverAddr = InetAddress.getByName(SERVER_IP);
                        socket = new Socket(serverAddr, SERVERPORT);

                    } catch (UnknownHostException e) {
                        e.printStackTrace();
                        Intent i = new Intent("dealwithit");
                        i.putExtra("details", "errorConnect");
                        sendBroadcast(i);
                        return;
                    } catch (IOException e) {
                        e.printStackTrace();
                        Intent i = new Intent("dealwithit");
                        i.putExtra("details", "errorConnect");
                        sendBroadcast(i);
                        return;
                    }


                    try {
                        PrintWriter out = new PrintWriter(new BufferedWriter(
                                new OutputStreamWriter(socket.getOutputStream())),
                                true);

                        out.println(what);

                        out.flush();
                    } catch (IOException e) {
                        e.printStackTrace();
                        return;
                    }
                    while(true){
                        String read = "";
                        try {
                            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                            read = in.readLine();
                        } catch (IOException e) {
                            e.printStackTrace();
                            return;
                        }


                        //now we can deal with what we've been given..
                        if(read == null){
                            System.out.println("Null data");
                            break;
                        }

                        System.out.println("Read: " + read);
                        if (read.startsWith("2")) {
                            database.updateLoginDetails("","");
                            Intent i = new Intent("dealwithit");
                            i.putExtra("details", "wrong");
                            sendBroadcast(i);
                        }

                        if (read.startsWith("3")) {
                            database.updateLoginDetails(u,p);
                            Intent i = new Intent("dealwithit");
                            i.putExtra("details", "correct");
                            sendBroadcast(i);

                        }



                    }
                }
            }).start();
        }


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
                if (extra.get("details").equals("correct")) {
                    Intent newWindow = new Intent(context, MainActivity.class);
                    startActivity(newWindow);
                    finish();
                }



                if (extra.get("details").equals("wrong")) {

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
                }


                if(extra.get("details").equals("errorConnect")){
                    System.out.println("Erorr connecting");
                    errorConnect();
                }

            }catch (Exception e){}
        }

    }


}
