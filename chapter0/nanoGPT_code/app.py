from flask import Flask, render_template, request, jsonify
from scipy.optimize import curve_fit
import numpy as np
from samplecurve import sample_points

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def quintic_x(t, a0, a1, a2, a3, a4, a5):
    return a0 + a1*t + a2*t**2 + a3*t**3 + a4*t**4 + a5*t**5

def quintic_y(t, b0, b1, b2, b3, b4, b5):
    return b0 + b1*t + b2*t**2 + b3*t**3 + b4*t**4 + b5*t**5


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    stroke = data.get('stroke', [])
    # Simple stub: if you have ≥2 points, keep going in the same direction
    
    zx = 50
    zy = 5

    if len(stroke) >= 6:
        print("stroke", stroke)
        predicted = sample_points(stroke, 1024, 1024)
        print("pred", predicted)
        """
        xs = [st[0] for st in stroke]
        ys = [st[1] for st in stroke]

        kp = min(len(stroke), zx)
    
        ts = np.linspace(0, 0.5, kp)
        initial_guess_x = [0]*6
        initial_guess_y = [0]*6

        # Fit the x-component
        popt_x, pcov_x = curve_fit(quintic_x, ts, xs[-kp:], p0=initial_guess_x)

        # Fit the y-component
        popt_y, pcov_y = curve_fit(quintic_y, ts, ys[-kp:], p0=initial_guess_y)


        predicted = []
        td = np.linspace(0.5, 1., zy)
        xpred = quintic_x(td, *popt_x)
        ypred = quintic_y(td, *popt_y)
        predicted = [[int(x), int(y)] for (x, y) in zip(xpred, ypred)]
        """

        return jsonify({'prediction': predicted})
    return jsonify({'prediction': []})

if __name__ == '__main__':
    app.run(debug=True)

