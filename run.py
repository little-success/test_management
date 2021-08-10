from apps import create_http


app = create_http()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081, debug=True)