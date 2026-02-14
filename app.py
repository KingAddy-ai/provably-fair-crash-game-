from flask import Flask, render_template_string, request
import hashlib
import random

app = Flask(__name__)

# ===== Server Setup =====
server_seed = hashlib.sha256(str(random.random()).encode()).hexdigest()
server_seed_hash = hashlib.sha256(server_seed.encode()).hexdigest()
nonce = 0
balance = 1000.0

def generate_crash_multiplier(server_seed, client_seed, nonce):
    message = f"{server_seed}:{client_seed}:{nonce}"
    hash_result = hashlib.sha256(message.encode()).hexdigest()
    h = int(hash_result[:13], 16)
    e = 2**52
    crash_point = (100 * e - h) / (e - h)
    return round(crash_point / 100, 2)


HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Crash Game</title>
<style>
body {
    background:#020617;
    font-family:Arial;
    color:#e5e7eb;
    display:flex;
    justify-content:center;
    align-items:center;
    height:100vh;
}
.card {
    width:400px;
    background:#0f172a;
    padding:20px;
    border-radius:12px;
    box-shadow:0 0 30px black;
}
h2 { text-align:center; }
.balance {
    background:#022c22;
    padding:10px;
    border-radius:8px;
    text-align:center;
    margin-bottom:10px;
    color:#22c55e;
    font-weight:bold;
}
<div id="status" style="text-align:center;color:#facc15;font-weight:bold;">
    FLYING...
</div>

.multiplier {
    font-size: 72px;
    font-weight: 800;
    text-align: center;
    color: #22c55e;
    text-shadow: 0 0 25px rgba(34,197,94,0.6);
    transition: color 0.2s ease;
}

}
input, button {
    width:100%;
    padding:10px;
    margin-top:8px;
    border-radius:6px;
    border:none;
}
button {
    background:#22c55e;
    font-weight:bold;
    cursor:pointer;
}
button:hover { background:#16a34a; }
.result {
    margin-top:12px;
    text-align:center;
    font-weight:bold;
}
.win { color:#22c55e; }
.lose { color:#ef4444; }
.hash {
    font-size:11px;
    color:#94a3b8;
    word-break:break-all;
}
</style>
</head>

<body>
<div class="card">
    <h2>🚀 Crash Game</h2>

    <div class="hash">
        Server Seed Hash:<br>{{ server_hash }}
    </div>

    <div class="balance">
        Balance: ₹{{ balance }}
    </div>

    <div id="multiplier" class="multiplier">1.00x</div>

    <form method="POST">
        <input name="client_seed" placeholder="Client Seed" required>
        <input type="number" step="0.01" name="bet" placeholder="Bet Amount" required>
        <input type="number" step="0.01" name="cashout" placeholder="Cashout Multiplier" required>
        <button type="submit">START ROUND</button>
    </form>

    {% if crash %}
   <script>
let multiplierEl = document.getElementById("multiplier");

let current = 1.00;
let crashPoint = {{ crash }};
let cashedOut = false;

// exponential growth like Aviator
function getIncrement(x) {
    return 0.002 * x;
}

function animate() {
    if (current >= crashPoint) {
        multiplierEl.innerHTML = crashPoint.toFixed(2) + "x 💥";
        multiplierEl.style.color = "#ef4444";
        return;
    }

    current += getIncrement(current);
    multiplierEl.innerHTML = current.toFixed(2) + "x";

    requestAnimationFrame(animate);
}

animate();
</script>


    <div class="result {{ result_type }}">
        {{ message }}
    </div>
    {% endif %}
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    global nonce, balance
    crash = None
    message = ""
    result_type = ""
    cashout = 0

    if request.method == "POST":
        client_seed = request.form["client_seed"]
        bet = float(request.form["bet"])
        cashout = float(request.form["cashout"])

        if bet <= 0 or bet > balance:
            return "Invalid bet"

        nonce += 1
        crash = generate_crash_multiplier(server_seed, client_seed, nonce)

        if cashout < crash:
            profit = bet * (cashout - 1)
            balance += profit
            message = f"✅ You won ₹{round(profit,2)}"
            result_type = "win"
        else:
            balance -= bet
            message = f"❌ You lost ₹{bet}"
            result_type = "lose"

    return render_template_string(
        HTML,
        server_hash=server_seed_hash,
        balance=round(balance,2),
        crash=crash,
        cashout=cashout,
        message=message,
        result_type=result_type
    )


if __name__ == "__main__":
    app.run(debug=True)
