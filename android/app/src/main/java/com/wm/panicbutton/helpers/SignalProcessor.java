package com.wm.panicbutton.helpers;

import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.util.Log;

import com.wm.panicbutton.interfaces.Processor;


public class SignalProcessor implements Processor {

    // TODO
    private static final String TAG = "PROCESSOR";
    private static final String EMERGENCY_NUMBER = "6692219715";
    private static final String SIGNAL_1 = "1";
    private static final String SIGNAL_2 = "2";
    private static final String SIGNAL_3 = "3";
    private static final String SEVERITY_MESSAGE_SIGNAL_1 = "INFO\n";
    private static final String SEVERITY_MESSAGE_SIGNAL_2 = "WARNING\n";
    private static final String SEVERITY_MESSAGE_SIGNAL_3 = "DANGER\n";

    private Context context;
    private Sms sms;
    private ContactManager contactManager;
    private static String severity;

    public SignalProcessor(Context context) {
        this.context = context;
        sms = new Sms(this.context);
        contactManager = new ContactManager(context);
    }

    @Override
    public void process(String signal) {
        // TODO
        Log.i(TAG, signal);
        severity = signal;
        String message = getSeverityMessage() + LocationUpdater.getAddress() == null? null:LocationUpdater.getAddress() + "\n" + LocationUpdater.getMapsURL();
        switch (severity) {
            case SIGNAL_1: {
                if(contactManager.hasFavoriteContact()) {
                    sms.sendSMSs(contactManager.getFavoriteContacts(), message);
                } else {
                    sms.sendSMSs(contactManager.getContacts(), message);
                }
                break;
            }
            case SIGNAL_2: {
                sms.sendSMSs(contactManager.getContacts(), message);
                break;
            }
            case SIGNAL_3: {
                sms.sendSMSs(contactManager.getContacts(), message);
                emergencyCall();
                break;
            }
        }
    }

    @SuppressLint("MissingPermission")
    private void emergencyCall() {
        Log.i(TAG, "emergency call activated");
        Intent intent = new Intent(Intent.ACTION_CALL);
        intent.setData(Uri.parse("tel:" + EMERGENCY_NUMBER));
        context.startActivity(intent);
    }

    public static String getSeverityMessage() {
        switch (severity) {
            case SIGNAL_1: {
                return SEVERITY_MESSAGE_SIGNAL_1;
            }
            case SIGNAL_2: {
                return SEVERITY_MESSAGE_SIGNAL_2;
            }
            case SIGNAL_3: {
                return SEVERITY_MESSAGE_SIGNAL_3;
            }
            default: {
                return SEVERITY_MESSAGE_SIGNAL_1;
            }
        }
    }

}
