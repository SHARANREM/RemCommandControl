<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>RemCheatControl</title>
    <style>
        body {
            background: #0d0d0d;
            color: #ffffff;
            font-family: Consolas, monospace;
            margin: 0;
            padding: 0;
        }

        header {
            padding: 40px;
            text-align: center;
            border-bottom: 2px solid white;
        }

        h1 {
            font-size: 40px;
            margin: 0;
        }

        h2 {
            color: #aaaaaa;
            font-weight: normal;
        }

        .container {
            padding: 30px;
            max-width: 900px;
            margin: auto;
        }

        .box {
            border: 1px solid white;
            padding: 15px;
            margin: 20px 0;
        }

        code {
            background: #1a1a1a;
            padding: 3px 6px;
            border-radius: 4px;
        }

        .command {
            color: #00ffcc;
        }

        footer {
            text-align: center;
            padding: 20px;
            border-top: 1px solid white;
            color: #888;
        }
    </style>

</head>

<body>

<header>
    <h1>RemCheatControl</h1>
    <h2>Turn your PC into a Cheat-Code Driven Operating System</h2>
</header>

<div class="container">

    <div class="box">
        <h2>🚀 What is this?</h2>
        <p>
            RemCheatControl is a game-style command system for Windows that lets you control your computer using cheat-like commands instead of clicks.
        </p>
        <p>
            Think GTA cheat codes, but for real productivity.
        </p>
    </div>

    <div class="box">
        <h2>⚡ Example Usage</h2>
        <p class="command">/browse github</p>
        <p class="command">/open chrome</p>
        <p class="command">/multi yt github chatgpt</p>
        <p class="command">/countdown 5</p>
        <p class="command">/help browse</p>
    </div>

    <div class="box">
        <h2>🧠 How It Works</h2>
        <p>
            The system is built on a plugin-based architecture:
        </p>
        <ul>
            <li><b>CheatInput</b> → UI command bar (GTA-style overlay)</li>
            <li><b>Brain</b> → Command parser + plugin loader</li>
            <li><b>Plugins</b> → Independent Python files that execute actions</li>
        </ul>
    </div>

    <div class="box">
        <h2>🧩 Plugin System</h2>
        <p>
            Every feature is a plugin inside the <code>plugins/</code> folder.
        </p>

        <p>Example:</p>
        <pre>

plugins/
browse.py
open.py
multi.py
countdown.py
</pre>

        <p>
            Each plugin contains:
        </p>

        <pre>

def run(\*args): # logic here
</pre>
</div>

    <div class="box">
        <h2>🔥 Key Features</h2>
        <ul>
            <li>Game-style cheat console UI</li>
            <li>Global hotkey activation</li>
            <li>Dynamic plugin loading (no restart needed)</li>
            <li>Multi-argument commands</li>
            <li>Command history system</li>
            <li>Help system per plugin</li>
            <li>Extensible architecture</li>
        </ul>
    </div>

    <div class="box">
        <h2>⚙️ How to Use</h2>

        <h3>1. Start the App</h3>
        <p>Run:</p>
        <code>python main.py</code>

        <h3>2. Open Command Console</h3>
        <p>Press:</p>
        <code>Ctrl + `</code>

        <h3>3. Enter Commands</h3>
        <p>Examples:</p>
        <pre>

/browse github
/open chrome
/multi yt github
/countdown 10
/help browse
</pre>

        <h3>4. Add New Features</h3>
        <p>
            Just create a new file in <code>plugins/</code>
        </p>

        <pre>

# plugins/weather.py

def run(\*args):
print("Weather plugin")
</pre>

        <p>
            It becomes instantly available as:
        </p>

        <code>/weather</code>
    </div>

    <div class="box">
        <h2>🧠 Vision</h2>
        <p>
            RemCheatControl turns your operating system into a command-driven game-like environment where every action is a cheat code.
        </p>
    </div>

</div>

<footer>
    Built for productivity. Designed like a game.
</footer>

</body>
</html>
