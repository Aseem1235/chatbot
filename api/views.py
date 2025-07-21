from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from .models import Document
from .serializers import DocumentSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import yrsExperience, LoginDetails,Recruiter,RecruiterArch,UsageDetails,TechInMenu,SkillsInMenu,Domain,Level,AI_Model
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
import datetime
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from io import BytesIO
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import speech_recognition as sr
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import re
from django.views.decorators.http import require_http_methods
from langchain.schema import Document as lc
from pydub import AudioSegment
import time


from django.contrib.auth import authenticate


responses = {}
questions = {}
load_dotenv()


    


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer







def run_assessment(query, response_key):
    
    
   
    
    embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'),model="text-embedding-3-small",organization="org-c2Ov83W6Qry8QAkIjwGMgxPI")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

    retrieved_docs = new_db.similarity_search(query)
    context = "\n\n".join([
        doc.page_content if hasattr(doc, "page_content") else str(doc)
        for doc in retrieved_docs
    ])
    
    
    prompt = f"""
    You are a professional career analyst.  
    Carefully read both the resume and job description.
    Consider skills, experience, education, and relevance.
    Given a candidate's resume and a job description, analyze and determine if the candidate is professionally suitable for the role.  
    You response should be directive of why or why not they are or aren't a good candidate for the job.



    {context}
    Here is the question:
    {query}
    ⚠️ Important:
        Respond ONLY as a JSON object. Do NOT use markdown or code fences.
        Respond exactly as below!
    Respond like:
    {{"reasoning": "Explain specifically which skills, experience, or qualifications match or don't match.", "response": "The response should be a one sentance summary of reasoning and could be a yes or no answer to question and also should make sense in the context of the question."}}
    
    """

    llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'),model="gpt-3.5-turbo",organization="org-c2Ov83W6Qry8QAkIjwGMgxPI")
    raw_output = llm.invoke(prompt).content
    cleaned = re.sub(r"```(?:json)?", "", raw_output).strip()
    parsed = json.loads(cleaned)

    
    responses[response_key] = parsed
    
        
@csrf_exempt
def process_pdfs(request):
    
    file_1 = request.FILES.get("file_one")
    file_2 = request.FILES.get("file_two")
    text = ""
    if file_1:

        pdf_reader = PdfReader(BytesIO(file_1.read()))
        for page in pdf_reader.pages:
            text+= page.extract_text()
            
    if file_2:
        pdf_reader = PdfReader(BytesIO(file_2.read()))
        for page in pdf_reader.pages:
            text+= page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 1000)
    chunks = text_splitter.split_text(text)
    embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'),model="text-embedding-3-small",organization="org-c2Ov83W6Qry8QAkIjwGMgxPI")
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")
    return JsonResponse({"message": "Success!"})
            


@csrf_exempt
def generate_questions(request):
    embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'),model="text-embedding-3-small",organization="org-c2Ov83W6Qry8QAkIjwGMgxPI")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retrieved_docs = new_db.similarity_search("Candidates resume and the Job description")
    context = "\n\n".join([
        doc.page_content if hasattr(doc, "page_content") else str(doc)
        for doc in retrieved_docs
    ])
    prompt = f"""
        You are a professional career analyst.  
        Carefully read the job description.
        Consider skills, experience, education, and relevance.
        Given a job description, analyze and create 5 technical interview questions(can be commonly used in interviews for this job description or can be created from scratch) with answers that must be answered in order to successfully work at the job in the job description.
        Here is the job description: {context}
        ⚠️ Important:
        Respond ONLY as a JSON object. Do NOT use markdown or code fences.
        Respond exactly as below!
        Respond like:{{
        "question 1 here, Ex:what experience do you have with ...": "answer to question 1 here",
        "question 2 here, Ex:Please explain garbage collection in python vs Java": "answer to question 2 here"
        }}
        For 5 questions with key(questions) and values(answers) both being strings.  Answers should be from the point of view of you answering these questions yourself.
    """
    llm = ChatOpenAI(api_key=os.getenv('OPENAI_API_KEY'),model="gpt-3.5-turbo",organization="org-c2Ov83W6Qry8QAkIjwGMgxPI")
    raw_output = llm.invoke(prompt).content
    cleaned = re.sub(r"```(?:json)?", "", raw_output).strip()
    parsed = json.loads(cleaned)
    return JsonResponse(parsed,safe=False)
@csrf_exempt
def response(request):
    
    if request.method=="POST":
         
        text = request.POST.get("text")
        audio_text = request.POST.get("audio")
                  
        
        if text:
           print(text)
           run_assessment(text, "text_response")     
            
        if audio_text:
            print(audio_text)
            run_assessment(audio_text,"audio_response")
        
        return JsonResponse(responses)
    return JsonResponse({"error":"invalid request method"},status=405)
@csrf_exempt
def transcribe_audio(request):
    start_time = time.time()
    audio_file = request.FILES.get("audio")
    audio = AudioSegment.from_file(audio_file, format="webm")
    audio.export("converted.wav", format="wav")
    recognizer = sr.Recognizer()
    with sr.AudioFile("converted.wav") as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)
        
        text = recognizer.recognize_google(audio)
        end_time= time.time()
        print(text)
        print(str(end_time-start_time))
        
        return JsonResponse({'transcribed_text':text})
    
        



            
        
    
        




@csrf_exempt
def selection_storage(request):
    if request.method == "POST":
        #print("FILES:", request.FILES)
        #print("POST DATA:", request.POST)
        
        user=request.user
        user_ob = LoginDetails.objects.get(username=request.POST.get("username"))
        user_id= user_ob.id
        now = datetime.datetime.now()
        usage = UsageDetails(
            id = user_id,
            usageDateTime = now.strftime("%Y-%m-%d %H:%M:%S"),
            techOpt = request.POST.get("tech"),
            skillOpt = f"{request.POST.get('lev')},{request.POST.get('exp')}",
            file_1=request.FILES.get("file_one"),
            file_2 = request.FILES.get("file_two")

        )

        usage.save()
    return JsonResponse({"":""},status=200)
    
@csrf_exempt
def custom_login_view(request):
    if request.method=="POST":
        data=json.loads(request.body)
        username_=data.get("username")
        password_=data.get("password")
        if username_ == "admin":
            user = authenticate(username=username_, password=password_)
            if user is not None:
                if user.is_superuser:
                    return JsonResponse({"status":"admin","redirect_url":"/admin/"},status=200)
                else:
                    return JsonResponse({"error":"Invalid credentials"},status=401)
        else:
            user = LoginDetails.objects.get(username=username_)
            if user.password == password_:

                if LoginDetails.objects.filter(username=username_,password=password_).exists():
                    return JsonResponse({"status":"user","user_id":user.id},status=200)
                else:
                    return JsonResponse({"error":"Invalid credentials"},status=401)
            else:
                return JsonResponse({"error":"Invalid credentials"},status=401)



                

        
        






def get_technologies(request):
    data = list(TechInMenu.objects.values())
    return JsonResponse(data, safe=False)
def get_domain(request):
    data = list(Domain.objects.values())
    return JsonResponse(data, safe=False)
def get_level(request):
    data = list(Level.objects.values())
    return JsonResponse(data, safe=False)
def get_aiModel(request):
    data = list(AI_Model.objects.values())
    return JsonResponse(data, safe=False)
def get_yrsExp(request):
    data = list(yrsExperience.objects.values())
    return JsonResponse(data, safe=False)

# Create your views here.
