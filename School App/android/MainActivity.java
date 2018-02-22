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
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.util.Arrays;

public class MainActivity extends AppCompatActivity {
    Context context = this;
    databaseHelper database = new databaseHelper(this);
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        String loginDetails = database.getLogin();
        if(loginDetails.length()<3) {

            Intent intent = new Intent(this,MainActivity.class);
            startActivity(intent);
            finish();
        }

        registerReceiver(new MyReceiver(),
                new IntentFilter("dealwithit"));

        updateTeachers(findViewById(android.R.id.content));



    }


    public void moveToSettings(View view){
        Intent intent = new Intent(this,Settings.class);
        startActivity(intent);
    }

    public void updateTeachers(View view){
        System.out.println("sending to update teachers");
        Intent sender = new Intent(this,connect.class);
        sender.putExtra("toSend","lis");
        startService(sender);


    }


    public void signIn(View view){
        final Dialog dialog = new Dialog(context);
        dialog.setContentView(R.layout.in);

        Button button = (Button) dialog.findViewById(R.id.noIn);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                dialog.dismiss();

            }
        });

        Button button2 = (Button) dialog.findViewById(R.id.yesIn);
        button2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                dialog.dismiss();
                Intent sender = new Intent(context,connect.class);
                sender.putExtra("toSend","sin");
                startService(sender);
            }
        });

        dialog.show();
    }


    public void signOut(View view){

        final Dialog dialog = new Dialog(context);
        dialog.setContentView(R.layout.out);

        Button button = (Button) dialog.findViewById(R.id.noOut);
        button.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                dialog.dismiss();

            }
        });

        Button button2 = (Button) dialog.findViewById(R.id.yesOut);
        button2.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                dialog.dismiss();

                EditText t = (EditText) dialog.findViewById(R.id.leavingReason);
                final String text = t.getText().toString();
                System.out.println("Text from reason: "+text);
                Intent sender = new Intent(context,connect.class);
                sender.putExtra("toSend","out:"+text);
                startService(sender);


            }
        });

        dialog.show();



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

                if (extra.get("who").equals("noone")) {
                    LinearLayout l = (LinearLayout) findViewById(R.id.teacherBlock);
                    TextView ev = new TextView(context);
                    ev.setText("All the teachers are in");
                    l.removeAllViews();
                    l.addView(ev);


                    Intent sender2 = new Intent(context,connect.class);
                    sender2.putExtra("toSend","cur");
                    startService(sender2);


                }


                else{

                    Intent sender2 = new Intent(context,connect.class);
                    sender2.putExtra("toSend","cur");
                    startService(sender2);


                    String read = extra.get("who").toString();
                    String[] teachers = read.split("~");
                    System.out.println(Arrays.toString(teachers));
                    LinearLayout.LayoutParams param = new LinearLayout.LayoutParams(0,LinearLayout.LayoutParams.MATCH_PARENT, 1);

                    LinearLayout l = (LinearLayout) findViewById(R.id.teacherBlock);

                    l.removeAllViews();
                    LinearLayout forthem1 = new LinearLayout(context);
                    forthem1.setOrientation(LinearLayout.HORIZONTAL);
                    TextView title1 = new TextView(context);
                    title1.setText("Teacher");
                    title1.setTypeface(null, Typeface.BOLD);
                    TextView title2 = new TextView(context);
                    title2.setText("Subject");
                    title2.setTypeface(null, Typeface.BOLD);
                    TextView title3 = new TextView(context);
                    title3.setText("Comment");
                    title3.setTypeface(null, Typeface.BOLD);

                    forthem1.addView(title1, param);
                    forthem1.addView(title2, param);
                    forthem1.addView(title3, param);
                    l.addView(forthem1);

                    for (String teacher : teachers) {
                        System.out.println(teacher);
                        String[] split = teacher.split(":",3);
                        System.out.println(Arrays.toString(split));
                        TextView name = new TextView(context);
                        name.setText(split[0]);

                        name.setPadding(0, 20, 0, 0);
                        TextView subject = new TextView(context);
                        subject.setText(split[1]);
                        subject.setPadding(0, 20, 0, 0);

                        TextView comment = new TextView(context);
                        comment.setText(split[2]);
                        comment.setPadding(0, 20, 0, 0);

                        LinearLayout forthem = new LinearLayout(context);
                        forthem.setOrientation(LinearLayout.HORIZONTAL);
                        forthem.addView(name,param);
                        forthem.addView(subject,param);
                        forthem.addView(comment,param);
                        l.addView(forthem);
                    }

                }


            }catch (Exception e){}

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

                if(extra.get("details").equals("in")){
                    new AlertDialog.Builder(context)
                            .setTitle("Updated")
                            .setMessage("Your status has been changed")
                            .setNegativeButton("Okay", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    // do nothing
                                }
                            })
                            .setIcon(android.R.drawable.ic_dialog_alert)
                            .show();
                    Intent sender2 = new Intent(context,connect.class);
                    sender2.putExtra("toSend","cur");
                    startService(sender2);

                }
                if(extra.get("details").equals("out")){
                    new AlertDialog.Builder(context)
                            .setTitle("Updated")
                            .setMessage("Your status has been changed")
                            .setNegativeButton("Okay", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    // do nothing
                                }
                            })
                            .setIcon(android.R.drawable.ic_dialog_alert)
                            .show();
                    Intent sender2 = new Intent(context,connect.class);
                    sender2.putExtra("toSend","cur");
                    startService(sender2);

                }


            }
            catch (Exception e){}

            try{
                if(extra.get("current").equals("yes")){
                    Button out = (Button) findViewById(R.id.signOut);
                    out.setVisibility(View.VISIBLE);
                    Button in = (Button) findViewById(R.id.signIn);
                    in.setVisibility(View.INVISIBLE);
                }
                if(extra.get("current").equals("no")) {

                    new AlertDialog.Builder(context)
                            .setTitle("Signed out")
                            .setMessage("Don't forget to sign back in!")
                            .setNegativeButton("I'll remember", new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    // do nothing
                                }
                            })
                            .setPositiveButton("Do it now",new DialogInterface.OnClickListener() {
                                public void onClick(DialogInterface dialog, int which) {
                                    signIn(findViewById(android.R.id.content));
                                }
                            })
                            .setIcon(android.R.drawable.ic_dialog_alert)
                            .show();
                    Button out = (Button) findViewById(R.id.signOut);
                    out.setVisibility(View.INVISIBLE);
                    Button in = (Button) findViewById(R.id.signIn);
                    in.setVisibility(View.VISIBLE);

                }
            }
            catch (Exception e){}
        }

    }

}
