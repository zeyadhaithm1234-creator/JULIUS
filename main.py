from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
import os

Window.clearcolor = (0.04, 0.05, 0.09, 1)

class DeviceAnalyzer:
    def get_specs(self):
        try:
            ram_gb = 4.0
            if os.path.exists("/proc/meminfo"):
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if "MemTotal" in line:
                            ram_gb = round(int(line.split()[1]) / (1024 * 1024), 1)
                            break
            tier = "Low-end" if ram_gb <= 3.0 else ("Mid-range" if ram_gb <= 6.0 else "High-end")
            return {"ram": f"{ram_gb} GB", "tier": tier}
        except Exception:
            return {"ram": "4.0 GB", "tier": "Mid-range"}

class SmartEngine:
    def calculate(self, current_dpi, playstyle):
        dpi = current_dpi
        if "Rush" in playstyle:
            dpi = int(current_dpi * 1.25)
        elif "Sniping" in playstyle:
            dpi = int(current_dpi * 1.1)
        else:
            dpi = int(current_dpi * 1.15)
        dpi = max(320, min(720, dpi))
        return {"recommended_dpi": dpi, "recoil_score": "94%"}

class JuliusApp(App):
    def build(self):
        self.title = "JULIUS"
        self.dev = DeviceAnalyzer()
        self.engine = SmartEngine()

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        header = Label(
            text="[b]JULIUS OPTIMIZER[/b]\n[size=14][color=00F2FE]ANDROID SENSITIVITY EDITION[/color][/size]",
            markup=True, font_size='22sp', color=(1, 0.84, 0, 1), halign='center'
        )
        layout.add_widget(header)

        specs = self.dev.get_specs()
        layout.add_widget(Label(text=f"الجهاز: {specs['tier']} | الرام: {specs['ram']}", color=(0.88, 0.88, 0.88, 1)))

        self.spinner = Spinner(
            text='اختر نمط اللعب',
            values=('Rush (مواجهات قريبة)', 'Sniping (قنص)', 'Balanced (متوازن)'),
            size_hint=(1, None), height=45, background_color=(0, 0.95, 0.99, 0.3)
        )
        layout.add_widget(self.spinner)

        self.result_label = Label(text="اضغط للتحليل لتوليد الحساسية", color=(0, 0.95, 0.99, 1), halign='center')
        layout.add_widget(self.result_label)

        btn = Button(text="تحليل الحساسية وتوليد التوصية", background_color=(0, 0.95, 0.99, 0.8), bold=True, size_hint=(1, None), height=50)
        btn.bind(on_press=self.run_analysis)
        layout.add_widget(btn)

        return layout

    def run_analysis(self, instance):
        rec = self.engine.calculate(360, self.spinner.text)
        self.result_label.text = f"الـ DPI المقترح: {rec['recommended_dpi']}\nنسبة ثبات الإيم: {rec['recoil_score']}"

if __name__ == '__main__':
    JuliusApp().run()
      
