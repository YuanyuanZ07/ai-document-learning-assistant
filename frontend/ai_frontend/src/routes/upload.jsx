'use client'
import "tailwindcss";
import { useState } from 'react';
const Upload = () => {
    const [file , setfile] = useState(null);  
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState('');
    const [summary, setSummary] = useState('');
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setfile(event.target.files[0]);
    };

    const handleScan = async () => {
    await handleUpdate("scan");
    };

    const handleAsk = async () => {
        if (
            message.toLowerCase().includes("summary") ||
            message.toLowerCase().includes("summarize")
        ) {
            handleSummary();
            return;
        }

        await handleUpdate("question");
    };

    const handleSummary = async () => {
         try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/summary/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: message })
            });

            const data = await res.json();
            setSummary(data.summary);
        } catch (err) {
            console.error(err);
        }
    };


    const handleUpdate = async (action) => {
        
        if (!file) {
            alert('Please select a file to upload.');
            return;
        }

        setLoading(true);

        const formData = new FormData();
        formData.append('file', file);
        formData.append('action',action);
        formData.append('message', message)

        try {
        
        const response = await fetch(`${import.meta.env.VITE_API_URL}/upload`, {
            method: 'POST',
            body: formData
        });
            const data = await response.json();
            setResponse(data.message);
            setMessage('');
            
            if (data.summary) {
                setSummary(data.summary);
                }
            } catch (err) {
                console.error(err);
                setResponse("An error occurred. Please try again.");
            } finally {
                setLoading(false);
            }
        };

    return (
        
        <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center justify-center p-6">

            <h1 className="text-5xl font-bold mb-2 text-center">Upload a Document</h1>
                <p className='mb-8 text-gray-400 text-center'>
                    Upload a document, scan it using AI, ask questions, or generate a summary.
                </p>
                    <form className="w-full max-w-3xl flex flex-col gap-4">

                <input
                    type="file"
                    onChange={handleFileChange}
                    className="w-full bg-gray-800 p-3 rounded-lg border border-gray-600 cursor-pointer"
                />

                <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Ask a question..."
                    rows={5}
                    className="w-full px-5 py-4 rounded-xl bg-gray-800 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <div className="flex gap-4 justify-center mt-2">
                    <button
                    disabled={loading}
                    onClick={handleScan}
                    type="button"
                    className="bg-blue-600 hover:bg-blue-700 px-6 py-2 rounded-lg font-medium transition"
                    >
                    {loading ? "Scanning..." : "Scan"}
                    </button>

                    <button
                    onClick={handleAsk}
                    type="button"
                    className="bg-green-600 hover:bg-green-700 px-6 py-2 rounded-lg font-medium transition"
                    >
                    Ask
                    </button>

                    <button
                    onClick={handleSummary}
                    type="button"
                    className="bg-purple-600 hover:bg-purple-700 px-6 py-2 rounded-lg font-medium transition"
                    >
                    Summary
                    </button>
                </div>
            </form>

            {response && (
                <div className="mt-6 w-full max-w-2xl bg-white p-4 rounded-lg shadow-md">
                    <p className='text-gray-800'>{response}</p>
                </div>
            )}
        </div>
    );
};
export default Upload;