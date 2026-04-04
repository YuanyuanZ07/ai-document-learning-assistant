import logging

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response

from .models import Document
from .serializers import DocumentSerializer, DocumentListSerializer, AskQuestionSerializer
from .services.file_parser import extract_text_from_file, get_file_extension, SUPPORTED_EXTENSIONS
from .services.summarizer import summarize_text
from .services.qa_service import answer_question

logger = logging.getLogger(__name__)


# ─── Health check ───────────────────────────────────────────────

@api_view(['GET'])
def health_check(request):
    return Response({"status": "ok", "message": "Backend is running"})


# ─── Frontend-compatible endpoints (match Emilly's frontend) ────

@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_file(request):
    """
    Handle file upload from frontend.
    Supports actions: 'scan' (extract text) and 'question' (Q&A).
    """
    file = request.FILES.get('file')
    if not file:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    ext = get_file_extension(file.name)
    if ext not in SUPPORTED_EXTENSIONS:
        return Response(
            {"error": f"Unsupported file type: {ext}. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    action = request.data.get('action', 'scan')
    message = request.data.get('message', '')

    # Save document to DB
    doc = Document.objects.create(
        file=file,
        filename=file.name,
        file_type=ext.lstrip('.'),
        file_size=file.size,
        status='processing',
    )

    # Extract text
    try:
        file.seek(0)
        doc.extracted_text = extract_text_from_file(file, file.name)
        doc.status = 'completed'
        doc.save()
    except Exception as e:
        logger.exception("Text extraction failed for %s", file.name)
        doc.status = 'failed'
        doc.save()
        return Response({"error": f"Text extraction failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    result = {"message": f"File '{file.name}' uploaded and scanned successfully."}

    # If action is 'question', answer the question using extracted text
    if action == 'question' and message:
        try:
            answer = answer_question(message, doc.extracted_text)
            result["message"] = answer
        except Exception as e:
            logger.exception("Q&A failed for document %s", doc.id)
            result["message"] = f"Q&A failed: {str(e)}"

    # If action is 'scan', also generate a summary
    if action == 'scan':
        try:
            doc.summary = summarize_text(doc.extracted_text)
            doc.save()
            result["summary"] = doc.summary
        except Exception as e:
            logger.exception("Summary generation failed for document %s", doc.id)
            result["summary"] = f"Summary generation failed: {str(e)}"

    return Response(result, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def summary(request):
    """Generate summary from text (frontend-compatible endpoint)."""
    text = request.data.get('text', '')
    if not text:
        return Response({"error": "No text provided"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        result = summarize_text(text)
        return Response({"summary": result})
    except Exception as e:
        logger.exception("Summarization failed")
        return Response({"error": f"Summarization failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ─── RESTful Document API ──────────────────────────────────────

@api_view(['GET'])
def document_list(request):
    """List all uploaded documents."""
    documents = Document.objects.all()
    serializer = DocumentListSerializer(documents, many=True)
    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
def document_detail(request, pk):
    """Retrieve or delete a single document."""
    try:
        doc = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        doc.file.delete()
        doc.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = DocumentSerializer(doc)
    return Response(serializer.data)


@api_view(['POST'])
def document_summary(request, pk):
    """Generate AI summary for a specific document."""
    try:
        doc = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

    if not doc.extracted_text:
        return Response({"error": "No text extracted from this document"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        doc.summary = summarize_text(doc.extracted_text)
        doc.save()
        return Response({"summary": doc.summary})
    except Exception as e:
        logger.exception("Summarization failed for document %s", pk)
        return Response({"error": f"Summarization failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def document_ask(request, pk):
    """Ask a question about a specific document."""
    try:
        doc = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AskQuestionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    question = serializer.validated_data['question']

    if not doc.extracted_text:
        return Response({"error": "No text extracted from this document"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        answer = answer_question(question, doc.extracted_text)
        return Response({"question": question, "answer": answer})
    except Exception as e:
        logger.exception("Q&A failed for document %s", pk)
        return Response({"error": f"Q&A failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)