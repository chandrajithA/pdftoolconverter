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

from pypdf import PdfReader
import math
import os
import math
from zipfile import ZipFile
from django.http import HttpResponse

def split_pdf(request):
    if request.method == "POST":
        if request.FILES.getlist('pdfs'):
            split_by = request.POST.get("split_by")  # "pages" or "size"
            value = int(request.POST.get("value"))   # pages or size in MB

            zip_buffer = io.BytesIO()
            with ZipFile(zip_buffer, 'w') as zip_file:
                for uploaded_file in request.FILES.getlist('pdfs'):
                    reader = PdfReader(uploaded_file)
                    base_filename = os.path.splitext(uploaded_file.name)[0]

                    if split_by == "pages":
                        chunks = math.ceil(len(reader.pages) / value)
                        for i in range(chunks):
                            writer = PdfWriter()
                            for j in range(value):
                                page_num = i * value + j
                                if page_num < len(reader.pages):
                                    writer.add_page(reader.pages[page_num])
                            output_stream = io.BytesIO()
                            writer.write(output_stream)
                            output_stream.seek(0)
                            zip_file.writestr(f"{base_filename}_part{i+1}.pdf", output_stream.read())

                    elif split_by == "size":
                        # Rough split by size (trial-and-error split; less accurate than by page count)
                        current_writer = PdfWriter()
                        current_stream = io.BytesIO()
                        current_size = 0
                        part = 1
                        for i, page in enumerate(reader.pages):
                            current_writer.add_page(page)
                            temp_stream = io.BytesIO()
                            current_writer.write(temp_stream)
                            current_size = temp_stream.tell() / 1024 / 1024  # in MB

                            if current_size >= value:
                                temp_stream.seek(0)
                                zip_file.writestr(f"{base_filename}_part{part}.pdf", temp_stream.read())
                                part += 1
                                current_writer = PdfWriter()  # Reset
                        # Write remaining pages
                        if len(current_writer.pages) > 0:
                            temp_stream = io.BytesIO()
                            current_writer.write(temp_stream)
                            temp_stream.seek(0)
                            zip_file.writestr(f"{base_filename}_part{part}.pdf", temp_stream.read())

            zip_buffer.seek(0)
            response = FileResponse(zip_buffer, as_attachment=True, filename="split_pdfs.zip")
            return response

        return HttpResponse("Upload one or more PDFs and specify split type.")
    return render(request, 'split_pdf.html')