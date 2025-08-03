# 🎙️ Audio Transcriber with Speaker Diarization

This is a simple yet effective Django web application that allows users to upload audio files (`.mp3` or `.wav`) and receive a transcribed text or Word document, complete with **speaker labels** (identifying "Bot" and "User"). It leverages the powerful AssemblyAI API for accurate speech-to-text conversion and speaker diarization.

---

## ✨ Features

- **Audio Uploads:** Supports `.mp3` and `.wav` file formats.
- **Speaker Diarization:** Automatically identifies and labels different speakers (e.g., "Bot" and "User") in the transcript.
- **Downloadable Transcripts:** Generates transcripts as plain text (`.txt`) or Microsoft Word documents (`.docx`).
- **User-Friendly Interface:** A clean and straightforward web form for easy interaction.

---

## 🚀 Technologies Used

- **Django:** A high-level Python web framework for rapid development.
- **AssemblyAI SDK:** Python library for interacting with the AssemblyAI Speech-to-Text API.
- **`python-docx`:** Python library for creating and modifying Microsoft Word (.docx) files.
- **`python-dotenv`:** For managing environment variables securely.
- **HTML/CSS:** For the web interface (minimal styling).

---

## 🛠️ Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Clone the Repository (if applicable)

If this code is part of a Git repository, start by cloning it:

```bash
git clone <your-repository-url>
cd <your-repository-name>
```

### 2. Set Up Your Python Environment

It's highly recommended to use a virtual environment to manage dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

Install all the required Python packages using pip:

```bash
pip install Django assemblyai python-dotenv python-docx
```

### 4. Configure AssemblyAI API Key

You'll need an API key from AssemblyAI to use their transcription service.

- **Obtain your API Key:** Sign up or log in to [AssemblyAI](https://www.assemblyai.com/) and find your API key in your dashboard.
- **Create a `.env` file:** In the **root directory** of your project (the same directory as `manage.py`), create a new file named `.env`.
- **Add your API key:**
  ```
  ASSEMBLYAI_API_KEY="YOUR_ACTUAL_ASSEMBLYAI_API_KEY_HERE"
  ```
  **Important**: Replace `"YOUR_ACTUAL_ASSEMBLYAI_API_KEY_HERE"` with your actual API key. **Do not commit this file to your public repository!** Add `.env` to your `.gitignore` file.

### 5. Django Project Configuration

Ensure your Django project is set up to recognize your app and handle file uploads.

- **`audio_transcriber_project/settings.py`**:

  - Add these lines at the **very top** to load environment variables:

    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv()
    ```

  - Add `'transcriber'` to your `INSTALLED_APPS` list:
    ```python
    INSTALLED_APPS = [
        # ... other Django apps ...
        'transcriber', # Add this line
    ]
    ```
  - Define `MEDIA_URL` and `MEDIA_ROOT` (usually at the bottom of the file):
    ```python
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    ```

- **`audio_transcriber_project/urls.py`**:

  - Update your main `urls.py` to include your app's URLs and serve media files during development:

    ```python
    from django.contrib import admin
    from django.urls import path, include
    from django.conf import settings
    from django.conf.urls.static import static

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('transcriber.urls')), # Include your app's URLs
    ]

    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```

### 6. App-Specific Files and Templates

Ensure the files within your `transcriber` app are correctly placed.

- **`transcriber/forms.py`**:

  ```python
  from django import forms

  class AudioUploadForm(forms.Form):
      audio_file = forms.FileField(label='Select an audio file (.mp3 or .wav)')
      file_type = forms.ChoiceField(choices=[('txt', 'Text File (.txt)'), ('docx', 'Word Document (.docx)')], initial='txt')
  ```

- **`transcriber/views.py`**: Place the provided Django view code (the one without comments) in this file.
- **`transcriber/urls.py`**:

  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
      path('', views.transcribe_audio, name='transcribe_audio'),
  ]
  ```

- **Template Structure**: This is crucial! Your HTML templates must be nested correctly.
  Create the following directory structure inside your `transcriber` app:
  ```
  transcriber/
  └── templates/
        ├── base.html
        └── upload.html
  ```
  Place the `base.html` and `upload.html` code (minimal styling versions) into their respective files within this structure.

---

## ▶️ Running the Application

Once everything is set up, you can run the Django development server.

1.  **Activate your virtual environment** (if not already active).
2.  **Run database migrations** (good practice for any Django project):
    ```bash
    python manage.py migrate
    ```
3.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will typically be accessible at `http://127.0.0.1:8000/`.

---

## 🖥️ Usage

1.  Open your web browser and go to `http://127.0.0.1:8000/`.
2.  You'll see a simple form.
3.  Click **"Choose File"** and select your `.mp3` or `.wav` audio file.
4.  Choose your desired **"Output File Type"** (Text File or Word Document).
5.  Click the **"Transcribe Audio"** button.

The application will process your audio, and your browser will then prompt you to download the generated transcript file!

---

## 🐛 Troubleshooting

- **`KeyError: 'ASSEMBLYAI_API_KEY'`**:
  - **Solution**: Verify that your `.env` file is in the root directory of your project and contains `ASSEMBLYAI_API_KEY="YOUR_KEY"`.
  - **Solution**: Ensure `from dotenv import load_dotenv` and `load_dotenv()` are at the very top of your `settings.py`.
  - **Solution**: Restart your server after modifying the `.env` file.
- **AssemblyAI API Errors (e.g., "Transcription failed")**:
  - **Solution**: Check your internet connection.
  - **Solution**: Confirm your AssemblyAI API key is correct and active.
  - **Solution**: Review the specific error message displayed on the page for more details.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE.md). (You might want to create a `LICENSE.md` file in your root directory if you're planning to share this publicly).
