from flask import Flask, request, jsonify
import os
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = '/var/www/html/uploads'
ALLOWED_EXTENSIONS = {'mp4'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Awake function")
    if 'file' not in request.files:
        print("Nothing file")
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        print("Nothing filename")
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        print("success")
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # シェルスクリプトを呼び出してファイル処理
        result = subprocess.run(["/changePermission.sh", file_path], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("200")
            return jsonify({"message": "File uploaded and script executed successfully"}), 200
        else:
            print("500")
            return jsonify({"error": "Script execution failed", "details": result.stderr}), 500

    return jsonify({"error": "File type not allowed"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

