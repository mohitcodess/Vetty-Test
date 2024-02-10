from flask import Flask, request, jsonify, render_template
import os

app = Flask(__name__)

STATIC_DIR = './static/'


def fetch_file_content(file_name, start, end):
    file_path = os.path.join(STATIC_DIR, f'{file_name}.txt')
    if not os.path.exists(file_path):
        return None

    with open(file_path, 'r', encoding='ascii', errors='ignore') as f:
        lines = f.readlines()
        end = min(end, len(lines))
        content = ''.join(lines[start:end])
    return content


@app.route('/file/<file_name>')
def get_file_content(file_name):
    start = request.args.get('start_line')
    end = request.args.get('end_line')

    if None in (start, end):
        return jsonify({'msg': 'Query parameters start and end are required!'}), 400

    if not start.isdigit() or not end.isdigit():
        return jsonify({'msg': 'Query parameters start and end must be integers!'}), 400

    start, end = int(start), int(end)

    if start >= end or start < 0:
        return jsonify({'msg': 'Invalid query parameters!'}), 400

    content = fetch_file_content(file_name, start, end)
    if content is None:
        return jsonify({'msg': f"File '{file_name}.txt' does not exist!"}), 404

    return render_template('index.html', data=content)


if __name__ == "__main__":
    app.run(debug=True)
