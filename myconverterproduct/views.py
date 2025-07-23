import io
import tempfile
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from pypdf import PdfWriter




# Create your views here.
def index(request):
    return render(request, 'index.html')

def word_to_pdf(request):
    return render(request, 'word_to_pdf.html')

def pdf_to_word(request):
    return render(request, 'pdf_to_word.html')

def compress_pdf(request):
    return render(request, 'compress_pdf.html')

def compress_word(request):
    return render(request, 'compress_word.html')

@csrf_exempt
def merge_pdf(request):
    if request.method == 'POST':

        if not request.FILES.getlist('pdfs'):
            return render(request, 'merge_pdf.html', {'error': 'No PDF files uploaded.'})

        merger = PdfWriter()

        try:
            for file in request.FILES.getlist('pdfs'):
                with tempfile.NamedTemporaryFile(delete=True) as temp_file:
                    for chunk in file.chunks():
                        temp_file.write(chunk)
                    temp_file.flush()
                    temp_file.seek(0)

                    merger.append(file)

            merged_pdf = io.BytesIO()
            merger.write(merged_pdf)
            merger.close()
            merged_pdf.seek(0)

            return FileResponse(
                merged_pdf,
                as_attachment=True,
                filename='merged.pdf',
                content_type='application/pdf'
            )

        except Exception as e:
            return render(request, 'merge_pdf.html', {'error': str(e)})

    # On GET request
    return render(request, 'merge_pdf.html')

def split_pdf(request):
    return render(request, 'split_pdf.html')