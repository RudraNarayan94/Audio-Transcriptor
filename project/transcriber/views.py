import os
import io
import docx
import assemblyai as aai
from django.shortcuts import render
from django.http import HttpResponse
from .forms import AudioUploadForm

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

def transcribe_audio(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if form.is_valid():
            audio_file = request.FILES['audio_file']
            output_type = request.POST['file_type']

            temp_path = 'temp_audio_file'
            with open(temp_path, 'wb+') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            try:
                config = aai.TranscriptionConfig(speaker_labels=True, speakers_expected=2)
                transcript = aai.Transcriber(config=config).transcribe(temp_path)

                if transcript.status == aai.TranscriptStatus.error:
                    return HttpResponse(f"Oops! Transcription failed: {transcript.error}", status=500)

                output_text = ""
                speaker_map = {"A": "Bot", "B": "User"}
                for utterance in transcript.utterances:
                    speaker_label = speaker_map.get(utterance.speaker, f"Speaker {utterance.speaker}")
                    output_text += f"{speaker_label}: {utterance.text}\n"

                if output_type == 'docx':
                    doc = docx.Document()
                    doc.add_paragraph(output_text)
                    buffer = io.BytesIO()
                    doc.save(buffer)
                    buffer.seek(0)
                    
                    response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
                    response['Content-Disposition'] = 'attachment; filename="transcript.docx"'
                    return response
                else:
                    response = HttpResponse(output_text, content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename="transcript.txt"'
                    return response

            except Exception as e:
                return HttpResponse(f"Oh no! An unexpected error occurred: {e}", status=500)
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        else:
            return render(request, 'upload.html', {'form': form})
    
    else:
        form = AudioUploadForm()
        return render(request, 'upload.html', {'form': form})