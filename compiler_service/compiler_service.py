from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/compile', methods=['POST'])
def compile_code():
    code = request.json.get('code')
    # Save code to a file and compile it
    with open('temp_code.cpp', 'w') as f:
        f.write(code)
    try:
        # Compile code (assuming C++ for this example)
        result = subprocess.run(['g++', 'temp_code.cpp', '-o', 'temp_code'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'message': 'Compilation successful'})
        else:
            return jsonify({'message': 'Compilation failed', 'error': result.stderr}), 400
    except Exception as e:
        return jsonify({'message': 'Error', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
