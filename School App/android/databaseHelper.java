package uk.co.appharriso.sixthform;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;

/**
 * Created by oharris on 14/04/16.
 */
public class databaseHelper extends SQLiteOpenHelper {


    public databaseHelper(Context context) {
        super(context, "appDataBase.db", null, 2);
    }



    public void updateLoginDetails(String username, String password) {
        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put("username", username);
        values.put("password", password);

        // updating row
        db.update("loginDetails", values, "id" + " = ?",
                new String[]{String.valueOf(1)});
    }


    public void logOutDatabase(){

        SQLiteDatabase db = this.getWritableDatabase();

        ContentValues values = new ContentValues();
        values.put("username", "");
        values.put("password", "");

        // updating row
        db.update("loginDetails", values, "id" + " = ?",
                new String[]{String.valueOf(1)});

    }


    public String getLogin(){
        SQLiteDatabase db = this.getReadableDatabase();

        Cursor cursor = db.query("loginDetails", new String[] { "id",
                        "username", "password" },"id=?",
                new String[] { String.valueOf(1) }, null, null, null, null);
        if (cursor != null)
            cursor.moveToFirst();

        return cursor.getString(1)+":"+cursor.getString(2);

    }


    public String getName(){
        SQLiteDatabase db = this.getReadableDatabase();

        Cursor cursor = db.query("loginDetails", new String[] { "id",
                        "username", "password" },"id=?",
                new String[] { String.valueOf(1) }, null, null, null, null);
        if (cursor != null)
            cursor.moveToFirst();

        return cursor.getString(1);

    }

    @Override
    public void onCreate(SQLiteDatabase db) {

        // creating required tables
        db.execSQL("CREATE TABLE loginDetails ( id INTEGER PRIMARY KEY, username TEXT, password TEXT)");
        ContentValues values = new ContentValues();
        values.put("username","");
        values.put("password", "");
        db.insert("loginDetails",null,values);
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        // on upgrade drop older tables
        db.execSQL("DROP TABLE IF EXISTS loginDetails");


        // create new tables
        onCreate(db);
    }

}
