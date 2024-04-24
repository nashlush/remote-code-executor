import React, { useState, useEffect, useRef } from 'react'
import Editor, { DiffEditor, useMonaco, loader } from '@monaco-editor/react';
import './editorBox.css';

const EditorBox = ({ defaultLanguage, defaultValues }) => {

    const[code, setCode] = useState("")
    const[language, setLanguage] = useState(defaultLanguage)
    const[input, setInput] = useState("")
    const [output, setOutput] = useState("");
    const outputRef = useRef(null);

    const handleLanguageChange = (event) => {
        setLanguage(event.target.value);
    };

    const handleEditorChange = (value, event) => {
        console.log('here is the current model value:', value);
        setCode(value)
    };

    const handleSubmit = () => {
        // Perform actions with submitted code
        console.log('Submitted code:', code);
        console.log('Input: ', input);

        outputRef.current.scrollIntoView({ behavior: "smooth" });

        // send the code to the python flask server to execute it
        fetch("http://localhost:5000/run-java",{
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                java_code: code,
                input_text: input
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.body);
            setOutput(data.body);
        })
        .catch(error => {
            console.error("Error: ", error)
        })
    };

    const handleInputChange = (event) => {
        setInput(event.target.value);
    };

  return (
    <div className="editor-box-container">
        <div className="panel">
            <h2>Code Editor</h2>
            <Editor
                className="editor"
                height="80vh"
                defaultLanguage={language}
                defaultValue="// write java code here."
                theme="vs-dark"
                onChange={handleEditorChange}
            />

            <select className="language-dropdown" value={language} onChange={handleLanguageChange}>
                <option value="javascript">JavaScript</option>
                <option value="java">Java</option>
                <option value="python">Python</option>
                <option value="cpp">C++</option>
            </select>

            <button className="submit-button" onClick={handleSubmit}>Submit</button>
        </div>

        <div className="panel">
            <h2>Input</h2>
            <textarea
                className="input-textarea"
                value={input}
                onChange={handleInputChange}
                placeholder="Enter input for the program..."
            />
        </div>

        <div className="panel" ref={outputRef}>
            <h2>Output</h2>
            <textarea
                className="output-textarea"
                value={output}
                readOnly
                placeholder="Output will be displayed here..."
            />
        </div>
    </div>
  )
}

export default EditorBox