package com.example.lifeassistant_project.menu_options;

import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.Toast;

import com.example.lifeassistant_project.R;
import com.example.lifeassistant_project.menu_interface.Menu_options_interface;


public class Life_option extends Menu_options_interface {
    public Life_option(View view, LinearLayout parent_layout){
        super(view,parent_layout,"生活");
        bmp= BitmapFactory.decodeResource(view.getResources(), R.drawable.newstand);
        bmp= Bitmap.createScaledBitmap(bmp,400,400,false);
        createView(parent_layout,"#00ffc5");
    }

    @Override
    public void createSubOption() {
        Toast.makeText(view.getContext(),"Click is OK Life",Toast.LENGTH_SHORT).show();
    }
}
