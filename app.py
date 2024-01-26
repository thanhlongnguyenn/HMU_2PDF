from flask import Flask, render_template, request
from utils import get_url, download_images, convert_imgs_folder_to_pdf

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        startpage = int(request.form.get('startpage'))
        endpage = int(request.form.get('endpage'))
        url = request.form.get('url')
        finaldestination = request.form.get('finaldestination')
        returnUrl = get_url(url)
        download_images(startpage, endpage, returnUrl)
        convert_imgs_folder_to_pdf(startpage, endpage, finaldestination)
        return 'PDF created!'
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)