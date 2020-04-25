package com.example.lifeassistant_project.menu_option_to_link;

import android.view.View;
import android.widget.LinearLayout;
import android.widget.Toast;

import com.example.lifeassistant_project.menu_interface.Options_choices_interface;

public class FinMan_Invoice extends Options_choices_interface {
    public FinMan_Invoice(LinearLayout linearLayout, View view, String choice_name, String backGround){
        super(linearLayout,view,choice_name,backGround);
    }

    @Override
    public void toLink() {
        Toast.makeText(view.getContext(), "For invoice", Toast.LENGTH_SHORT).show();
    }
}
