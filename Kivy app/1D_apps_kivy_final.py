from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
# =============================================================================
# #get the firebase function
# =============================================================================

from firebase import *

def getAction(dict_bin_info):
    bin_ack = dict_bin_info["ack"]
    bin_status = dict_bin_info["status"]
    
    if bin_ack == "N" and bin_status != "not full, no spill":
        return "I'll Go!"
        
    elif bin_ack == "Y" and bin_status != "not full, no spill":
        return "Report Faulty"
        
    else:
        return ""

class HomeScreen(Screen): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        home_f = FloatLayout()
        
        # get background image
        home_img = Image(source='homescreen.jpg',
                         allow_stretch=True,
                         keep_ratio=False)
        
        # instantiate button widgets for home
        homelabel_x = 0.55
        homelabel_y = 0.06
        home_btn = Button(size_hint=(homelabel_x, homelabel_y),
                          background_color = [0,0,0,0],
                          pos_hint={'x':0.5-(homelabel_x/2), 'y':0.34-(homelabel_y/2)})        
        
        quit_btn = Button(size_hint=(homelabel_x, homelabel_y),
                          background_color = [0,0,0,0],
                          pos_hint={'x':0.5-(homelabel_x/2), 'y':0.275-(homelabel_y/2)})  
        
        # bind events to widgets
        home_btn.bind(on_press = self.to_building)
        quit_btn.bind(on_press = self.close_app)
        
        home_f.add_widget(home_img)
        home_f.add_widget(home_btn)
        home_f.add_widget(quit_btn)
        self.add_widget(home_f)
        
    def to_building(self, instance):
        print("to building")
        App.get_running_app().root.switch_to(BuildingScreen())
    
    def close_app(self, *args):
        print("closing app")
        App.get_running_app().stop()
        
class BuildingScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        bldg_f = FloatLayout()
        
        #get the background image source based on bin status in each level
        if "l1" in getWarning():
            bldg_source = "building_warning.jpg"
        else:
            bldg_source = "building_no_warning.jpg"
        
        bldg_pic = Image(source = bldg_source,
                         allow_stretch = True, 
                         keep_ratio = False)
        
        # instantiate button widgets for each level in the building
        level_x = 0.55
        level_y = 0.145
        btn_level1 = Button(text = "l1",
                            color = [0,0,0,0],
                            size_hint=(level_x, level_y),
                            background_color = [0,0,0,0],
                            pos_hint={'x':0.5-(level_x/2), 'y':0.388-(level_y/2)})        
       
        bldg_btn_back = Button(background_color = [0,0,0,0],
                               size_hint = (0.4, 0.07),
                               pos_hint = {"x":0, "y":0.93})

        # bind events to widgets
        btn_level1.bind(on_press = self.to_level)
        bldg_btn_back.bind(on_press = self.to_home)
        
        bldg_f.add_widget(bldg_pic)
        bldg_f.add_widget(btn_level1)

        bldg_f.add_widget(bldg_btn_back)
        self.add_widget(bldg_f)
        
    def to_home(self, instance):
        print("back to home")
        App.get_running_app().root.switch_to(HomeScreen())
    
    def to_level(self, instance):
        App.get_running_app().level = instance.text
        print("go level")
        App.get_running_app().root.switch_to(LevelScreen())
 
          
class LevelScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        level_f = FloatLayout()
              
        # Extract bin1, bin2, bin3 information from firebase
        dict_bin1_info, bin1_color, message1 = getBinMessage_Info(App.get_running_app().level, "bin1")
        dict_bin2_info, bin2_color, message2 = getBinMessage_Info(App.get_running_app().level, "bin2")
        dict_bin3_info, bin3_color, message3 = getBinMessage_Info(App.get_running_app().level, "bin3")
        
        # get background image
        level_img = Image(source='floorplan.jpg',
                          allow_stretch=True,
                          keep_ratio=False)
        
        # instantiate button widgets for bin1, bin2, bin 3, back
        self.d1 = Button(background_normal = '',
                         background_color = bin1_color + [1],
                         text='1', 
                         size_hint=(0.1,0.1),
                         color = [0,0,0,1],
                         pos_hint={'x':0.35, 'y':0.3})
        self.d2 = Button(background_normal = '',
                         background_color = bin2_color + [1],
                         text='2',
                         size_hint=(0.1,0.1),
                         color = [0,0,0,1],
                         pos_hint={'x':.19, 'y':.7})
        self.d3 = Button(background_normal = '',
                         background_color = bin3_color + [1],
                         text='3',
                         size_hint=(0.1,0.1),
                         color = [0,0,0,1],
                         pos_hint={'x':0.63, 'y':0.5})
        
        level_btn_back = Button(background_color = [0,0,0,0],
                                size_hint = (0.4, 0.07),
                                pos_hint = {"x":0, "y":0.93})
        
        #bind events to widgets
        level_btn_back.bind(on_press = self.to_building) 
        self.d1.bind(on_press = self.to_bin)
        self.d2.bind(on_press = self.to_bin)
        self.d3.bind(on_press = self.to_bin)
        
        #add widgets
        level_f.add_widget(level_img)
        level_f.add_widget(self.d1)
        level_f.add_widget(self.d2)
        level_f.add_widget(self.d3)
        level_f.add_widget(level_btn_back)
        
        self.add_widget(level_f)
        
    def to_building(self, instance):
        App.get_running_app().root.switch_to(BuildingScreen())
  
    def to_bin(self, instance):
        print("to bin information")
        App.get_running_app().bin_name = "bin"+instance.text
        App.get_running_app().root.switch_to(BinScreen())
        
        
class BinScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dict_bin_info, bin_color, message = getBinMessage_Info(App.get_running_app().level,App.get_running_app().bin_name)
        loc_status = "{}, {}".format(dict_bin_info["location"],dict_bin_info["status"])
        
        bin_f = FloatLayout()
        
        #get the background image source based on bin color
        if dict_bin_info["color"] == "green":
            bg_source = "dustbin_G.jpg"
        elif dict_bin_info["color"] == "yellow":
            bg_source = "dustbin_Y.jpg"
        else:
            bg_source = "dustbin_R.jpg"
        
        bg_pic = Image(source = bg_source, 
                       allow_stretch = True, 
                       keep_ratio = False)
        
        # instantiate label widgets for bin description, location status
        lbl_binDesc_x = 0.1
        lbl_binDesc_y = 0.1
        lbl_binDesc = Label(text = message,
                            color = [0,0,0,1],
                            size_hint = (lbl_binDesc_x, lbl_binDesc_y),
                            pos_hint = {"x":0.5-(lbl_binDesc_x/2), "y":0.80-(lbl_binDesc_y/2)},
                            halign = "center") 
        
        #set different font size for different messages
        if message == "I'm Good! :)":
            lbl_binDesc.font_size = "30sp"
        else:
            lbl_binDesc.font_size = "15sp"
        
        lbl_location_status_x = 0.1
        lbl_location_status_y = 0.1
        lbl_location_status = Label(text = loc_status,
                                    font_size = "15sp",
                                    color = [0,0,0,1],
                                    size_hint = (lbl_location_status_x,lbl_location_status_y), 
                                    pos_hint = {"x":0.5-(lbl_location_status_x/2), "y":0.74-(lbl_location_status_y/2)})
            
        # instantiate button widget for back
        btn_back = Button(background_color = [0,0,0,0],
                          size_hint = (0.4, 0.07),
                          pos_hint = {"x":0, "y":0.93})
        
        action = getAction(dict_bin_info)
        
        btn_action_x = 0.5
        btn_action_y = 0.08
        self.btn_action = Button(text = action,
                                 #background_color = [222/255, 229/255, 234/255, 1],
                                 font_size = 20,
                                 size_hint = (btn_action_x, btn_action_y),
                                 pos_hint = {"x":0.505-(btn_action_x/2), "y":0.0+(btn_action_y/2)})
         
        btn_back.bind(on_press = self.to_level)
        self.btn_action.bind(on_press = self.updateDb)
        
        bin_f.add_widget(bg_pic)
        bin_f.add_widget(lbl_binDesc)
        bin_f.add_widget(lbl_location_status)
        bin_f.add_widget(btn_back)
        
        if action != "":
            bin_f.add_widget(self.btn_action)
        
        #add widget
        self.add_widget(bin_f)
        
    def to_level(self, instance):
        print("to level btn pressed")
        App.get_running_app().root.switch_to(LevelScreen())
        
    def updateDb(self,instance):
        if self.btn_action.text == "I'll Go!":
            print("I'll Go!")
            updateBin_ack(App.get_running_app().level, App.get_running_app().bin_name)
            
        else:
            print("report faulty")
            updateBin_ack(App.get_running_app().level, App.get_running_app().bin_name, True)
            
        print("back to level")
        App.get_running_app().root.switch_to(LevelScreen())
  
    
class MyApp(App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.level = "l1"
        self.bin_name = "bin1"
    
    def build(self):
# =============================================================================
#         # instantiate screen manager
# =============================================================================
        sm = ScreenManager()
        home_screen = HomeScreen(name="home screen")
        level_screen = LevelScreen(name = "level screen")
            
        # Adding screen widgets to parent sm
        sm.add_widget(home_screen)
        sm.add_widget(level_screen)
        
        return sm

# =============================================================================
# #main function
# =============================================================================

if __name__ == "__main__":
    MyApp().run()

