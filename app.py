from flask import Flask, request, render_template, jsonify
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict_production', methods=['POST'])
def predict_production():
    # Membaca input dari permintaan dan persediaan
    data = request.get_json()
    less = data['less']
    stock = data['stock']

    # Membuat variabel fuzzy untuk permintaan
    less_turun = ctrl.Antecedent(np.arange(0, 1000000, 1), 'less_turun')
    less_sedang = ctrl.Antecedent(np.arange(0, 1000000, 1), 'less_sedang')
    less_naik = ctrl.Antecedent(np.arange(0, 1000000, 1), 'less_naik')

    # Membuat variabel fuzzy untuk persediaan
    stock_sedikit = ctrl.Antecedent(np.arange(0, 10000000, 1), 'stock_sedikit')
    stock_sedang = ctrl.Antecedent(np.arange(0, 10000000, 1), 'stock_sedang')
    stock_banyak = ctrl.Antecedent(np.arange(0, 10000000, 1), 'stock_banyak')

    # Membuat variabel fuzzy untuk produksi
    production_berkurang = ctrl.Consequent(np.arange(0, 100000000, 1), 'production_berkurang')
    production_lumayan = ctrl.Consequent(np.arange(0, 100000000, 1), 'production_lumayan')
    production_bertambah = ctrl.Consequent(np.arange(0, 100000000, 1), 'production_bertambah')

    # Menentukan fungsi keanggotaan untuk variabel permintaan
    less_turun['turun'] = fuzz.trimf(less_turun.universe, [0, 0, 500000])
    less_sedang['sedang'] = fuzz.trimf(less_sedang.universe, [0, 500000, 1500000])
    less_naik['naik'] = fuzz.trimf(less_naik.universe, [500000, 1500000, 10000000])

    # Menentukan fungsi keanggotaan untuk variabel persediaan
    stock_sedikit['sedikit'] = fuzz.trimf(stock_sedikit.universe, [0, 0, 1000000])
    stock_sedang['sedang'] = fuzz.trimf(stock_sedang.universe, [0, 1000000, 7000000])
    stock_banyak['banyak'] = fuzz.trimf(stock_banyak.universe, [1000000, 7000000, 20000000])

    # Menentukan fungsi keanggotaan untuk variabel produksi
    production_berkurang['berkurang'] = fuzz.trimf(production_berkurang.universe, [0, 0, 100000000])
    production_lumayan['lumayan'] = fuzz.trimf(production_lumayan.universe, [0, 100000000, 150000000])
    production_bertambah['bertambah'] = fuzz.trimf(production_bertambah.universe, [100000000, 150000000, 200000000])

    # Membuat aturan fuzzy
    rule1 = ctrl.Rule(stock_banyak['banyak'] & less_naik['naik'], production_bertambah['bertambah'])
    rule2 = ctrl.Rule(stock_banyak['banyak'] & less_sedang['sedang'], production_lumayan['lumayan'])
    rule3 = ctrl.Rule(stock_banyak['banyak'] & less_turun['turun'], production_berkurang['berkurang']) 
    rule4 = ctrl.Rule(stock_sedang['sedang'] & less_naik['naik'], production_bertambah['bertambah'])
    rule5 = ctrl.Rule(stock_sedang['sedang'] & less_sedang['sedang'], production_lumayan['lumayan'])
    rule6 = ctrl.Rule(stock_sedang['sedang'] & less_turun['turun'],production_berkurang['berkurang'])
    rule7 = ctrl.Rule(stock_sedikit['sedikit'] & less_naik['naik'], production_bertambah['bertambah'])
    rule8 = ctrl.Rule(stock_sedikit['sedikit'] & less_sedang['sedang'], production_lumayan['lumayan'])
    rule9 = ctrl.Rule(stock_sedikit['sedikit'] & less_turun['turun'], production_berkurang['berkurang'])

    # Membuat sistem kontrol fuzzy
    production_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
    production_prediction = ctrl.ControlSystemSimulation(production_ctrl)

    # Set input ke sistem kontrol fuzzy
    less  = less-input['less']
    stock = stock-input['stock']


    # menghitung simulasi
    production_prediction.compute()

    # Mendapatkan output produksi
    defuzz_value = np.sum(production_prediction['production'] * production_prediction['production'] ) / np.sum(production_prediction['production'])

    return jsonify({'production': defuzz_value})
    
if __name__ == '__main__':
    app.run(debug=True)
