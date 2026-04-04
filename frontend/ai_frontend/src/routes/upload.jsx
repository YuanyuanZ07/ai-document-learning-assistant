import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
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
        if (file) {
            await handleUpdate("scan");
            return;
        }

        if (!message.trim()) {
            alert("Please upload a file or enter text to summarize.");
            return;
        }

        setLoading(true);
        try {
            const res = await fetch(`${import.meta.env.VITE_API_URL}/summary/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ text: message })
            });

            const data = await res.json();
            setSummary(data.summary || "No summary returned.");
        } catch (err) {
            console.error(err);
            setSummary("An error occurred while generating the summary.");
        } finally {
            setLoading(false);
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
        
        const response = await fetch(`${import.meta.env.VITE_API_URL}/upload/`, {
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
        
        <div className="min-h-screen bg-white text-gray-900 flex flex-col items-center justify-center p-6">

            <h1 className="text-5xl font-bold mb-2 text-center">AI Document Learning Assistant</h1>
                <p className='mb-8 text-gray-500 text-center'>
                    Upload a document, scan it using AI, ask questions, or generate a summary.
                </p>
                    <form className="w-full max-w-3xl flex flex-col gap-4">

                <input
                    type="file"
                    onChange={handleFileChange}
                    className="w-full bg-gray-50 p-3 rounded-lg border border-gray-300 cursor-pointer"
                />

                <textarea
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    placeholder="Ask a question..."
                    rows={5}
                    className="w-full px-5 py-4 rounded-xl bg-gray-50 text-gray-900 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500"
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
                <div className="mt-6 w-full max-w-2xl bg-blue-50 p-6 rounded-xl shadow-md border border-blue-200">
                    <h2 className="text-lg font-semibold text-blue-700 mb-3">Response</h2>
                    <div className="text-gray-800 prose prose-sm max-w-none
                        prose-headings:text-gray-900 prose-headings:font-semibold prose-headings:mt-4 prose-headings:mb-2
                        prose-p:my-2 prose-p:leading-relaxed
                        prose-ul:my-2 prose-ul:pl-5 prose-li:my-1
                        prose-strong:text-gray-900">
                        <ReactMarkdown>{response}</ReactMarkdown>
                    </div>
                </div>
            )}

            {summary && (
                <div className="mt-6 w-full max-w-2xl bg-purple-50 p-6 rounded-xl shadow-md border border-purple-200">
                    <h2 className="text-lg font-semibold text-purple-700 mb-3">Summary</h2>
                    <div className="text-gray-800 prose prose-sm max-w-none
                        prose-headings:text-gray-900 prose-headings:font-semibold prose-headings:mt-4 prose-headings:mb-2
                        prose-p:my-2 prose-p:leading-relaxed
                        prose-ul:my-2 prose-ul:pl-5 prose-li:my-1
                        prose-strong:text-gray-900">
                        <ReactMarkdown>{summary}</ReactMarkdown>
                    </div>
                </div>
            )}
        </div>
    );
};
export default Upload;