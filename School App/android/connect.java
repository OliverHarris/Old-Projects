package uk.co.appharriso.sixthform;

import android.app.IntentService;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

/**
 * Created by oharris on 16/07/16.
 */
public class connect  extends IntentService {
    public connect() {
        super("Connect");
    }
    Bundle extras;
    Context context = this;
    @Override
    protected void onHandleIntent(Intent intent) {

    }


    public int onStartCommand(Intent intent, int flags, int startId) {
        System.out.println("At service, block 1");
        try {
            extras = intent.getExtras();
        }
        catch (Exception e){

        }
        start();

        return START_STICKY;
    }
    private void start() {
        try {
            databaseHelper database = new databaseHelper(this);
            Socket socket = null;
            System.out.println("Sending this: " + extras.get("toSend").toString());
            final int SERVERPORT = 2030;
            final String SERVER_IP = "chepstow.website";
            new Thread(new Runnable() {
                public void run() {
                    databaseHelper database = new databaseHelper(context);
                    Socket socket = null;
                    //we only need to connect once..
                    try {
                        InetAddress serverAddr = InetAddress.getByName(SERVER_IP);
                        System.out.println(serverAddr.toString());
                        socket = new Socket(serverAddr, SERVERPORT);

                    } catch (UnknownHostException e) {
                        System.out.println(e.getMessage().toString());
                        Intent i = new Intent("dealwithit");
                        i.putExtra("details", "errorConnect");
                        sendBroadcast(i);
                        return;
                    } catch (IOException e) {
                        System.out.println(e.getMessage().toString());
                        Intent i = new Intent("dealwithit");
                        i.putExtra("details", "errorConnect");
                        sendBroadcast(i);
                        return;
                    }


                    try {
                        PrintWriter out = new PrintWriter(new BufferedWriter(
                                new OutputStreamWriter(socket.getOutputStream())),
                                true);

                        out.println(database.getLogin());

                        out.flush();
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                    while (true) {
                        String read = "";
                        try {
                            BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

                            read = in.readLine();
                        } catch (IOException e) {
                            e.printStackTrace();
                        }


                        //now we can deal with what we've been given..
                        try {
                            if (read == null || extras.get("toSend") == null) {
                                System.out.println("Null data");
                                break;
                            }
                        } catch (Exception e) {
                            System.out.println(e.getMessage().toString());
                            return;
                        }

                        System.out.println("Read: " + read);
                        if (read.startsWith("2")) {
                            database.updateLoginDetails("", "");
                            Intent i = new Intent("dealwithit");
                            i.putExtra("details", "wrong");
                            sendBroadcast(i);
                        }

                        if (read.startsWith("3")) {
                            try {
                                PrintWriter out = new PrintWriter(new BufferedWriter(
                                        new OutputStreamWriter(socket.getOutputStream())),
                                        true);

                                out.println(extras.get("toSend").toString());
                                out.flush();
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }

                        if (read.startsWith("4")) {
                            Intent i = new Intent("dealwithit");
                            i.putExtra("who", "noone");
                            sendBroadcast(i);
                        }
                        if (read.startsWith("5")) {
                            Intent i = new Intent("dealwithit");
                            i.putExtra("who", read.substring(1, read.length()));
                            sendBroadcast(i);
                        }
                        if (read.startsWith("6")) {
                            System.out.println("its at 6");
                            Intent i = new Intent("dealwithit");
                            i.putExtra("details", "out");
                            sendBroadcast(i);
                        }
                        if (read.startsWith("7")) {
                            Intent i = new Intent("dealwithit");
                            i.putExtra("details", "in");
                            sendBroadcast(i);
                        }
                        if (read.startsWith("8")) {
                            Intent i = new Intent("dealwithit");
                            i.putExtra("current", "no");
                            sendBroadcast(i);
                        }
                        if (read.startsWith("9")) {
                            Intent i = new Intent("dealwithit");
                            i.putExtra("current", "yes");
                            sendBroadcast(i);
                        }


                    }
                }


            }


            ).start();
        }catch(Exception e){
                System.out.println("Avoiding crash.. but the error is: ");
                System.out.println(e.getMessage().toString());
            }
    }


}
