from stream.server import stream_server,get_local_ip,streamer
import flet as ft
import json
import os

SETTINGS_FILE = "settings.json"

# Default settings
default_settings = {
    "port": "80",
    "quality": 50,
    "fps": 30,
    "monitor": "0",
    "cursor_size": "30",
    "cursor_type": 1
}
# Load settings from JSON
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return default_settings.copy()

# Save settings to JSON
def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

class ModernContainer(ft.Container):
    def __init__(self, label, content, on_click=None, height=70):
        super().__init__()
        self.content = ft.Row([
            ft.Text(label, size=16, weight='w500', color="#F0F0F0"),
            content                
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        self.bgcolor = '#1c1c1e'
        self.on_click = on_click
        self.border_radius = 15
        self.padding = 15
        self.height = height
        self.shadow = ft.BoxShadow(
            spread_radius=1,
            blur_radius=4,
            color=ft.Colors.BLACK54,
            offset=ft.Offset(0, 2)
        )
        self.expand=True
        self.animate = ft.Animation(300, ft.AnimationCurve.EASE_OUT)

class App(ft.Container):
    def __init__(self,content):
        super().__init__()
        self.content = content
        self.padding=ft.Padding.all(25)
        self.alignment=ft.Alignment.TOP_CENTER
        self.bgcolor="#121212"


primary_color="#467C6F"

def main(page: ft.Page):
    settings = load_settings()
    page.window.resizable = False
    page.window.maximizable = False
    page.window.width = 700
    page.window.height = 700
    page.title = 'LanStream'
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = '#121212'
    page.window.icon = 'icon.ico'
    page.run_task(stream_server)
    page.run_task(streamer.capture_loop)
    
    # Status indicator
    status_indicator = ft.Row([
        ft.Text('Online',color=ft.Colors.WHITE,size=18),
        ft.Container(
            width=15,
            height=15,
            border_radius=50,
            bgcolor=ft.Colors.GREEN_700,
            tooltip="Online"
        ),
    ])
    
    # Quality slider
    quality_slider = ft.Slider(
        min=1, 
        max=100, 
        value=settings["quality"], 
        divisions=100,
        width=200,
        active_color=primary_color,
        inactive_color=ft.Colors.GREY_800,
        thumb_color='white',
        label="{value}%"
    )
    
    # FPS slider
    fps_slider = ft.Slider(
        min=1, 
        max=60, 
        value=settings["fps"], 
        divisions=60,
        width=200,
        active_color=primary_color,
        inactive_color=ft.Colors.GREY_800,
        thumb_color='white',
        label="{value} FPS",
    )
    
    # Cursor size field
    cursor_size = ft.TextField(
        value=settings["cursor_size"],
        width=100,
        height=40,
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        border_color=ft.Colors.GREY_700,
        focused_border_color=primary_color,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREY_900
    )
    
    # Port field
    port_field = ft.TextField(
        value=settings["port"],
        width=100,
        height=40,
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        border_color=ft.Colors.GREY_700,
        focused_border_color=primary_color,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREY_900
    )
    
    # Monitor index field
    monitor_index = ft.TextField(
        value=settings["monitor"],
        width=100,
        height=40,
        text_align=ft.TextAlign.CENTER,
        border_radius=10,
        border_color=ft.Colors.GREY_700,
        focused_border_color=primary_color,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREY_900
    )
    
    # Streaming switch
    streaming_switch = ft.Switch(
        value=True,
        active_color=ft.Colors.WHITE70,
        active_track_color=ft.Colors.BLUE_700,
        inactive_thumb_color=ft.Colors.GREY_600,
        inactive_track_color=ft.Colors.GREY_800
    )
    
    # Cursor selection
    def cursor_box(img, idx):
        return ft.Container(
            ft.Image(src=img), 
            padding=8,
            border_radius=8,
            border=ft.Border.all(3 if settings["cursor_type"]==idx else 2, primary_color if settings["cursor_type"]==idx else "white"),
            data=idx,
            on_click=lambda e: select_cursor(e)
        )
    
    cursor_options = ft.Row([
        cursor_box('./assets/cursor1.png',1),
        cursor_box('./assets/cursor4.png',2),
        cursor_box('./assets/cursor3.png',3)
    ], spacing=5)

    # Function to toggle status
    def toggle_streaming(e):
        if streaming_switch.value:
            status_indicator.controls[1].bgcolor = ft.Colors.GREEN_700
            status_indicator.controls[1].tooltip = "Online"
            status_indicator.controls[0].value = 'Online'

        else:
            status_indicator.controls[1].bgcolor = ft.Colors.RED_700
            status_indicator.controls[1].tooltip = "Offline"
            status_indicator.controls[0].value = 'Offline'
        status_indicator.update()
    
    streaming_switch.on_change = toggle_streaming

    # Cursor selection function
    def select_cursor(e):
        for c in cursor_options.controls:
            c.border = ft.Border.all(2,"white")
        e.control.border = ft.Border.all(3,primary_color)
        settings["cursor_type"] = e.control.data
        cursor_options.update()
    
    # Save button
    def save_clicked(e):
        settings_data = {
            "port": port_field.value,
            "quality": int(quality_slider.value),
            "fps": int(fps_slider.value),
            "monitor": monitor_index.value,
            "cursor_size": cursor_size.value,
            "cursor_type": settings["cursor_type"]
        }
        save_settings(settings_data)
        page.snack_bar = ft.SnackBar(ft.Text("Settings saved!", color=ft.Colors.WHITE))
        page.snack_bar.open = True
        page.update()

    save_button = ft.Button(
        content=ft.Text("Save Settings", weight="w600"),
        width=200,
        height=45,
        style=ft.ButtonStyle(
            bgcolor=primary_color,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=save_clicked
    )
    
    # Build the UI
    page.add(
        App(
            ft.Column([
                # Header
                ft.Container(
                    ft.Row([
                        ft.Text(get_local_ip(), size=24, weight='w700', color="#D1D1D1",font_family='consolas'),
                        status_indicator
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.Padding.only(bottom=20)
                ),
                
                # Settings sections
                ft.Row([
                    ModernContainer(
                        "Status",
                        ft.Row([ft.Text("Online",color=ft.Colors.GREY_400), streaming_switch])
                    ),
                    ModernContainer(
                        "Port",
                        port_field
                    ),
                ]),
                ft.Row([
                    ModernContainer(
                        "Video Quality",
                        quality_slider,
                        height=85
                    ),
                    ModernContainer(
                        "FPS",
                        fps_slider,
                        height=85
                    ),
                ]),
                
                ft.Row([
                    ModernContainer(
                        "Monitor",
                        monitor_index
                    ),
                    
                    ModernContainer(
                        "Cursor Size",
                        cursor_size
                    ),
                ]),
                
                ModernContainer(
                    "Cursor Type",
                    cursor_options
                ),
                
                # Save button
                ft.Container(
                    save_button,
                    alignment=ft.Alignment.CENTER,
                    padding=ft.Padding.only(top=20)
                )
                
            ],horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        )
    )

ft.run(main)
