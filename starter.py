from flask import Flask, render_template, request, redirect, send_file
import pytube
import os

app = Flask(__name__)

# Specify the path to the downloads folder
downloads_folder = os.path.join(os.getcwd(), 'downloads')


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/download', methods=['POST'])
def download():
    video_url = request.form['video_url']
    youtube = pytube.YouTube(video_url)

    format = request.form['format']

    if format == 'mp3':
        audio_stream = youtube.streams.filter(only_audio=True).first()
        filename = youtube.title + ".mp3"
        audio_stream.download(output_path=downloads_folder, filename=filename)
    elif format == 'mp4':
        mp4_stream = youtube.streams.get_highest_resolution()
        filename = youtube.title + ".mp4"
        mp4_stream.download(output_path=downloads_folder, filename=filename)

    return send_file(os.path.join(downloads_folder, filename), as_attachment=True)


@app.route('/clear_downloads', methods=['POST'])
def clear_downloads():
    # Remove all files from the downloads folder
    for file in os.listdir(downloads_folder):
        file_path = os.path.join(downloads_folder, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return redirect('/')


if __name__ == '__main__':
    app.run()
