// src/MainApp.js
import React from "react";
import './MainApp.css';
import { useEffect, useState, useRef} from "react";

const MainApp = () => {
    const [questionInput,setQuestionInput] = useState("");
    const [voice, setVoice] = useState(false);
    const [recording, setRecording] = useState(null);
    const mediaRecorderRef = useRef(null);
    const audioChunksRef = useRef([]);
    const [finalData, setFinalData] = useState(null);
    const [textai_response, setTextAiResponse] = useState("");
    const [audioai_response, setAudioAiResponse] = useState("");
    const [questions,setQuestions]=useState(null);
    const startRecording = async () => {
    
        const stream = await navigator.mediaDevices.getUserMedia({audio: true});
        mediaRecorderRef.current = new MediaRecorder(stream);
        audioChunksRef.current=[];
        mediaRecorderRef.current.ondataavailable = (event) => {
            if (event.data.size>0){
                audioChunksRef.current.push(event.data);

            }
        };

        mediaRecorderRef.current.onstop = () => {
            const audioBlob = new Blob(audioChunksRef.current, {type: "audio/webm"});
            handleNewRecording(audioBlob);
        };
        mediaRecorderRef.current.start();
        
        
    };
    const startTime = performance.now();
    const stopRecording = () => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive"){
            mediaRecorderRef.current.stop();
            
        }
        
    };
    useEffect(()=>{
        if(recording){
            setShowResponse(true);
        }
    },[recording]);
    const handleNewRecording = (newBlob) => {
        setShowResponse(false);
        setRecording(newBlob);
    }
    const toggleVoice = () => {
        if (!voice) {
        startRecording();
    } else {
        stopRecording();
    }
    setVoice(!voice);
    };
    
    
    
    
    
    
    const handleSubmit = () => {
        setShowResponse(false);
        if(questionInput.trim() && recording){
            const formData = new FormData();
            formData.append("audio",recording,"audio.webm")
            fetch("http://127.0.0.1:8000/api/transcribe_audio/",{
                method: "POST",
                body: formData,
            })
            .then(res=>res.json())
            .then(data=>{
                setFinalData({
                    text: questionInput.trim(),
                    audio:data.transcribed_text,
                    
                    
                })

            });
            
            
                
            setShowResponse(true);
            
            
            
            
        }else if(recording){
            const formData = new FormData();
            formData.append("audio",recording,"audio.webm")
            fetch("http://127.0.0.1:8000/api/transcribe_audio/",{
                method: "POST",
                body: formData,
            })
            .then(res=>res.json())
            .then(data=>{
                setFinalData({
                    audio:data.transcribed_text,
                    
                    
                })

            });
            setShowResponse(true);
            
            
            
        }else if(questionInput.trim()){
            
            setFinalData({
                text:questionInput.trim(),
            });
            setShowResponse(true);
        };
            
           
       
        
        

    };
    const handleGen = ()=> {
        const formData = new FormData();
        fetch("http://127.0.0.1:8000/api/generate_questions/",{
                method: "POST"
        })
        .then(res=>res.json())
        .then(data=>{
            setQuestions(data)

        });

    }; 
    const [showResponse, setShowResponse] = useState(false);
    useEffect(()=>{
            if(showResponse && finalData){
                getResponse(finalData);
                const endTime = performance.now();
                const totalLatency = (endTime - startTime) / 1000;
                console.log("Total Latency (Frontend + Backend):", totalLatency, "s");
            }
        },[showResponse, finalData]);




    
    
    const [isCollapsed, setIsCollapsed] = useState(false);
    const toggleSidebar = () => {
        setIsCollapsed(!isCollapsed);
    };
    
    const [technologies, setTechnologies] = useState([]);
    const [selectedTech, setSelTech] = useState("");
    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/technologies/")
        .then((res)=>res.json())
        .then((data)=>setTechnologies(data));
    },[]);
    const [domain, setDomain] = useState([]);
    const [selectedDomain, setSelDomain] = useState("");
    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/domain/")
        .then((res)=>res.json())
        .then((data)=>setDomain(data));
    },[]);
    const [level, setLevel] = useState([]);
    const [selectedLevel, setSelLevel] = useState("");
    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/level/")
        .then((res)=>res.json())
        .then((data)=>setLevel(data));
    },[]);
    const [aiModel, setAiModel] = useState([]);
    const [selectedAiModel, setSelAiModel] = useState("");
    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/aiModel/")
        .then((res)=>res.json())
        .then((data)=>setAiModel(data));
    },[]);
    const [yrsExp, setyrsExp] = useState([]);
    const [selectedYrsExp, setSelYrsExp] = useState("");
    useEffect(() => {
        fetch("http://127.0.0.1:8000/api/yrsExp/")
        .then((res)=>res.json())
        .then((data)=>setyrsExp(data));
    },[]);
    
    const fileInputRef = useRef(null);
    const HandleStorageUsage = (event) => {
        const formData = new FormData();
        const files = fileInputRef.current?.files;
        formData.append("file_one",files[0])
        formData.append("file_two",files[1])
        fetch("http://127.0.0.1:8000/api/process_pdfs/",{
            method:"POST",
            body:formData,
        })
        
        
        
        if((selectedTech || selectedDomain || selectedLevel || selectedYrsExp || selectedAiModel) && files){
            const formData = new FormData();
            const username = localStorage.getItem("username");
            formData.append("username",username);
            formData.append("tech",selectedTech);
            formData.append("dom",selectedDomain);
            formData.append("lev",selectedLevel);
            formData.append("exp",selectedYrsExp);
            formData.append("ai",selectedAiModel);
            if (files){
                formData.append("file_one",files[0]);
                formData.append("file_two",files[1]);
            }
            
                
            fetch("http://127.0.0.1:8000/api/store_selection/",{
                method:"POST",
                    
                body: formData,
            })
            .then((res) => res.json())
            .then((data) => {
                console.log("✅ Response from server:", data);
            })
            .catch((err) => {
                console.error("❌ Upload failed:", err);
            });
            
        }
            
    };

        useEffect(() => {
    if (technologies.length > 0 && !selectedTech) {
        setSelTech(technologies[0].techName);
    }
    }, [technologies]);
     useEffect(() => {
    if (domain.length > 0 && !selectedDomain) {
        setSelDomain(domain[0].domainName);
    }
    }, [domain]);
     useEffect(() => {
    if (level.length > 0 && !selectedLevel) {
        setSelLevel(level[0].levelName);
    }
    }, [level]);
     useEffect(() => {
    if (aiModel.length > 0 && !selectedAiModel) {
        setSelAiModel(aiModel[0].modelName);
    }
    }, [aiModel]);
     useEffect(() => {
    if (yrsExp.length > 0 && !selectedYrsExp) {
        setSelYrsExp(yrsExp[0].yrsexp);
    }
    }, [yrsExp]);

    const getResponse = async (finalData) => {
        if(!finalData) return;
        const formData = new FormData();
        if (finalData.audio && finalData.text) {
            formData.append("text", finalData.text);
            formData.append("audio", finalData.audio);
            
        } else if (finalData.audio) {
            formData.append("audio", finalData.audio); 
        } else if (finalData.text) {
            formData.append("text", finalData.text);
        }
        const res = await fetch("http://127.0.0.1:8000/api/response/",{
            method:"POST",
            body: formData,
        });
        const data = await res.json();
        setTextAiResponse(data.text_response)
        setAudioAiResponse(data.audio_response)
        
        
    };
        


    
    




 return (
    
    <div className="container">
        {isCollapsed && (
            <button className={"osb-toggle"} onClick={toggleSidebar}>☰</button>
        )}
        
            
        
        <div className = {`sidebar ${isCollapsed ? 'open':'closed'}`}>
            {!isCollapsed && (
                <button className={"sb-toggle"} onClick={toggleSidebar}>←</button>
            )}
            
            
            <h2>Upload Resume and Job Description: </h2>
            <p>Upload your Files and Click on the Submit to Process</p>
            <div className ="upload-box">
                <p className="dd-files">Upload your resume and job description here</p>
                
                <input
                    type="file"
                    ref={fileInputRef}
                    multiple
                    style={{ display: 'none' }}
                    
                />
                <button onClick={()=>fileInputRef.current.click()}>Browse Files</button>
                
            </div>
            
            
            <div className = "user-input">
                <p className="small-text-1">Select your preferred technology</p>
                <select onChange={(e)=>setSelTech(e.target.value)} className ="drop-1">
                    
                    {Array.isArray(technologies) && technologies.map((tech)=>(
                (
                    <option key ={tech.techId} value={tech.techName}>{tech.techName}</option>
                )
                    ))}
                </select>
                <p className="small-text-2">Select your Domain</p>
                <select onChange={(e)=>setSelDomain(e.target.value)} className ="drop-2">
                    {Array.isArray(domain) && domain.map((domain)=>(
                (
                    <option value={domain.domainName}>{domain.domainName}</option>
                )
                    ))}
                </select>
                <p className="small-text-3">Select your Level</p>
                <select onChange={(e)=>setSelLevel(e.target.value)} className ="drop-3">
                    {Array.isArray(level) && level.map((lev)=>(
                        (
                            <option value = {lev.levelName} >{lev.levelName}</option>
                        )
                    ))}
                </select>
                <p className="small-text-4">Select the amount of experience you have</p>
                <select onChange={(e)=>setSelYrsExp(e.target.value)} className ="drop-4">
                    {Array.isArray(yrsExp) && yrsExp.map((yrs)=>(
                (
                    <option value={yrs.yrsexp}>{yrs.yrsexp}</option>
                )
                    ))}
                </select>
                <p className="small-text-5">Select your preferred AI Model(Default Gemini pro 1.5)</p>
                <select onChange={(e)=>setSelAiModel(e.target.value)} className ="drop-5">
                    {Array.isArray(aiModel) && aiModel.map((ai)=>(
                (
                    <option key ={ai.modelName} value={ai.modelName}>{ai.modelName}</option>
                )
                    ))}
                </select>
                




            </div>

            <button onClick = {()=>HandleStorageUsage()} className = "user-input-submit">Submit</button>
        

        </div>
        <div className = {`main-app ${isCollapsed ? 'open':'closed'}`}>
            <h1 className = "main-text">
                Type or voice your questions relating to the pdf's
            </h1>
            
            <div className = "question-wrapper">
                <div className = "inputs">
                    <textarea className = "question" onChange = {(e)=>setQuestionInput(e.target.value)} value = {questionInput} placeholder="Type here..."></textarea>
                    <button className = "voice-question" onClick = {()=>toggleVoice()}>
                        {!voice ?
                            <i className="fas fa-microphone"></i>:<i className="fas fa-stop"></i>}

                    </button>
                </div>
                <button className ="question-submit" onClick={handleSubmit}>
                    Submit 
                    
                </button>
            </div>
            
            {showResponse && finalData && textai_response &&(
               
            <>
                <p><strong>Reasoning:</strong> {textai_response.reasoning}</p>
                <p><strong>Response:</strong> {textai_response.response}</p>
            </>
            )}
            {showResponse && finalData && audioai_response &&(
               
            <>
                <p><strong>Reasoning:</strong> {audioai_response.reasoning}</p>
                <p><strong>Response:</strong> {audioai_response.response}</p>
            </>
            )}

            <div className="question-area">
                <button className="generate-questions" onClick={handleGen}>
                    Generate Questions!
                </button>
                {questions &&(
                    Object.entries(questions).map(([q,a],index)=>(
                        <div key={index}>
                            <strong>Q:{q}</strong>
                            <p>A: {a}</p>
                        </div>


                    ))
                )}
            </div>
                
        
            


            

            
        </div>
    </div>
  );
};

export default MainApp;
