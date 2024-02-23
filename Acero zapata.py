from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import math

class ZapataCalcApp(App):
    def build(self):
        main_layout = BoxLayout(orientation='vertical', padding=5)
        inputs_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5))
        results_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.5))

        # Campos de entrada para los parámetros necesarios
        self.inputs = {}
        for field in ['Mu (kN-m)', 'b (m)', 'd (m)', 'fc (MPa)', 'fy (MPa)', 'Área de varilla (cm²)', 'Recubrimiento (cm)']:
            field_layout = BoxLayout(orientation='horizontal', height=30, size_hint_y=None)
            field_label = Label(text=field, size_hint_x=0.5)
            field_input = TextInput(multiline=False, size_hint_x=0.5)
            field_layout.add_widget(field_label)
            field_layout.add_widget(field_input)
            self.inputs[field] = field_input
            inputs_layout.add_widget(field_layout)

        # Botón para calcular
        calc_button = Button(text='Calcular área de acero', size_hint_y=None, height=50)
        calc_button.bind(on_press=self.calcular_area_acero)
        inputs_layout.add_widget(calc_button)

        # Etiqueta para mostrar resultado
        self.resultado = Label(size_hint_y=None, height=150)
        results_layout.add_widget(self.resultado)

        main_layout.add_widget(inputs_layout)
        main_layout.add_widget(results_layout)

        return main_layout

    def calcular_area_acero(self, instance):
        mu = float(self.inputs['Mu (kN-m)'].text) * 100000  # Convertir a N-mm
        b = float(self.inputs['b (m)'].text)
        d = float(self.inputs['d (m)'].text)
        fc = float(self.inputs['fc (MPa)'].text)
        fy = float(self.inputs['fy (MPa)'].text)
        n = float(self.inputs['Área de varilla (cm²)'].text)
        r = float(self.inputs['Recubrimiento (cm)'].text)
        fi = 0.9

        # Cálculos según el procedimiento
        Rn = mu / (fi * b * d**2)
        P = (0.85 * fc) / fy * (1 - math.sqrt(1 - (2 * Rn) / (0.85 * fc)))
        A = P * b * d
        Pza = A / n
        S = (b - 2*r) / (Pza - 1)

        # Mostrar resultados
        self.resultado.text = f'Rn (Momento de resistencia nominal): {Rn:.2f}\n' + \
                              f'p (Porcentaje de acero teórico): {P:.4f}\n' + \
                              f'A (Área de acero requerida): {A:.2f} mm²\n' + \
                              f'Pza (Piezas de varilla): {Pza:.2f}\n' + \
                              f'S (Separación entre varillas): {S:.2f} mm'

if __name__ == '__main__':
    ZapataCalcApp().run()
